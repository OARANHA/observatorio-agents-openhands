"""Reconcile *successful synthetic* SDK telemetry with BudgetBook.

Never authorizes live transport. Used only by isolated tests with pre-reserved
fake LiteLLM sinks. The SDK must produce an LLMResponse and update its metrics;
neither caller-provided usage nor a guess can substitute for those observations.
"""
from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

from canary_budget import MILLION
from canary_controls import GateError
from canary_sdk import _metrics


def settle_success_from_sdk_metrics(gate, llm, before, sdk_response):
    """Fail-closed exact synthetic USD calculation from SDK metrics deltas."""
    try:
        if getattr(sdk_response, "metrics", None) is None:
            raise GateError("sdk_success_metrics_missing")
        now = _metrics(llm)
        response_snapshot = _metrics(SimpleNamespace(metrics=sdk_response.metrics))
        if now != response_snapshot:
            raise GateError("sdk_response_metrics_not_authoritative")
        before_usd, before_input, before_output = before
        delta_input = now[1] - before_input
        delta_output = now[2] - before_output
        delta_cost = Decimal(str(now[0])) - Decimal(str(before_usd))
        if delta_input < 0 or delta_output < 0 or delta_input + delta_output == 0:
            raise GateError("sdk_success_usage_missing_or_decreased")
        if delta_cost <= 0 or not delta_cost.is_finite():
            raise GateError("sdk_success_cost_missing_or_decreased")
        # No cache pricing has been reviewed. Cache buckets are not part of
        # the synthetic flat-rate price. Reject any cache token activity.
        usage = llm.metrics.accumulated_token_usage
        prior_cache = getattr(gate, "_canary_prior_cache", (0, 0))
        current_cache = (
            getattr(usage, "cache_read_tokens", 0),
            getattr(usage, "cache_write_tokens", 0),
        )
        if any(type(x) is not int or x < 0 for x in (*prior_cache, *current_cache)):
            raise GateError("sdk_cache_accounting_invalid")
        if current_cache != prior_cache:
            raise GateError("sdk_cache_pricing_not_reviewed")
        ir, out = gate.card_rates()
        expected = (Decimal(delta_input) * ir +
                    Decimal(delta_output) * out) / MILLION
        if delta_cost != expected:
            raise GateError("sdk_synthetic_cost_mismatch")
        gate.settle(
            input_tokens=delta_input,
            output_tokens=delta_output,
            reported_usd=str(delta_cost),
        )
        return delta_input, delta_output, delta_cost
    except BaseException:
        gate.book.abort(gate.guard)
        raise


def snapshot_success_start(gate, llm):
    """Get an SDK baseline for one isolated call, before any transport."""
    try:
        usage = llm.metrics.accumulated_token_usage
        if usage is None:
            raise GateError("sdk_usage_baseline_missing")
        gate._canary_prior_cache = (
            getattr(usage, "cache_read_tokens", 0),
            getattr(usage, "cache_write_tokens", 0),
        )
        return _metrics(llm)
    except BaseException:
        gate.book.abort(gate.guard)
        raise
