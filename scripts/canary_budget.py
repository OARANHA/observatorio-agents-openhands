"""Offline fail-closed preflight for a future Explorer canary.

No credentials, networking, SDK calls, model selection or agent execution.
Not yet wired to SDK provider routes; never grants operational authorization.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation, Context, localcontext, Inexact, Rounded
from functools import wraps
from threading import RLock
from urllib.parse import urlsplit
from canary_controls import GateError

MILLION=Decimal(1_000_000)
MAX_RATE_AGE_DAYS=30
OFFICIAL_HOSTS={
    "openai":frozenset({"openai.com","platform.openai.com","developers.openai.com"}),
    "anthropic":frozenset({"anthropic.com","docs.anthropic.com"}),
    "google":frozenset({"ai.google.dev","cloud.google.com"}),
}

def exact_money(fn):
    """Independent exact arithmetic; never inherit caller rounding or traps."""
    @wraps(fn)
    def checked(*args, **kwargs):
        context = Context(prec=80, Emin=-99, Emax=99)
        context.traps[Inexact] = context.traps[Rounded] = True
        with localcontext(context):
            return fn(*args, **kwargs)
    return checked


def _positive_decimal(value: str, error: str) -> Decimal:
    if not isinstance(value,str) or not value.strip() or len(value)>64:
        raise GateError(error)
    try:
        result=Decimal(value)
    except InvalidOperation as exc:
        raise GateError(error) from exc
    if (not result.is_finite() or result<=0 or len(result.as_tuple().digits)>30
        or abs(result.as_tuple().exponent)>18 or result.adjusted()>12):
        raise GateError(error)
    return result

def _positive_int(value: int, error: str) -> int:
    if type(value) is not int or value<=0 or value>1_000_000_000:
        raise GateError(error)
    return value

def _identity(value: str, error: str) -> str:
    if not isinstance(value,str) or not value or not value.strip() or value!=value.strip():
        raise GateError(error)
    return value

@dataclass(frozen=True)
class RateCard:
    provider: str
    model: str
    input_usd_per_million: str
    output_usd_per_million: str
    evidence_url: str
    checked_on: str
    evidence: str="synthetic"
    pricing_variant: str="standard_no_cache"

    def validate(self, *, live: bool=False, today: date|None=None) -> tuple[Decimal,Decimal]:
        provider=_identity(self.provider,"provider_unknown")
        _identity(self.model,"model_unknown")
        input_rate=_positive_decimal(self.input_usd_per_million,"input_rate_invalid")
        output_rate=_positive_decimal(self.output_usd_per_million,"output_rate_invalid")
        if self.pricing_variant!="standard_no_cache":
            raise GateError("pricing_variant_unaccounted")
        if self.evidence not in ("synthetic","operator_verified"):
            raise GateError("pricing_evidence_invalid")
        if not live:
            return input_rate,output_rate
        if self.evidence!="operator_verified":
            raise GateError("rates_not_operator_verified")
        if provider not in OFFICIAL_HOSTS:
            raise GateError("provider_not_reviewed")
        parsed=urlsplit(self.evidence_url)
        try:
            allowed_url=(parsed.scheme=="https"
                and parsed.hostname in OFFICIAL_HOSTS[provider]
                and parsed.username is None and parsed.password is None
                and parsed.port in (None,443))
        except ValueError:
            allowed_url=False
        if not allowed_url:
            raise GateError("price_source_not_official")
        try:
            verified_date=date.fromisoformat(self.checked_on)
        except (TypeError,ValueError) as exc:
            raise GateError("pricing_date_invalid") from exc
        age=((today or date.today())-verified_date).days
        if age<0 or age>MAX_RATE_AGE_DAYS:
            raise GateError("pricing_expired")
        return input_rate,output_rate

@dataclass(frozen=True)
class TokenCaps:
    context_window: int
    max_input_tokens: int
    max_output_tokens: int
    num_retries: int=0
    max_calls: int=6
    input_bound_proven: bool=False
    output_bound_proven: bool=False
    extra_charges_ruled_out: bool=False

    def validate(self, *, live: bool=False) -> None:
        context=_positive_int(self.context_window,"context_window_missing")
        input_cap=_positive_int(self.max_input_tokens,"input_ceiling_missing")
        output_cap=_positive_int(self.max_output_tokens,"output_ceiling_missing")
        _positive_int(self.max_calls,"call_limit_invalid")
        if type(self.num_retries) is not int or self.num_retries!=0:
            raise GateError("retries_forbidden")
        if input_cap+output_cap>context:
            raise GateError("context_window_exceeded")
        if live and (self.input_bound_proven is not True
            or self.output_bound_proven is not True
            or self.extra_charges_ruled_out is not True):
            raise GateError("provider_limits_unproven")

@dataclass(frozen=True)
class Reservation:
    serial: int
    provider: str
    model: str
    ceiling_usd: Decimal
    input_rate_usd_per_million: Decimal
    output_rate_usd_per_million: Decimal
    max_input_tokens: int
    max_output_tokens: int
    max_calls: int

class BudgetBook:
    """Single-in-flight reserve/settle; uncertain failures never refund/resume.

    Requires shared Guard; not wired into all provider routes in this PR.
    """
    def __init__(self,budget_usd: str,max_calls: int=6):
        self.budget=_positive_decimal(budget_usd,"budget_invalid")
        self.max_calls=_positive_int(max_calls,"call_limit_invalid")
        self.spent=Decimal(0)
        self.calls=0
        self.active: Reservation|None=None
        self.closed=False
        self._lock=RLock()
        self._guard=None

    def _require_guard(self, guard):
        if self._guard is None:
            self._guard=guard
        elif self._guard is not guard:
            raise GateError("guard_identity_mismatch")

    @exact_money
    def reserve(self,guard,rates: RateCard,caps: TokenCaps,*,live: bool=False,
                today: date|None=None) -> Reservation:
        with self._lock:
            try:
                self._require_guard(guard)
                if self.closed or guard.cancelled or guard.clock()>=guard.deadline:
                    raise GateError("mission_unavailable")
                if self.active is not None:
                    raise GateError("parallel_requests_forbidden")
                if self.calls>=min(self.max_calls,caps.max_calls) or caps.max_calls>self.max_calls:
                    raise GateError("call_limit_exceeded")
                caps.validate(live=live)
                irate,orate=rates.validate(live=live,today=today)
                worst=(Decimal(caps.max_input_tokens)*irate+
                       Decimal(caps.max_output_tokens)*orate)/MILLION
                if self.spent+worst>self.budget:
                    raise GateError("worst_case_over_budget")
                if Decimal(str(guard.cost))+worst>Decimal(str(guard.budget)):
                    raise GateError("worst_case_over_guard_budget")
                guard.reserve()
                self.calls+=1
                reservation=Reservation(self.calls,rates.provider,rates.model,worst,irate,orate,
                                        caps.max_input_tokens,caps.max_output_tokens,
                                        min(caps.max_calls,self.max_calls,guard.max_calls))
                self.active=reservation
                return reservation
            except BaseException:
                self.abort(guard)
                raise

    @exact_money
    def settle(self,guard,reservation: Reservation,*,input_tokens: int,
               output_tokens: int,reported_usd: str) -> Decimal:
        with self._lock:
            try:
                self._require_guard(guard)
                if self.closed or self.active is not reservation or guard.cancelled:
                    raise GateError("reservation_not_active")
                if guard.clock()>=guard.deadline:
                    raise GateError("reservation_expired")
                if (type(input_tokens) is not int or type(output_tokens) is not int
                    or input_tokens<0 or output_tokens<0
                    or input_tokens>reservation.max_input_tokens
                    or output_tokens>reservation.max_output_tokens):
                    raise GateError("token_usage_outside_reservation")
                charged=_positive_decimal(reported_usd,"reported_cost_missing")
                minimum=(Decimal(input_tokens)*reservation.input_rate_usd_per_million+
                         Decimal(output_tokens)*reservation.output_rate_usd_per_million)/MILLION
                if charged<minimum:
                    raise GateError("reported_cost_below_expected")
                if charged>reservation.ceiling_usd or self.spent+charged>self.budget:
                    raise GateError("charge_exceeded_reservation")
                guard.record(float(charged),input_tokens,output_tokens)
                if guard.cancelled and (guard.clock()>=guard.deadline
                                        or guard.cost<guard.budget):
                    raise GateError("guard_stopped_during_settlement")
                self.spent+=charged
                self.active=None
                if (guard.cancelled or self.spent==self.budget
                    or self.calls>=reservation.max_calls):
                    self.closed=True
                    guard.cancel()
                return charged
            except BaseException:
                self.abort(guard)
                raise

    def abort(self,guard):
        with self._lock:
            guard.cancel()
            if self._guard is not None and self._guard is not guard:
                self._guard.cancel()
            self.closed=True

@exact_money
def validate_sdk_config(llm,rates: RateCard,caps: TokenCaps,*,live: bool=False,
                        today: date|None=None) -> Decimal:
    """Only inert SDK field comparison, not proof of provider enforcement."""
    caps.validate(live=live)
    irate,orate=rates.validate(live=live,today=today)
    # Nominal only: these observations never prove provider/network enforcement.
    if (getattr(llm,'stream',False) is not False
        or getattr(llm,'caching_prompt',False) is not False
        or getattr(llm,'fallback_strategy',None) is not None
        or getattr(llm,'_api_key_refresh_hook',None) is not None
        or getattr(llm,'litellm_extra_body',{}) != {}):
        raise GateError('sdk_unreviewed_route')
    for key,expected in {
        "model":rates.model,"num_retries":0,
        "max_output_tokens":caps.max_output_tokens
    }.items():
        actual=getattr(llm,key,None)
        if type(expected) is int:
            if type(actual) is not int or actual!=expected:
                raise GateError("sdk_model_limits_mismatch")
        elif actual!=expected:
            raise GateError("sdk_model_limits_mismatch")
    for key,expected in (
        ("input_cost_per_token",irate),("output_cost_per_token",orate)
    ):
        actual=getattr(llm,key,None)
        if type(actual) not in (int,float,str,Decimal):
            raise GateError("sdk_rate_missing")
        try:
            value=Decimal(str(actual))
        except InvalidOperation as exc:
            raise GateError("sdk_rate_invalid") from exc
        if not value.is_finite() or value<=0 or value!=expected/MILLION:
            raise GateError("sdk_rate_mismatch")
    return (Decimal(caps.max_input_tokens)*irate+
            Decimal(caps.max_output_tokens)*orate)/MILLION
