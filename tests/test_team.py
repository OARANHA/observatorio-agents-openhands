"""Contrato estático da equipe: não prova registro no OpenHands nem execução remota."""
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEAM = ROOT / "team"
CATALOG = TEAM / "catalog.json"


class TeamContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_schema_and_non_deployed_status(self):
        data = self.data
        self.assertEqual(1, data["schema_version"])
        self.assertEqual("observatorio-team-v1", data["catalog_id"])
        self.assertEqual("proposto_nao_ativado", data["stage"])
        for value in data["deployment"].values():
            if isinstance(value, bool):
                self.assertFalse(value, "Nenhuma capacidade runtime pode ser marcada como verificada.")
        self.assertFalse(data["policy"]["graph_evidence"] is None)
        self.assertFalse(data["policy"]["budgets"]["max_concurrent_missions"] > 1)
        self.assertEqual(0, data["policy"]["budgets"]["max_tool_executions_unverified"])
        self.assertEqual("always_confirm", data["policy"]["budgets"]["default_approval"])
        self.assertNotIn("never_confirm", CATALOG.read_text(encoding="utf-8"))

    def test_three_distinct_roles_with_verified_reuse_gate(self):
        roles = self.data["roles"]
        self.assertEqual({"explorador", "construtor", "verificador"},
                         {r["id"] for r in roles})
        self.assertEqual(len(roles), len({r["openhands_agent_name"] for r in roles}))
        by_name = {r["id"]: r for r in roles}
        self.assertEqual("built_in_candidate", by_name["explorador"]["role_type"])
        self.assertEqual("code-explorer", by_name["explorador"]["openhands_agent_name"])
        self.assertIsNone(by_name["explorador"]["agent_definition"])
        for agent in roles:
            with self.subTest(role=agent["id"]):
                self.assertFalse(agent["external_side_effects_allowed"])
                self.assertTrue(agent["execution_status"].startswith("nao_"))
                self.assertTrue(agent["capabilities"])
                self.assertTrue(agent["required_input"])
                self.assertTrue(agent["evidence_requirement"])
        self.assertEqual("verificador", by_name["construtor"]["next"])
        self.assertEqual("human_gate", by_name["verificador"]["next"])

    def test_project_agent_files_follow_official_format(self):
        for role in ("construtor", "verificador"):
            item = next(r for r in self.data["roles"] if r["id"] == role)
            relative = pathlib.PurePosixPath(item["agent_definition"])
            self.assertEqual((".agents", "agents"), relative.parts[:2])
            self.assertEqual(".md", relative.suffix)
            path = ROOT.joinpath(*relative.parts)
            self.assertTrue(path.is_file(), str(path))
            content = path.read_text(encoding="utf-8")
            match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", content, re.S)
            self.assertIsNotNone(match, str(path))
            header, body = match.groups()
            self.assertIn("name: observatorio-" + role, header)
            self.assertIn("description:", header)
            self.assertIn("tools:", header)
            self.assertIn("model: inherit", header)
            self.assertIn("permission_mode: always_confirm", header)
            self.assertRegex(header, r"max_iteration_per_run:\s*[1-9]\d*")
            self.assertNotIn("never_confirm", content)
            self.assertNotIn("mcp_servers:", content)
            self.assertTrue(body.strip().startswith("#"))
            self.assertIn("não", body.lower())

    def test_scope_permissions_and_provenance(self):
        policy = self.data["policy"]
        for action in ["start_llm_task", "file_write", "merge_pr",
                       "deployment", "cross_project_access"]:
            self.assertIn(action, policy["approval_required_for"])
        levels = policy["graph_evidence"]["evidence_levels"]
        self.assertIn("design", levels)
        self.assertIn("authenticated_read", levels)
        self.assertIn("human_approved", levels)
        required = policy["graph_evidence"]["required_metadata"]
        for field in ("origin", "observed_at", "evidence_level", "authorized_scope"):
            self.assertIn(field, required)
        self.assertIn("não cria agentes em execução", (TEAM / "README.md").read_text(encoding="utf-8").lower())
        self.assertIn("VIGIAFAST", (TEAM / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
