# ADM-CYCLE011D-01 — versão, identidade, ACL e revogação: auditoria estática

Data 2026-10-12. Base main `8380e26ed25f7c00dcd83be2f74ab0fc89a7f58e`. Somente código/documentação públicos e modelo sintético offline.

## REAL NOW → PROVEN EVIDENCE
1. `OpenHands/OpenHands/package.json` e `config/defaults.json` consultados no ciclo C07 declaram Canvas `1.26.0`, TypeScript client e Agent Server `1.54.0`, mínimo Agent Server `1.51.0`. **Não é versão comprovada da instalação do proprietário.**
2. `OpenHands/software-agent-sdk/openhands-agent-server/openhands/agent_server/api.py` cria `APIRouter(prefix="/api", dependencies=[Depends(require_initialized), Depends(check_session_api_key)])` e inclui rotas de conversa. A dependência geral de sessão é compartilhada.
3. `dependencies.py`: `check_session_api_key` confere membership em `config.session_api_keys` quando existem chaves configuradas. Nenhum parâmetro de projeto, conversa/tenant ou papel aparece nesse trecho.
4. `conversation_router.py`: `search_conversations` usa `ConversationService.search_conversations`, `get_conversation` usa serviço por UUID; `delete_conversation` chama `ConversationService.delete_conversation(conversation_id)`. O handler examinado não demonstra política independente de recurso/projeto. **Existência de delete é superfície de risco, não ação executada**.
5. `host.agentServer.request` e `AgentServerClient.request` são interfaces de transporte/seleção de backend e sessão. O runtime instalado, configurações de proxy, controles adicionais ou ACL de outros componentes **não foram observados**.

Fontes públicas:
- https://github.com/OpenHands/OpenHands/blob/main/config/defaults.json
- https://github.com/OpenHands/OpenHands/blob/main/package.json
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/api.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/dependencies.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/conversation_router.py

## PROVEN GAPS / threat model
- **Compatibilidade:** versão instalada, hash e cadeia host/servidor reais continuam desconhecidos.
- **Identidade:** possuir chave de sessão não estabelece sujeito/tenant/role de autorização por conversa. Chaves de workspace em cookies não autorizam APIs de conversa.
- **ACL recurso/projeto:** escopo autenticado servidor por conversa e projeto não demonstrado nos handlers examinados; não inferir ausência global de controles.
- **Revogação:** nenhum teste comprovou revogação de acesso a conversa/projeto no servidor instalado. Retirada de chave de sessão e revogação de associação por projeto são operações distintas.
- **Operações destrutivas:** método DELETE aparece no upstream; vedado qualquer teste real nesta etapa.
- **Lista/paginação:** não consultar `/search` nem usar `selected_repository` como ACL.

## REUSE GATE / DECISION
Reutilizar SDK/Agent Server apenas após comprovar autorização por recurso nas versões efetivas. `tests/cycle011_d01_revocation_acl.test.mjs` é um **modelo de decisão sintético**, não validação da API real. Sem rota nova/BFF, credencial, GET autenticado, simulação de requisição contra terceiros, merge ou deploy.

**G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO · NO-GO operacional**.
