"""Regressão local do diagnóstico; CI não precisa instalar OpenHands SDK."""
import ast
import importlib.metadata
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from check_team_sdk import inspect_definitions, inspect_sdk  # noqa: E402

GOOD_HEADER = """---
name: {name}
description: Teste sintético.
tools:
  - terminal
model: inherit
max_iteration_per_run: 10
permission_mode: always_confirm
---
# Definição sintética
"""


class DiagnosticContract(unittest.TestCase):
    def fill(self, root):
        target = root / ".agents" / "agents"
        target.mkdir(parents=True)
        for name in ("observatorio-construtor", "observatorio-verificador"):
            (target / (name + ".md")).write_text(GOOD_HEADER.format(name=name), encoding="utf-8")

    def test_arquivo_ausente_nao_eh_ativacao(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = inspect_definitions(pathlib.Path(tmp))
            self.assertFalse(output["valid"])
            self.assertTrue(all(v["status"] == "ausente" for v in output["agents"].values()))
            self.assertFalse(output["registration_performed"])

    def test_contratos_validos_e_alteracao_de_politica_rejeitada(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.fill(root)
            self.assertTrue(inspect_definitions(root)["valid"])
            target = root / ".agents" / "agents" / "observatorio-verificador.md"
            target.write_text(target.read_text().replace("always_confirm", "never_confirm"))
            self.assertFalse(inspect_definitions(root)["valid"])

    def test_sdk_loader_nao_chama_registro_ou_delegacao(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.fill(root)
            preset = root / "subagents"
            preset.mkdir()
            (preset / "code_explorer.md").write_text("---\nname: code-explorer\n---\n")
            sdk_register = mock.Mock(side_effect=AssertionError("registro nao permitido"))
            builtin_register = mock.Mock(side_effect=AssertionError("registro nao permitido"))
            pkg = types.ModuleType("openhands")
            pkg.__path__ = []
            sdk = types.ModuleType("openhands.sdk")
            sdk.__path__ = []
            subagent = types.ModuleType("openhands.sdk.subagent")
            subagent.load_project_agents = lambda _workspace: [
                types.SimpleNamespace(name=x) for x in ("observatorio-construtor", "observatorio-verificador")
            ]
            subagent.register_file_agents = sdk_register
            tools = types.ModuleType("openhands.tools")
            tools.TaskToolSet = type("TaskToolSet", (), {})
            tools.register_builtins_agents = builtin_register
            with mock.patch.dict(sys.modules, {
                "openhands": pkg, "openhands.sdk": sdk, "openhands.sdk.subagent": subagent,
                "openhands.tools": tools,
            }), mock.patch("importlib.resources.files", return_value=root), mock.patch("importlib.metadata.version", return_value="1.53.0"):

                output = inspect_sdk(root)
            self.assertEqual(output["status"], "loader_oficial_executado_sem_registro")
            self.assertTrue(output["expected_agent_names_loaded"])
            self.assertTrue(output["builtin_code_explorer_definition_present"])
            self.assertFalse(output["registration_performed"])
            self.assertFalse(output["delegation_performed"])
            sdk_register.assert_not_called()
            builtin_register.assert_not_called()

    def test_sdk_version_mismatch_stops_before_loader(self):
        with mock.patch("importlib.metadata.version", return_value="1.52.0"):
            output = inspect_sdk(ROOT)
        self.assertEqual("versao_incompativel", output["status"])
        self.assertFalse(output["registration_performed"])

    def test_sdk_missing_returns_safe_error(self):
        with mock.patch("importlib.metadata.version", side_effect=importlib.metadata.PackageNotFoundError):
            output = inspect_sdk(ROOT)
        self.assertEqual("nao_verificavel", output["status"])
        self.assertEqual("PackageNotFoundError", output["error_type"])

    def test_fonte_nao_invoca_operacoes_de_registro(self):
        source = ast.parse((ROOT / "scripts/check_team_sdk.py").read_text(encoding="utf-8"))
        called = {n.func.id for n in ast.walk(source)
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        for forbidden in ("register_file_agents", "register_builtins_agents", "register_agent",
                          "TaskToolSet", "Conversation", "mkdir", "write_text", "subprocess"):
            self.assertNotIn(forbidden, called)


if __name__ == "__main__":
    unittest.main()
