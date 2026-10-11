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
