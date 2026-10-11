"""No network and no SDK/provider invocation: four synthetic LiteLLM sinks."""
import asyncio
from pathlib import Path
import sys
import types
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from canary_budget import BudgetBook, RateCard, TokenCaps
from canary_controls import GateError, Guard
from canary_transport_probe import (
    SINK_NAMES, SyntheticTransportGate, synthetic_litellm_sinks,
)


def rates():
    return RateCard("synthetic", "fake/only", "2", "8",
                    "https://example.invalid/unused", "2026-10-11", "synthetic")


def caps():
    return TokenCaps(context_window=2000, max_input_tokens=500,
                     max_output_tokens=500, max_calls=6)


def setup(budget="0.02"):
    guard, book = Guard(), BudgetBook(budget)
    return SyntheticTransportGate(guard, book, rates(), caps())


def fake_sinks(*, raises=False):
    module = types.ModuleType("canary_synthetic_litellm")
    attempts = []
    def sync(*args, **kwargs):
        attempts.append("sync")
        if raises:
            raise RuntimeError("synthetic_transient")
        return "fake_response"
    async def async_fn(*args, **kwargs):
        attempts.append("async")
        await asyncio.sleep(0)
        if raises:
            raise RuntimeError("synthetic_transient")
        return "fake_response"
    module.litellm_completion = sync
    module.litellm_acompletion = async_fn
    module.litellm_responses = sync
    module.litellm_aresponses = async_fn
    return module, attempts


