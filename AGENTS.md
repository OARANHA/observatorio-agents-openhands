# AGENTS
Ordem: docs/PROJECT_SOURCE.md -> docs/CANONICAL_STATE.md -> docs/decisions/ -> docs/ARCHITECTURE.md -> README.md -> código/testes.
- Produto: aplicativo de visualização do OpenHands Canvas; nunca alterar OpenHands Core, VIGIAFAST, Wandora, ELUS, brokers ou VPS por implicação.
- Nunca chamar dados mockados de agentes reais. Não inventar telemetria, custos ou sucesso das tarefas.
- Código do app roda com contexto autenticado: nenhuma credencial, cookie, token ou prompt para GitHub ou navegador; ações start/stop/merge/deploy precisam de autorização específica e revisão.
- Verificar Shadow DOM, lifecycle, API, evidências e licenças; branch + PR, sem merge nem deploy automático, sem polling de CI.
