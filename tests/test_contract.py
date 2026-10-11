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

    def test_nota_do_sistema_solar_nao_fica_atras_das_metricas(self):
        # A nota e as metricas compartilham um empilhamento vertical; nenhum
        # dos dois fica com bottom absoluto independente.
        source = (ROOT / 'extension.js').read_text()
        style_line = next((line for line in source.splitlines()
                           if line.startswith('const STYLE = ')), None)
        markup_line = next((line for line in source.splitlines()
                            if line.startswith('const MARKUP = ')), None)
        self.assertIsNotNone(style_line)
        self.assertIsNotNone(markup_line)
        css = json.loads(style_line[len('const STYLE = '):-1])
        markup = json.loads(markup_line[len('const MARKUP = '):-1])
        self.assertIn('.scene-bottom{position:absolute;z-index:9;bottom:24px;', css)
        self.assertIn('.solar-note{position:static;', css)
        self.assertIn('.solar-note.hidden{display:none}', css)
        self.assertIn('.metrics{position:static;width:100%;', css)
        self.assertIn('.scene-bottom{bottom:18px}', css)
        self.assertIn('.scene-bottom{left:9px;right:9px}', css)
        self.assertIn('class="scene-bottom"><div class="solar-note hidden" id="solar-note"', markup)
        self.assertLess(markup.index('id="solar-note"'), markup.index('id="metrics"'))
        self.assertIn("$('solar-note').classList.add('hidden')", source)
        self.assertIn("$('solar-note').classList.remove('hidden')", source)

    def test_visual_v04_cenarios_e_motion_sao_demo(self):
        source = (ROOT / 'extension.js').read_text()
        style_line = next(line for line in source.splitlines()
                          if line.startswith('const STYLE = '))
        markup_line = next(line for line in source.splitlines()
                           if line.startswith('const MARKUP = '))
        css = json.loads(style_line[len('const STYLE = '):-1])
        markup = json.loads(markup_line[len('const MARKUP = '):-1])
        self.assertIn('id="visual-demo"', markup)
        self.assertIn('PROTÓTIPO · DADOS ILUSTRATIVOS', markup)
        self.assertIn('visualScenarios=[', source)
        for state in ('idle', 'active', 'attention', 'error'):
            self.assertIn("'" + state + "'", source)
        self.assertIn('demoAgentVisual(', source)
        self.assertIn('demoSystemVisual(', source)
        self.assertIn('data-activity=', source)
        self.assertIn('SIMULAÇÃO:', source)
        self.assertIn('SIMULAR: ', source)
        self.assertIn('uActivity', source)
        self.assertIn('Math.min(visual.tasks,2)', source)
        self.assertIn('@keyframes obStarDrift', css)
        self.assertIn('@keyframes obOrbitRevolve', css)
        self.assertIn('@media(prefers-reduced-motion:reduce)', css)
        self.assertIn('.system-tile[data-activity="active"]', css)
        self.assertIn('.planet-slot[data-activity="active"]', css)
        self.assertNotIn('host.agentServer.request', source)
        self.assertNotIn('fetch(', source)

    def test_sintaxe(self):
        subprocess.run(['node', '--check', str(ROOT / 'extension.js')], check=True)


if __name__ == '__main__':
    unittest.main()
