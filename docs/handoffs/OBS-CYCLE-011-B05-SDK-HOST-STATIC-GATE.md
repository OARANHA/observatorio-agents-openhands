# ADM-CYCLE011B-05 — SDK / Agent Server / Canvas: verificação estática

Data 2026-10-12. Base `main` = `295afef198f789432a1df202595da64a212db600` (merge da PR #57). **Nenhum GET autenticado, deploy ou execução de agentes.**

## Evidências por superfície

| Superfície | Evidência estática | Limites e veredito |
|---|---|---|
| **Observatório Canvas local** | `scripts/extension-template.txt`: `host.agentServer.request({method:'GET',path:'/api/conversations/'+id})` após clique, com UUID e status validados | **Comprovado no código** apenas GET pontual. O host efetivo não foi inspecionado em runtime e não se provou contrato de `GET /search`. |
| **OpenHands Agent Server upstream** | `OpenHands/software-agent-sdk`, `openhands-agent-server/openhands/agent_server/conversation_router.py`: `@conversation_router.get("/search")` com `page_id`, `limit: 1..100`, `status`, `sort_order`; retorna `ConversationPage`. Também `GET /{conversation_id}`. | **Rota confirmada no upstream consultado**. Não se demonstrou versão instalada, proxy do Canvas, autorização do host, semântica de tenancy ou repositório. Não chamar. |
| **Cloud App Server V1** | API independente sob `/api/v1/app-conversations/search`, Bearer para Cloud, documentada no CYCLE011-B-1. | Não mapear para o host Canvas; caminhos e sessão distintos. |
| **Agent Server auth** | Referência pública `OpenHands/extensions/skills/openhands-api/SKILL.md` diferencia Bearer Cloud e `X-Session-API-Key` para Agent Server. | Formas de autenticação **não provam isolamento por projeto**; não manipular nem carregar credenciais. |
| **Agente e projeto** | Nenhuma prova de vínculo autenticado conversa↔agente↔projeto no contrato da extensão. | P02 **NÃO PROVADO**; nenhuma promoção automática de nós. |

Fontes de código/documentação, verificação em 2026-10-12:
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/conversation_router.py
- https://github.com/OpenHands/extensions/blob/main/skills/openhands-api/SKILL.md
- `docs/handoffs/OBS-CYCLE-011-B-AUTHORIZED-DISCOVERY-MATRIX.md` no repositório local.

**Cautela de versão:** consulta feita ao `main` público do SDK, não a um snapshot comprovadamente correspondente ao Agent Server do Canvas do usuário. O SDK 1.53.0 usado em testes antigos do Observatório não comprova a versão da sessão Canvas instalada.

## Hipóteses adversariais e reutilização

1. Um endpoint upstream `/search` não assegura que `host.agentServer.request` o aceite na sessão Canvas instalada.
2. Mesmo que retorne `ConversationPage`, lista não comprova vínculo a repositório específico ou controle de acesso por projeto. Falhar fechado.
3. Paginação aceita pela API não autoriza seguir automaticamente o cursor; limites devem ser explícitos e aprovados separadamente.
4. O campo `execution_status` não atesta agente individual nem sucesso semântico da tarefa.
5. Contratos Cloud (`app-conversations`) e Agent Server (`conversations`) não devem ser fundidos.

## Teste offline de gates (modelo de decisão, sem runtime)

`tests/cycle011_b05_authority_gate.test.mjs` representa propositalmente uma regra conservadora: disponibilidade estática da rota sem prova de host+autorização+projeto = **NO-GO**; só aceita configuração sintética quando todas as provas são verdadeiras. Não há código de descoberta no app, HTTP, token ou retorno de cliente.

## Decisão

**GO para documentação e experimentos offline, NO-GO para descoberta real.**
Antes de qualquer proposta operacional: evidência da versão efetiva de host/Agent Server; contrato acessível e documentado via `host`; RBAC/projeto autenticados; decisão sobre escopo, cardinalidade, retenção e revogação. **G11 não comprovado, G12 bloqueado, P02 não comprovado.** Revisão adversarial/JEV consultivos; não alterar gates formalmente.

## Fechamento técnico ADM-CYCLE011B-06 — 2026-10-12
- No HEAD `f135db59c044c120f0be7ee959cf8d63bc9964c8`, CI Observatório run `38205999792` e Canary Worker Inert SDK run `38205999845` foram SUCCESS.
- O job da CI confirma a execução bem-sucedida de **Gate estático de autoridade CYCLE011-B05 (offline)**, além dos contratos e do build existentes.
- Revisão: o teste é uma função de decisão hipotética, **não** prova autorização efetiva, versão do Canvas, isolamento por repositório ou presença de rota no host.
- Decisão: incremento documental/contratual pronto para avaliação de integração posterior; **NO-GO** para descoberta real, G11 não provado, G12 bloqueado, P02 não provado.
- Este fechamento gera novo HEAD documental, cuja CI não deve ser confundida com a do commit anterior. Sem merge/deploy.
