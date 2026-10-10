# Estado canônico — 2026-10-10

## Evidência local
- `OARANHA/observatorio-agents-openhands` estava vazio quando iniciado (apenas README bootstrap criado na main).
- `OpenHands/demos/vibe-kanban` demonstrou `canvas-extension.json` e `activate(host) / host.registerPage`.
- V0.2 foi preservada em source. V0.3 adapta ao Canvas via Shadow DOM e ciclo de vida de mount/unmount.
- Testes locais de sintaxe e navegação desktop/mobile em Canvas simulado passaram no ambiente de desenvolvimento.

## Não comprovado
- Instalação em Agent Canvas real, permissões/route/CSP do servidor instalado, WebGL2 com GPU real, inventário real de agentes, isolamento multi-tenant, CI remoto e integração read-only.
- Nenhuma permissão de deploy/instalação do Canvas foi concedida por este commit.

## Gates
1. Revisão PR e CI, sem polling contínuo.
2. Avaliação de JS privilegiado e autorização específica para instalar desabilitado em Canvas real.
3. Validação no navegador com sessão owner, sem dados de clientes.
4. BFF de leitura com RBAC, auditoria, minimização e prova de isolamento antes de telemetria real.
