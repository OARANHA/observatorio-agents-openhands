"""BudgetBook at SDK route names with synthetic, in-memory transports only."""
import asyncio
from decimal import Decimal
from pathlib import Path
import sys
import types
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from canary_budget import BudgetBook, RateCard, TokenCaps
from canary_budget_boundary import ROUTES, synthetic_budgeted_llm_routes
from canary_controls import GateError, Guard


def rates():
    return RateCard("synthetic","fake/explorer","2","8",
                    "https://example.invalid/offline","2026-10-11","synthetic")


def caps():
    return TokenCaps(context_window=2000,max_input_tokens=500,
                     max_output_tokens=500,num_retries=0,max_calls=6)


class FakeLLM:
    _canary_fake_transport=True
    model="fake/explorer"
    num_retries=0
    stream=False
    caching_prompt=False
    max_output_tokens=500
    input_cost_per_token=0.000002
    output_cost_per_token=0.000008

    def __init__(self):
        self.metrics=types.SimpleNamespace(
            accumulated_cost=0.0,
            accumulated_token_usage=types.SimpleNamespace(
                prompt_tokens=0,completion_tokens=0))
        self.dispatches=0
        self.fail=False
        self.nested=False
        self.silent=False
        self.overcharge=False

    def consume(self):
        self.dispatches+=1
        if self.fail:
            raise RuntimeError("synthetic_failure")
        if self.nested:
            self.completion(["nested"])
        if not self.silent:
            self.metrics.accumulated_cost+=0.006 if self.overcharge else 0.001
            self.metrics.accumulated_token_usage.prompt_tokens+=100
            self.metrics.accumulated_token_usage.completion_tokens+=100
        return "synthetic-result"

    def completion(self,messages,**kwargs):
        return self.consume()

    async def acompletion(self,messages,**kwargs):
        await asyncio.sleep(0)
        return self.consume()

    def responses(self,messages,**kwargs):
        return self.consume()

    async def aresponses(self,messages,**kwargs):
        await asyncio.sleep(0)
        return self.consume()

    def model_copy(self):
        return type(self)()


