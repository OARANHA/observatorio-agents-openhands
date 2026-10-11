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

# Recognizer for this project's six-field contract, NOT a general YAML parser.
# Unsupported YAML forms fail closed; the SDK remains the authoritative loader.
ROLE_LIMITS = {
    "observatorio-construtor": ({"terminal", "file_editor"}, 12),
    "observatorio-verificador": ({"terminal"}, 10),
}
FIELDS = {"name", "description", "tools", "model", "permission_mode", "max_iteration_per_run"}


def valid_contract_header(header: str, name: str) -> bool:
    """Accept only unique plain keys, block tool lists and plain/folded descriptions."""
    if any(ord(char) < 32 and char != "\n" for char in header):
        return False
    lines = header.splitlines()
    values = {}
    index = 0
    while index < len(lines):
        match = re.fullmatch(r"([a-z_]+):(?: (.*))?", lines[index])
        if not match:
            return False
        key, value = match.groups()
        if key not in FIELDS or key in values:
            return False
        index += 1
        if key == "tools":
            if value is not None:
                return False
            tools = []
            while index < len(lines) and lines[index].startswith(" "):
                item = re.fullmatch(r"  - ([a-z_]+)", lines[index])
                if not item:
                    return False
                tools.append(item.group(1))
                index += 1
            if len(tools) != len(set(tools)):
                return False
            values[key] = set(tools)
        elif key == "description":
            if value == ">":
                start = index
                while index < len(lines) and lines[index].startswith(" "):
                    if not re.fullmatch(r"  \S.*", lines[index]):
                        return False
                    index += 1
                if index == start:
                    return False
            elif (not value or not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ][\w .,;()/+-]*", value)
                  or value.lower() in {"null", "true", "false", "yes", "no", "on", "off"}):
                return False
            values[key] = value
        else:
            values[key] = value
    tools, ceiling = ROLE_LIMITS[name]
    iterations = values.get("max_iteration_per_run") or ""
    return (set(values) == FIELDS
            and values["name"] == name
            and values["model"] == "inherit"
            and values["permission_mode"] == "always_confirm"
            and values["tools"] == tools
            and re.fullmatch(r"[1-9][0-9]?", iterations) is not None
            and int(iterations) <= ceiling)


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
        required = (found is not None and valid_contract_header(header, name)
                    and bool(raw[found.end():].strip()) and "never_confirm" not in raw)
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
