"""Synthetic mission-scope tests: no subprocess, SDK, browser, network or LLM."""
import pathlib
import sys
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from canary_controls import Guard, MissionCancelled, GateError


class MissionCommandScopeTests(unittest.TestCase):
    def bind(self, guard=None, approval=None, commands=("cat AGENTS.md",)):
        from canary_command_scope import bind_mission_command_scope
        return bind_mission_command_scope(
            guard or Guard(), commands=commands,
            approval=approval if approval is not None else (lambda *_: True),
        )

    def test_one_exact_command_is_allowed_when_human_approves(self):
        guard = Guard()
        human = Mock(return_value=True)
        bound = self.bind(guard, human)
        self.assertIs(bound("task-synthetic", "cat AGENTS.md"), True)
        human.assert_called_once_with("task-synthetic", "cat AGENTS.md")
        self.assertFalse(guard.cancelled)

    def test_other_globally_allowed_command_denied_without_asking_human(self):
        guard = Guard()
        human = Mock(return_value=True)
        bound = self.bind(guard, human)
        with self.assertRaises(MissionCancelled):
            bound("synthetic", "cat team/catalog.json")
        human.assert_not_called()
        self.assertTrue(guard.cancelled)
        with self.assertRaises(MissionCancelled):
            bound("synthetic", "cat AGENTS.md")

    def test_untrusted_command_and_type_confusion_denied(self):
        for command in ("pwd", "cat AGENTS.md; env", "cat ../secret", 123, None):
            with self.subTest(command=command):
                guard = Guard()
                human = Mock(return_value=True)
                bound = self.bind(guard, human)
                with self.assertRaises(MissionCancelled):
                    bound("synthetic", command)
                human.assert_not_called()
                self.assertTrue(guard.cancelled)

    def test_missing_and_invalid_human_approval_denied(self):
        from canary_command_scope import bind_mission_command_scope
        for approval in (
            None, lambda *_: "yes", lambda *_: False,
            lambda *_: (_ for _ in ()).throw(RuntimeError("private data")),
        ):
            guard = Guard()
            if approval is None:
                with self.assertRaises(GateError):
                    bind_mission_command_scope(
                        guard, commands=("cat AGENTS.md",), approval=None,
                    )
            else:
                bound = self.bind(guard, approval)
                with self.assertRaises(MissionCancelled):
                    bound("x", "cat AGENTS.md")
            self.assertTrue(guard.cancelled)

    def test_invalid_scope_must_cancel_guard(self):
        from canary_command_scope import bind_mission_command_scope
        for commands in (
            None, (), ("cat ../secret",),
            ("cat AGENTS.md", "cat AGENTS.md"), "cat AGENTS.md",
            ("cat AGENTS.md", 1), ("cat AGENTS.md", "env"),
            ("cat AGENTS.md",) * 5,
        ):
            with self.subTest(commands=commands):
                guard = Guard()
                with self.assertRaises(GateError):
                    bind_mission_command_scope(
                        guard, commands=commands, approval=lambda *_: True,
                    )
                self.assertTrue(guard.cancelled)

    def test_external_mutation_does_not_enlarge_scope(self):
        allowed = ["cat AGENTS.md"]
        guard = Guard()
        bound = self.bind(guard, commands=allowed)
        allowed.append("cat team/catalog.json")
        with self.assertRaises(MissionCancelled):
            bound("synthetic", "cat team/catalog.json")
        self.assertTrue(guard.cancelled)

    def test_bad_guard_type_does_not_expose_approval(self):
        from canary_command_scope import bind_mission_command_scope
        human = Mock(return_value=True)
        with self.assertRaises(GateError):
            bind_mission_command_scope(
                object(), commands=("cat AGENTS.md",), approval=human,
            )
        human.assert_not_called()


if __name__ == "__main__":
    unittest.main()
