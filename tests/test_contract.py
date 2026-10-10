"""Testes de contrato e regressão visual da extensão, sem rede."""
import json
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent


class Contract(unittest.TestCase):
    def test_manifest(self):
        data = json.loads((ROOT / 'canvas-extension.json').read_text())
        self.assertEqual(data['schema_version'], 1)
        self.assertEqual(data['entrypoint'], 'extension.js')
        self.assertEqual(data['contributes']['pages'][0]['id'], 'observatorio')

    def test_sem_rede(self):
        source = (ROOT / 'extension.js').read_text()
        self.assertIn("host.registerPage('observatorio'", source)
        for forbidden in ['fetch(', 'XMLHttpRequest', 'WebSocket(', 'localStorage',
                          'sessionStorage', 'document.cookie', 'host.agentServer.request']:
            self.assertNotIn(forbidden, source)
        self.assertIn('attachShadow', source)
        self.assertIn('cancelAnimationFrame', source)

    def test_sidebar_do_canvas_nao_ser_ocultada(self):
        # O ::before fixo escapava do painel e encobria a barra lateral do Canvas.
        source = (ROOT / 'extension.js').read_text()
        style_line = next((line for line in source.splitlines()
                           if line.startswith('const STYLE = ')), None)
        self.assertIsNotNone(style_line)
        self.assertTrue(style_line.endswith(';'))
        css = json.loads(style_line[len('const STYLE = '):-1])
        self.assertIn('.ob-wrap:before{content:"";position:absolute;', css)
        self.assertIn('#starfield{position:absolute;', css)
        self.assertNotIn('position:fixed', css)

    def test_sintaxe(self):
        subprocess.run(['node', '--check', str(ROOT / 'extension.js')], check=True)


if __name__ == '__main__':
    unittest.main()
