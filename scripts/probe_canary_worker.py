#!/usr/bin/env python3
"""Prova inert OpenHands SDK/Tools 1.53.0: nenhum agente/LLM/conversa real.

Apenas executável explícito --synthetic-worker. Este módulo nunca registra
agentes, não chama TaskExecutor/start_task, não lê credenciais e não é um
worker operacional. O processo deve rodar em runner efêmero supervisionado.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace

from canary_controls import ALLOWED, GateError, Guard, MissionCancelled, snapshot, supervise
from canary_sdk import explorer_action, sdk_bindings, task_spec, terminal_tools


def assemble_inert_tools(conv_state, root, guard, approval):
    """Vincular as duas ferramentas oficiais a UM Guard, sem agente ou LLM.

    O registro do terminal é mutação do registry de ferramentas DO PROCESSO
    DESCARTÁVEL, não registro operacional de subagente no Canvas/servidor.
    A função falha se resolução não reutiliza exatamente nosso executor.
    """
    from openhands.sdk.tool.registry import register_tool, resolve_tool
    from openhands.tools.terminal.definition import TerminalTool
    from openhands.tools.task.definition import TaskToolSet

    Tool, _, _register_agents = sdk_bindings()  # somente imports/verificação
    restricted = terminal_tools(conv_state, root, guard, approval)
    if len(restricted) != 1 or restricted[0].executor is None:
        raise GateError("restricted_terminal_missing")
    register_tool(TerminalTool.name, restricted[0])
    terminal_spec = Tool(name=TerminalTool.name)
    resolved_terminal = resolve_tool(terminal_spec, conv_state)
    if len(resolved_terminal) != 1 or resolved_terminal[0] is not restricted[0]:
        raise GateError("restricted_terminal_not_inherited")

    task = resolve_tool(task_spec(guard, approval), conv_state)
    if len(task) != 1 or task[0].executor is None:
        raise GateError("task_tool_missing")
    manager = getattr(task[0].executor, "_manager", None)
    if manager is None or not callable(getattr(manager, "_confirmation_handler", None)):
        raise GateError("task_callback_not_bound")
    # O TaskManager oficial permanece INERTE: start_task não é invocado.
    return resolved_terminal[0], task[0], manager


def synthetic_worker() -> dict:
    """Teste fim-a-fim do wiring inerte + bwrap efetivo, sem TaskAction dispatch."""
    from openhands.tools.terminal.definition import TerminalAction, TerminalObservation

    with tempfile.TemporaryDirectory(prefix="obs-inert-worker-") as temp:
        base = Path(temp).resolve()
        source = base / "public"
        source.mkdir()
        for command in ALLOWED.values():
            if len(command) != 2:
                continue
            target = source / command[1]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("SYNTHETIC_PUBLIC_ONLY\n", encoding="utf-8")
        marker = source / "never-copied.secret"
        marker.write_text("SYNTHETIC_MARKER\n", encoding="utf-8")
        root = snapshot(source, base / "state")
        if (root / marker.name).exists() or (root / ".git").exists():
            raise GateError("snapshot_exposed_extra_files")

        guard = Guard(max_calls=6, seconds=12, budget=.10)
        confirmations = []
        def approval(task_id, command):
            # Policy explicitly authorizes only one exact public command.
            confirmations.append((task_id, command))
            return command == "cat AGENTS.md"

        # O SDK acessa working_dir para criar TerminalTool; o TaskToolSet
        # consulta conv_state.agent somente se houver definições registradas.
        # Não registrar nenhum agente nesta prova, nem criar Agent/Conversation.
        state = SimpleNamespace(
            workspace=SimpleNamespace(working_dir=str(root)),
            agent=SimpleNamespace(tools=[]),
        )
        terminal, task_tool, manager = assemble_inert_tools(state, root, guard, approval)
        action = TerminalAction(command="cat AGENTS.md", is_input=False)
        observation = terminal.executor(action)
        if not isinstance(observation, TerminalObservation):
            raise GateError("official_terminal_observation_missing")
        if len(confirmations) != 1 or confirmations[0][1] != "cat AGENTS.md":
            raise GateError("approval_audit_incorrect")
        if (root / "AGENTS.md").read_text(encoding="utf-8") != "SYNTHETIC_PUBLIC_ONLY\n":
            raise GateError("snapshot_changed")

        # Só construir uma TaskAction oficial, SEM despachar executor/start_task.
        spec = explorer_action(guard)
        if spec.subagent_type != "code-explorer" or spec.resume is not None:
            raise GateError("explorer_action_invalid")
        if guard.delegations != 1 or guard.calls != 0:
            raise GateError("unexpected_llm_or_delegation_count")
        # Provar fail-closed: confirmação negada bloqueia globalmente terminal
        # e fronteiras LLM; não chama TaskTool.executor com a TaskAction.
        denied = TerminalAction(command="env", is_input=False)
        try:
            manager._confirmation_handler("synthetic-task", [
                SimpleNamespace(action=denied)
            ])
            raise GateError("denial_was_accepted")
        except MissionCancelled:
            pass
        if not guard.cancelled:
            raise GateError("guard_not_cancelled")
        try:
            terminal.executor(TerminalAction(command="cat AGENTS.md", is_input=False))
            raise GateError("terminal_ran_after_denial")
        except MissionCancelled:
            pass
        try:
            guard.reserve()
            raise GateError("llm_boundary_ran_after_denial")
        except GateError as error:
            if str(error) != "global_limit":
                raise

        return {
            "mode": "inert_sdk_wiring",
            "sdk": "1.53.0",
            "terminal": "official_restricted_executor_resolved",
            "task": "official_manager_callback_bound_not_dispatched",
            "snapshot": "synthetic_only",
            "command": "sandboxed_public_read",
            "denial": "stopped_all_further_actions",
            "actual_llm_calls": 0,
            "actual_agent_registrations": 0,
            "actual_task_dispatches": 0,
        }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Inert SDK wiring, no agents or LLM")
    parser.add_argument("--synthetic-worker", action="store_true")
    args = parser.parse_args(argv)
    if not args.synthetic_worker:
        parser.error("Only --synthetic-worker is supported; no operational mode")
    result = synthetic_worker()
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
