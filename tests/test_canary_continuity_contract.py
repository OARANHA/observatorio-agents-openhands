"""Synthetic same-conversation proposals. No SDK, provider or dispatch."""
import copy
import importlib.util
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from canary_controls import GateError
from canary_audit_bundle import synthetic_audit_bundle
from test_canary_transport_attempts import setup

SHA='a'*40
CONVERSATION='00000000-0000-4000-8000-000000000001'
MESSAGE='OBS-TEST-V1 | mission=DEMO-001 | synthetic continuation only'

class ContinuityContractTests(unittest.TestCase):
    def session(self,gate=None):
        self.assertIsNotNone(importlib.util.find_spec('canary_continuity_contract'))
        from canary_continuity_contract import SyntheticContinuationSession
        gate=gate or setup()
        return gate,SyntheticContinuationSession(gate,conversation_id=CONVERSATION,
            source_sha=SHA)
    def request(self,gate):
        return dict(schema='obs.synthetic.continuation.v1',classification='synthetic',
            conversation_id=CONVERSATION,state='paused',permission_mode='always_confirm',
            retries=0,cursor='00000000-0000-4000-8000-000000000002',
            message=MESSAGE,approval=True,audit=synthetic_audit_bundle(gate,source_sha=SHA))
    def test_inert_prepare_reserves_exact_budget_without_dispatch(self):
        gate,s=self.session();r=s.prepare(self.request(gate))
        self.assertEqual('prepared_inert',r['state']);self.assertFalse(r['operational_go'])
        self.assertFalse(r['dispatch_allowed']);self.assertFalse(r['authenticity_proven'])
        self.assertEqual('0.005',r['held_usd']);self.assertEqual(1,gate.guard.calls)
        self.assertEqual(0,gate.book.spent);self.assertNotIn('message',r)
        s.close();self.assertTrue(gate.guard.cancelled);self.assertTrue(gate.book.closed)
        self.assertIsNotNone(gate.book.active)
    def test_first_denial_cancels_shared_guard_and_no_later_preparation(self):
        for approval in (False,None,1,'yes'):
            gate,s=self.session();r=self.request(gate);r['approval']=approval
            with self.assertRaises(GateError):s.prepare(r)
            self.assertTrue(gate.guard.cancelled);self.assertTrue(gate.book.closed)
            with self.assertRaises(GateError):s.prepare(self.request(gate))
            self.assertEqual(0,gate.guard.calls)
    def test_running_terminal_unknown_states_are_denied(self):
        for state in ('running','finished','error','waiting_for_confirmation','stuck',''):
            gate,s=self.session();r=self.request(gate);r['state']=state
            with self.assertRaises(GateError):s.prepare(r)
            self.assertTrue(gate.guard.cancelled)
    def test_unknown_private_missing_and_noncanonical_fields_are_denied(self):
        changes=({'prompt':'SYNTHETIC_PRIVATE_MARKER'}, {'message':'arbitrary command'},
            {'classification':'live'}, {'schema':'unknown'}, {'conversation_id':CONVERSATION.upper()},
            {'conversation_id':'00000000-0000-4000-8000-000000000099'},
            {'cursor':'a'*257},{'cursor':'cursor?api_key=SYNTHETIC'},
            {'permission_mode':'auto'},{'retries':1},{'retries':False})
        # Uppercase digits-only UUID is unchanged; use an actual different spelling.
        changes=tuple(x for x in changes if x.get('conversation_id')!=CONVERSATION)
        for change in changes:
            gate,s=self.session();r=self.request(gate);r.update(change)
            with self.assertRaisesRegex(GateError,'^synthetic_continuation_denied$'):s.prepare(r)
            self.assertEqual(0,gate.guard.calls)
        gate,s=self.session();r=self.request(gate);del r['cursor']
        with self.assertRaises(GateError):s.prepare(r)
    def test_audit_binding_and_observed_accounting_must_match(self):
        gate,s=self.session();r=self.request(gate);other=setup('0.03')
        r['audit']=synthetic_audit_bundle(other,source_sha=SHA)
        with self.assertRaises(GateError):s.prepare(r)
        gate,s=self.session();r=self.request(gate)
        r['audit']=synthetic_audit_bundle(gate,source_sha='b'*40)
        with self.assertRaises(GateError):s.prepare(r)
    def test_expired_guard_and_insufficient_budget_never_prepare(self):
        for condition in ('expired','cancelled','budget'):
            gate=setup('0.001' if condition=='budget' else '0.02')
            gate,s=self.session(gate);r=self.request(gate)
            if condition=='expired':gate.guard.deadline=gate.guard.clock()-1
            if condition=='cancelled':gate.guard.cancel()
            with self.assertRaises(GateError):s.prepare(r)
            self.assertTrue(gate.guard.cancelled)
    def test_second_or_concurrent_proposal_keeps_hold_and_stops(self):
        gate,s=self.session();r=self.request(gate)
        def prepare():
            try:return s.prepare(copy.deepcopy(r))['state']
            except GateError:return 'denied'
        with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(lambda _:prepare(),range(2)))
        self.assertEqual(['denied','prepared_inert'],sorted(results))
        self.assertEqual(1,gate.book.calls);self.assertTrue(gate.guard.cancelled)
        self.assertIsNotNone(gate.book.active)
    def test_parameters_fail_closed(self):
        from canary_continuity_contract import SyntheticContinuationSession
        for field,value in (('source_sha','A'*40),('conversation_id','../private'),('conversation_id',None)):
            gate=setup();kw=dict(conversation_id=CONVERSATION,source_sha=SHA);kw[field]=value
            with self.assertRaises(GateError):SyntheticContinuationSession(gate,**kw)
            self.assertTrue(gate.guard.cancelled)
    def test_module_has_no_execution_or_transport_imports(self):
        import ast
        from canary_continuity_contract import __file__ as path
        tree=ast.parse(Path(path).read_text());imports=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):imports += [n.name for n in node.names]
            if isinstance(node,ast.ImportFrom):imports.append(node.module)
        self.assertFalse(any(x.split('.')[0] in {'openhands','litellm','requests','httpx',
            'urllib','socket','subprocess','os','pathlib'} for x in imports))

if __name__=='__main__':unittest.main(verbosity=2)
