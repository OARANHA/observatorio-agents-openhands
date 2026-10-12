"""Negative tests for an inert planning envelope: no SDK, provider or dispatch."""
import copy
import json
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from canary_controls import GateError
from mission_plan_v1 import SyntheticMissionPlanQueue, RECEIPT

SAMPLE = json.loads((ROOT / 'tests/fixtures/mission_plan_v1.synthetic.json').read_text(encoding='utf-8'))


class MissionPlanV1Tests(unittest.TestCase):
    def queue(self, **kwargs):
        return SyntheticMissionPlanQueue(
            repository=SAMPLE['source']['repository'],
            base_sha=SAMPLE['source']['base_sha'], issue=46, **kwargs,
        )

    def test_one_synthetic_proposal_is_not_dispatch(self):
        queue = self.queue()
        receipt = queue.propose(copy.deepcopy(SAMPLE))
        self.assertEqual(RECEIPT, receipt['schema'])
        self.assertEqual('planned_offline', receipt['state'])
        self.assertEqual(1, receipt['accepted_plans'])
        self.assertFalse(receipt['operational_go'])
        self.assertFalse(receipt['dispatch_allowed'])
        self.assertFalse(receipt['authenticity_proven'])
        self.assertNotIn('tools', receipt)
        self.assertNotIn('objective_id', receipt)
        self.assertNotIn('mission_id', queue.summary())
        self.assertEqual('ephemeral_process_only', queue.summary()['retention'])

    def test_no_approval_and_future_statuses_are_not_runnable(self):
        for field, value in [('authorization', 'approved'), ('authorization', True),
                             ('state', 'approved'), ('state', 'executing'),
                             ('state', 'verified'), ('dispatch_allowed', True),
                             ('operational_go', True), ('classification', 'live'),
                             ('budget_usd', '0.10'), ('evidence_id', 'fake-proof'),
                             ('objective_id', 'run_agent')]:
            with self.subTest(field=field, value=value):
                queue = self.queue()
                sample = copy.deepcopy(SAMPLE)
                sample[field] = value
                with self.assertRaisesRegex(GateError, '^synthetic_plan_denied$'):
                    queue.propose(sample)
                self.assertEqual('closed', queue.summary()['state'])
                self.assertEqual(0, queue.summary()['accepted_plans'])

    def test_repo_sha_and_issue_binding_rejected(self):
        for field, value in [('repository', 'OTHER/project'),
                             ('base_sha', 'b' * 40), ('issue', 47),
                             ('issue', True)]:
            queue = self.queue()
            sample = copy.deepcopy(SAMPLE)
            sample['source'][field] = value
            with self.subTest(field=field):
                with self.assertRaises(GateError):
                    queue.propose(sample)
                with self.assertRaises(GateError):
                    queue.propose(copy.deepcopy(SAMPLE))

    def test_unknown_private_fields_missing_fields_and_action_injection(self):
        for mutation in ('private', 'missing', 'unauthorized_tool',
                         'duplicate_tool', 'credential', 'bad_uuid'):
            queue = self.queue()
            sample = copy.deepcopy(SAMPLE)
            if mutation == 'private':
                sample['prompt'] = 'SYNTHETIC_PRIVATE_MARKER'
            elif mutation == 'missing':
                del sample['authorization']
            elif mutation == 'unauthorized_tool':
                sample['tools'] = ['cat /etc/passwd']
            elif mutation == 'duplicate_tool':
                sample['tools'] = ['pwd', 'pwd']
            elif mutation == 'credential':
                sample['source']['token'] = 'SYNTHETIC_SECRET'
            else:
                sample['mission_id'] = 'untrusted mission'
            with self.subTest(mutation=mutation):
                with self.assertRaises(GateError):
                    queue.propose(sample)

    def test_limits_type_confusion_and_retries_rejected(self):
        for key, value in [('max_actions', 7), ('max_actions', 0),
                           ('max_actions', True), ('timeout_seconds', 121),
                           ('timeout_seconds', 0), ('timeout_seconds', False),
                           ('retries', 1), ('retries', True)]:
            queue = self.queue()
            sample = copy.deepcopy(SAMPLE)
            sample[key] = value
            with self.subTest(key=key, value=value):
                with self.assertRaises(GateError):
                    queue.propose(sample)
                self.assertEqual(0, queue.summary()['accepted_plans'])

    def test_duplicate_id_or_full_capacity_stops_further_proposals(self):
        queue = self.queue()
        queue.propose(copy.deepcopy(SAMPLE))
        with self.assertRaises(GateError):
            queue.propose(copy.deepcopy(SAMPLE))
        self.assertEqual('closed', queue.summary()['state'])
        queue = self.queue(max_plans=1)
        queue.propose(copy.deepcopy(SAMPLE))
        another = copy.deepcopy(SAMPLE)
        another['mission_id'] = '00000000-0000-4000-8000-000000000047'
        with self.assertRaises(GateError):
            queue.propose(another)
        self.assertEqual(1, queue.summary()['accepted_plans'])

    def test_concurrent_identical_proposals_cannot_both_pass(self):
        queue = self.queue()
        def attempt(_):
            try:
                queue.propose(copy.deepcopy(SAMPLE))
                return True
            except GateError:
                return False
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(attempt, range(2)))
        self.assertEqual([False, True], sorted(outcomes))
        self.assertEqual(1, queue.summary()['accepted_plans'])
        self.assertEqual('closed', queue.summary()['state'])

    def test_invalid_queue_configuration_is_rejected(self):
        source = SAMPLE['source']
        cases = [
            dict(repository='bad', base_sha=source['base_sha'], issue=46),
            dict(repository=source['repository'], base_sha='bad', issue=46),
            dict(repository=source['repository'], base_sha=source['base_sha'], issue=True),
            dict(repository=source['repository'], base_sha=source['base_sha'], issue=46, max_plans=0),
        ]
        for kw in cases:
            with self.subTest(kw=kw):
                with self.assertRaises(GateError):
                    SyntheticMissionPlanQueue(**kw)


if __name__ == '__main__':
    unittest.main()