class TransportAttemptGateTests(unittest.TestCase):
    def test_each_of_four_sinks_gets_reservation_before_fake_dispatch(self):
        for name in SINK_NAMES:
            with self.subTest(name=name):
                gate=setup()
                module, attempts=fake_sinks()
                with synthetic_litellm_sinks(module, gate):
                    with gate.logical_call():
                        if name.startswith("litellm_a"):
                            result=asyncio.run(getattr(module, name)(messages=[]))
                        else:
                            result=getattr(module, name)(messages=[])
                        self.assertEqual("fake_response", result)
                        self.assertEqual(1, gate.book.calls)
                        self.assertEqual(1, gate.guard.calls)
                        self.assertEqual(1, len(attempts))
                        gate.settle(input_tokens=100, output_tokens=100,
                                    reported_usd="0.001")
                self.assertEqual(1,gate.attempts)
                self.assertEqual("0.001", str(gate.book.spent))
                self.assertIsNone(gate.book.active)
                self.assertFalse(gate.book.closed)

    def test_unreserved_transport_never_reaches_fake_sink(self):
        gate=setup()
        module, attempts=fake_sinks()
        with synthetic_litellm_sinks(module, gate):
            with self.assertRaisesRegex(GateError,"transport_outside_authorized_scope"):
                module.litellm_completion(messages=[])
        self.assertEqual([],attempts)
        self.assertEqual(0,gate.book.calls)
        self.assertTrue(gate.guard.cancelled)

    def test_second_attempt_inside_same_public_call_cannot_escape(self):
        for first, second in (("litellm_completion","litellm_completion"),
                              ("litellm_completion","litellm_responses"),
                              ("litellm_acompletion","litellm_aresponses"),
                              ("litellm_responses","litellm_acompletion")):
            with self.subTest(first=first,second=second):
                gate=setup()
                module, attempts=fake_sinks()
                with synthetic_litellm_sinks(module,gate):
                    with self.assertRaisesRegex(GateError,"second_transport_attempt_forbidden"):
                        with gate.logical_call():
                            for name in (first,second):
                                if name.startswith("litellm_a"):
                                    asyncio.run(getattr(module,name)(messages=[]))
                                else:
                                    getattr(module,name)(messages=[])
                self.assertEqual(1,len(attempts))
                self.assertEqual(1,gate.book.calls)
                self.assertTrue(gate.book.closed)

    def test_hidden_provider_retry_after_error_is_blocked(self):
        gate=setup()
        module, attempts=fake_sinks(raises=True)
        with synthetic_litellm_sinks(module,gate):
            with self.assertRaisesRegex(GateError,"second_transport_attempt_forbidden"):
                with gate.logical_call():
                    try:
                        module.litellm_completion(messages=[])
                    except RuntimeError:
                        module.litellm_completion(messages=[])
        self.assertEqual(1,len(attempts))
        self.assertTrue(gate.book.closed)

    def test_settled_first_request_cannot_fund_another_attempt_in_same_scope(self):
        gate=setup()
        module, attempts=fake_sinks()
        with synthetic_litellm_sinks(module,gate):
            with self.assertRaisesRegex(GateError,"second_transport_attempt_forbidden"):
                with gate.logical_call():
                    module.litellm_completion(messages=[])
                    gate.settle(input_tokens=100,output_tokens=100,reported_usd="0.001")
                    module.litellm_completion(messages=[])
        self.assertEqual(1,len(attempts))
        self.assertTrue(gate.guard.cancelled)

    def test_two_separate_logical_calls_each_need_new_reservation(self):
        gate=setup()
        module, attempts=fake_sinks()
        with synthetic_litellm_sinks(module,gate):
            for _ in range(2):
                with gate.logical_call():
                    module.litellm_responses(messages=[])
                    gate.settle(input_tokens=100,output_tokens=100,reported_usd="0.001")
        self.assertEqual(2,len(attempts))
        self.assertEqual(2,gate.book.calls)

    def test_insufficient_budget_denies_before_transport(self):
        gate=setup("0.004")
        module, attempts=fake_sinks()
        with synthetic_litellm_sinks(module,gate):
            with self.assertRaisesRegex(GateError,"worst_case_over_budget"):
                with gate.logical_call():
                    module.litellm_completion(messages=[])
        self.assertEqual([],attempts)
        self.assertTrue(gate.guard.cancelled)

    def test_missing_settlement_or_invalid_actual_usage_aborts(self):
        for bad in ("no_settle", "no_charge", "too_many_tokens"):
            with self.subTest(bad=bad):
                gate=setup()
                module, attempts=fake_sinks()
                with synthetic_litellm_sinks(module,gate):
                    with self.assertRaises(GateError):
                        with gate.logical_call():
                            module.litellm_completion(messages=[])
                            if bad == "no_charge":
                                gate.settle(input_tokens=100,output_tokens=100,
                                            reported_usd="0")
                            elif bad == "too_many_tokens":
                                gate.settle(input_tokens=501,output_tokens=100,
                                            reported_usd="0.003")
                self.assertEqual(1,len(attempts))
                self.assertTrue(gate.book.closed)

    def test_async_cancelled_transport_aborts_without_second_attempt(self):
        gate=setup()
        module, attempts=fake_sinks()
        async def cancelled(*args,**kwargs):
            attempts.append("cancelled")
            raise asyncio.CancelledError()
        module.litellm_aresponses=cancelled
        with synthetic_litellm_sinks(module,gate):
            with self.assertRaises(asyncio.CancelledError):
                with gate.logical_call():
                    asyncio.run(module.litellm_aresponses(messages=[]))
        self.assertEqual(1,len(attempts))
        self.assertTrue(gate.book.closed)

    def test_other_task_and_parallel_logical_scope_fail_closed(self):
        gate=setup()
        module,attempts=fake_sinks()
        with synthetic_litellm_sinks(module,gate):
            with self.assertRaisesRegex(GateError,"parallel_logical_calls_forbidden"):
                with gate.logical_call():
                    with gate.logical_call():
                        self.fail("nested scope should be refused")
        self.assertEqual([],attempts)
        self.assertTrue(gate.book.closed)

    def test_async_task_without_owner_permission_is_blocked(self):
        gate=setup()
        module,attempts=fake_sinks()
        async def outsider():
            with gate.logical_call():
                return await asyncio.create_task(module.litellm_acompletion(messages=[]))
        with synthetic_litellm_sinks(module,gate):
            with self.assertRaisesRegex(GateError,"transport_outside_authorized_scope"):
                asyncio.run(outsider())
        self.assertEqual([],attempts)
        self.assertTrue(gate.book.closed)

    def test_real_sdk_module_is_refused_and_originals_are_restored(self):
        gate=setup()
        real_module,attempts=fake_sinks()
        real_module.__name__="openhands.sdk.llm.llm"
        with self.assertRaisesRegex(GateError,"actual_sdk_or_unknown_transport_forbidden"):
            with synthetic_litellm_sinks(real_module,gate):
                self.fail("must not patch real SDK")
        self.assertEqual([],attempts)
        fake, attempts=fake_sinks()
        original=fake.litellm_completion
        with self.assertRaisesRegex(RuntimeError,"synthetic_exit"):
            with synthetic_litellm_sinks(fake,setup()):
                raise RuntimeError("synthetic_exit")
        self.assertIs(fake.litellm_completion,original)
        self.assertFalse(hasattr(fake,"__canary_synthetic_transport_active__"))


if __name__ == "__main__":
    unittest.main()
