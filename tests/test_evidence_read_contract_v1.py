"""Adversarial offline fixture tests: no SDK, network, browser or provider."""
import ast
import copy
import json
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from evidence_read_contract_v1 import EvidenceDenied, SyntheticReadOnlyEvidenceIndex

SAMPLE = json.loads((ROOT / 'tests/fixtures/evidence_read_v1.synthetic.json').read_text('utf-8'))


class EvidenceReadContractV1Tests(unittest.TestCase):
    def index(self, **changes):
        options = {
            **SAMPLE['source'],
            'window_start_utc': '2026-10-11T21:00:00Z',
            'window_end_utc': '2026-10-11T23:00:00Z',
        }
        options.update(changes)
        return SyntheticReadOnlyEvidenceIndex(**options)

    def test_consulted_finished_is_not_success_or_authenticated_relation(self):
        projection = self.index().accept(copy.deepcopy(SAMPLE))
        self.assertEqual('CONSULTED', projection['provenance_kind'])
        self.assertEqual('finished', projection['subject_state'])
        self.assertEqual('none', projection['project_relation'])
        for key in ('authenticity_proven', 'agent_identity_proven',
                    'task_success_proven', 'operational_go', 'dispatch_allowed'):
            self.assertIs(projection[key], False)
        for key in ('source', 'prompt', 'agent_name', 'authorization', 'subject_id'):
            self.assertNotIn(key, projection)
        self.assertEqual(64, len(projection['evidence_digest_sha256']))

    def test_five_nonverified_kinds_have_distinct_origin_and_relation(self):
        configurations = [
            ('DEMO', 'fixture', 'not_observed', 'none'),
            ('PLANNED', 'github_issue_fixture', 'planned', 'none'),
            ('CONSULTED', 'canvas_get_fixture', 'finished', 'none'),
            ('MANUAL', 'operator_fixture', 'not_observed', 'manual_unverified'),
            ('INFERRED', 'heuristic_fixture', 'not_observed', 'inferred_unverified'),
        ]
        for kind, origin, state, relation in configurations:
            with self.subTest(kind=kind):
                payload = copy.deepcopy(SAMPLE)
                payload.update(provenance_kind=kind, origin=origin,
                               subject_state=state, project_relation=relation)
                view = self.index().accept(payload)
                self.assertEqual((kind, state, relation), (
                    view['provenance_kind'], view['subject_state'], view['project_relation']))
                self.assertIs(view['authenticity_proven'], False)

    def test_verified_and_unauthorized_promotions_fail_closed(self):
        changes = [
            ('provenance_kind', 'VERIFIED'), ('provenance_kind', 'live'),
            ('classification', 'live'), ('authorization', 'approved'),
            ('authenticity_proven', True), ('agent_identity_proven', True),
            ('task_success_proven', True), ('operational_go', True),
            ('dispatch_allowed', True), ('project_relation', 'authenticated'),
            ('origin', 'canvas_get_real'), ('redaction', 'raw'),
            ('subject_state', 'succeeded'), ('retention', 'persistent'),
        ]
        for field, value in changes:
            with self.subTest(field=field, value=value):
                item = copy.deepcopy(SAMPLE)
                item[field] = value
                index = self.index()
                with self.assertRaisesRegex(EvidenceDenied, '^synthetic_evidence_denied$'):
                    index.accept(item)
                self.assertTrue(index.summary()['closed'])
                with self.assertRaises(EvidenceDenied):
                    index.accept(copy.deepcopy(SAMPLE))

    def test_scope_type_confusion_unknown_and_private_fields(self):
        for mode in ('repo', 'sha', 'issue', 'bool_issue', 'extra', 'missing', 'private', 'bad_digest', 'bad_id'):
            with self.subTest(mode=mode):
                item = copy.deepcopy(SAMPLE)
                if mode in ('repo', 'sha', 'issue', 'bool_issue'):
                    key = {'repo': 'repository', 'sha': 'base_sha', 'issue': 'issue',
                           'bool_issue': 'issue'}[mode]
                    item['source'][key] = {'repo': 'other/repo', 'sha': 'b'*40,
                                           'issue': 48, 'bool_issue': True}[mode]
                elif mode == 'extra':
                    item['raw_output'] = 'SYNTHETIC_PRIVATE_MARKER'
                elif mode == 'missing':
                    del item['authorization']
                elif mode == 'private':
                    item['source']['token'] = 'SYNTHETIC_SECRET'
                elif mode == 'bad_digest':
                    item['subject_id'] = 'email@example.invalid'
                else:
                    item['record_id'] = 'raw conversation uuid'
                with self.assertRaises(EvidenceDenied):
                    self.index().accept(item)

    def test_temporal_window_and_replay_are_fatal(self):
        item = copy.deepcopy(SAMPLE)
        index = self.index()
        index.accept(item)
        with self.assertRaises(EvidenceDenied):
            index.accept(copy.deepcopy(item))
        self.assertEqual(1, index.summary()['accepted_records'])
        self.assertTrue(index.summary()['closed'])
        for timestamp in ('2026-10-11T20:59:59Z', '2026-10-11T23:00:01Z',
                          '2026-02-30T22:00:00Z', '2026-10-11T22:00:00+00:00'):
            with self.subTest(timestamp=timestamp):
                item = copy.deepcopy(SAMPLE)
                item['observed_at_utc'] = timestamp
                with self.assertRaises(EvidenceDenied):
                    self.index().accept(item)
        index = self.index()
        index.accept(copy.deepcopy(SAMPLE))
        earlier = copy.deepcopy(SAMPLE)
        earlier['record_id'] = '00000000-0000-4000-8000-000000000048'
        earlier['observed_at_utc'] = '2026-10-11T21:59:59Z'
        with self.assertRaises(EvidenceDenied):
            index.accept(earlier)

    def test_relabelled_record_cannot_replay_same_subject_and_time(self):
        index = self.index()
        index.accept(copy.deepcopy(SAMPLE))
        relabelled = copy.deepcopy(SAMPLE)
        relabelled['record_id'] = '00000000-0000-4000-8000-000000000048'
        with self.assertRaises(EvidenceDenied):
            index.accept(relabelled)
        self.assertTrue(index.summary()['closed'])

    def test_capacity_and_concurrency(self):
        index = self.index(max_records=1)
        index.accept(copy.deepcopy(SAMPLE))
        self.assertTrue(index.summary()['closed'])
        with self.assertRaises(EvidenceDenied):
            index.accept(copy.deepcopy(SAMPLE))
        index = self.index()
        def accept(_):
            try:
                index.accept(copy.deepcopy(SAMPLE))
                return True
            except EvidenceDenied:
                return False
        with ThreadPoolExecutor(max_workers=2) as pool:
            result = list(pool.map(accept, range(2)))
        self.assertEqual([False, True], sorted(result))
        self.assertEqual(1, index.summary()['accepted_records'])
        self.assertTrue(index.summary()['closed'])

    def test_no_effectful_imports_or_functions(self):
        path = ROOT / 'scripts/evidence_read_contract_v1.py'
        parsed = ast.parse(path.read_text('utf-8'))
        imports = [node.module for node in ast.walk(parsed) if isinstance(node, ast.ImportFrom)]
        imports += [alias.name for node in ast.walk(parsed) if isinstance(node, ast.Import)
                    for alias in node.names]
        for forbidden in ('requests', 'urllib', 'socket', 'subprocess', 'openhands', 'httpx'):
            self.assertNotIn(forbidden, imports)
        self.assertNotIn('eval(', path.read_text('utf-8'))

    def test_constructor_requires_closed_boundaries(self):
        for extra in ({'issue': True}, {'max_records': 0}, {'max_records': 33},
                      {'repository': 'invalid'}, {'base_sha': 'invalid'},
                      {'window_start_utc': '2026-10-12T00:00:00Z'}):
            with self.subTest(extra=extra):
                with self.assertRaises(EvidenceDenied):
                    self.index(**extra)


if __name__ == '__main__':
    unittest.main()
