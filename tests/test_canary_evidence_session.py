import copy,importlib.util,json,hashlib,unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from canary_controls import GateError
from canary_audit_bundle import synthetic_audit_bundle
from test_canary_transport_attempts import setup

class EvidenceSessionTests(unittest.TestCase):
    def api(self):
        self.assertIsNotNone(importlib.util.find_spec('canary_evidence_session'),'ephemeral replay consumer missing')
        from canary_evidence_session import SyntheticEvidenceSession
        return SyntheticEvidenceSession
    def session(self,**kwargs):
        return self.api()(source_sha='a'*40,window_start_utc='2026-10-11T00:00:00Z',
            window_end_utc='2026-10-11T23:59:59Z',**kwargs)
    def bundle(self,stamp='2026-10-11T12:00:00Z'):
        b=synthetic_audit_bundle(setup(),source_sha='a'*40);b['observed_at_utc']=stamp
        return self.rehash(b)
    def rehash(self,b):
        b['sha256']=hashlib.sha256(json.dumps({k:v for k,v in b.items() if k!='sha256'},
            sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest()
        return b
    def test_roundtrip_indices_and_detached_minimal_summary(self):
        s=self.session();b=self.bundle()
        self.assertEqual(1,s.accept(b))
        self.assertEqual(2,s.accept(self.bundle('2026-10-11T12:00:01Z')))
        b['accounting']['book_calls']=99
        r=s.summary();self.assertEqual(2,r['accepted_records'])
        self.assertFalse(r['operational_go']);self.assertFalse(r['authenticity_proven'])
        self.assertNotIn('accounting',r);self.assertNotIn('evidence_id',r)
    def test_replay_is_terminal_even_after_digest_recomputation(self):
        s=self.session();b=self.bundle();s.accept(b)
        altered=copy.deepcopy(b);altered['observed_at_utc']='2026-10-11T12:00:01Z'
        with self.assertRaises(GateError):s.accept(self.rehash(altered))
        with self.assertRaises(GateError):s.accept(self.bundle('2026-10-11T12:00:02Z'))
        self.assertEqual(1,s.summary()['accepted_records']);self.assertTrue(s.summary()['stopped'])
    def test_wrong_source_window_and_backward_time_are_denied(self):
        for kind in ('source','outside','backward'):
            with self.subTest(kind=kind):
                s=self.session();s.accept(self.bundle())
                b=self.bundle('2026-10-11T12:00:01Z')
                if kind=='source':b['source_sha']='b'*40
                if kind=='outside':b['observed_at_utc']='2026-10-12T00:00:00Z'
                if kind=='backward':b['observed_at_utc']='2026-10-11T11:59:59Z'
                with self.assertRaises(GateError):s.accept(self.rehash(b))
                self.assertTrue(s.summary()['stopped'])
    def test_money_and_counter_regression_are_denied(self):
        for kind in ('money','counter','budget'):
            s=self.session();a=self.bundle()
            a['accounting'].update(verified_spent_usd='0.001',book_uncommitted_usd='0.019',
                book_calls=1,guard_calls=1,guard_observed_input_tokens=100)
            s.accept(self.rehash(a));b=self.bundle('2026-10-11T12:00:01Z')
            if kind=='budget':b['accounting'].update(book_budget_usd='0.03',book_uncommitted_usd='0.03')
            if kind=='counter':b['accounting'].update(verified_spent_usd='0.001',book_uncommitted_usd='0.019')
            if kind=='money':b['accounting'].update(book_calls=1,guard_calls=1,guard_observed_input_tokens=100)
            with self.assertRaises(GateError):s.accept(self.rehash(b))
    def test_terminal_report_and_capacity_stop_acceptance(self):
        for terminal in (True,False):
            s=self.session(max_records=1);b=self.bundle()
            if terminal:b['accounting']['state']='closed_verified'
            s.accept(self.rehash(b))
            self.assertTrue(s.summary()['stopped'])
            with self.assertRaises(GateError):s.accept(self.bundle('2026-10-11T12:00:01Z'))
    def test_bad_parameters_and_private_payload_are_denied(self):
        for value in (0,True,65):
            with self.assertRaises(GateError):self.session(max_records=value)
        s=self.session();b=self.bundle();b['prompt']='SYNTHETIC_PRIVATE_ONLY'
        with self.assertRaisesRegex(GateError,'^synthetic_session_invalid$'):s.accept(self.rehash(b))
        self.assertTrue(s.summary()['stopped'])
    def test_concurrent_replay_cannot_be_accepted_twice(self):
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        s=self.session();b=self.bundle();barrier=Barrier(2)
        def accept():
            barrier.wait(timeout=2)
            try:return s.accept(b)
            except GateError:return 0
        with ThreadPoolExecutor(max_workers=2) as pool:
            values=list(pool.map(lambda _:accept(),range(2)))
        self.assertEqual([0,1],sorted(values));self.assertEqual(1,s.summary()['accepted_records'])
    def test_inexact_money_or_invalid_json_cannot_become_session_evidence(self):
        s=self.session();b=self.bundle();b['accounting']['held_usd']=False
        with self.assertRaises(GateError):s.accept(self.rehash(b))
        self.assertEqual(0,s.summary()['accepted_records'])

if __name__=='__main__':unittest.main(verbosity=2)

