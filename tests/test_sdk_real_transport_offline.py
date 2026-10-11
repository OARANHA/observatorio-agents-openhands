"""Exercise the *actual* OpenHands SDK 1.53.0 public methods with offline stubs.

ONLY for the ephemeral GitHub runner inside bubblewrap's unshared network
namespace. The test must prove the namespace differs from its runner host.
Never import a provider credential or send requests. The fake sinks always
raise locally; no successful inference, SDK task or agent is created.
"""
from __future__ import annotations

import asyncio
from contextlib import ExitStack, contextmanager
import importlib.metadata
import os
from pathlib import Path
import socket
import sys
import unittest
from unittest.mock import patch
from pydantic import SecretStr

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from canary_budget import BudgetBook, RateCard, TokenCaps
from canary_controls import GateError, Guard
from canary_transport_probe import SyntheticTransportGate

try:
    from openhands.sdk.llm import LLM
    import openhands.sdk.llm.llm as sdk_module
    HAS_SDK = importlib.metadata.version("openhands-sdk") == "1.53.0"
except (ImportError, importlib.metadata.PackageNotFoundError):
    LLM = None
    sdk_module = None
    HAS_SDK = False


if (os.environ.get("OBS_CANARY_HOST_NETNS")
    and os.environ.get("LITELLM_LOCAL_MODEL_COST_MAP") != "True"):
    raise RuntimeError("litellm_offline_cost_map_not_enabled")

if os.environ.get("OBS_CANARY_HOST_NETNS") and not HAS_SDK:
    raise RuntimeError("sdk_153_missing_in_isolated_runner")


class OfflineSyntheticHalt(BaseException):
    """Not caught by the SDK's provider-error fallback/retry handlers."""


class OfflineSDKFixture:
    def __init__(self):
        self.guard = Guard()
        self.book = BudgetBook("0.02")
        self.card = RateCard(
            provider="synthetic", model="openai/gpt-4o-mini",
            input_usd_per_million="2", output_usd_per_million="8",
            evidence_url="https://example.invalid/only-fake",
            checked_on="2026-10-11", evidence="synthetic",
        )
        self.caps = TokenCaps(
            context_window=2000, max_input_tokens=500,
            max_output_tokens=500, num_retries=0,
        )
        self.gate = SyntheticTransportGate(
            self.guard, self.book, self.card, self.caps
        )
        self.arrived = []

    def llm(self):
        # Known, public model identifier used only for SDK formatting; every
        # transport is a local stub and the process has no network namespace.
        return LLM(
            model="openai/gpt-4o-mini",
            api_key="NON_SECRET_SYNTHETIC_DO_NOT_USE",
            num_retries=0,
            max_output_tokens=500,
            api_mode="chat",
            stream=False,
            caching_prompt=False,
            log_completions=False,
            input_cost_per_token=0.000002,
            output_cost_per_token=0.000008,
        )

    @contextmanager
    def patch_all_four_litellm_exports(self, *, mode="halt"):
        """Patch the SDK module's imported LiteLLM bindings, not real HTTP."""
        with ExitStack() as stack:
            def stop(name):
                def fake(**_kwargs):
                    self.arrived.append(name)
                    if mode == "runtime_error":
                        raise RuntimeError("synthetic transport failure")
                    raise OfflineSyntheticHalt("synthetic sink reached")
                return fake

            def astop(name):
                async def fake(**_kwargs):
                    self.arrived.append(name)
                    if mode == "runtime_error":
                        raise RuntimeError("synthetic transport failure")
                    raise OfflineSyntheticHalt("synthetic sink reached")
                return fake

            for name in (
                "litellm_completion", "litellm_acompletion",
                "litellm_responses", "litellm_aresponses",
            ):
                if name.startswith("litellm_a"):
                    original = getattr(sdk_module, name)
                    stack.enter_context(patch.object(
                        sdk_module, name,
                        self._guarded_async(astop(name)),
                    ))
                else:
                    original = getattr(sdk_module, name)
                    stack.enter_context(patch.object(
                        sdk_module, name,
                        self._guarded_sync(stop(name)),
                    ))
                if original is None:
                    raise GateError("sdk_litellm_sink_missing")
            yield

    def _guarded_sync(self, fn):
        def wrapped(**kwargs):
            return self.gate.invoke(fn, **kwargs)
        return wrapped

    def _guarded_async(self, fn):
        async def wrapped(**kwargs):
            return await self.gate.ainvoke(fn, **kwargs)
        return wrapped


