"""Synthetic provenance and integrity; no SDK, network, or private payloads."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from canary_controls import GateError
from test_canary_transport_attempts import setup


class SyntheticAuditTests(unittest.TestCase):
    def api(self):
        self.assertIsNotNone(importlib.util.find_spec('canary_audit_bundle'),
                             'versioned synthetic bundle is missing')
        import canary_audit_bundle
        return canary_audit_bundle

    def bundle(self):
        return self.api().synthetic_audit_bundle(setup(), source_sha='a'*40)

    def rehash(self, bundle):
        data={k:v for k,v in bundle.items() if k!='sha256'}
        bundle['sha256']=hashlib.sha256(json.dumps(data,sort_keys=True,
            separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest()
        return bundle

    def test_roundtrip_and_unique_synthetic_identity(self):
        api=self.api()
        a,b=self.bundle(),self.bundle()
        self.assertNotEqual(a['evidence_id'], b['evidence_id'])
        self.assertEqual(a,api.load_synthetic_audit_bundle(json.dumps(a)))
        self.assertFalse(a['operational_go'])
        self.assertFalse(a['authenticity_proven'])
        self.assertEqual('caller_declared_public_git_sha',a['source_claim'])

    def test_tampering_without_new_digest_fails(self):
        b=self.bundle()
        b['source_sha']='b'*40
        with self.assertRaises(GateError):
            self.api().verify_synthetic_audit_bundle(b)

    def test_rehashed_operational_claims_and_private_fields_fail(self):
        for field,value in [('operational_go',True),('authenticity_proven',True),
                            ('classification','operational'),('api_key','SYNTHETIC_ONLY')]:
            with self.subTest(field=field):
                b=self.bundle(); b[field]=value
                with self.assertRaises(GateError):
                    self.api().verify_synthetic_audit_bundle(self.rehash(b))
        b=self.bundle(); b['accounting']['prompt']='SYNTHETIC_ONLY'
        with self.assertRaises(GateError):
            self.api().verify_synthetic_audit_bundle(self.rehash(b))

    def test_exact_finances_counts_and_state(self):
        mutations=[('book_calls',False),('guard_calls',-1),
                   ('book_budget_usd',.02),('held_usd','NaN'),
                   ('verified_spent_usd','0.03'),('state','closed_uncertain')]
        for field,value in mutations:
            with self.subTest(field=field):
                b=self.bundle(); b['accounting'][field]=value
                with self.assertRaises(GateError):
                    self.api().verify_synthetic_audit_bundle(self.rehash(b))

    def test_duplicate_malformed_and_oversized_json_fail(self):
        api=self.api(); b=self.bundle(); raw=json.dumps(b)
        duplicate=raw[:-1]+',"operational_go":false}'
        for text in [duplicate,'{','[]','{"x":NaN}',raw+' '*8192]:
            with self.subTest(text=text[:20]):
                with self.assertRaises(GateError):
                    api.load_synthetic_audit_bundle(text)

    def test_invalid_declared_source_closes_gate_without_dispatch(self):
        for sha in ['main','a'*39,'G'*40,False]:
            with self.subTest(sha=sha):
                gate=setup()
                with self.assertRaises(GateError):
                    self.api().synthetic_audit_bundle(gate,source_sha=sha)
                self.assertTrue(gate.book.closed)
                self.assertTrue(gate.guard.cancelled)
                self.assertEqual(0,gate.attempts)

    def test_reserved_uncertain_report_remains_synthetic(self):
        api=self.api(); gate=setup()
        with self.assertRaises(GateError):
            with gate.logical_call():
                gate.invoke(lambda: 'synthetic_unsettled_response')
                raise GateError('synthetic_denial')
        bundle=api.synthetic_audit_bundle(gate,source_sha='a'*40)
        self.assertEqual('closed_uncertain',bundle['accounting']['state'])
        self.assertEqual(bundle,api.verify_synthetic_audit_bundle(bundle))

    def test_identity_time_and_required_fields_fail_closed(self):
        for field,value in [('evidence_id','SYNTHETIC-not-a-uuid'),
                            ('observed_at_utc','2026-02-30T00:00:00Z'),
                            ('target_sdk','latest')]:
            b=self.bundle(); b[field]=value
            with self.assertRaises(GateError):
                self.api().verify_synthetic_audit_bundle(self.rehash(b))
        b=self.bundle(); del b['source_sha']
        with self.assertRaises(GateError):
            self.api().verify_synthetic_audit_bundle(self.rehash(b))

    def test_non_ascii_timestamp_digits_are_denied_even_with_valid_digest(self):
        for stamp in ('٢026-10-11T12:00:00Z','2026-10-1١T12:00:00Z',
                      '2026-10-11T1٢:00:00Z','2026-10-11T12:0٠:00Z',
                      '2026-10-11T12:00:0٠Z'):
            with self.subTest(stamp=stamp):
                b=self.bundle();b['observed_at_utc']=stamp
                with self.assertRaisesRegex(GateError,'^synthetic_audit_invalid$'):
                    self.api().verify_synthetic_audit_bundle(self.rehash(b))

    def test_calendar_leap_century_and_uuid_variant_boundaries(self):
        api=self.api()
        for stamp in ('2000-02-29T23:59:59Z','2024-02-29T00:00:00Z'):
            b=self.bundle();b['observed_at_utc']=stamp
            self.assertEqual(stamp,api.verify_synthetic_audit_bundle(self.rehash(b))['observed_at_utc'])
        for field,value in (
                ('observed_at_utc','1900-02-29T00:00:00Z'),
                ('observed_at_utc','2026-02-29T00:00:00Z'),
                ('observed_at_utc','2026-10-11T12:00:60Z'),
                ('evidence_id','SYNTHETIC-00000000-0000-4000-0000-000000000000'),
                ('evidence_id','SYNTHETIC-00000000-0000-5000-8000-000000000000'),
                ('evidence_id','SYNTHETIC-ABCDEF00-0000-4000-8000-000000000000')):
            with self.subTest(field=field,value=value):
                b=self.bundle();b[field]=value
                with self.assertRaises(GateError):api.verify_synthetic_audit_bundle(self.rehash(b))
