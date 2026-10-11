"""Bounded in-memory consumer of SYNTHETIC audit v1; never an authenticator.

Window/SHA are caller-declared. Replay state is lost on process disposal.
No persistence, credentials, SDK, network or execution APIs.
"""
from datetime import datetime
from decimal import Decimal
import re
from threading import RLock

from canary_audit_bundle import verify_synthetic_audit_bundle,MONEY,COUNTS
from canary_controls import GateError


def _time(value):
    if type(value) is not str or re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z',value) is None:
        raise GateError('synthetic_session_invalid')
    try:return datetime.strptime(value,'%Y-%m-%dT%H:%M:%SZ')
    except ValueError:raise GateError('synthetic_session_invalid') from None


class SyntheticEvidenceSession:
    def __init__(self,*,source_sha,window_start_utc,window_end_utc,max_records=16):
        if (type(source_sha) is not str or re.fullmatch('[0-9a-f]{40}',source_sha) is None
            or type(max_records) is not int or not 1<=max_records<=64):
            raise GateError('synthetic_session_invalid')
        start,end=_time(window_start_utc),_time(window_end_utc)
        if end<start:raise GateError('synthetic_session_invalid')
        self._sha=source_sha;self._start=start;self._end=end;self._cap=max_records
        self._ids=set();self._digests=set();self._last=None;self._stopped=False
        self._lock=RLock()

    def accept(self,bundle):
        """One local index per accepted record; any refusal latches stopped."""
        with self._lock:
            try:
                if self._stopped or len(self._ids)>=self._cap:raise GateError('capacity_or_stop')
                checked=verify_synthetic_audit_bundle(bundle)
                stamp=_time(checked['observed_at_utc'])
                if (checked['source_sha']!=self._sha or not self._start<=stamp<=self._end
                    or checked['evidence_id'] in self._ids or checked['sha256'] in self._digests):
                    raise GateError('binding_or_replay')
                if self._last is not None:
                    previous=self._last['accounting'];current=checked['accounting']
                    if (stamp<_time(self._last['observed_at_utc'])
                        or Decimal(previous[MONEY[0]])!=Decimal(current[MONEY[0]])
                        or Decimal(previous[MONEY[1]])>Decimal(current[MONEY[1]])
                        or any(current[f]<previous[f] for f in COUNTS)):
                        raise GateError('regression')
                self._ids.add(checked['evidence_id']);self._digests.add(checked['sha256'])
                self._last=checked
                if (checked['accounting']['state'].startswith('closed_')
                    or len(self._ids)>=self._cap):self._stopped=True
                return len(self._ids)
            except BaseException:
                self._stopped=True
                raise GateError('synthetic_session_invalid') from None

    def summary(self):
        with self._lock:
            return {'schema':'obs.synthetic.session.v1','operational_go':False,
                    'authenticity_proven':False,'accepted_records':len(self._ids),
                    'stopped':self._stopped,'retention':'ephemeral_process_only'}