@unittest.skipUnless(HAS_SDK, "requires SDK 1.53.0 in isolated runner")
class RealSDKOfflineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Independent of the Python mocks. Bubblewrap --unshare-all creates a
        # fresh network namespace; refuse to test if this boundary is absent.
        host = os.environ.get("OBS_CANARY_HOST_NETNS")
        if not host or not host.startswith("net:["):
            raise AssertionError("missing_host_netns_evidence")
        current = os.readlink("/proc/self/ns/net")
        if host == current:
            raise AssertionError("network_namespace_not_isolated")
        interfaces = {name for _index, name in socket.if_nameindex()}
        if interfaces - {"lo"}:
            raise AssertionError("unexpected_network_interfaces")
        # This does not itself prove absolute no-egress; CI's explicit bwrap
        # flags and namespace comparison are the primary evidence.
        cls.namespace_identity = current

    def test_litellm_does_not_fetch_remote_price_map_at_import(self):
        self.assertEqual(
            "True", os.environ["LITELLM_LOCAL_MODEL_COST_MAP"]
        )

    def test_network_namespace_is_independent_of_sdk_stubs(self):
        host = os.environ["OBS_CANARY_HOST_NETNS"]
        self.assertNotEqual(host,self.namespace_identity)
        # Both checks must be independent of any patch of LiteLLM functions.
        self.assertLessEqual(
            {name for _index,name in socket.if_nameindex()}, {"lo"}
        )

    def test_four_public_sdk_routes_reach_the_guarded_stub_once(self):
        routes = {
            "completion": "litellm_completion",
            "acompletion": "litellm_acompletion",
            "responses": "litellm_responses",
            "aresponses": "litellm_aresponses",
        }
        for route, expected in routes.items():
            with self.subTest(route=route):
                fixture = OfflineSDKFixture()
                llm = fixture.llm()
                async def acall():
                    with fixture.gate.logical_call():
                        await getattr(llm, route)(messages=[])
                with fixture.patch_all_four_litellm_exports():
                    with self.assertRaises(OfflineSyntheticHalt):
                        if route.startswith("a"):
                            asyncio.run(acall())
                        else:
                            with fixture.gate.logical_call():
                                getattr(llm, route)(messages=[])
                self.assertEqual([expected],fixture.arrived)
                self.assertEqual(1,fixture.gate.attempts)
                self.assertEqual(1,fixture.book.calls)
                self.assertTrue(fixture.guard.cancelled)
                self.assertTrue(fixture.book.closed)

    def test_unreserved_real_sdk_call_cannot_reach_stub(self):
        fixture = OfflineSDKFixture()
        llm = fixture.llm()
        with fixture.patch_all_four_litellm_exports():
            with self.assertRaisesRegex(
                GateError, "transport_outside_authorized_scope"
            ):
                llm.completion(messages=[])
        self.assertEqual([], fixture.arrived)
        self.assertEqual(0,fixture.book.calls)
        self.assertTrue(fixture.book.closed)

    def test_real_sdk_cache_fallback_must_not_dispatch_twice(self):
        fixture = OfflineSDKFixture()
        llm = fixture.llm()
        with fixture.patch_all_four_litellm_exports(mode="runtime_error"):
            # Force the *real* completion() fallback branch after the first
            # synthetic RuntimeError. The second attempt must be denied at the
            # patched sink before a fake dispatch (zero provider I/O).
            with patch.object(
                sdk_module,"is_prompt_cache_too_small",
                side_effect=lambda error: (
                    type(error) is RuntimeError
                    and str(error) == "synthetic transport failure"
                )
            ), patch.object(
                LLM,"is_caching_prompt_active",return_value=True
            ):
                with self.assertRaises(GateError):
                    with fixture.gate.logical_call():
                        llm.completion(messages=[])
        self.assertEqual(["litellm_completion"],fixture.arrived)
        self.assertEqual(1,fixture.book.calls)
        self.assertTrue(fixture.book.closed)

    def test_real_sdk_refresh_path_must_not_dispatch_twice(self):
        fixture = OfflineSDKFixture()
        llm = fixture.llm()
        with fixture.patch_all_four_litellm_exports(mode="runtime_error"):
            with patch.object(
                sdk_module,"is_prompt_cache_too_small",return_value=False
            ), patch.object(
                LLM,"_resolve_refreshed_api_key",
                autospec=True,
                side_effect=lambda _self,error: (
                    SecretStr("SYNTHETIC_REFRESH_VALUE")
                    if type(error) is RuntimeError
                    and str(error) == "synthetic transport failure"
                    else None
                )
            ):
                with self.assertRaises(GateError):
                    with fixture.gate.logical_call():
                        llm.completion(messages=[])
        self.assertEqual(["litellm_completion"], fixture.arrived)
        self.assertEqual(1,fixture.book.calls)
        self.assertTrue(fixture.book.closed)


if __name__=="__main__":
    unittest.main()
