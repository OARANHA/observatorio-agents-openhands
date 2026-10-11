"""In-memory SYNTHETIC gateway model; never a server, client or dispatcher.

Accepts no arbitrary content or callback. Delivery outcome is supplied by tests,
not Slack. Dedupe is ephemeral and bounded; restart loses all replay state.
"""
import json
import uuid
from threading import RLock

from canary_controls import GateError
from canary_audit_bundle import verify_synthetic_audit_bundle
from canary_evidence_session import SyntheticEvidenceSession

FIELDS=frozenset(('schema','source','mission','conversation_id','seq','event','status','audit'))
EVENT_STATES={'needs_review':'blocked','task_finished':'finished','task_failed':'error'}


class SyntheticEventGateway:
    def __init__(self,*,conversation_id,source_sha,window_start_utc,window_end_utc,max_records=16):
        try:
            if type(conversation_id) is not str or str(uuid.UUID(conversation_id))!=conversation_id:
                raise GateError('invalid')
            self._session=SyntheticEvidenceSession(source_sha=source_sha,
                window_start_utc=window_start_utc,window_end_utc=window_end_utc,max_records=max_records)
        except (ValueError,TypeError,GateError):
            raise GateError('synthetic_gateway_denied') from None
        self._conversation=conversation_id;self._seen={};self._attempts=0
        self._stopped=False;self._lock=RLock()

    def deliver(self,event,*,mock_outcome):
        """Simulate one sanitized notification; no retries after uncertainty."""
        with self._lock:
            try:
                if (self._stopped or type(event) is not dict or frozenset(event)!=FIELDS
                    or type(mock_outcome) is not str or mock_outcome not in ('success','failed','unknown')):
                    raise GateError('invalid')
                checked=dict(event)
                if (any(type(checked[f]) is not str for f in FIELDS-{'seq','audit'})
                    or checked['schema']!='obs.synthetic.gateway.event.v1'
                    or checked['source']!='openhands-synthetic' or checked['mission']!='DEMO-001'
                    or checked['conversation_id']!=self._conversation
                    or type(checked['seq']) is not int or not 0<=checked['seq']<64
                    or checked['event'] not in EVENT_STATES
                    or checked['status']!=EVENT_STATES[checked['event']]):
                    raise GateError('invalid')
                checked['audit']=verify_synthetic_audit_bundle(checked['audit'])
                fingerprint=json.dumps(checked,sort_keys=True,separators=(',',':'),allow_nan=False)
                seq=checked['seq']
                if seq in self._seen:
                    if self._seen[seq]!=fingerprint:raise GateError('conflicting_replay')
                    return self._result('duplicate_ignored')
                if seq!=len(self._seen):raise GateError('sequence_gap')
                self._session.accept(checked['audit'])
                self._seen[seq]=fingerprint;self._attempts+=1
                if mock_outcome!='success':
                    self._stopped=True
                    return self._result('delivery_uncertain')
                result=self._result('simulated_delivered')
                result['message']=('OBS-TEST-V1 | source=openhands-synthetic | event='+checked['event']+
                    ' | mission=DEMO-001 | status='+checked['status']+' | Nenhum agente real executado.')
                return result
            except BaseException:
                self._stopped=True
                raise GateError('synthetic_gateway_denied') from None

    @staticmethod
    def _result(state):
        return {'schema':'obs.synthetic.gateway.result.v1','state':state,
            'operational_go':False,'authenticity_proven':False,'actions_allowed':False}

    def summary(self):
        with self._lock:
            return {'schema':'obs.synthetic.gateway.summary.v1','operational_go':False,
                'authenticity_proven':False,'stopped':(self._stopped or self._session.summary()['stopped']),
                'mock_attempts':self._attempts,'retention':'ephemeral_process_only'}
