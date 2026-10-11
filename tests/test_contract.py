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
                          'sessionStorage', 'document.cookie']:
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
        self.assertIn('@keyframes obOrbitFlow', css)
        self.assertIn('@media(prefers-reduced-motion:reduce)', css)
        self.assertIn('.system-tile[data-activity="active"]', css)
        self.assertIn('.planet-slot[data-activity="active"]', css)
        self.assertIn('host.agentServer.request', source)
        self.assertNotIn('fetch(', source)


    def test_universe_orbits_preserve_ellipse_tilt(self):
        # A V0.4 girava o SVG inteiro: elipses ficavam verticais/cortadas.
        # Na V0.4.1 apenas o brilho acompanha o tracado.
        source = (ROOT / 'extension.js').read_text()
        style_line = next(line for line in source.splitlines()
                          if line.startswith('const STYLE = '))
        css = json.loads(style_line[len('const STYLE = '):-1])
        self.assertIn('class="orbit-stream"', source)
        self.assertIn('transform="rotate(-17 224 77)"', source)
        self.assertIn('.system-tile .sys-orbits .orbit-stream{', css)
        self.assertIn('stroke-dashoffset:-480', css)
        self.assertIn('.system-tile[data-activity="active"] .orbit-stream{', css)
        self.assertIn('.system-tile[data-activity="attention"] .orbit-stream{', css)
        self.assertIn('.system-tile[data-activity="error"] .orbit-stream{', css)
        self.assertIn('.system-tile .sys-orbits .orbit-stream,.system-tile:before,', css)
        self.assertNotIn('obOrbitRevolve', css)
        self.assertNotIn('.sys-orbits{transform-box:', css)


    def test_real_read_requires_manual_uuid_without_secrets(self):
        source = (ROOT / 'extension.js').read_text()
        self.assertIn("method:'GET',path:'/api/conversations/'+id", source)
        self.assertIn("Projeto declarado:", source)
        self.assertIn("não atestada pela API", source)
        self.assertIn("Observado em (hora do navegador):", source)
        self.assertNotIn('fetch(', source)
        self.assertNotIn('localStorage', source)
        self.assertNotIn('setInterval(', source)


    def test_lua_real_separada_das_simulacoes(self):
        source = (ROOT / 'extension.js').read_text()
        markup_line = next(line for line in source.splitlines() if line.startswith('const MARKUP = '))
        markup = json.loads(markup_line[len('const MARKUP = '):-1])
        self.assertIn('id="real-lua"', markup)
        self.assertIn('function openVerifiedSystem()', source)
        self.assertIn('function renderVerifiedPanel()', source)
        self.assertIn('function applyVerifiedMission(observation)', source)
        self.assertIn("systems.push('observado')", source)
        self.assertIn('AGENTES COMPROVADOS', source)
        self.assertIn('Manual', source)
        self.assertIn('Os demais planetas são demonstrações.', source)
        self.assertIn('SIMULAÇÃO:', source)
        self.assertIn("host.agentServer.request({method:'GET',path:'/api/conversations/'+id})", source)
        self.assertNotIn('fetch(', source)
        self.assertNotIn('setInterval(', source)
        self.assertNotIn('document.cookie', source)

    def test_sintaxe(self):
        subprocess.run(['node', '--check', str(ROOT / 'extension.js')], check=True)



class GraphV050(unittest.TestCase):
    """Contratos: modo Grafo, identidade multiprojeto e dados rastreaveis."""

    def test_manifest_v050(self):
        data = json.loads((ROOT / 'canvas-extension.json').read_text(encoding='utf-8'))
        self.assertEqual(data['version'], '0.5.0')
        self.assertIn('grafo', data['description'].lower())

    def test_graph_navigation_and_interaction(self):
        source = (ROOT / 'extension.js').read_text(encoding='utf-8')
        style_line = next(line for line in source.splitlines() if line.startswith('const STYLE = '))
        markup_line = next(line for line in source.splitlines() if line.startswith('const MARKUP = '))
        css = json.loads(style_line[len('const STYLE = '):-1])
        markup = json.loads(markup_line[len('const MARKUP = '):-1])
        for expected in ('id="top-graph"', 'id="rail-graph"', 'id="graph"',
                         'id="graph-scope"', 'id="graph-search"', 'id="graph-map"',
                         'id="graph-surface"'):
            self.assertIn(expected, markup)
        for expected in ('function openGraph()', 'function graphModel()',
                         'function renderGraph()', 'function renderGraphPanel()',
                         'graphScope', 'graphQuery', 'graphZoom', "graphSelected"):
            self.assertIn(expected, source)
        self.assertIn(".graph.hidden{display:none}", css)
        self.assertIn(".graph-node[data-kind=\"verified\"]", css)
        self.assertIn(".graph-node[data-kind=\"manual\"]", css)
        self.assertIn("graph-surface", css)
        self.assertIn("graphScope='all'", source)
        self.assertIn("graphScope==='demo'", source)

    def test_grafo_nao_inventa_agentes_vinculos_ou_sucesso(self):
        source = (ROOT / 'extension.js').read_text(encoding='utf-8')
        self.assertIn("if(verifiedMission){", source)
        self.assertIn("kind:'verified'", source)
        self.assertIn("kind:'manual'", source)
        self.assertIn("kind:'demo'", source)
        self.assertIn("kind:'demo-hub'", source)
        self.assertIn("edges.push({from:'real-origin',to:'real-mission',kind:'verified'})", source)
        self.assertIn("edges.push({from:'real-mission',to:'manual-project',kind:'manual'})", source)
        self.assertIn("O servidor não confirmou o vínculo", source)
        self.assertIn("Uma conversa concluída não garante sucesso da tarefa.", source)
        self.assertNotIn("setInterval(", source)
        self.assertNotIn("fetch(", source)
        self.assertNotIn("document.cookie", source)

    def test_consulta_recolhe_formulario_sem_apagar_resultado(self):
        source = (ROOT / 'extension.js').read_text(encoding='utf-8')
        self.assertIn("detail.open=false;", source)
        self.assertIn("onVerified({conversationId:id", source)


if __name__ == '__main__':
    unittest.main()
