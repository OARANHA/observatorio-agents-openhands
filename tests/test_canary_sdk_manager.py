"""Optional SDK compatibility tests: official manager, only mocked conversations.

No Agent, Conversation, registry, start_task, delegation or LLM is instantiated.
Run under the isolated SDK/Tools 1.53.0 environment; dependency-free CI skips.
"""
import importlib.metadata
import pathlib
import sys
import types
import unittest
from unittest import mock
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
from canary_controls import Guard, MissionCancelled
from canary_sdk import task_spec


def installed():
    try:
        return all(importlib.metadata.version(p) == '1.53.0'
                   for p in ('openhands-sdk', 'openhands-tools'))
    except importlib.metadata.PackageNotFoundError:
        return False


@unittest.skipUnless(installed(), 'requires isolated SDK/Tools 1.53.0')
class OfficialManager(unittest.TestCase):
    def test_cleanup_failure_cannot_reopen_cancelled_guard(self):
        from openhands.tools.task.manager import TaskManager,ConversationExecutionStatus,ConversationState
        from canary_controls import GateError
        for phase in ('metrics','pause','close'):
            with self.subTest(phase=phase):
                guard=Guard();callback=task_spec(guard,lambda *_:False).params['confirmation_handler']
                manager=TaskManager(confirmation_handler=callback)
                manager._parent_conversation=mock.Mock(_visualizer=None)
                conversation=mock.Mock()
                conversation.state.execution_status=ConversationExecutionStatus.WAITING_FOR_CONFIRMATION
                task=types.SimpleNamespace(id='synthetic',conversation=conversation,
                    set_error=mock.Mock(),model_copy=mock.Mock())
                event=types.SimpleNamespace(action=types.SimpleNamespace(command='pwd',is_input=False))
                if phase!='metrics':getattr(conversation,phase).side_effect=RuntimeError('SYNTHETIC_CLEANUP')
                with mock.patch.object(ConversationState,'get_unmatched_actions',return_value=[event]), \
                     mock.patch.object(manager,'_update_parent_metrics',side_effect=
                         RuntimeError('SYNTHETIC_CLEANUP') if phase=='metrics' else None):
                    with self.assertRaisesRegex(RuntimeError,'SYNTHETIC_CLEANUP'):
                        manager._run_task(task,'synthetic public only')
                self.assertTrue(guard.cancelled);conversation.run.assert_called_once()
                with self.assertRaises(GateError):guard.reserve()
                with self.assertRaises(MissionCancelled):callback('synthetic',[event])
                task.set_error.assert_not_called()
                # Official SDK finally is sequential: early failure skips later cleanup.
                self.assertEqual(phase!='metrics',conversation.pause.called)
                self.assertEqual(phase=='close',conversation.close.called)

    def _inert_cycle(self,mode):
        """Official manager loop, mocked conversation, fake LLM and terminal output.

        Never invokes start_task, TaskExecutor, registration or an actual LLM.
        """
        from openhands.tools.task.manager import TaskManager, ConversationExecutionStatus, ConversationState
        from canary_budget import BudgetBook,TokenCaps
        from canary_budget_boundary import synthetic_budgeted_llm_routes
        from canary_controls import GateError,terminal_executor
        from test_canary_budget_boundary import FakeLLM,rates
        now=[0.];guard=Guard(clock=lambda:now[0]);book=BudgetBook('.02')
        cap=TokenCaps(2000,500,500,max_calls=1 if mode=='last_call' else 6)
        llm=FakeLLM();approvals=[];pending=[]
        def approve(task_id,command):
            approvals.append((task_id,command))
            if mode=='timeout':now[0]=guard.deadline
            return True
        approval=None if mode=='missing' else approve
        callback=task_spec(guard,approval).params['confirmation_handler']
        manager=TaskManager(confirmation_handler=callback)
        manager._parent_conversation=mock.Mock(_visualizer=None)
        conversation=mock.Mock()
        terminal=terminal_executor(pathlib.Path('/synthetic-public-snapshot'),guard,approval)
        approved=types.SimpleNamespace(command='cat AGENTS.md',is_input=False)
        denied=types.SimpleNamespace(command='env',is_input=False)
        def run():
            if conversation.run.call_count>1:terminal(approved)
            llm.completion(['SYNTHETIC_PUBLIC_ONLY'])
            pending[:]=[types.SimpleNamespace(action=approved if conversation.run.call_count==1 else denied)]
            conversation.state.execution_status=ConversationExecutionStatus.WAITING_FOR_CONFIRMATION
        conversation.run.side_effect=run
        task=types.SimpleNamespace(id='synthetic',conversation=conversation,set_error=mock.Mock(),model_copy=mock.Mock(return_value=object()))
        with synthetic_budgeted_llm_routes(FakeLLM,guard,book,rates(),cap), \
             mock.patch.object(ConversationState,'get_unmatched_actions',side_effect=lambda _:list(pending)), \
             mock.patch.object(manager,'_update_parent_metrics') as parent_metrics, \
             mock.patch('canary_controls.supervise',return_value='SYNTHETIC_PUBLIC_ONLY') as subprocess_call:
            with self.assertRaises(MissionCancelled):manager._run_task(task,'synthetic read-only cycle')
            expected=2 if mode=='denial_after_read' else 1
            self.assertEqual(expected,llm.dispatches)
            self.assertEqual(expected,book.calls)
            self.assertEqual(expected,conversation.run.call_count)
            self.assertEqual(expected-1,subprocess_call.call_count)
            if subprocess_call.called:
                argv,timeout=subprocess_call.call_args.args
                self.assertEqual('/usr/bin/bwrap',argv[0])
                self.assertEqual(['/usr/bin/cat','AGENTS.md'],argv[-2:])
                self.assertLessEqual(timeout,30)
            # Swallowing the terminal signal cannot re-open any execution boundary.
            with self.assertRaises(GateError):llm.completion([])
            with self.assertRaises(MissionCancelled):terminal(approved)
            self.assertEqual(expected,llm.dispatches)
            self.assertEqual(expected-1,subprocess_call.call_count)
            parent_metrics.assert_called_once()
        self.assertTrue(guard.cancelled);self.assertTrue(book.closed)
        task.set_error.assert_not_called()
        conversation.pause.assert_called_once();conversation.close.assert_called_once()
        self.assertIsNone(book.active)

    def test_complete_mock_cycle_denial_stops_llm_and_terminal_after_cleanup(self):
        self._inert_cycle('denial_after_read')
    def test_complete_mock_cycle_missing_approval_stops_on_first_action(self):
        self._inert_cycle('missing')
    def test_complete_mock_cycle_timeout_during_approval_stops_every_boundary(self):
        self._inert_cycle('timeout')
    def test_complete_mock_cycle_last_global_call_prevents_actions(self):
        self._inert_cycle('last_call')

    def test_false_returns_to_run_in_official_sdk(self):
        from openhands.tools.task.manager import TaskManager, ConversationExecutionStatus, ConversationState
        manager = TaskManager(confirmation_handler=lambda *_: False)
        conversation = mock.Mock()
        conversation.state.execution_status = ConversationExecutionStatus.WAITING_FOR_CONFIRMATION
        def finish():
            if conversation.run.call_count == 2:
                conversation.state.execution_status = ConversationExecutionStatus.FINISHED
        conversation.run.side_effect = finish
        with mock.patch.object(ConversationState, 'get_unmatched_actions', return_value=[object()]):
            manager._run_until_finished('synthetic', conversation)
        self.assertEqual(2, conversation.run.call_count)
        conversation.reject_pending_actions.assert_called_once()

    def test_cancellation_escapes_official_error_handler_and_cleans_up(self):
        from openhands.tools.task.manager import TaskManager, ConversationExecutionStatus, ConversationState
        guard = Guard()
        callback = task_spec(guard, lambda *_: False).params['confirmation_handler']
        manager = TaskManager(confirmation_handler=callback)
        manager._parent_conversation = mock.Mock(_visualizer=None)
        conversation = mock.Mock()
        conversation.state.execution_status = ConversationExecutionStatus.WAITING_FOR_CONFIRMATION
        task = types.SimpleNamespace(id='synthetic', conversation=conversation, set_error=mock.Mock(),
                                     model_copy=mock.Mock(return_value=object()))
        event = types.SimpleNamespace(action=types.SimpleNamespace(command='pwd', is_input=False))
        with mock.patch.object(ConversationState, 'get_unmatched_actions', return_value=[event]), \
             mock.patch.object(manager, '_update_parent_metrics') as metrics, \
             mock.patch.object(manager, '_evict_task', wraps=manager._evict_task) as cleanup:
            with self.assertRaises(MissionCancelled):
                manager._run_task(task, 'synthetic public test')
        self.assertTrue(guard.cancelled)
        conversation.run.assert_called_once()
        conversation.reject_pending_actions.assert_not_called()
        task.set_error.assert_not_called()
        metrics.assert_called_once()
        cleanup.assert_called_once_with(task)
        conversation.pause.assert_called_once()
        conversation.close.assert_called_once()
