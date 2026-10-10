"""Contratos mínimos, sem npm nem rede."""
import json, pathlib, subprocess, unittest
ROOT=pathlib.Path(__file__).resolve().parent.parent
class Contract(unittest.TestCase):
    def test_manifest(self):
        d=json.loads((ROOT/'canvas-extension.json').read_text())
        self.assertEqual(d['schema_version'],1)
        self.assertEqual(d['entrypoint'],'extension.js')
        self.assertEqual(d['contributes']['pages'][0]['id'],'observatorio')
    def test_sem_rede(self):
        s=(ROOT/'extension.js').read_text()
        self.assertIn("host.registerPage('observatorio'",s)
        for forbidden in ['fetch(','XMLHttpRequest','WebSocket(','localStorage','sessionStorage','document.cookie','host.agentServer.request']:
            self.assertNotIn(forbidden,s)
        self.assertIn('attachShadow',s)
        self.assertIn('cancelAnimationFrame',s)
    def test_sintaxe(self):
        subprocess.run(['node','--check',str(ROOT/'extension.js')],check=True)
if __name__=='__main__':unittest.main()
