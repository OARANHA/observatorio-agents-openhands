"""Adversarial monetary tests, exclusively synthetic and dependency-free."""
from decimal import Decimal, localcontext, ROUND_DOWN
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from canary_budget import BudgetBook,RateCard,TokenCaps
from canary_controls import Guard,GateError

class MoneyPrecision(unittest.TestCase):
    def card(self):
        return RateCard('synthetic','fake/explorer','2.000001','8.000001','https://example.invalid','2026-10-11')
    def caps(self):
        return TokenCaps(2000,500,500)
    def test_low_precision_cannot_underreserve(self):
        with localcontext() as ambient:
            ambient.prec=2;ambient.rounding=ROUND_DOWN
            guard=Guard();book=BudgetBook('0.0050000009')
            with self.assertRaisesRegex(GateError,'worst_case_over_budget'):
                book.reserve(guard,self.card(),self.caps())
            self.assertEqual(0,guard.calls)
            self.assertTrue(book.closed)
    def test_exact_reserve_settle_ignores_ambient_precision(self):
        with localcontext() as ambient:
            ambient.prec=2;ambient.rounding=ROUND_DOWN
            guard=Guard();book=BudgetBook('0.1')
            ticket=book.reserve(guard,self.card(),self.caps())
            self.assertEqual(Decimal('0.005000001'),ticket.ceiling_usd)
            book.settle(guard,ticket,input_tokens=100,output_tokens=100,reported_usd='0.0010000002')
            self.assertEqual(Decimal('0.0010000002'),book.spent)
            self.assertEqual(2,ambient.prec)
    def test_unbounded_numeric_representations_rejected(self):
        for value in ['1e999999','1e-999999','1.'+'2'*1000]:
            with self.subTest(value=value[:20]),self.assertRaises(GateError): BudgetBook(value)

    def test_mock_boundary_cost_delta_is_not_rounded(self):
        from test_canary_budget_boundary import FakeLLM,rates,caps
        from canary_budget_boundary import synthetic_budgeted_llm_routes
        class Fractional(FakeLLM):
            def consume(self):
                result=super().consume()
                self.metrics.accumulated_cost=0.001234567
                return result
        with localcontext() as ambient:
            ambient.prec=2;ambient.rounding=ROUND_DOWN
            guard=Guard();book=BudgetBook('0.1')
            with synthetic_budgeted_llm_routes(Fractional,guard,book,rates(),caps()):
                Fractional().completion([])
            self.assertEqual(Decimal('0.001234567'),book.spent)

class MetricsBinding(unittest.TestCase):
    def fixture(self):
        import types
        from canary_transport_probe import SyntheticTransportGate
        guard=Guard();book=BudgetBook('0.1')
        gate=SyntheticTransportGate(guard,book,RateCard('synthetic','fake','2','8','https://example.invalid','2026-10-11'),TokenCaps(2000,500,500))
        llm=types.SimpleNamespace(metrics=types.SimpleNamespace(accumulated_cost=0.,accumulated_token_usage=types.SimpleNamespace(prompt_tokens=0,completion_tokens=0,cache_read_tokens=0,cache_write_tokens=0)))
        return gate,llm
    def response(self,llm):
        import copy,types
        return types.SimpleNamespace(metrics=copy.deepcopy(llm.metrics))
    def transport(self,gate,llm):
        def fake():
            llm.metrics.accumulated_cost+=.001
            llm.metrics.accumulated_token_usage.prompt_tokens+=100
            llm.metrics.accumulated_token_usage.completion_tokens+=100
        gate.invoke(fake)
    def test_baseline_requires_active_logical_scope(self):
        from canary_sdk_success_probe import snapshot_success_start
        gate,llm=self.fixture()
        with self.assertRaises(GateError):snapshot_success_start(gate,llm)
        self.assertTrue(gate.book.closed)
    def test_invalid_or_unpriced_cache_denied_before_transport(self):
        from canary_sdk_success_probe import snapshot_success_start
        for value in (-1,True,None,1):
            gate,llm=self.fixture();llm.metrics.accumulated_token_usage.cache_read_tokens=value
            with self.assertRaises(GateError):
                with gate.logical_call():
                    with self.assertRaisesRegex(GateError, "sdk_cache_"):snapshot_success_start(gate,llm)
            self.assertEqual(0,gate.book.calls)
    def test_baseline_from_other_llm_never_settles(self):
        import copy
        from canary_sdk_success_probe import snapshot_success_start,settle_success_from_sdk_metrics
        gate,llm=self.fixture();other=copy.deepcopy(llm)
        with self.assertRaises(GateError):
            with gate.logical_call():
                before=snapshot_success_start(gate,llm)
                self.transport(gate,other)
                settle_success_from_sdk_metrics(gate,other,before,self.response(other))
        self.assertIsNotNone(gate.book.active)
        self.assertEqual(Decimal(0),gate.book.spent)
    def test_forged_or_stale_baseline_cannot_be_reused(self):
        from canary_sdk_success_probe import snapshot_success_start,settle_success_from_sdk_metrics
        gate,llm=self.fixture()
        with gate.logical_call():
            before=snapshot_success_start(gate,llm);self.transport(gate,llm)
            settle_success_from_sdk_metrics(gate,llm,before,self.response(llm))
        with self.assertRaises(GateError):
            with gate.logical_call():
                self.transport(gate,llm)
                settle_success_from_sdk_metrics(gate,llm,before,self.response(llm))
        self.assertEqual(Decimal('.001'),gate.book.spent)
    def test_response_cache_snapshot_must_match(self):
        from canary_sdk_success_probe import snapshot_success_start,settle_success_from_sdk_metrics
        gate,llm=self.fixture()
        with self.assertRaises(GateError):
            with gate.logical_call():
                before=snapshot_success_start(gate,llm);self.transport(gate,llm)
                response=self.response(llm)
                response.metrics.accumulated_token_usage.cache_read_tokens=1
                settle_success_from_sdk_metrics(gate,llm,before,response)
        self.assertTrue(gate.book.closed)

    def test_forged_tuple_and_replaced_metrics_are_denied(self):
        import copy
        from canary_sdk_success_probe import snapshot_success_start,settle_success_from_sdk_metrics
        for mode in ('tuple','replaced'):
            gate,llm=self.fixture()
            with self.assertRaisesRegex(GateError,'sdk_baseline_not_authoritative'):
                with gate.logical_call():
                    before=snapshot_success_start(gate,llm)
                    self.transport(gate,llm)
                    if mode=='tuple':before=(0.,0,0)
                    else:llm.metrics=copy.deepcopy(llm.metrics)
                    settle_success_from_sdk_metrics(gate,llm,before,self.response(llm))
            self.assertTrue(gate.guard.cancelled)
            self.assertIsNotNone(gate.book.active)

