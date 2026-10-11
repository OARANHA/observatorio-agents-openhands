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
