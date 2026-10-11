import pathlib
import subprocess
import unittest


class GraphIdentityContract(unittest.TestCase):
    def test_compound_identity_contract(self):
        root = pathlib.Path(__file__).resolve().parent.parent
        result = subprocess.run(['node', '--test', '--test-reporter=tap',
                                 'tests/graph_identity_contract.mjs'], cwd=root,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('# pass 8', result.stdout)
        self.assertIn('# skipped 0', result.stdout)
