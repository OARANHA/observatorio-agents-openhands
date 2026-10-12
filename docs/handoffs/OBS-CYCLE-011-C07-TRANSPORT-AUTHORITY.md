# ADM-CYCLE011C-07 — versão pública, client.request e ACL por recurso

Data 2026-10-12. Base main `1edec9e42588fb52070734f2af358af872345f2f`. **Análise pública/offline; NO-GO operacional.**

## REAL NOW → PROVEN EVIDENCE

- `OpenHands/OpenHands/package.json`: versão do pacote Agent Canvas **1.26.0**; dependência `@openhands/typescript-client` **1.54.0**.
- `OpenHands/OpenHands/config/defaults.json`: pin público `versions.agentServer=1.54.0`, `versions.agentCanvas=1.26.0`, `compatibility.minimumAgentServer=1.51.0`. São números do código público consultado, **não identificam a versão instalada**.
- `src/api/canvas-extensions-service.ts`: `getClientForBackend` rejeita backend ausente/cloud e instancia `new AgentServerClient({host:backend.host,apiKey:backend.apiKey,timeout:60000})`; `requestAgentServer` rejeita caminho não raiz/`//`, depois `client.request({method,path,body,headers})`. Não foi observada allowlist por recurso nessa função.
- `OpenHands/software-agent-sdk/clients/typescript/src/client/openhands-client.ts`: `AgentServerClient.request` resolve host e chave do cliente, instancia/reutiliza `HttpClient` e chama `client.request({method,url,params,data,headers,timeout,...})`, retornando `response.data`. Não foram identificadas, nesse método, validações explícitas de vínculo conversa/repositório.
- Agent Server público `api.py` e `dependencies.py`: autenticação condicional à chave de sessão configurada, não atestado de ACL multiprojeto. **Ausência de prova aqui não é uma auditoria exaustiva do transporte, proxies, plugins ou instalação.**

Fontes:
- https://github.com/OpenHands/OpenHands/blob/main/package.json
- https://github.com/OpenHands/OpenHands/blob/main/config/defaults.json
- https://github.com/OpenHands/OpenHands/blob/main/src/api/canvas-extensions-service.ts
- https://github.com/OpenHands/OpenHands/blob/main/src/api/agent-server-client-options.ts
- https://github.com/OpenHands/software-agent-sdk/blob/main/clients/typescript/src/client/openhands-client.ts

## GAPS / REUSE GATE / DECISION

| Condição | Resultado |
|---|---|
| Pins do código público | Comprovados no conteúdo inspecionado |
| Hash/versão da instalação do operador | NÃO PROVADO |
| Cadeia host → AgentServerClient.request → HttpClient.request | Comprovada estaticamente até chamada HttpClient |
| Implementação interna do HttpClient + interceptadores/proxy | NÃO AUDITADA nesta etapa |
| ACL por conversa e projeto no servidor instalado | NÃO PROVADO |
| Revogação efetiva por projeto | NÃO PROVADA |

**Risco adversarial:** presença de `apiKey`, passagem de headers, método e path genéricos são meios de transporte/autenticação, não autorização a recursos. Um status `finished` ou `selected_repository` também não concede direitos. A versão mínima declarada não valida compatibilidade do conjunto efetivamente implantado.

Os testes de `tests/cycle011_c07_transport_authority.test.mjs` representam somente lógica sintética de falha fechada; **não instrumentam `HttpClient` real**. Exigir rastreio específico do middleware servidor/ACL, versão instalada verificável e gate humano antes de qualquer chamada real ou ampliação de escopo.

**G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO · NO-GO operacional.**
