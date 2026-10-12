"""Fail-closed command-subset binding for the existing synthetic SDK callbacks.

This is not a standalone authorization service, runnable worker or source
of human approval. The same callback must be passed to TaskToolSet and
TerminalTool. It does not certify enforcement in a real OpenHands process.
"""
from threading import RLock

from canary_controls import ALLOWED, GateError, Guard, MissionCancelled


def bind_mission_command_scope(guard, *, commands, approval):
    """Bind an immutable exact subset of the global terminal allowlist.

    Returns the approval callable used by existing mission_confirmation.
    Invalid scope permanently cancels the shared Guard. An out-of-scope
    command never reaches the human approval callback.
    """
    if type(guard) is not Guard:
        raise GateError("mission_command_scope_invalid")
    if (type(commands) not in (list, tuple) or not 1 <= len(commands) <= 4
            or any(type(cmd) is not str or cmd not in ALLOWED for cmd in commands)
            or len(set(commands)) != len(commands) or not callable(approval)):
        guard.cancel()
        raise GateError("mission_command_scope_invalid")

    accepted = frozenset(commands)
    lock = RLock()

    def scoped(task_id, command):
        with lock:
            if guard.cancelled or type(command) is not str or command not in accepted:
                guard.cancel()
                raise MissionCancelled("mission_command_scope_denied")
            try:
                if approval(task_id, command) is not True:
                    guard.cancel()
                    raise MissionCancelled("mission_command_scope_denied")
            except BaseException:
                guard.cancel()
                raise MissionCancelled("mission_command_scope_denied") from None
            if guard.cancelled:
                raise MissionCancelled("mission_command_scope_denied")
            return True

    return scoped
