# CYCLE007 — Candidata V0.5.2 · Grafo Estelar (somente visual/offline)

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

- Base reconciliada `main`: `5cedc0eada928fcd1f46cc50e2144d02822181be` (PR #43 grafo V0.5.1 e PR #44 plano CYCLE006 integradas). PRs #7 draft e #35 abertas, intocadas.
- Capturas fornecidas pelo operador mostram Observatório **V0.5.1 já atualizado e ativado no Canvas** com ref `5cedc0eada928fcd1f46cc50e2144d02822181be`, uma página, menu Apps. Outra captura mostra o grafo de cinco nós DEMO (quatro projetos + hub), linhas e controles efetivamente renderizados no Canvas. Essas capturas **não provam** WebGL2/touch, consulta de conversa, autorização por projeto ou operação de agentes.
- Feedback humano: grafo atual “meio sem graça”. Pedido expresso para preparar candidata **V0.5.2** em PR separada, sem modificar Canvas instalado.
- Arquivos/fonte reutilizados: `source/observatorio-v02.html`, `scripts/build.mjs`, `scripts/extension-template.txt`, testes Chromium, contrato do manifesto e docs. Build base V0.5.1 reproduzido byte-a-byte **antes** das alterações.
- Mudanças previstas: fundo de constelações feito apenas com CSS local; aura/rings nos nós; distribuição orgânica determinística mantendo hub DEMO e cluster consultado separados; arestas curvas SVG path em camadas, cor/traçado por origem `demo/verified/manual`; leitura de teclado, zoom, pan, filtro, seleção e `prefers-reduced-motion` preservados; sem novos requests, dependências ou runtime de agentes.
- Manifesto aumenta somente `0.5.1` → `0.5.2`; `extension.js` é gerado deterministicamente, não editado isoladamente. Contratos/testes atualizados para caminhos SVG e 3 novos cenários Chromiun; total **22 DOM esperados**, até CI provar. Nenhuma CI do novo commit foi consultada ou declarada GREEN.
- Proveniência: 4 nós DEMO permanecem **DEMO**, hub **APENAS DEMO**, conversas só após GET opt-in com origem explícita, ligação com projeto classificada **manual**, e status da conversa não equivale a sucesso do agente. `local-view-not-tenant` não constitui RBAC.
- **GAPS:** validar CI, screenshot 1440px e 390px, links/foco, contexto Canvas instalado na versão candidata, WebGL2 físico, touch/leitor de tela. GET timeout é local e não cancela transporte. Operação real e memórias não provadas.
- **DECISION:** entregar branch e PR **draft**, sem merge, instalação/habilitação Canvas, deploy, dados privados, agentes/LLM ou alteração externa. **G11 NÃO PROVADO; G12 BLOQUEADO; P01 PARCIAL; P02/P03 NÃO PROVADOS; ADR-0001 PROPOSTO; NO-GO operacional**. Próxima revisão: CI por aviso do proprietário (sem polling), inspeção de screenshots do runner e Codex adversarial.

## Critérios de aceite técnico preliminares
- Grafo continua navegável por Tab/Enter/Escape e setas com foco restaurado; zoom/pan bounded.
- Temas `DEMO`/fonte consultada/vínculo manual distinguíveis sem cor isolada (tag + traçado sólido/tracejado).
- Sem WebGL externo ou novos fetch; renderização puramente CSS/SVG de dados existentes.
- `prefers-reduced-motion:reduce` desabilita pulse/transições dos nós.
- Mapa mobile não impede scroll vertical e pinch do browser.
- Screenshots sintéticos de CI não são evidência de homologação do Canvas.

## CI RED pontual e correção do contrato estático (2026-10-11)

- HEAD anterior `7105dcf0154aa6bcc6d6677a6c7e6cbeae54b735`: workflow CI Observatorio [38179029418](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38179029418) **failure**: `tests/test_contract.py:197`, caso `test_grafo_nao_inventa_agentes_vinculos_ou_sucesso` exige por igualdade textual o `if(verifiedMission&&validGraphIdentity(...))` da V0.5.1. Na V0.5.2 essa condição foi extraída para `const hasConsulted=!!(verifiedMission&&validGraphIdentity(verifiedMission.graphIdentity));` e aplicada por `if(hasConsulted){`. Não houve evidência de bypass lógico; **é contrato estático não atualizado**.
- Dois workflows do mesmo HEAD **GREEN**: Graph DOM Offline [38179029437](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38179029437) **22/22**; Canary Worker Inert SDK [38179029414](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38179029414) sem ações reais.
- Correção mínima `tests/test_contract.py`: exigir **ambas** a atribuição com `validGraphIdentity` e a guarda `if(hasConsulted){`; manter demais asserts sobre tipos, relações, origem e ausência de sucesso inventado.
- Nenhum `source/observatorio-v02.html`, `extension.js`, manifesto, runtime, CSS, host ou Canvas alterados nessa correção. **CI do próximo SHA PENDENTE**, workflow verde do SHA anterior não valida o novo commit. Sem polling; proprietário informa `green`/`red`.
- G11 NÃO PROVADO; G12 BLOQUEADO; P01 PARCIAL; P02/P03 NÃO PROVADOS; ADR-0001 PROPOSTO, NO-GO operacional.

## Revisão adversarial Codex — P2 colisão em 900×700 (2026-10-11)
- Revisor Codex examinou PR #45 HEAD `73d035542e30fd256dfa16bd59498ce92ae7b46c` árvore `79591af8aada48260141b0707327adc071b60b3f` base `5cedc0eada928fcd1f46cc50e2144d02822181be`, somente leitura. Parecer **CORREÇÕES NECESSÁRIAS**, sem P0/P1 demonstrados. Revisou geração byte-a-byte, proveniência, escaping, curvas SVG e consultas tardias. Não conseguiu testar Chromium localmente.
- Achado P2: no layout **com conversa consultada**, hub em (34%,49%) e cartão VIGIAFAST em (16%,21%) podem se sobrepor em viewport 900×700 (mapa 525×338 px, interseção estimada 15,5×4,36 px). Cálculo de geometria, não reprodução direta no navegador pelo Codex.
- Alteração estritamente visual: hub consultado em (40%,50%); DEMO direito superior em y15%, direito inferior em y85%. Sem consulta, layout preservado. Nós, vínculos, proveniência e contrato host inalterados.
- Nova regressão Chromium por `getBoundingClientRect()` mede oito nós após GET sintético e exige interseções vazias em 900×700 e 390×844 (esperados **23 testes Graph DOM**, **nova CI NÃO VALIDADA**). Viewports adicionais/Canvas/touch e acessibilidade não comprovados por isso.
- Artefato `extension.js` regenerado com algoritmo oficial após comparar baseline byte-a-byte. Sem merge, Canvas, deploy, LLM/agente real ou dados privados. **G11 NÃO PROVADO; G12 BLOQUEADO; P01 PARCIAL; P02/P03 NÃO PROVADOS; ADR-0001 PROPOSTO; NO-GO operacional**. Aguardar proprietário informar GREEN/RED, sem polling.

## RED em 23/23 — remediação da coluna consultada, viewport 900×700 (2026-10-11)
- GitHub PR #45 HEAD anterior `d56b316eaaa77551851fedcbbb5687bdb087d3e9`: [Graph DOM Offline 38181224586](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38181224586) **RED**, 22/23 testes aprovados. Novo teste geométrico detectou em Chromium 900×700 sobreposição **FONTE CONSULTADA → CONVERSA** (110 × 3,89 px) e **CONVERSA → PROJETO INFORMADO** (110 × 5,22 px). Isso é medição `getBoundingClientRect`, não apenas cálculo. A colisão hub DEMO/VIGIAFAST já não consta do erro. [CI Observatorio 38181224559](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38181224559) GREEN; [Canary Worker Inert SDK 38181224742](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38181224742) GREEN.
- Remediação incremental: regra CSS somente para `min-width:871px` e `max-height:760px` compacta **sem max-height e sem clipping** os cartões consultados `verified/manual` (padding/gap/beacon/texto menor, altura mínima 76px). Não move outros nós, não altera proveniência, leitura, dados, arestas ou comportamento de host. O teste Chromium de colisão permanece igual em 900×700 e 390×844; total esperado 23.
- `extension.js` regenerado a partir da mesma fonte/template, com baseline anterior idêntico byte a byte. CI do **novo commit** ainda não comprovada; aguardar aviso GREEN/RED, **sem polling**. G11 NÃO PROVADO, G12 BLOQUEADO, P01 PARCIAL, P02/P03 NÃO PROVADOS; Canvas continua V0.5.1, NO-GO operacional.