class BudgetBoundary(unittest.TestCase):
    def test_four_routes_reserve_before_synthetic_dispatch_and_settle(self):
        for route in ROUTES:
            with self.subTest(route=route):
                guard,book=Guard(),BudgetBook("0.01")
                fake=FakeLLM()
                with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),caps()):
                    if route.startswith("a"):
                        result=asyncio.run(getattr(fake,route)(["synthetic"]))
                    else:
                        result=getattr(fake,route)(["synthetic"])
                    self.assertEqual("synthetic-result",result)
                    self.assertEqual(1,fake.dispatches)
                    self.assertEqual(1,guard.calls)
                    self.assertEqual(1,book.calls)
                    self.assertIsNone(book.active)
                    self.assertEqual(Decimal("0.001"),book.spent)

    def test_budget_rejects_before_any_dispatch(self):
        for route in ROUTES:
            with self.subTest(route=route):
                guard,book=Guard(),BudgetBook("0.004")
                fake=FakeLLM()
                with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),caps()):
                    with self.assertRaisesRegex(GateError,"worst_case_over_budget"):
                        if route.startswith("a"):
                            asyncio.run(getattr(fake,route)(["synthetic"]))
                        else:
                            getattr(fake,route)(["synthetic"])
                self.assertEqual(0,fake.dispatches)
                self.assertEqual(0,guard.calls)
                self.assertTrue(guard.cancelled)
                self.assertTrue(book.closed)

    def test_multiple_sequential_calls_and_clone_share_one_book(self):
        guard,book=Guard(),BudgetBook("0.006")
        fake=FakeLLM()
        with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),caps()):
            self.assertEqual("synthetic-result",fake.completion(["a"]))
            clone=fake.model_copy()
            self.assertEqual("synthetic-result",asyncio.run(clone.aresponses(["b"])))
            self.assertEqual(2,book.calls)
            self.assertEqual(Decimal("0.002"),book.spent)
            with self.assertRaisesRegex(GateError,"worst_case_over_budget"):
                fake.responses(["c"])
            self.assertEqual(1,fake.dispatches)
            self.assertEqual(1,clone.dispatches)
        self.assertTrue(book.closed)

    def test_nested_fallback_refused_without_second_dispatch(self):
        guard,book=Guard(),BudgetBook("0.02")
        fake=FakeLLM()
        fake.nested=True
        with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),caps()):
            with self.assertRaisesRegex(GateError,"parallel_requests_forbidden"):
                fake.responses(["original"])
        self.assertEqual(1,fake.dispatches)
        self.assertTrue(guard.cancelled)
        self.assertTrue(book.closed)

    def test_missing_metrics_and_missing_usage_abort(self):
        for variant in ("missing", "silent"):
            guard,book=Guard(),BudgetBook("0.01")
            fake=FakeLLM()
            if variant=="missing":
                fake.metrics=None
            else:
                fake.silent=True
            with self.subTest(variant=variant):
                with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),caps()):
                    with self.assertRaises(GateError):
                        fake.completion(["synthetic"])
                self.assertEqual(0 if variant=="missing" else 1,fake.dispatches)
                self.assertTrue(book.closed)

    def test_exception_after_reserve_does_not_refund_or_retry(self):
        guard,book=Guard(),BudgetBook("0.01")
        fake=FakeLLM()
        fake.fail=True
        with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),caps()):
            with self.assertRaisesRegex(RuntimeError,"synthetic_failure"):
                fake.completion(["synthetic"])
        self.assertEqual(1,fake.dispatches)
        self.assertEqual(1,book.calls)
        self.assertIsNotNone(book.active)
        self.assertTrue(guard.cancelled)

    def test_reported_charge_above_reservation_is_blocked(self):
        guard,book=Guard(),BudgetBook("0.02")
        fake=FakeLLM()
        fake.overcharge=True
        with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),caps()):
            with self.assertRaisesRegex(GateError,"charge_exceeded_reservation"):
                fake.completion(["synthetic"])
        self.assertTrue(book.closed)
        self.assertEqual(1,fake.dispatches)

    def test_sdk_fields_or_call_overrides_rejected_before_dispatch(self):
        for kind in ("model", "retries", "tokens", "cache", "stream", "extra"):
            guard,book=Guard(),BudgetBook("0.02")
            fake=FakeLLM()
            if kind=="model":fake.model="unreviewed/model"
            if kind=="retries":fake.num_retries=1
            if kind=="tokens":fake.max_output_tokens=2000
            if kind=="cache":fake.caching_prompt=True
            if kind=="stream":fake.stream=True
            with self.subTest(kind=kind):
                with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),caps()):
                    with self.assertRaises(GateError):
                        fake.completion(["synthetic"],**({"max_tokens":999} if kind=="extra" else {}))
                self.assertEqual(0,fake.dispatches)
                self.assertTrue(book.closed)

    def test_no_real_sdk_class_or_unsigned_rates(self):
        class SDKLooking(FakeLLM):pass
        SDKLooking.__module__="openhands.sdk.llm.llm"
        with self.assertRaisesRegex(GateError,"provider_backed_sdk_forbidden"):
            with synthetic_budgeted_llm_routes(SDKLooking,Guard(),BudgetBook("0.01"),rates(),caps()):pass
        wrong=RateCard("openai","fake/explorer","2","8",
                "https://openai.com","2026-10-11","operator_verified")
        with self.assertRaisesRegex(GateError,"synthetic_rates_required"):
            with synthetic_budgeted_llm_routes(FakeLLM,Guard(),BudgetBook("0.01"),wrong,caps()):pass

    def test_patch_restores_after_synthetic_error_and_blocks_reentrant_context(self):
        original=FakeLLM.completion
        guard,book=Guard(),BudgetBook("0.01")
        with self.assertRaisesRegex(RuntimeError,"aborted"):
            with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),caps()):
                with self.assertRaisesRegex(GateError,"boundary_already_active"):
                    with synthetic_budgeted_llm_routes(FakeLLM,Guard(),BudgetBook("0.01"),rates(),caps()):pass
                raise RuntimeError("aborted")
        self.assertIs(original,FakeLLM.completion)
        self.assertFalse(hasattr(FakeLLM,"__canary_budget_mock_active__"))


if __name__=="__main__":
    unittest.main()
