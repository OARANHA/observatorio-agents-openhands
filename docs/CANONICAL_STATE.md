# Estado canônico — Observatório de Agentes (2026-10-10)

## REAL NOW — GitHub
- Repositório: `OARANHA/observatorio-agents-openhands`.
- PR #1 da V0.3.1 integrada à `main` no commit `6305e725da0ee2121831e57ae085f43f085e48dd` após CI concluída com sucesso no HEAD `1a82439c7bc21f55d3b9c429657baf2c5785eaa3`.
- Evolução V0.3.2 em branch de correção; integração na `main` depende de CI e revisão humana. Não presumir instalação real antes da validação no Canvas.

## PROVEN EVIDENCE
- Extensão por manifesto `canvas-extension.json`, ESM e `activate(host)`/`registerPage`, com Shadow DOM e WebGL2/fallback 2D.
- A V0.3.1 já foi exibida pelo usuário no Canvas real (screenshot) após a correção anterior da sidebar.
- Captura da visualização WANDORA mostrou a caixa explicativa parcialmente coberta pelo painel de métricas.
- Causa no código: `.solar-note` e `.metrics` tinham `position:absolute`, com `bottom:93px` e `bottom:24px` respectivamente; seus intervalos verticais se sobrepunham.
- Correção V0.3.2: um `.scene-bottom` organiza nota e métricas verticalmente, mantém a nota oculta no universo e reposiciona o conjunto nos breakpoints existentes; testes de contrato cobrem CSS, DOM e controle de visibilidade.
- Projetos, papéis, tarefas e estados são **dados demonstrativos**, não telemetria real.

## GAPS E GATES
- CI e validação visual da nova revisão no Canvas real, inclusive desktop e mobile; nenhum resultado presumido.
- Futuro inventário de agentes reais requer BFF de leitura, origem, observação temporal, RBAC por projeto/tenant e auditoria. Não expor credenciais, sessões ou conteúdo de clientes.
- Nenhuma operação de deploy/restart, escrita em VPS ou alteração de outros produtos está autorizada por este slice.
- Não realizar merge/deploy automáticos nem polling contínuo de CI.
