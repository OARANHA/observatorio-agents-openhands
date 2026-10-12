# CYCLE011-B — Descoberta autorizada: inventário de superfícies (somente offline)

Data: 2026-10-12. Base: main `128425855a84828df96cd522e93ebd8689999e7d` (merge PR #56).
**Status: pesquisa/documentação e testes sintéticos; nenhuma descoberta em runtime autorizada.**

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

O Observatório atual usa exclusivamente `host.agentServer.request({method:'GET',path:'/api/conversations/'+uuid})` sob clique explícito. A validação confere `item.id` e `execution_status`; o projeto é declarado pelo operador e `local-view-not-tenant` **não** é autenticação. A PR #56 incorporou testes de erro e regressão DOM, sem acesso transversal.

| Superfície identificada em documentação upstream | Resposta/recursos documentados | Proveniência/autoridade efetivamente provada neste Canvas | Decisão |
|---|---|---|---|
| OpenHands **Cloud/App Server V1**: `GET /api/v1/app-conversations/search?limit=20` | `items[]`, `next_page_id`, `id`, `execution_status`, `selected_repository`; documentação exemplifica bearer token | **Não provada**: App Server não é necessariamente o Agent Server do `host`, nem `selected_repository` representa autorização multiprojeto | CANDIDATO, não chamar |
| OpenHands **Cloud legado**: `GET /api/conversations` | `results[]`, `next_page_id`, `conversation_id`; inclui campos sensíveis como `session_api_key` | Não provada; contrato distinto do V1, potencial exposição de dados; endpoint V0 documentado como deprecado | NÃO UTILIZAR para descoberta |
| OpenHands **Agent Server SDK**: rotas de conversas e /search no serviço próprio | API de Agent Server é separada, pode depender de `X-Session-API-Key` | Não prova existência/alcance de rota de listagem via `host.agentServer.request` no Canvas | INVESTIGAR SDK/host sem chamada real |
| Canvas `host.agentServer.request` atual, `GET /api/conversations/{uuid}` | Consulta individual de estado e timestamp; comportamento real previamente observado para UUID explícito | Ponto existente reutilizável, mas não lista nem estabelece vínculo autenticado projeto/agent | PRESERVAR, sem novo código de rede |
| Catálogo de **agentes** / agent identity / projeto → conversa | Nenhum endpoint e esquema de identidade/relacionamento comprovado nesta pesquisa | **NÃO PROVADO** | Não criar nós AGENTE comprovados |

Fontes upstream públicas (consultadas 2026-10-12):
- https://github.com/OpenHands/docs/blob/main/openhands/usage/cloud/cloud-api.mdx
- https://docs.openhands.dev/api-reference/search-conversations
- https://github.com/OpenHands/docs/blob/main/sdk/arch/agent-server.mdx
- https://github.com/OpenHands/extensions/blob/main/skills/openhands-api/SKILL.md

**Importante:** documentação oficial de uma instalação/versão não atesta compatibilidade, permissões ou roteamento da instalação Canvas específica. A documentação V1 apresenta `items`; a documentação V0 apresenta `results`. Nunca combinar esses contratos por suposição.

## Contrato mínimo de futura descoberta (proposto, não ativado)

- **Fonte:** `host`/SDK oficial comprovado com identidade e escopo; proibir browser fetch arbitrário, cookies, tokens e BFF paralelo.
- **Método:** somente GET via interface autorizada; sem auto-polling, POST, GET transversal ou enumeração por UUID.
- **Escopo:** exigir autorização autenticada e demonstrável de repositório/projeto antes de exibir ou agregar conversas. `selected_repository` em uma resposta não substitui prova de autorização.
- **Paginação:** `items` de V1 e `next_page_id` somente após compatibilidade estabelecida; limitar páginas e cardinalidade; tokens nunca persistidos ou exibidos.
- **Saída minimizada:** IDs e estados apenas quando autorizados e validados; não transportar `title`, `session_api_key`, URLs privadas, tokens, prompts ou conteúdos de conversas.
- **Fail closed:** 401/403, resposta malformada, projeto não atestado, falha parcial, paginação inesperada ou deriva de schema ⇒ não promover como dados comprovados.
- **Agentes:** inferência conversa→agente proibida até contrato oficial de identidade agente/associação comprovado.
- **Testes:** somente fixtures negativas separadas por tenant, paginação inválida, duplicidade e campos sensíveis; nenhum GET real.

## Gate de reutilização e decisão

**CYCLE011-B-1: GO apenas para pesquisa e testes offline. NO-GO para integração de descoberta.**
Antes de implementar UI/listagem real, obter: (1) contrato documentado da versão SDK/host efetiva; (2) prova de autorização servidor para múltiplos projetos; (3) escopo mínimo e política de paginação; (4) avaliação de riscos. Não confundir G11/G12 com esta trilha de produto: G11 não comprovado, G12 bloqueado, P02 não provado. Sem merge/deploy/Canvas automático.
