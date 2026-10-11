"""Minimal synthetic ledger evidence; never grants an operational GO.

No SDK invocation, external requests, environment/credential reads or agents.
Fields are selected explicitly, never serialize LLM, gate or baseline objects.
"""
from decimal import Decimal
from canary_budget import exact_money, BudgetBook, RateCard, TokenCaps
from canary_controls import GateError, Guard
from canary_transport_probe import SyntheticTransportGate


@exact_money
def synthetic_accounting_evidence(gate):
    try:
        if not isinstance(gate,SyntheticTransportGate):
            raise GateError('synthetic_gate_required')
        if gate.rates.provider!='synthetic' or gate.rates.evidence!='synthetic':
            raise GateError('synthetic_rates_required')
        gate.rates.validate(live=False)
        book,guard=gate.book,gate.guard
        with book._lock, guard.lock:
            if book._guard is not None and book._guard is not guard:
                raise GateError('guard_identity_mismatch')
            held=book.active.ceiling_usd if book.active is not None else Decimal(0)
            amounts=(book.budget,book.spent,held)
            if any(type(x) is not Decimal or not x.is_finite() or x<0 for x in amounts):
                raise GateError('evidence_amount_invalid')
            remaining=book.budget-book.spent-held
            if book.budget<=0 or remaining<0:
                raise GateError('evidence_overcommitted')
            limits=(book.max_calls,guard.max_calls)
            if any(type(x) is not int or x<1 for x in limits):
                raise GateError('evidence_limit_invalid')
            counts=(book.calls,guard.calls,guard.input_tokens,guard.output_tokens)
            if (any(type(x) is not int or x<0 for x in counts)
                or book.calls>book.max_calls or guard.calls<book.calls or guard.calls>guard.max_calls
                or type(book.closed) is not bool or type(guard.cancelled) is not bool):
                raise GateError('evidence_state_invalid')
            stopped=book.closed or guard.cancelled
            state=('closed_uncertain' if held else 'closed_verified') if stopped else (
                'open_reserved' if held else 'open_idle')
            return {
                'schema':'obs.synthetic.accounting.v1',
                'operational_go':False,
                'state':state,
                'book_budget_usd':format(book.budget,'f'),
                'verified_spent_usd':format(book.spent,'f'),
                'held_usd':format(held,'f'),
                'book_uncommitted_usd':format(remaining,'f'),
                'book_calls':book.calls,
                'guard_calls':guard.calls,
                'guard_observed_input_tokens':guard.input_tokens,
                'guard_observed_output_tokens':guard.output_tokens,
            }
    except BaseException:
        if isinstance(gate,SyntheticTransportGate):
            gate.book.abort(gate.guard)
        raise


def synthetic_demo():
    """One in-memory fake response; contains no SDK LLM or provider object."""
    from types import SimpleNamespace
    from canary_sdk_success_probe import snapshot_success_start, settle_success_from_sdk_metrics
    rates=RateCard('synthetic','fake','2','8','https://example.invalid','2026-10-11')
    gate=SyntheticTransportGate(Guard(),BudgetBook('.01'),rates,TokenCaps(2000,500,500,max_calls=1))
    usage=SimpleNamespace(prompt_tokens=0,completion_tokens=0,cache_read_tokens=0,cache_write_tokens=0)
    llm=SimpleNamespace(model='fake',num_retries=0,max_output_tokens=500,
                        input_cost_per_token=.000002,output_cost_per_token=.000008,
                        metrics=SimpleNamespace(accumulated_cost=0.,accumulated_token_usage=usage))
    def fake():
        llm.metrics.accumulated_cost=.001
        usage.prompt_tokens=usage.completion_tokens=100
        return SimpleNamespace(metrics=llm.metrics)
    with gate.logical_call():
        before=snapshot_success_start(gate,llm)
        response=gate.invoke(fake)
        settle_success_from_sdk_metrics(gate,llm,before,response)
    return synthetic_accounting_evidence(gate)


if __name__=='__main__':
    import json
    print(json.dumps(synthetic_demo(),sort_keys=True))
