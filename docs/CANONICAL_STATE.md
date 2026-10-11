# Estado canônico — Observatório de Agentes (2026-10-10)

## REAL NOW
- Repositório: `OARANHA/observatorio-agents-openhands`.
- `main` verificada em `9deda677ec382197a9cfcfa02d5a8b7bc3755eef` no início desta correção, com V0.4.0 e PR #3 mesclada.
- V0.4.1 proposta em branch de correção; CI e revisão pendentes. Não interpretar o commit da `main` acima como estado futuro.

## EVIDÊNCIA DO CANVAS REAL
- Screenshot do usuário confirma Observatório V0.4 carregando cenário `SIMULAR: CALMO`, 4 sistemas solares, painel e menu normais.
- Regressão visual: as órbitas SVG de cada cartão ficam quase verticais, fora de suas proporções anteriores, porque `.sys-orbits` recebe animação `transform:rotate(360deg)` no SVG inteiro.
- Fonte previa inclinação fixa `rotate(-17 224 77)` nas elipses. Rodar o SVG completo altera a aparência, pode cortar a órbita e invadir áreas visuais.
- Correção V0.4.1: preservar a orientação original e animar `stroke-dashoffset` somente num traço luminoso sobre a elipse externa; velocidade por cenário, opção `prefers-reduced-motion`.

## LIMITES, GATES E FUTURO
- V0.4.1 é somente apresentação: `SIMULAR` segue identificando dados fictícios. Sem telemetria, execuções, credenciais, chamadas HTTP ou bibliotecas adicionadas.
- CI da revisão e validação visual com screenshots desktop/mobile ainda necessárias. Não alegar validação em navegador nem alteração da instalação.
- Integração futura com fontes reais requer BFF autenticado, RBAC por projeto/tenant e origem/horário de observação; nenhuma alteração de VPS, imagens Docker ou OpenHands Core está autorizada.
- Fluxo de trabalho: branch + PR, revisar/aguardar CI, sem polling contínuo e sem merge/deploy automático.

## Reconciliação e slice V0.4.2 (2026-10-10)
- `main` publicada verificada: `3c97c9427df9462f16a1f7fc3fd0d3004e6dd977` (V0.4.1); snapshot anterior acima é histórico.
- MCP OpenHands read saudável; list/status/result disponíveis. Missão sintética nova aguardava `waiting_for_confirmation` (gate humano) na última consulta.
- Código V0.4.2 proposto em branch: leitura pontual e manual pelo host autenticado, sem mudança de backend; vínculo ao projeto declarado, não atestado.
- Pendente: CI, revisão, teste real no Canvas e autorização de instalação; sem RBAC multi-tenant, sem clientes reais, sem deploy.

## Ajuste visual integrado à PR #5
- Missão OBS-REAL-001 verificada como `finished` e resultado `OBS-REAL-001|OK` pela leitura MCP, sem escrita no CRISE.
- Nova proposta: após GET da conversa via Canvas, o Multiverso cria em memória sistema Observatório com uma lua real, sem planetas de agentes falsos. Não há conexão contínua nem persistência.
- **PENDENTE:** CI do novo HEAD, teste autenticado no Canvas, aprovação de merge/instalação. Dados de outros projetos continuam demonstrativos.
