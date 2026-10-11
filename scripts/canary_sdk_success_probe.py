"""Reconcile *successful synthetic* SDK telemetry with BudgetBook.

Never authorizes live transport. Used only by isolated tests with pre-reserved
fake LiteLLM sinks. The SDK must produce an LLMResponse and update its metrics;
neither caller-provided usage nor a guess can substitute for those observations.
"""
from __future__ import annotations

from decimal import Decimal
from dataclasses import dataclass
from types import SimpleNamespace

from canary_budget import MILLION, exact_money, validate_sdk_config
from canary_controls import GateError
from canary_sdk import _metrics


@dataclass(frozen=True)
class SDKBaseline:
    gate: object
    llm: object
    metrics: object
    serial: int
    totals: tuple


def _cache(metrics):
    usage = getattr(metrics,'accumulated_token_usage',None)
    if usage is None:
        raise GateError('usage_missing')
    counts = (getattr(usage, "cache_read_tokens", None),
              getattr(usage, "cache_write_tokens", None))
    if any(type(x) is not int or x < 0 for x in counts):
        raise GateError("sdk_cache_accounting_invalid")
    if any(counts):
        raise GateError("sdk_cache_pricing_not_reviewed")
    return counts


@exact_money
def settle_success_from_sdk_metrics(gate, llm, before, sdk_response):
    """Fail-closed exact synthetic USD calculation from SDK metrics deltas."""
    try:
        serial = gate.scope_identity()
        validate_sdk_config(llm,gate.rates,gate.caps,live=False)
        if (not isinstance(before, SDKBaseline) or gate._sdk_baseline is not before
            or before.gate is not gate or before.llm is not llm
            or before.metrics is not llm.metrics or before.serial != serial):
            raise GateError("sdk_baseline_not_authoritative")
        if getattr(sdk_response, "metrics", None) is None:
            raise GateError("sdk_success_metrics_missing")
        now = _metrics(llm)
        response_snapshot = _metrics(SimpleNamespace(metrics=sdk_response.metrics))
        if now != response_snapshot:
            raise GateError("sdk_response_metrics_not_authoritative")
        before_usd, before_input, before_output = before.totals
        delta_input = now[1] - before_input
        delta_output = now[2] - before_output
        delta_cost = Decimal(str(now[0])) - Decimal(str(before_usd))
        if delta_input < 0 or delta_output < 0 or delta_input + delta_output == 0:
            raise GateError("sdk_success_usage_missing_or_decreased")
        if delta_cost <= 0 or not delta_cost.is_finite():
            raise GateError("sdk_success_cost_missing_or_decreased")
        _cache(llm.metrics)
        _cache(sdk_response.metrics)
        ir, out = gate.rates.validate(live=False)
        expected = (Decimal(delta_input) * ir +
                    Decimal(delta_output) * out) / MILLION
        if delta_cost != expected:
            raise GateError("sdk_synthetic_cost_mismatch")
        gate.settle(
            input_tokens=delta_input,
            output_tokens=delta_output,
            reported_usd=str(delta_cost),
        )
        gate._sdk_baseline = None
        return delta_input, delta_output, delta_cost
    except BaseException:
        gate.book.abort(gate.guard)
        raise


def snapshot_success_start(gate, llm):
    """Get an SDK baseline for one isolated call, before any transport."""
    try:
        serial = gate.scope_identity()
        validate_sdk_config(llm,gate.rates,gate.caps,live=False)
        if gate.attempts != 0 or gate._sdk_baseline is not None:
            raise GateError("sdk_baseline_not_before_transport")
        _cache(llm.metrics)
        baseline = SDKBaseline(gate, llm, llm.metrics, serial, _metrics(llm))
        gate._sdk_baseline = baseline
        return baseline
    except BaseException:
        gate.book.abort(gate.guard)
        raise