class TerminalSettlement(unittest.TestCase):
    def card(self):return RateCard('synthetic','fake','2','8','https://example.invalid','2026-10-11')
    def test_token_caps_call_limit_closes_after_last_verified_call(self):
        book=BudgetBook('.1');guard=Guard();caps=TokenCaps(2000,500,500,max_calls=1)
        hold=book.reserve(guard,self.card(),caps)
        book.settle(guard,hold,input_tokens=100,output_tokens=100,reported_usd='.001')
        self.assertTrue(book.closed);self.assertTrue(guard.cancelled)
        with self.assertRaises(GateError):book.reserve(guard,self.card(),caps)
        self.assertEqual(1,book.calls)
        self.assertIsNone(book.active)
    def test_exact_guard_budget_exhaustion_records_known_spend_once(self):
        book=BudgetBook('.005');guard=Guard(budget=.005)
        hold=book.reserve(guard,self.card(),TokenCaps(2000,500,500))
        self.assertEqual(Decimal('.005'),book.settle(guard,hold,input_tokens=500,output_tokens=500,reported_usd='.005'))
        self.assertEqual(Decimal('.005'),book.spent)
        self.assertIsNone(book.active);self.assertTrue(book.closed);self.assertTrue(guard.cancelled)
        with self.assertRaises(GateError):book.settle(guard,hold,input_tokens=500,output_tokens=500,reported_usd='.005')
        self.assertEqual(Decimal('.005'),book.spent)
    def test_expired_reservation_is_uncertain_not_refunded(self):
        now=[0];guard=Guard(seconds=1,clock=lambda:now[0]);book=BudgetBook('.1')
        hold=book.reserve(guard,self.card(),TokenCaps(2000,500,500));now[0]=1
        with self.assertRaisesRegex(GateError,'reservation_expired'):
            book.settle(guard,hold,input_tokens=100,output_tokens=100,reported_usd='.001')
        self.assertIs(book.active,hold);self.assertTrue(book.closed)
    def test_a_different_guard_cannot_reset_the_mission(self):
        book=BudgetBook('.1');guard=Guard();caps=TokenCaps(2000,500,500)
        hold=book.reserve(guard,self.card(),caps)
        book.settle(guard,hold,input_tokens=100,output_tokens=100,reported_usd='.001')
        other=Guard()
        with self.assertRaisesRegex(GateError,'guard_identity_mismatch'):book.reserve(other,self.card(),caps)
        self.assertTrue(guard.cancelled);self.assertTrue(other.cancelled);self.assertTrue(book.closed)
    def test_no_further_llm_or_terminal_actions_after_last_call(self):
        from test_canary_budget_boundary import FakeLLM,rates
        from canary_budget_boundary import synthetic_budgeted_llm_routes
        from canary_controls import mission_confirmation,MissionCancelled
        import types
        book=BudgetBook('.1');guard=Guard();llm=FakeLLM()
        with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),TokenCaps(2000,500,500,max_calls=1)):
            llm.completion([])
            with self.assertRaises(GateError):llm.completion([])
        self.assertEqual(1,llm.dispatches)
        event=types.SimpleNamespace(action=types.SimpleNamespace(command='pwd',is_input=False))
        with self.assertRaises(MissionCancelled):mission_confirmation(guard,'synthetic',[event],lambda *_:True)

    def test_smaller_guard_budget_is_reserved_preventively(self):
        book=BudgetBook('.1');guard=Guard(budget=.004)
        with self.assertRaisesRegex(GateError,'worst_case_over_guard_budget'):
            book.reserve(guard,self.card(),TokenCaps(2000,500,500))
        self.assertEqual(0,guard.calls);self.assertIsNone(book.active)
