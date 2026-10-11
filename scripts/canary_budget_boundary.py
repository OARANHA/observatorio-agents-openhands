"""Synthetic-only budget preflight at four OpenHands SDK 1.53.0 method names.

Never use with a provider-backed LLM. No runtime/CLI/credentials/SDK import.
Patch is confined to a dedicated, disposable test process. This adapter
is deliberately NOT an operational spending ceiling.
"""
from __future__ import annotations

from contextlib import contextmanager
from decimal import Decimal
import inspect

from canary_controls import GateError
from canary_budget import validate_sdk_config
from canary_sdk import _metrics

ROUTES=("completion","acompletion","responses","aresponses")
ASYNC_ROUTES=frozenset({"acompletion","aresponses"})


@contextmanager
def synthetic_budgeted_llm_routes(llm_class, guard, book, rates, caps):
    """Connect BudgetBook reserve/settle to four *fake* SDK-shaped routes.

    Caller MUST substitute fake transports. This gate never authorizes
    a real OpenHands SDK LLM, even if its public API has these four names.
    Nested retries within an SDK method are not covered and must be audited
    separately before any operational use.
    """
    if rates.evidence!="synthetic" or rates.provider!="synthetic":
        raise GateError("synthetic_rates_required")
    if getattr(llm_class,"__canary_budget_mock_active__",False):
        raise GateError("boundary_already_active")
    if llm_class.__module__.startswith("openhands."):
        raise GateError("provider_backed_sdk_forbidden")
    originals={name:getattr(llm_class,name,None) for name in ROUTES}
    for name,fn in originals.items():
        if not callable(fn) or inspect.iscoroutinefunction(fn)!=(name in ASYNC_ROUTES):
            raise GateError("route_signature_mismatch")

    def before(llm,kwargs):
        if getattr(llm,"_canary_fake_transport",None) is not True:
            raise GateError("synthetic_transport_required")
        # For now, extra SDK call arguments (including model/output overrides,
        # streaming and fallback flags) are unapproved. The official SDK can
        # construct such arguments internally, hence this gate is MOCK ONLY.
        if kwargs:
            raise GateError("call_overrides_unreviewed")
        if getattr(llm,"stream",False) is not False:
            raise GateError("streaming_not_reviewed")
        if getattr(llm,"caching_prompt",False) is not False:
            raise GateError("cache_fallback_not_reviewed")
        validate_sdk_config(llm,rates,caps,live=False)
        starting=_metrics(llm)
        reservation=book.reserve(guard,rates,caps,live=False)
        return starting,reservation

    def after(llm,starting,reservation):
        finish=_metrics(llm)
        cost=Decimal(str(finish[0]))-Decimal(str(starting[0]))
        input_delta=finish[1]-starting[1]
        output_delta=finish[2]-starting[2]
        book.settle(guard,reservation,input_tokens=input_delta,
                    output_tokens=output_delta,reported_usd=str(cost))

    def wrap(name,fn):
        if name in ASYNC_ROUTES:
            async def async_call(llm,*args,**kwargs):
                try:
                    start,ticket=before(llm,kwargs)
                    result=await fn(llm,*args,**kwargs)
                    after(llm,start,ticket)
                    return result
                except BaseException:
                    book.abort(guard)
                    raise
            return async_call
        def call(llm,*args,**kwargs):
            try:
                start,ticket=before(llm,kwargs)
                result=fn(llm,*args,**kwargs)
                after(llm,start,ticket)
                return result
            except BaseException:
                book.abort(guard)
                raise
        return call

    setattr(llm_class,"__canary_budget_mock_active__",True)
    installed=[]
    try:
        for name,fn in originals.items():
            setattr(llm_class,name,wrap(name,fn))
            installed.append(name)
        yield
    finally:
        for name in reversed(installed):
            setattr(llm_class,name,originals[name])
        delattr(llm_class,"__canary_budget_mock_active__")
