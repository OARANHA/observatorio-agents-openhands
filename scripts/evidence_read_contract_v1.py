"""Synthetic read-only evidence projections; no source authentication or I/O.

Does NOT call Canvas/OpenHands/GitHub, certify agents, prove task success,
or authorize project relations. The memory-only replay fence is not durable.
"""
from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime
from threading import RLock

SCHEMA = 'obs.synthetic.evidence.read.v1'
VIEW_SCHEMA = 'obs.synthetic.evidence.view.v1'
KINDS = frozenset(('DEMO', 'PLANNED', 'CONSULTED', 'MANUAL', 'INFERRED', 'VERIFIED'))
ORIGINS = {
    'DEMO': ('fixture', 'not_observed', 'none'),
    'PLANNED': ('github_issue_fixture', 'planned', 'none'),
    'MANUAL': ('operator_fixture', 'not_observed', 'manual_unverified'),
    'INFERRED': ('heuristic_fixture', 'not_observed', 'inferred_unverified'),
}
FIELDS = frozenset((
    'schema', 'classification', 'record_id', 'source', 'provenance_kind',
    'origin', 'subject_id', 'subject_state', 'project_relation',
    'observed_at_utc', 'authorization', 'authenticity_proven',
    'agent_identity_proven', 'task_success_proven', 'operational_go',
    'dispatch_allowed', 'redaction', 'retention',
))
SOURCE_FIELDS = frozenset(('repository', 'base_sha', 'issue'))
_SHA = re.compile(r'[0-9a-f]{40}\Z')
_DIGEST = re.compile(r'[0-9a-f]{64}\Z')
_REPO = re.compile(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z')
_UTC = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\Z')


class EvidenceDenied(ValueError):
    """Refusal without echoing source payload or identifiers."""


def _timestamp(value):
    if type(value) is not str or not _UTC.fullmatch(value):
        raise EvidenceDenied('invalid_time')
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        raise EvidenceDenied('invalid_time') from None


def _uuid(value):
    try:
        return type(value) is str and str(uuid.UUID(value)) == value
    except (ValueError, AttributeError, TypeError):
        return False


class SyntheticReadOnlyEvidenceIndex:
    """Fail-closed bounded process-only fixture index; not an RBAC service."""

    def __init__(self, *, repository, base_sha, issue, window_start_utc,
                 window_end_utc, max_records=8):
        if (type(repository) is not str or not _REPO.fullmatch(repository)
                or type(base_sha) is not str or not _SHA.fullmatch(base_sha)
                or type(issue) is not int or issue < 1
                or type(max_records) is not int or not 1 <= max_records <= 32):
            raise EvidenceDenied('invalid_scope')
        start, end = _timestamp(window_start_utc), _timestamp(window_end_utc)
        if start > end:
            raise EvidenceDenied('invalid_window')
        self._source = {'repository': repository, 'base_sha': base_sha, 'issue': issue}
        self._start, self._end, self._cap = start, end, max_records
        self._ids, self._digests, self._subjects = set(), set(), set()
        self._closed = False
        self._last = None
        self._lock = RLock()

    def accept(self, observation):
        """Return safe synthetic metadata, never VERIFIED or operational activity."""
        with self._lock:
            try:
                if self._closed or len(self._ids) >= self._cap:
                    raise EvidenceDenied('stopped')
                if type(observation) is not dict or frozenset(observation) != FIELDS:
                    raise EvidenceDenied('fields_denied')
                source = observation['source']
                if (type(source) is not dict or frozenset(source) != SOURCE_FIELDS
                        or any(type(source[key]) is not type(expected) or source[key] != expected
                               for key, expected in self._source.items())):
                    raise EvidenceDenied('source_denied')
                kind = observation['provenance_kind']
                # VERIFIED is reserved; offline fixtures can never assert it.
                if type(kind) is not str or kind not in KINDS or kind == 'VERIFIED':
                    raise EvidenceDenied('provenance_denied')
                if kind == 'CONSULTED':
                    allowed = (observation['origin'] == 'canvas_get_fixture'
                               and observation['subject_state'] in ('unknown', 'running', 'finished', 'failed')
                               and observation['project_relation'] == 'none')
                else:
                    allowed = (observation['origin'], observation['subject_state'],
                               observation['project_relation']) == ORIGINS[kind]
                if (not allowed or observation['schema'] != SCHEMA
                        or observation['classification'] != 'synthetic'
                        or observation['authorization'] != 'not_granted'
                        or observation['authenticity_proven'] is not False
                        or observation['agent_identity_proven'] is not False
                        or observation['task_success_proven'] is not False
                        or observation['operational_go'] is not False
                        or observation['dispatch_allowed'] is not False
                        or observation['redaction'] != 'metadata_only'
                        or observation['retention'] != 'ephemeral_process_only'
                        or not _uuid(observation['record_id'])
                        or type(observation['subject_id']) is not str
                        or not _DIGEST.fullmatch(observation['subject_id'])):
                    raise EvidenceDenied('claim_denied')
                stamp = _timestamp(observation['observed_at_utc'])
                if not self._start <= stamp <= self._end:
                    raise EvidenceDenied('outside_window')
                if self._last is not None and stamp < self._last:
                    raise EvidenceDenied('out_of_order')
                digest = hashlib.sha256(json.dumps(observation, sort_keys=True,
                                                    separators=(',', ':'),
                                                    ensure_ascii=True).encode()).hexdigest()
                observation_key = (kind, observation['subject_id'], observation['observed_at_utc'])
                if (observation['record_id'] in self._ids or digest in self._digests
                        or observation_key in self._subjects):
                    raise EvidenceDenied('replay')
                self._subjects.add(observation_key)
                self._ids.add(observation['record_id'])
                self._digests.add(digest)
                self._last = stamp
                if len(self._ids) >= self._cap:
                    self._closed = True
                return {
                    'schema': VIEW_SCHEMA,
                    'classification': 'synthetic',
                    'provenance_kind': kind,
                    'subject_state': observation['subject_state'],
                    'project_relation': observation['project_relation'],
                    'record_id': observation['record_id'],
                    'evidence_digest_sha256': digest,
                    'authenticity_proven': False,
                    'agent_identity_proven': False,
                    'task_success_proven': False,
                    'operational_go': False,
                    'dispatch_allowed': False,
                }
            except Exception:
                self._closed = True
                raise EvidenceDenied('synthetic_evidence_denied') from None

    def summary(self):
        with self._lock:
            return {
                'schema': VIEW_SCHEMA,
                'accepted_records': len(self._ids),
                'closed': self._closed,
                'authenticity_proven': False,
                'operational_go': False,
                'dispatch_allowed': False,
                'retention': 'ephemeral_process_only',
            }
