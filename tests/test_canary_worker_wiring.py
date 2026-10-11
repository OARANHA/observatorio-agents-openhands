"""Contrato do worker inerte; executável sem dependências OpenHands em CI comum."""
import json
import pathlib
import sys
import types
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import probe_canary_worker as worker
from canary_controls import GateError, Guard

GOOD = {
    "mode": "inert_sdk_wiring",
    "terminal": "official_restricted_executor_resolved",
    "task": "official_manager_callback_bound_not_dispatched",
    "denial": "stopped_all_further_actions",
    "actual_llm_calls": 0,
    "actual_agent_registrations": 0,
    "actual_task_dispatches": 0,
}


class WorkerContract(unittest.TestCase):
    def test_parent_supervises_entire_worker_without_llm(self):
        with mock.patch.object(worker, "supervise", return_value=json.dumps(GOOD)) as run:
            self.assertEqual(worker.main(["--supervise-synthetic-worker"]), 0)
        args, seconds = run.call_args.args
        self.assertEqual("--synthetic-child", args[-1])
        self.assertEqual(str(pathlib.Path(worker.__file__).resolve()), args[-2])
        self.assertEqual(60, seconds)

    def test_parent_rejects_incorrect_inert_output(self):
        for wrong in (
            {"actual_llm_calls": 1},
            {"actual_agent_registrations": 1},
            {"actual_task_dispatches": 1},
            {"terminal": "host_fallback"},
        ):
            payload = {**GOOD, **wrong}
            with self.subTest(wrong=wrong), mock.patch.object(
                worker, "supervise", return_value=json.dumps(payload)
            ):
                with self.assertRaises(GateError):
                    worker.main(["--supervise-synthetic-worker"])

    def test_supervisor_error_propagates_no_fallback(self):
        with mock.patch.object(worker, "supervise", side_effect=GateError("worker_failed_no_fallback")) as run:
            with self.assertRaises(GateError):
                worker.main(["--supervise-synthetic-worker"])
            self.assertEqual(1, run.call_count)

    def test_no_implicit_run_mode(self):
        with self.assertRaises(SystemExit):
            worker.main([])

    def test_tool_registry_resolution_requires_exact_restricted_instance(self):
        original = types.SimpleNamespace(executor=object())
        other = types.SimpleNamespace(executor=object())
        seen = []
        fake_registry = types.ModuleType("openhands.sdk.tool.registry")
        fake_registry.register_tool = lambda name, instance: seen.append((name, instance))
        fake_registry.resolve_tool = lambda spec, state: [other] if spec.name == "terminal" else [types.SimpleNamespace(executor=types.SimpleNamespace(_manager=types.SimpleNamespace(_confirmation_handler=lambda *_: True)))]
        fake_terminal = types.ModuleType("openhands.tools.terminal.definition")
        fake_terminal.TerminalTool = types.SimpleNamespace(name="terminal")
        fake_task = types.ModuleType("openhands.tools.task.definition")
        fake_task.TaskToolSet = types.SimpleNamespace(name="task")
        fake_tool = lambda name: types.SimpleNamespace(name=name)
        with mock.patch.dict(sys.modules, {
            "openhands.sdk.tool.registry": fake_registry,
            "openhands.tools.terminal.definition": fake_terminal,
            "openhands.tools.task.definition": fake_task,
        }), mock.patch.object(worker, "sdk_bindings", return_value=(fake_tool, None, None)), mock.patch.object(
            worker, "terminal_tools", return_value=[original]
        ), mock.patch.object(worker, "task_spec", return_value=fake_tool("task")):
            with self.assertRaisesRegex(GateError, "restricted_terminal_not_inherited"):
                worker.assemble_inert_tools(object(), pathlib.Path("/workspace"), Guard(), None)
        self.assertEqual([("terminal", original)], seen)


if __name__ == "__main__":
    unittest.main()
