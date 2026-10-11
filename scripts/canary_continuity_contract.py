"""Inert, one-shot proposal for a SYNTHETIC continuation of one conversation.

Reuses Guard/BudgetBook and the synthetic audit envelope. This neither sends a
message nor authorizes execution. State/cursor are caller-declared, not live.
An uncertain reservation remains held on denial/close. No refunds or retries.
"""
import re
from threading import RLock
import uuid

from canary_accounting_evidence import synthetic_accounting_evidence
from canary_audit_bundle import verify_synthetic_audit_bundle
from canary_controls import GateError
from canary_transport_probe import SyntheticTransportGate

MESSAGE='OBS-TEST-V1 | mission=DEMO-001 | synthetic continuation only'
FIELDS=frozenset(('schema','classification','conversation_id','state',
    'permission_mode','retries','cursor','message','approval','audit'))


def _uuid(value):
    try:
        return type(value) is str and str(uuid.UUID(value))==value
    except (ValueError,TypeError):
        return False


class SyntheticContinuationSession:
    def __init__(self,gate,*,conversation_id,source_sha):
        self._gate=gate;self._used=False;self._closed=False;self._lock=RLock()
        if (type(gate) is not SyntheticTransportGate or not _uuid(conversation_id)
            or type(source_sha) is not str or re.fullmatch('[0-9a-f]{40}',source_sha) is None):
            if isinstance(gate,SyntheticTransportGate):gate.book.abort(gate.guard)
            raise GateError('synthetic_continuation_denied')
        self._conversation=conversation_id;self._sha=source_sha

    def prepare(self,request):
        """Reserve only fictitious money; returns no runnable request or content."""
        with self._lock:
            try:
                if (self._closed or self._used or type(request) is not dict
                    or frozenset(request)!=FIELDS):raise GateError('invalid')
                if (any(type(request[f]) is not str for f in FIELDS-{'approval','audit','retries'})
                    or request['schema']!='obs.synthetic.continuation.v1'
                    or request['classification']!='synthetic'
                    or request['conversation_id']!=self._conversation
                    or request['state'] not in ('idle','paused')
                    or request['permission_mode']!='always_confirm'
                    or type(request['retries']) is not int or request['retries']!=0
                    or request['message']!=MESSAGE or request['approval'] is not True
                    or re.fullmatch('[A-Za-z0-9_=-]{1,256}',request['cursor']) is None):
                    raise GateError('invalid')
                audit=verify_synthetic_audit_bundle(request['audit'])
                if (audit['source_sha']!=self._sha
                    or audit['accounting']!=synthetic_accounting_evidence(self._gate)):
                    raise GateError('invalid')
                reservation=self._gate.book.reserve(self._gate.guard,self._gate.rates,
                    self._gate.caps,live=False)
                self._used=True
                return {'schema':'obs.synthetic.continuation.result.v1',
                    'state':'prepared_inert','operational_go':False,
                    'dispatch_allowed':False,'authenticity_proven':False,
                    'held_usd':format(reservation.ceiling_usd,'f')}
            except BaseException:
                self._closed=True;self._gate.book.abort(self._gate.guard)
                raise GateError('synthetic_continuation_denied') from None

    def close(self):
        with self._lock:
            self._closed=True;self._gate.book.abort(self._gate.guard)
