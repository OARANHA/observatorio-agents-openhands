# ADM-CYCLE011C-01 — Compatibilidade host/SDK/Canvas e autorização (offline)

Data: 2026-10-12. Main inicial: `6dc7fcef8c8b1b967961ea3a6fde6ce27286a0d7`.
**Resultado: NO-GO operacional.** Sem GET real, Canvas, credenciais ou deploy.

## REAL NOW / PROVEN EVIDENCE

Código público `OpenHands/software-agent-sdk`, branch principal consultada:
- `openhands-agent-server/openhands/agent_server/api.py`: `APIRouter(prefix="/api", dependencies=[Depends(require_initialized), Depends(check_session_api_key)])` no código de montagem, com `conversation_catalog_router` precedendo `conversation_router`; **evidência estática de dependências compartilhadas das rotas**.
- `conversation_router.py`: rota `/search` e `/{conversation_id}`; `search_conversations` depende de `get_conversation_service`, aceita page_id, limit, status e sort_order. Nenhuma política RBAC por repositório foi demonstrada no handler inspecionado.
- `dependencies.py`: `check_session_api_key` rejeita chave ausente/inválida **quando** `session_api_keys` foi configurada. Não identifica tenant/repositório ou ACL por conversa. Se não houver chaves configuradas, o ramo de rejeição não se aplica; **não extrapolar** para instalação.
- `auth_router.py`: cookie de workspace limitado a arquivos, não as APIs de conversa.
- `OARANHA/observatorio-agents-openhands`: extensão utiliza somente `host.agentServer.request` para GET pontual sob clique; não há inventário automaticamente ativado ou prova de `/search` pelo host.

Fontes:
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/api.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/conversation_router.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/dependencies.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/auth_router.py
- `docs/handoffs/OBS-CYCLE-011-B11-NEXT-AUTHORITY-GATE.md`

## GAPS / REUSE GATE
1. Nenhuma correspondência comprovada entre **versão efetiva** do Canvas/SDK e o código público consultado: **compatibilidade não provada**.
2. `host.agentServer.request` é ponte do frontend: não confundir API documentada do servidor com disponibilidade, proxy e permissões reais no host.
3. Dependência de chave de sessão é autenticação no servidor **não** autorização por recurso/projeto.
4. `selected_repository`, projeto digitado e estado `finished` são metadados, não prova de ACL, identidade individual de agente ou tarefa concluída com êxito.
5. Paginação e deduplicação não substituem autorização. Uma lista de conversas pode conter informação transversal; não buscar.

## Revisão adversarial e plano
Modelo de negação sintético em `tests/cycle011_c01_host_rbac.test.mjs` representa prova cumulativa; **não implementa nem testa o RBAC OpenHands real**.

Próximo gate humano: primeiro demonstrar versão instalada e contrato documental do host; depois localizar no código servidor a política real de autorização por conversa/projeto e seus testes de revogação/escopo. Se não existir, manter NO-GO ou desenhar camada de autorização sob decisão separada (sem implementá-la nesta etapa).

**G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO.** JEV é consultivo e não relaxa gates.

## Fechamento ADM-CYCLE011C-02 — 2026-10-12
- HEAD validado: `352435c5895ef75a202dea1686162bdd680db764`.
- CI Observatório run `38208025194`: SUCCESS; job `contract` e etapa `CYCLE011-C01 host e ACL sintéticos (offline)`: SUCCESS.
- Canary Worker Inert SDK run `38208025120`: SUCCESS.
- Revisão dos três arquivos alterados: handoff, teste sintético e workflow. Nenhuma modificação de Canvas ou integração real.
- Parecer: escopo offline apto para futura decisão de integração documental, sem comprovar versão instalada, rota disponível pelo host, ACL por conversa/projeto ou revogação.
- **G11 NÃO PROVADO; G12 BLOQUEADO; P02 NÃO PROVADO; NO-GO operacional.** Este registro documental cria outro HEAD; a CI desse novo commit não está validada por aquelas execuções. Sem merge, GET real ou deploy.
