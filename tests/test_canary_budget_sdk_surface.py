"""SDK 1.53.0 surface compatibility, no LLM instance/provider requests."""
import importlib.metadata
import inspect
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from canary_budget import BudgetBook, RateCard, TokenCaps
from canary_budget_boundary import ROUTES, ASYNC_ROUTES, synthetic_budgeted_llm_routes
from canary_controls import GateError,Guard

try:
    from openhands.sdk.llm import LLM
    HAS_153 = importlib.metadata.version("openhands-sdk") == "1.53.0"
except (ImportError, importlib.metadata.PackageNotFoundError):
    LLM=None
    HAS_153=False


@unittest.skipUnless(HAS_153,"requires isolated SDK 1.53.0")
class OfficialSDKRouteSurface(unittest.TestCase):
    def test_four_real_methods_are_present_and_match_async_kinds(self):
        for name in ROUTES:
            with self.subTest(name=name):
                fn=getattr(LLM,name)
                self.assertEqual(name in ASYNC_ROUTES,inspect.iscoroutinefunction(fn))
                parameters=inspect.signature(fn).parameters
                self.assertIn("self",parameters)
                self.assertIn("messages",parameters)

    def test_real_provider_backed_sdk_is_denied_before_patch_or_network(self):
        originals={name:getattr(LLM,name) for name in ROUTES}
        card=RateCard("synthetic","fake/explorer","2","8","https://example.invalid",
                      "2026-10-11","synthetic")
        caps=TokenCaps(context_window=2000,max_input_tokens=500,max_output_tokens=500)
        with self.assertRaisesRegex(GateError,"provider_backed_sdk_forbidden"):
            with synthetic_budgeted_llm_routes(LLM,Guard(),BudgetBook("0.01"),card,caps):
                self.fail("should not enter")
        for name,original in originals.items():
            self.assertIs(original,getattr(LLM,name))


if __name__=="__main__":
    unittest.main()
