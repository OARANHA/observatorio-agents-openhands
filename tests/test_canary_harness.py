"""Synthetic gate tests: never import or execute an LLM."""
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
from canary_controls import GateError, Guard, confirm, ALLOWED, sandbox_argv, snapshot, supervise, terminal_executor, quote
from canary_sdk import guarded_llm, task_spec, sdk_bindings

class Controls(unittest.TestCase):
    def test_confirmation_denies_missing_approval_and_unknown_actions(self):
        event = types.SimpleNamespace(action=types.SimpleNamespace(command='cat AGENTS.md', is_input=False))
        self.assertFalse(confirm('task', [event]))
        self.assertTrue(confirm('task', [event], lambda task, command: True))
        self.assertFalse(confirm('task', [event], lambda task, command: 'yes'))
        for command in ['cat AGENTS.md; env', 'cat ../secret', 'env', 'curl x', 'pwd > x', 'cat $(pwd)', 'cat AGENTS.md\n']:
            event.action.command = command
            self.assertFalse(confirm('task', [event], lambda *_: True))
        self.assertFalse(confirm('task', [], lambda *_: True))
        self.assertFalse(confirm('task', [object()], lambda *_: True))
        self.assertFalse(confirm('task', [event], lambda *_: 1/0))

    def test_counter_is_global_and_cancel_is_terminal(self):
        g = Guard(max_calls=2, clock=lambda: 0)
        g.reserve(); g.reserve()
        with self.assertRaises(GateError): g.reserve()
        g.cancel()
        with self.assertRaises(GateError): g.reserve()

    def test_deadline_and_invalid_limits(self):
        now=[0.0]; g=Guard(seconds=1, clock=lambda: now[0]); now[0]=1
        with self.assertRaises(GateError): g.reserve()
        for kwargs in [{'max_calls':0},{'max_calls':True},{'seconds':float('nan')},{'budget':-1}]:
            with self.assertRaises(ValueError): Guard(**kwargs)

    def test_usage_missing_or_budget_exhausted_stops(self):
        g=Guard(budget=.1)
        g.record(.1, 20, 10)
        self.assertEqual(30,g.input_tokens+g.output_tokens)
        with self.assertRaises(GateError): g.reserve()
        for values in [(float('nan'),1,1),(-1,1,1),(0,1,1),(.01,-1,1),(.01,None,1)]:
            with self.assertRaises(GateError): Guard().record(*values)

    def test_snapshot_copies_only_public_allowlist_and_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp); source=root/'source'; source.mkdir(); dest=root/'state'
            for path in ALLOWED.values():
                if len(path)==2:
                    target=source/path[1]; target.parent.mkdir(parents=True,exist_ok=True); target.write_text('synthetic')
            (source/'secret').write_text('not copied')
            out=snapshot(source,dest)
            self.assertFalse((out/'secret').exists())
            (source/'AGENTS.md').unlink(); (source/'AGENTS.md').symlink_to(source/'secret')
            with self.assertRaises(GateError): snapshot(source,root/'other')

    def test_sandbox_has_no_host_root_network_or_environment(self):
        args=sandbox_argv(pathlib.Path('/synthetic/snapshot'), 'cat AGENTS.md')
        self.assertIn('--unshare-all',args); self.assertIn('--clearenv',args)
        self.assertNotIn('--share-net',args); self.assertNotIn('--bind',args)
        self.assertEqual(['/usr/bin/cat','AGENTS.md'],args[-2:])
        with self.assertRaises(GateError): sandbox_argv(pathlib.Path('/x'),'env')

    def test_supervisor_timeout_kills_group_without_retry(self):
        proc=mock.Mock(pid=123);proc.communicate.side_effect=[__import__('subprocess').TimeoutExpired('x',1), ('','')]
        with mock.patch('canary_controls.subprocess.Popen',return_value=proc) as popen, mock.patch('canary_controls.os.killpg') as kill:
            with self.assertRaises(GateError): supervise(['synthetic'],1)
            self.assertEqual(1,popen.call_count);kill.assert_called_once()
            self.assertEqual({},popen.call_args.kwargs['env'])

    def test_executor_requires_approval_even_if_called_directly(self):
        g=Guard(); action=types.SimpleNamespace(command='cat AGENTS.md',is_input=False)
        with mock.patch('canary_controls.supervise',return_value='public') as run:
            execute=terminal_executor(pathlib.Path('/snapshot'),g)
            with self.assertRaises(GateError): execute(action)
            run.assert_not_called()
            execute=terminal_executor(pathlib.Path('/snapshot'),Guard(),lambda *_:True)
            self.assertEqual('public',execute(action))
            action.command='env'
            with self.assertRaises(GateError): execute(action)
            self.assertEqual(1,run.call_count)

    def test_only_one_delegation_can_be_reserved(self):
        g=Guard();g.claim_delegation('code-explorer')
        with self.assertRaises(GateError): g.claim_delegation('code-explorer')
        with self.assertRaises(GateError): Guard().claim_delegation('bash-runner')

    def test_offline_rates_are_not_account_availability(self):
        catalog={'synthetic':{'input_cost_per_token':.000001,'output_cost_per_token':.000002}}
        self.assertAlmostEqual(.0003,quote(catalog,'synthetic',100,100))
        with self.assertRaises(GateError): quote(catalog,'absent',100,100)
        with self.assertRaises(GateError): quote({'x':{}},'x',100,100)

    def test_hard_timeout_on_synthetic_process(self):
        with self.assertRaises(GateError): supervise(['/bin/sleep','1'],.02)


