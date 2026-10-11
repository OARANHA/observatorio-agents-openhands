"""Execute frozen PR7 pure-model contracts, never its browser/host integration."""
import pathlib
import subprocess
import unittest


class GraphModelOffline(unittest.TestCase):
    def test_frozen_model_contracts(self):
        root = pathlib.Path(__file__).resolve().parent.parent
        result = subprocess.run(['node', '--test', '--test-reporter=tap',
                                 'tests/graph_model_contract.mjs'],
                                cwd=root, capture_output=True, text=True, timeout=15,
                                check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('# tests 6', result.stdout)
        self.assertIn('# pass 6', result.stdout)
        self.assertIn('# skipped 0', result.stdout)
