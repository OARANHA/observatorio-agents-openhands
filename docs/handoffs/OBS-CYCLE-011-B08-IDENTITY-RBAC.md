# ADM-CYCLE011B-08 — Identidade e RBAC multiprojeto (estático / offline)

Data: 2026-10-12. Base main `d9818126fe4b7ed463de1434558c38a03f5e9dfb`.
**Decisão: NO-GO descoberta multiprojeto.** Nenhuma API real consultada.

## Evidências de código público OpenHands

1. Agent Server `openhands-agent-server/openhands/agent_server/dependencies.py`: `check_session_api_key` lê `config.session_api_keys` e, **quando há chaves configuradas**, rejeita chave ausente/incorreta via HTTP 401. A função não implementa verificação por repositório ou tenant. Quando a configuração está vazia, essa verificação não rejeita a requisição com base na chave; não inferir segurança ou configuração do Canvas instalado.
2. `check_workspace_session` aceita header ou cookie `oh_workspace_session_key` somente para rotas de arquivos do workspace. O comentário no upstream explicita que cookie **não** é honrado pelas demais APIs. Nunca usar cookie de workspace como prova de autorização de conversa.
3. `auth_router.py` define emissão de cookie workspace via POST autenticado, reservado a arquivos incorporados. Essa capacidade é fora do escopo; nenhuma chamada, criação ou leitura de cookie foi feita.
4. `conversation_router.py` dispõe de `/search` e `/{conversation_id}`, com serviço `get_conversation_service`. A existência da rota **não comprova** filtro RBAC por projeto, escopo de operador ou versão instalada do Canvas.
5. `selected_repository` existe em modelos/SDK upstream, mas é **metadado de conversa**, não um atestado criptográfico nem decisão de autorização.

Fontes upstream (código público inspecionado em 2026-10-12):
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/dependencies.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/auth_router.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/conversation_router.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/clients/typescript/src/models/api.ts

## Modelo de ameaça e exigência futura

| Cenário | Risco | Regra proposta |
|---|---|---|
| UUID de conversa recuperável | Leitura cruzada não comprovadamente negada | Prova de decisão de autorização pelo servidor por conversa, não pelo cliente |
| Chave de sessão válida | Acesso ao serviço não equivale a role/tenant | Não promover a ACL de projeto |
| `selected_repository` igual ao projeto selecionado | Confusão entre classificação e autorização | Tratar como informação, não autorização |
| Cookie de arquivo do workspace | Escopo de autenticação distinto | Nunca tratar como credencial da API de listagem |
| Busca paginada | Possível inventário interprojeto | Não executar; bloquear até prova de escopo e paginação |
| Conversa com estado `finished` | Confusão com agente e sucesso | Não inferir execução bem-sucedida nem identidade de agente |

## Decisão de arquitetura

Reutilizar somente uma superfície oficial comprovadamente autorizada para a instalação efetiva, quando houver autorização separada. Não criar BFF, endpoints, polling, descoberta real ou mudanças no Canvas. G11 NÃO PROVADO; G12 BLOQUEADO; P02 NÃO PROVADO. Testes que acompanham este documento são **modelos de decisão sintéticos**, não testes da API real ou prova de RBAC.
