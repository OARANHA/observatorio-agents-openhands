"""Offline preventive budget tests: no real LLM/provider calls."""
from datetime import date
from decimal import Decimal
from pathlib import Path
import sys
import types
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from canary_controls import GateError,Guard
from canary_budget import BudgetBook,RateCard,TokenCaps,validate_sdk_config

def fixture():
    return RateCard("synthetic","fake/explorer","2.00","8.00",
                    "https://example.invalid/pricing","2026-10-11","synthetic")

def caps(**kwargs):
    return TokenCaps(**({"context_window":2000,"max_input_tokens":500,
                          "max_output_tokens":500,"max_calls":6}|kwargs))

class OfflineBudget(unittest.TestCase):
    def test_reserve_input_output_worst_case_before_provider(self):
        book,guard=BudgetBook("0.010000"),Guard()
        hold=book.reserve(guard,fixture(),caps())
        self.assertEqual(Decimal("0.005"),hold.ceiling_usd)
        self.assertEqual(1,guard.calls)
        actual=book.settle(guard,hold,input_tokens=125,output_tokens=125,reported_usd="0.00125")
        self.assertEqual(Decimal("0.00125"),actual)
        self.assertEqual(Decimal("0.00125"),book.spent)
        self.assertIsNone(book.active)
        next_reservation=book.reserve(guard,fixture(),caps())
        self.assertEqual(2,next_reservation.serial)

    def test_budget_preflight_rejects_before_guard_call(self):
        guard,book=Guard(),BudgetBook("0.004999")
        with self.assertRaisesRegex(GateError,"worst_case_over_budget"):
            book.reserve(guard,fixture(),caps())
        self.assertEqual(0,guard.calls)
        self.assertEqual(0,book.calls)
        self.assertTrue(guard.cancelled)

    def test_only_one_call_in_flight_and_denial_terminal(self):
        guard,book=Guard(),BudgetBook("0.10")
        book.reserve(guard,fixture(),caps())
        with self.assertRaisesRegex(GateError,"parallel_requests_forbidden"):
            book.reserve(guard,fixture(),caps())
        self.assertTrue(guard.cancelled)
        self.assertTrue(book.closed)

    def test_unknown_provider_outcome_never_refunded(self):
        guard,book=Guard(),BudgetBook("0.10")
        hold=book.reserve(guard,fixture(),caps())
        book.abort(guard)
        self.assertIs(book.active,hold)
        with self.assertRaises(GateError):book.reserve(guard,fixture(),caps())

    def test_settlement_checks_actual_tokens_missing_overcharge_undercharge(self):
        cases=[
            ({"input_tokens":501,"output_tokens":1,"reported_usd":"0.001"},"token_usage_outside_reservation"),
            ({"input_tokens":1,"output_tokens":501,"reported_usd":"0.001"},"token_usage_outside_reservation"),
            ({"input_tokens":10,"output_tokens":10,"reported_usd":"0.005001"},"charge_exceeded_reservation"),
            ({"input_tokens":10,"output_tokens":10,"reported_usd":"0"},"reported_cost_missing"),
            ({"input_tokens":10,"output_tokens":10,"reported_usd":"0.00001"},"reported_cost_below_expected"),
        ]
        for kwargs,code in cases:
            with self.subTest(kwargs=kwargs):
                guard,book=Guard(),BudgetBook("0.10")
                hold=book.reserve(guard,fixture(),caps())
                with self.assertRaisesRegex(GateError,code):book.settle(guard,hold,**kwargs)
                self.assertTrue(guard.cancelled)
                self.assertTrue(book.closed)

    def test_context_token_retries_call_limit_fail_closed(self):
        cases=[
            ({"max_input_tokens":0},"input_ceiling_missing"),
            ({"max_output_tokens":0},"output_ceiling_missing"),
            ({"context_window":100},"context_window_exceeded"),
            ({"num_retries":1},"retries_forbidden"),
            ({"max_calls":7},"call_limit_exceeded"),
        ]
        for overrides,error in cases:
            with self.subTest(overrides=overrides):
                guard,book=Guard(),BudgetBook("0.1")
                with self.assertRaisesRegex(GateError,error):
                    book.reserve(guard,fixture(),caps(**overrides))
                self.assertEqual(0,guard.calls)

    def test_live_mode_requires_verified_rates_and_proven_limits(self):
        complete=caps(input_bound_proven=True,output_bound_proven=True,
                      extra_charges_ruled_out=True)
        guard,book=Guard(),BudgetBook("0.1")
        with self.assertRaisesRegex(GateError,"rates_not_operator_verified"):
            book.reserve(guard,fixture(),complete,live=True)
        placeholder=RateCard("openai","mock","1","1",
              "https://openai.com/api/pricing","2026-10-11","operator_verified")
        guard,book=Guard(),BudgetBook("0.1")
        with self.assertRaisesRegex(GateError,"provider_limits_unproven"):
            book.reserve(guard,placeholder,caps(),live=True,today=date(2026,10,11))

    def test_price_source_exact_host_age_and_valid_number(self):
        sample=RateCard("openai","mock","1","2",
                "https://openai.com/api/pricing","2026-10-11","operator_verified")
        self.assertEqual((Decimal(1),Decimal(2)),sample.validate(live=True,today=date(2026,10,11)))
        cases=[
            (RateCard("openai","mock","1","2","https://openai.com.evil.invalid/x",
                      "2026-10-11","operator_verified"),"price_source_not_official"),
            (RateCard("openai","mock","1","2","https://openai.com/api/pricing",
                      "2026-08-01","operator_verified"),"pricing_expired"),
            (RateCard("unknown","mock","1","2","https://unknown.invalid",
                      "2026-10-11","operator_verified"),"provider_not_reviewed"),
            (RateCard("synthetic","mock","NaN","2","x","2026-10-11"),"input_rate_invalid"),
        ]
        for card,error in cases:
            with self.subTest(error=error),self.assertRaisesRegex(GateError,error):
                card.validate(live=card.evidence=="operator_verified",today=date(2026,10,11))

    def test_sdk_model_retry_output_cap_and_token_rates_exact(self):
        card=fixture(); cap=caps()
        llm=types.SimpleNamespace(model="fake/explorer",num_retries=0,
             max_output_tokens=500,input_cost_per_token=0.000002,
             output_cost_per_token=0.000008)
        self.assertEqual(Decimal("0.005"),validate_sdk_config(llm,card,cap))
        for field,value in [("model","other"),("num_retries",1),
                            ("max_output_tokens",1000),
                            ("output_cost_per_token",0.000009),
                            ("input_cost_per_token",None)]:
            with self.subTest(field=field):
                damaged=types.SimpleNamespace(**vars(llm))
                setattr(damaged,field,value)
                with self.assertRaises(GateError):
                    validate_sdk_config(damaged,card,cap)

    def test_exact_budget_edge_then_insufficient_remaining(self):
        guard,book=Guard(),BudgetBook("0.005")
        hold=book.reserve(guard,fixture(),caps())
        self.assertEqual(Decimal("0.005"),hold.ceiling_usd)
        book.settle(guard,hold,input_tokens=1,output_tokens=1,reported_usd="0.00001")
        with self.assertRaisesRegex(GateError,"worst_case_over_budget"):
            book.reserve(guard,fixture(),caps())

if __name__=="__main__":
    unittest.main()
