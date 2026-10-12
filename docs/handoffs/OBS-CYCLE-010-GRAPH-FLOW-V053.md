# CYCLE010 — fluxo vertical do Grafo Estelar V0.5.3

Data: 2026-10-11 (Brasília). Correção visual limitada; sem instalação Canvas.

## REAL NOW
- GitHub reconfirmado: main `f9b8049d89ea6ebb8086bab1a281bf9d3bad5e91`, PR #53 merged e somente documental. Branch existente `fix/cycle010-graph-toolbar-flow-v0521-20261011`, base `1cf12721eee0911aec7471b0e46f246d57c789a3`, continha apenas regressão sobre main. PRs #49–#52 permanecem independentes e intocadas.
- Última evidência Canvas é do operador: v0.5.2 ativa na ref `08d9072240411c5c980faadaf39b0336349591ef`; esta missão não inspecionou nem atualizou o aplicativo instalado. ADR-0001 continua PROPOSTO.

## PROVEN EVIDENCE — RED → GREEN
- Regressão original falhou antes da correção: em 1550×870 a distância descrição/filtros era só 2,81 px. Regressão ampliada mediu sobreposição real em 600×700: cabeçalho/filtros −36,19 px; filtros/mapa −23 px; mapa/legenda −53 px. Texto multilinha ampliou a colisão.
- Causa comprovada: acima de 580 px as regiões utilizavam posicionamento absoluto e offsets fixos; alturas da descrição e dos filtros crescem quando texto/controles quebram linhas.
- Reuso do fluxo já existente no mobile: cabeçalho, filtros, mapa, legenda e indicadores agora reservam espaço em todas as larguras. Mapa desktop com altura responsiva mínima de 350 px; mobile continua 350 px ou 540 px no layout consultado estreito. Margens, cores e interações existentes preservadas.
- Geometria Chromium GREEN em 14 viewports (1550, 1440, 1200, 1024, 900, 871, 870, 820, 700, 600, 581, 580, 390, 320 px), cada um com texto original e descrição triplicada. Distância mínima testada 7 px entre regiões, mapa utilizável, sem overflow horizontal e três indicadores visíveis.
- Suíte completa Graph DOM: 25/25 PASS, zero falhas/skips; cobre teclado, foco, pan/zoom/reset, seleção, proveniência sintética, Shadow DOM, reduced-motion, resize e teardown.
- Python: 218 testes, 190 PASS, 28 skips opcionais por SDK ausente; zero falhas. Os wrappers executam também os contratos Node. `node scripts/build.mjs`, `node --check extension.js` e `git diff --check` PASS. Geração repetida idêntica.
- Local: Playwright 1.62.1 + `/usr/bin/chromium`, sandbox habilitado, fixtures interceptadas sem sessão Canvas. Adaptador de caminho somente no scratch; CI mantém Playwright 1.58.0 fixado e seu Chromium oficial. CI do novo HEAD ainda deve ser confirmada.
- Capturas sintéticas desktop/mobile e multilinha examinadas. Captura fullPage omitiu texto dos indicadores fora do viewport; causa de composição não isolada. Captura específica após rolagem mostra as três colunas completas. Não confundir essa limitação com homologação real.
- Revisão automatizada separada examinou CSS/testes/build; não substitui revisão humana formal G11.

## GAPS
- CI e revisão GitHub do HEAD exato pendentes até readback da PR; merge ainda não comprovado. Se workflows executando, aguardar GREEN/RED do proprietário, sem polling contínuo.
- Nenhuma prova adicional de Canvas autenticado, GPU real, touch físico, leitor de tela, RBAC ou memória persistente. G11 NÃO PROVADO; G12 BLOQUEADO; P01 PARCIAL; P02/P03 NÃO PROVADOS; NO-GO operacional.

## REUSE GATE → DECISION
- Fonte oficial `source/observatorio-v02.html`; `extension.js` gerado exclusivamente com `node scripts/build.mjs`. Manifesto e rótulo visual `CONSTELAÇÕES · V0.5.3` sincronizados.
- `scripts/build.mjs` e `scripts/extension-template.txt` inspecionados e inalterados. JS funcional, API GET existente, credenciais, dependências de runtime e comportamento operacional inalterados. Zero agentes/LLM/dispatch reais; nenhuma intervenção Core/VPS/Docker/outros projetos.
- Abrir PR da branch existente para main. Merge visual já autorizado pelo proprietário somente com GREEN do HEAD exato, sem bloqueantes e exigências de revisão cumpridas. Status e SHA exatos devem constar no readback GitHub; este documento não antecipa merge.
- Atualização manual futura do Canvas deve usar SHA imutável validado na PR/merge, após decisão separada. Não usar o SHA histórico da base como se contivesse a correção. Esta missão não instala nem habilita o app.
