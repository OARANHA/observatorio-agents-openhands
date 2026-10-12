"""Inert, memory-only planning queue. NEVER dispatches an OpenHands task or agent.

Only a closed, synthetic intent envelope is accepted. This is not an
authorization system, durable replay ledger, budget enforcer or worker.
"""
from __future__ import annotations

import re
import uuid
from threading import RLock

from canary_controls import ALLOWED, GateError

SCHEMA = 'obs.synthetic.mission.plan.v1'
RECEIPT = 'obs.synthetic.mission.plan.receipt.v1'
FIELDS = frozenset((
    'schema', 'classification', 'mission_id', 'source', 'objective_id',
    'state', 'authorization', 'tools', 'max_actions', 'timeout_seconds',
    'budget_usd', 'retries', 'evidence_id', 'redaction', 'retention',
    'operational_go', 'dispatch_allowed',
))
SOURCE_FIELDS = frozenset(('repository', 'base_sha', 'issue'))
OBJECTIVE = 'inspect_public_contracts'


def _is_uuid(value):
    try:
        return type(value) is str and str(uuid.UUID(value)) == value
    except (ValueError, TypeError, AttributeError):
        return False


class SyntheticMissionPlanQueue:
    """Bounded in-memory proposal validation; no execution or authentication."""

    def __init__(self, *, repository, base_sha, issue, max_plans=8):
        if (type(repository) is not str or re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository) is None
                or type(base_sha) is not str or re.fullmatch(r'[0-9a-f]{40}', base_sha) is None
                or type(issue) is not int or issue < 1
                or type(max_plans) is not int or not 1 <= max_plans <= 16):
            raise GateError('mission_plan_scope_invalid')
        self._repository = repository
        self._sha = base_sha
        self._issue = issue
        self._max = max_plans
        self._seen = set()
        self._closed = False
        self._lock = RLock()

    def propose(self, plan):
        """Return a *non-runnable* receipt or permanently stop this queue."""
        with self._lock:
            try:
                if self._closed or len(self._seen) >= self._max:
                    raise GateError('queue_stopped')
                if type(plan) is not dict or frozenset(plan) != FIELDS:
                    raise GateError('fields_denied')
                source = plan['source']
                if (type(source) is not dict or frozenset(source) != SOURCE_FIELDS
                        or type(source['repository']) is not str
                        or source['repository'] != self._repository
                        or type(source['base_sha']) is not str
                        or source['base_sha'] != self._sha
                        or type(source['issue']) is not int
                        or source['issue'] != self._issue):
                    raise GateError('source_binding_denied')
                tools = plan['tools']
                if (type(tools) is not list or not 1 <= len(tools) <= 4
                        or any(type(t) is not str or t not in ALLOWED for t in tools)
                        or len(set(tools)) != len(tools)):
                    raise GateError('tools_denied')
                if (plan['schema'] != SCHEMA or plan['classification'] != 'synthetic'
                        or plan['objective_id'] != OBJECTIVE
                        or plan['state'] != 'planned'
                        or plan['authorization'] != 'not_granted'
                        or plan['redaction'] != 'deny_private_fields'
                        or plan['retention'] != 'ephemeral_process_only'
                        or plan['budget_usd'] is not None
                        or plan['evidence_id'] is not None
                        or plan['operational_go'] is not False
                        or plan['dispatch_allowed'] is not False
                        or type(plan['retries']) is not int or plan['retries'] != 0
                        or type(plan['max_actions']) is not int or not 1 <= plan['max_actions'] <= 6
                        or type(plan['timeout_seconds']) is not int
                        or not 1 <= plan['timeout_seconds'] <= 120
                        or not _is_uuid(plan['mission_id'])
                        or plan['mission_id'] in self._seen):
                    raise GateError('plan_denied')
                self._seen.add(plan['mission_id'])
                return {
                    'schema': RECEIPT,
                    'state': 'planned_offline',
                    'classification': 'synthetic',
                    'operational_go': False,
                    'dispatch_allowed': False,
                    'authenticity_proven': False,
                    'accepted_plans': len(self._seen),
                }
            except Exception:
                self._closed = True
                raise GateError('synthetic_plan_denied') from None

    def summary(self):
        with self._lock:
            return {
                'schema': RECEIPT,
                'state': 'closed' if self._closed else 'planned_offline',
                'accepted_plans': len(self._seen),
                'operational_go': False,
                'dispatch_allowed': False,
                'authenticity_proven': False,
                'retention': 'ephemeral_process_only',
            }
