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
