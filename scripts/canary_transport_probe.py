"""Synthetic transport-attempt gate; NEVER patch a real SDK or provider.

This deliberately checks one reservation for each fake transport attempt,
not merely one reservation per public completion method. No networking,
credentials, SDK monkeypatching, agent registration or LLM usage.
"""
from __future__ import annotations

import asyncio
from contextlib import contextmanager
from inspect import iscoroutinefunction
from threading import RLock, get_ident

from canary_budget import BudgetBook, RateCard, TokenCaps
from canary_controls import GateError, Guard

SINK_NAMES = (
    "litellm_completion",
    "litellm_acompletion",
    "litellm_responses",
    "litellm_aresponses",
)
ASYNC_SINKS = frozenset(("litellm_acompletion", "litellm_aresponses"))


def _execution_owner():
    try:
        task = asyncio.current_task()
    except RuntimeError:
        task = None
    return (get_ident(), task)


class SyntheticTransportGate:
    """Single logical call, single underlying transport; fail permanently on retry.

    It is *not* an SDK integration. The transport module must be an explicit
    synthetic module created by tests. A live SDK can make additional HTTP
    requests through other libraries; that remains outside this guarantee.
    """
    def __init__(self, guard: Guard, book: BudgetBook, rates: RateCard, caps: TokenCaps):
        if rates.provider != "synthetic" or rates.evidence != "synthetic":
            raise GateError("synthetic_rates_required")
        self.guard, self.book, self.rates, self.caps = guard, book, rates, caps
        self._lock = RLock()
        self._active = False
        self._owner = None
        self.attempts = 0
        self._settled = False

    def _deny(self, code):
        self.book.abort(self.guard)
        raise GateError(code)

    @contextmanager
    def logical_call(self):
        with self._lock:
            if self._active:
                self._deny("parallel_logical_calls_forbidden")
            if self.book.closed or self.guard.cancelled:
                self._deny("transport_mission_stopped")
            self._active = True
            self._owner = _execution_owner()
            self.attempts = 0
            self._settled = False
        try:
            yield self
            if not self._settled:
                self._deny("transport_usage_not_settled")
        except BaseException:
            self.book.abort(self.guard)
            raise
        finally:
            with self._lock:
                self._active = False
                self._owner = None

    def _before_transport(self):
        with self._lock:
            if not self._active or self._owner != _execution_owner():
                self._deny("transport_outside_authorized_scope")
            if self.attempts != 0:
                self._deny("second_transport_attempt_forbidden")
            if self._settled:
                self._deny("transport_after_settlement")
            # A single failed attempt may have been billed; any later retry
            # is forbidden even if the first fake raised an Exception.
            self.attempts += 1
            return self.book.reserve(self.guard, self.rates, self.caps, live=False)

    def settle(self, *, input_tokens: int, output_tokens: int, reported_usd: str):
        with self._lock:
            if not self._active or self._owner != _execution_owner():
                self._deny("settlement_outside_scope")
            if self.attempts != 1 or self._settled:
                self._deny("settlement_without_one_transport")
            ticket = self.book.active
            if ticket is None:
                self._deny("transport_reservation_missing")
            self.book.settle(self.guard, ticket, input_tokens=input_tokens,
                             output_tokens=output_tokens, reported_usd=reported_usd)
            self._settled = True

    def invoke(self, fn, *args, **kwargs):
        self._before_transport()
        try:
            return fn(*args, **kwargs)
        except BaseException:
            self.book.abort(self.guard)
            raise

    async def ainvoke(self, fn, *args, **kwargs):
        self._before_transport()
        try:
            return await fn(*args, **kwargs)
        except BaseException:
            self.book.abort(self.guard)
            raise


@contextmanager
def synthetic_litellm_sinks(module, gate: SyntheticTransportGate):
    """Patch only fake module named canary_synthetic_litellm; restore on exit."""
    if getattr(module, "__name__", None) != "canary_synthetic_litellm":
        raise GateError("actual_sdk_or_unknown_transport_forbidden")
    if getattr(module, "__canary_synthetic_transport_active__", False):
        raise GateError("transport_patch_already_active")
    originals = {name: getattr(module, name, None) for name in SINK_NAMES}
    for name, fn in originals.items():
        if not callable(fn) or iscoroutinefunction(fn) != (name in ASYNC_SINKS):
            raise GateError("unrecognized_synthetic_sink")
    installed = []
    try:
        module.__canary_synthetic_transport_active__ = True
        for name, fn in originals.items():
            if name in ASYNC_SINKS:
                async def wrapped_async(*args, _fn=fn, **kwargs):
                    return await gate.ainvoke(_fn, *args, **kwargs)
                setattr(module, name, wrapped_async)
            else:
                def wrapped_sync(*args, _fn=fn, **kwargs):
                    return gate.invoke(_fn, *args, **kwargs)
                setattr(module, name, wrapped_sync)
            installed.append(name)
        yield gate
    finally:
        for name in reversed(installed):
            setattr(module, name, originals[name])
        if getattr(module, "__canary_synthetic_transport_active__", False):
            delattr(module, "__canary_synthetic_transport_active__")
