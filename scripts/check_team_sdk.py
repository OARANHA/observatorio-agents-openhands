#!/usr/bin/env python3
"""Diagnóstico não destrutivo da equipe OpenHands.

Modo padrão: valida arquivos conhecidos sem dependências externas.
--sdk: carrega definições com o loader oficial, sem registrar agentes,
abrir conversas ou delegar tarefas. Nenhum segredo é exibido.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import importlib.resources
import json
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
os.environ.setdefault("OPENHANDS_SUPPRESS_BANNER", "1")

EXPECTED = {
    "observatorio-construtor": ".agents/agents/observatorio-construtor.md",
    "observatorio-verificador": ".agents/agents/observatorio-verificador.md",
}
HEADER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)


def inspect_definitions(workspace: Path) -> dict:
    """Inspeciona somente arquivos de agentes conhecidos, sem acesso transversal."""
    agents = {}
    for name, relative in EXPECTED.items():
        path = workspace / relative
        if not path.is_file():
            agents[name] = {"path": relative, "status": "ausente"}
            continue

        raw = path.read_text(encoding="utf-8")
        found = HEADER.match(raw)
        header = found.group(1) if found else ""
        required = all((
            re.search(r"(?m)^name:[ \t]*" + re.escape(name) + r"[ \t]*$", header),
            re.search(r"(?m)^description:[ \t]*", header),
            re.search(r"(?m)^model:[ \t]*inherit[ \t]*$", header),
            re.search(r"(?m)^permission_mode:[ \t]*always_confirm[ \t]*$", header),
            re.search(r"(?m)^max_iteration_per_run:[ \t]*[1-9][0-9]*[ \t]*$", header),
            re.search(r"(?m)^tools:[ \t]*\n[ \t]+-[ \t]+(?:terminal|file_editor)[ \t]*$", header),
        )) and not re.search(r"(?m)^mcp_servers:[ \t]*", header) and "never_confirm" not in raw
        agents[name] = {
            "path": relative,
            "status": "contrato_estatico_valido" if required else "contrato_estatico_invalido",
        }
    return {
        "valid": all(x["status"] == "contrato_estatico_valido" for x in agents.values()),
        "agents": agents,
        "registration_performed": False,
        "delegation_performed": False,
    }


def inspect_sdk(workspace: Path) -> dict:
    """Executa load_project_agents somente; funções mutadoras NÃO são chamadas."""
    try:
        versions = {package: importlib.metadata.version(package)
                    for package in ("openhands-sdk", "openhands-tools")}
        if any(version != "1.53.0" for version in versions.values()):
            return {
                "status": "versao_incompativel",
                "package_versions": versions,
                "registration_performed": False,
                "delegation_performed": False,
            }
        from openhands.sdk.subagent import load_project_agents, register_file_agents
        from openhands.tools import TaskToolSet, register_builtins_agents

        if not callable(register_file_agents) or not callable(register_builtins_agents) or TaskToolSet is None:
            raise TypeError("Interfaces SDK incompatíveis")
        names = sorted(str(agent.name) for agent in load_project_agents(workspace))
        builtin_found = importlib.resources.files("openhands.tools.preset").joinpath(
            "subagents", "code_explorer.md"
        ).is_file()
    except Exception as error:
        return {
            "status": "nao_verificavel",
            "error_type": type(error).__name__,
            "registration_performed": False,
            "delegation_performed": False,
        }
    return {
        "status": "loader_oficial_executado_sem_registro",
        "package_versions": versions,
        "project_agent_names": [name for name in names if name in EXPECTED],
        "expected_agent_names_loaded": all(n in names for n in EXPECTED),
        "builtin_code_explorer_definition_present": builtin_found,
        "registration_performed": False,
        "delegation_performed": False,
        "session_tools_enabled": "nao_verificado",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validar agentes OpenHands sem ativação")
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="Workspace local já preparado; não cria/clona diretórios")
    parser.add_argument("--sdk", action="store_true",
                        help="Usar loader SDK oficial em modo leitura (sem registrar)")
    args = parser.parse_args()
    static = inspect_definitions(args.workspace)
    payload = {
        "diagnostic_id": "OBS-TEAM-SDK-READONLY-001",
        "stage": "definicoes_apenas_nao_ativadas",
        "static": static,
    }
    ok = static["valid"]
    if args.sdk:
        sdk = inspect_sdk(args.workspace)
        payload["sdk"] = sdk
        ok = ok and sdk["status"] == "loader_oficial_executado_sem_registro" and (
            sdk["expected_agent_names_loaded"] and sdk["builtin_code_explorer_definition_present"]
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
