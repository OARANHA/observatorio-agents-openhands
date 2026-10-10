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
    def test_sidebar_do_canvas_nao_ser_ocultada(self):
        # Bug real: ::before fixo ocupava o viewport e encobria o texto da sidebar.
        import re
        source=(ROOT/'extension.js').read_text()
        match=re.search(r'^const STYLE = (.+);
        subprocess.run(['node','--check',str(ROOT/'extension.js')],check=True)
if __name__=='__main__':unittest.main()
, source, flags=re.M)
        self.assertIsNotNone(match)
        css=json.loads(match.group(1))
        self.assertIn('.ob-wrap:before{content:"";position:absolute;', css)
        self.assertIn('#starfield{position:absolute;',css)
        self.assertNotIn('position:fixed',css)

    def test_sintaxe(self):
        subprocess.run(['node','--check',str(ROOT/'extension.js')],check=True)
if __name__=='__main__':unittest.main()