class FakeLLM:
    num_retries=0
    def __init__(self): self.metrics=types.SimpleNamespace(accumulated_cost=0., accumulated_token_usage=types.SimpleNamespace(prompt_tokens=0,completion_tokens=0))
    def completion(self):
        self.metrics.accumulated_cost+=.01
        self.metrics.accumulated_token_usage.prompt_tokens+=5
        self.metrics.accumulated_token_usage.completion_tokens+=2
        return 'synthetic'
    responses=completion
    async def acompletion(self): return self.completion()
    aresponses=acompletion

class Wiring(unittest.TestCase):
    def test_llm_global_guard_spans_copies_and_is_restored(self):
        original=FakeLLM.completion;g=Guard(max_calls=2)
        with guarded_llm(FakeLLM,g):
            self.assertEqual('synthetic',FakeLLM().completion())
            FakeLLM().responses()
            with self.assertRaises(GateError): FakeLLM().completion()
        self.assertIs(original,FakeLLM.completion)
        self.assertEqual(10,g.input_tokens);self.assertEqual(4,g.output_tokens)

    def test_nonzero_retries_rejected_before_call(self):
        llm=FakeLLM();llm.num_retries=1
        with guarded_llm(FakeLLM,Guard()):
            with self.assertRaises(GateError): llm.completion()
        self.assertEqual(0.,llm.metrics.accumulated_cost)

    def test_sdk_bindings_does_not_register_or_delegate(self):
        register=mock.Mock(side_effect=AssertionError('forbidden'))
        sdk=types.ModuleType('openhands.sdk'); sdk.Tool=mock.Mock(side_effect=lambda **kw:kw)
        tools=types.ModuleType('openhands.tools');tools.register_builtins_agents=register;tools.TaskToolSet=types.SimpleNamespace(name='TaskToolSet')
        with mock.patch.dict(sys.modules,{'openhands.sdk':sdk,'openhands.tools':tools}),mock.patch('importlib.metadata.version',return_value='1.53.0'):
            spec=task_spec(lambda *_:False)
            self.assertTrue(callable(spec['params']['confirmation_handler']))
            self.assertEqual({'tools':True,'mcp_servers':True},spec['params']['sub_agent_scope'])
        register.assert_not_called()
        with mock.patch('importlib.metadata.version',return_value='1.52.0'):
            with self.assertRaises(GateError): sdk_bindings()

    def test_invalid_metrics_stop_before_provider_boundary(self):
        llm=FakeLLM();llm.metrics.accumulated_cost=float('nan')
        with guarded_llm(FakeLLM,Guard()):
            with self.assertRaises(GateError): llm.completion()
        self.assertEqual(0,llm.metrics.accumulated_token_usage.prompt_tokens)

    def test_async_routes_and_exception_restore(self):
        import asyncio
        original=FakeLLM.acompletion
        guard=Guard(max_calls=1)
        with guarded_llm(FakeLLM,guard):
            with self.assertRaises(GateError): asyncio.run(FakeLLM().acompletion())
        self.assertTrue(guard.cancelled)
        self.assertIs(original,FakeLLM.acompletion)

    def test_official_action_is_single_explorer_and_never_executed(self):
        from canary_sdk import explorer_action
        module=types.ModuleType('openhands.tools.task')
        module.TaskAction=mock.Mock(side_effect=lambda **kw:kw)
        guard=Guard()
        with mock.patch.dict(sys.modules,{'openhands.tools.task':module}):
            action=explorer_action(guard)
            self.assertEqual('code-explorer',action['subagent_type'])
            self.assertIsNone(action['resume'])
            with self.assertRaises(GateError): explorer_action(guard)
        self.assertEqual(1,module.TaskAction.call_count)

    def test_snapshot_rejects_symlink_state_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=pathlib.Path(tmp); source=root/'source'; source.mkdir()
            for argv in ALLOWED.values():
                if len(argv)==2:
                    file=source/argv[1];file.parent.mkdir(parents=True,exist_ok=True);file.write_text('public')
            (root/'outside').mkdir()
            (root/'link').symlink_to(root/'outside',target_is_directory=True)
            with self.assertRaises(GateError): snapshot(source,root/'link'/'state')
