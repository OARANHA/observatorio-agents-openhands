import pathlib
import re
import subprocess
import unittest


class GraphIdentityContract(unittest.TestCase):
    def test_compound_identity_contract(self):
        root = pathlib.Path(__file__).resolve().parent.parent
        result = subprocess.run(['node', '--test', '--test-reporter=tap',
                                 'tests/graph_identity_contract.mjs'], cwd=root,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        tests = re.search(r'^# tests (\d+)$', result.stdout, re.MULTILINE)
        passed = re.search(r'^# pass (\d+)$', result.stdout, re.MULTILINE)
        self.assertIsNotNone(tests, result.stdout)
        self.assertIsNotNone(passed, result.stdout)
        self.assertGreaterEqual(int(tests.group(1)), 9)
        self.assertEqual(tests.group(1), passed.group(1))
        self.assertIn('# fail 0', result.stdout)
        self.assertIn('# skipped 0', result.stdout)
