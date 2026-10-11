"""Lifecycle faults are synthetic; never start an SDK agent or provider."""
from pathlib import Path
import signal
import subprocess
import sys
import unittest
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from canary_controls import GateError,Guard,MissionCancelled,supervise,terminal_executor


class SupervisorFailures(unittest.TestCase):
    def test_uncertain_hold_survives_worker_failure_and_kill_precedes_reap(self):
        from test_canary_transport_attempts import setup
        gate=setup();order=[];proc=mock.Mock(pid=123)
        def communicate(*,timeout):
            order.append(('communicate',timeout))
            if len(order)==1:raise subprocess.TimeoutExpired('synthetic',timeout)
            return ('','')
        proc.communicate.side_effect=communicate
        with mock.patch('canary_controls.os.killpg',side_effect=lambda *_:order.append(('kill',None))):
            with self.assertRaises(GateError):
                with gate.logical_call():
                    gate.invoke(lambda:supervise(['synthetic'],1,popen=mock.Mock(return_value=proc)))
        self.assertEqual([('communicate',1),('kill',None),('communicate',1)],order)
        self.assertTrue(gate.guard.cancelled);self.assertTrue(gate.book.closed)
        self.assertIsNotNone(gate.book.active);self.assertEqual(0,gate.book.spent)
        with self.assertRaises(GateError):
            with gate.logical_call():gate.invoke(lambda:self.fail('resumed'))
    def test_startup_exception_is_minimized_and_not_retried(self):
        start=mock.Mock(side_effect=OSError('SYNTHETIC_PRIVATE_PAYLOAD'))
        with self.assertRaisesRegex(GateError,'^worker_start_failed$'):
            supervise(['synthetic'],1,popen=start)
        start.assert_called_once()

    def test_timeout_cleanup_reap_has_its_own_bound(self):
        proc=mock.Mock(pid=123)
        proc.communicate.side_effect=[subprocess.TimeoutExpired('synthetic',1),('partial','')]
        with mock.patch('canary_controls.os.killpg') as kill:
            with self.assertRaisesRegex(GateError,'^worker_interrupted_or_timed_out$'):
                supervise(['synthetic'],1,popen=mock.Mock(return_value=proc))
        kill.assert_called_once_with(123,signal.SIGKILL)
        self.assertEqual([mock.call(timeout=1),mock.call(timeout=1)],proc.communicate.call_args_list)

    def test_group_kill_failure_still_attempts_bounded_reap_and_denies(self):
        proc=mock.Mock(pid=123)
        proc.communicate.side_effect=[subprocess.TimeoutExpired('synthetic',1),('','')]
        with mock.patch('canary_controls.os.killpg',side_effect=PermissionError('SYNTHETIC_PRIVATE')):
            with self.assertRaisesRegex(GateError,'^worker_cleanup_failed$'):
                supervise(['synthetic'],1,popen=mock.Mock(return_value=proc))
        self.assertEqual(2,proc.communicate.call_count)
        self.assertEqual(mock.call(timeout=1),proc.communicate.call_args)

    def test_reap_failure_never_returns_partial_output_or_retries(self):
        proc=mock.Mock(pid=123)
        proc.communicate.side_effect=[subprocess.TimeoutExpired('synthetic',1),
                                     subprocess.TimeoutExpired('synthetic',1,output='SYNTHETIC_PRIVATE')]
        start=mock.Mock(return_value=proc)
        with mock.patch('canary_controls.os.killpg'):
            with self.assertRaisesRegex(GateError,'^worker_cleanup_failed$'):
                supervise(['synthetic'],1,popen=start)
        start.assert_called_once();self.assertEqual(2,proc.communicate.call_count)

    def test_terminal_start_failure_cancels_guard_and_denies_second_action(self):
        guard=Guard();action=mock.Mock(command='pwd',is_input=False)
        execute=terminal_executor(Path('/synthetic'),guard,lambda *_:True)
        with mock.patch('canary_controls.subprocess.Popen',side_effect=OSError('SYNTHETIC_PRIVATE')) as start:
            with self.assertRaisesRegex(GateError,'^worker_start_failed$'):execute(action)
            with self.assertRaises(MissionCancelled):execute(action)
        start.assert_called_once();self.assertTrue(guard.cancelled)

    def test_already_exited_group_and_cancelled_communication_stay_terminal(self):
        proc=mock.Mock(pid=123)
        proc.communicate.side_effect=[MissionCancelled('synthetic'),('','')]
        with mock.patch('canary_controls.os.killpg',side_effect=ProcessLookupError):
            with self.assertRaisesRegex(GateError,'^worker_interrupted_or_timed_out$'):
                supervise(['synthetic'],1,popen=mock.Mock(return_value=proc))
