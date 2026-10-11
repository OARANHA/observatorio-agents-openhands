"""Static SDK transport inventory; installed-SDK tests run in disposable CI."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from canary_controls import GateError
from audit_canary_sdk_transport import check_source, inspect_installed_sdk


def synthetic_sdk_source():
    return '''
from litellm import completion as litellm_completion
from litellm import acompletion as litellm_acompletion
from litellm.responses.main import responses as litellm_responses
from litellm.responses.main import aresponses as litellm_aresponses
class LLM:
    def completion(self):
        pass
    async def acompletion(self):
        pass
    def responses(self):
        return litellm_responses()
    async def aresponses(self):
        return await litellm_aresponses()
    def _transport_call(self):
        return litellm_completion()
    async def _atransport_call(self):
        return await litellm_acompletion()
    def _make_retry_decorator(self):
        pass
    def _handle_error(self):
        pass
    async def _ahandle_error(self):
        pass
    def _resolve_refreshed_api_key(self):
        pass
    def _auth_refreshed_llm(self):
        pass
    def resolve_runtime_metadata(self):
        return resolve_provider_metadata_sync(self)
    async def aresolve_runtime_metadata(self):
        return await aresolve_provider_metadata(self)
'''


class SyntheticAstAudit(unittest.TestCase):
    def test_exact_approved_sink_inventory(self):
        out=check_source(synthetic_sdk_source())
        self.assertEqual(4,len(out["reviewed_sinks"]))
        self.assertEqual("surface_inventory_only_no_live_go",out["verdict"])

    def test_new_sink_call_fails_before_any_execution(self):
        code=synthetic_sdk_source().replace(
            "return litellm_completion()",
            "litellm_completion(); return litellm_completion()")
        with self.assertRaisesRegex(GateError,"sdk_transport_calls_changed"):
            check_source(code)

    def test_moved_sink_call_fails(self):
        code=synthetic_sdk_source().replace(
            "return litellm_responses()","return litellm_completion()")
        with self.assertRaisesRegex(GateError,"sdk_transport_calls_changed"):
            check_source(code)

    def test_new_call_outside_sdk_llm_class_is_detected(self):
        code=synthetic_sdk_source()+"\ndef shadow_transport():\n    return litellm_completion()\n"
        with self.assertRaisesRegex(GateError,"sdk_unreviewed_litellm_sink_call"):
            check_source(code)

    def test_new_direct_litellm_call_fails(self):
        code=synthetic_sdk_source().replace(
            "return litellm_responses()", "return litellm.completion()")
        with self.assertRaisesRegex(GateError,"sdk_new_direct_litellm_call"):
            check_source(code)

    def test_missing_metadata_discovery_inventory_fails(self):
        code=synthetic_sdk_source().replace(
            "return resolve_provider_metadata_sync(self)","return None")
        with self.assertRaisesRegex(GateError,"sdk_metadata_egress_inventory_changed"):
            check_source(code)

    def test_new_alias_or_removed_method_fails(self):
        code=synthetic_sdk_source().replace(
            "from litellm import completion as litellm_completion",
            "from alternate import completion as litellm_completion")
        with self.assertRaisesRegex(GateError,"sdk_litellm_alias_inventory_changed"):
            check_source(code)


try:
    from importlib.metadata import version
    HAS_SDK=(version("openhands-sdk")=="1.53.0")
except Exception:
    HAS_SDK=False


@unittest.skipUnless(HAS_SDK,"requires isolated SDK 1.53.0")
class OfficialSDKTransportAudit(unittest.TestCase):
    def test_exact_installed_sdk_v153_source_inventory(self):
        out=inspect_installed_sdk()
        self.assertEqual(4,len(out["reviewed_sinks"]))
        self.assertEqual(
            ["aresolve_provider_metadata","resolve_provider_metadata_sync"],
            out["known_metadata_egress"])
        self.assertEqual(0,out["provider_calls_in_audit"])


if __name__=="__main__":
    unittest.main()
