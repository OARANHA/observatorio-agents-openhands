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
{tools}
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
            (target / (name + ".md")).write_text(GOOD_HEADER.format(name=name, tools="  - terminal" + ("\n  - file_editor" if name.endswith("construtor") else "")), encoding="utf-8")

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

    def assert_rejected(self, transform, role="verificador"):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.fill(root)
            target = root / ".agents/agents" / ("observatorio-" + role + ".md")
            target.write_text(transform(target.read_text(encoding="utf-8")), encoding="utf-8")
            self.assertFalse(inspect_definitions(root)["valid"])

    def test_tools_extras_desconhecidas_ou_de_outro_papel(self):
        for role, tool in (("construtor", "browser"), ("verificador", "file_editor")):
            with self.subTest(role=role):
                self.assert_rejected(lambda s: s.replace("  - terminal", "  - terminal\n  - " + tool), role)

    def test_tools_duplicadas(self):
        for role in ("construtor", "verificador"):
            with self.subTest(role=role):
                self.assert_rejected(lambda s: s.replace("  - terminal", "  - terminal\n  - terminal"), role)

    def test_chaves_duplicadas_inclusive_valores_iguais(self):
        for line in ("name: observatorio-verificador", "tools:",
                     "permission_mode: always_confirm", "permission_mode: never_confirm",
                     "max_iteration_per_run: 10", "description: Outra", "model: inherit"):
            with self.subTest(line=line):
                self.assert_rejected(lambda s: s.replace("\n---\n#", "\n" + line + "\n---\n#"))

    def test_iteracoes_invalidas_ou_acima_do_teto(self):
        for role, value in (("construtor", "13"), ("verificador", "11"),
                            ("verificador", "999999"), ("construtor", "0"),
                            ("verificador", "-1"), ("construtor", "true"),
                            ("verificador", "1.5"), ("verificador", '"10"')):
            with self.subTest(role=role, value=value):
                self.assert_rejected(lambda s: s.replace("max_iteration_per_run: 10", "max_iteration_per_run: " + value), role)

    def test_campos_obrigatorios_ausentes_ou_invalidos(self):
        for line in ("name: observatorio-verificador", "description: Teste sintético.",
                     "tools:\n  - terminal", "model: inherit", "max_iteration_per_run: 10",
                     "permission_mode: always_confirm"):
            with self.subTest(missing=line):
                self.assert_rejected(lambda s: s.replace(line + "\n", ""))
        for old, new in (("description: Teste sintético.", "description:"),
                         ("model: inherit", "model: other"),
                         ("permission_mode: always_confirm", "permission_mode: confirm_risky"),
                         ("name: observatorio-verificador", "name: other"),
                         ("  - terminal", "  - file_editor")):
            with self.subTest(invalid=new):
                self.assert_rejected(lambda s: s.replace(old, new))

    def test_sintaxe_malformada_ou_nao_suportada(self):
        for transform in (
            lambda s: s.replace("\n---\n#", "\n#"),
            lambda s: s.replace("tools:\n  - terminal", "tools: [terminal]"),
            lambda s: s.replace("  - terminal", "\t- terminal"),
            lambda s: s.replace("model: inherit", "hooks: {}\nmodel: inherit"),
            lambda s: s.replace("model: inherit", "<<: *defaults\nmodel: inherit"),
            lambda s: s.replace("name: observatorio-verificador", '"name": observatorio-verificador'),
            lambda s: s.replace("description: Teste sintético.", "description: !custom value"),
            lambda s: s.replace("description: Teste sintético.", "description: [value]"),
            lambda s: s.replace("description: Teste sintético.", "description: null"),
            lambda s: s.replace("description: Teste sintético.", "description: >\n  Texto\n    permission_mode: never_confirm"),
        ):
            with self.subTest(transform=transform):
                self.assert_rejected(transform)

    def test_limites_e_descricao_folded_preservados(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.fill(root)
            path = root / ".agents/agents/observatorio-construtor.md"
            text = path.read_text().replace("max_iteration_per_run: 10", "max_iteration_per_run: 12")
            text = text.replace("description: Teste sintético.", "description: >\n  Descrição sintética.\n  <example>Teste</example>")
            path.write_text(text, encoding="utf-8")
            self.assertTrue(inspect_definitions(root)["valid"])

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
