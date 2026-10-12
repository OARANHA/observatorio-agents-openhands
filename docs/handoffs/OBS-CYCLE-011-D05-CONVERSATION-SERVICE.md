# ADM-CYCLE011D-05 — ConversationService, armazenamento e autorização (offline)

Data: 2026-10-12. Base main `18745a8ee780551d114b8a5008c321c815e69c97`. Sem API real, deploy, Canvas ou merge.

## Código público inspecionado

- `OpenHands/software-agent-sdk/openhands-agent-server/openhands/agent_server/conversation_service.py`: `ConversationService` mantém `_conversation_records: dict[UUID, _ConversationRecord]` e `_event_services`; o catálogo lê `meta.json` de diretórios de conversas e, quando presente, estado de execução persistido.
- `search_conversations` chama `_search_conversations(page_id, limit, execution_status, sort_order)`; no corpo examinado, `_search_conversations` percorre `self._conversation_records.items()`, filtra estado, ordena por `created_at`/`updated_at` e pagina por cursor de UUID. **Nos parâmetros e na passagem examinados, não há identidade do usuário, tenant ou autorização de projeto.**
- `get_conversation(conversation_id)` consulta `_conversation_records` ou `_event_services` por UUID, sem argumento explícito de sujeito/tenant.
- `delete_conversation(conversation_id)` opera sobre registro/serviço por UUID, sem argumento explícito de sujeito/tenant. Isto **não** autoriza testar DELETE.
- `conversation_router.py`: handlers públicos da busca, GET pontual e DELETE delegam esses métodos a `ConversationService`. `api.py` tem autenticação de sessão comum; não é prova de controle por recurso.

Fonte upstream: https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/conversation_service.py

## Limites e ameaças

A evidência é **estática**, do código público consultado; não abrange políticas de proxy, configuração, isolamento de processos, wrapper/cloud service, plugins ou versão instalada. A ausência de parâmetros de tenant nesses métodos **não demonstra falta universal de isolamento**, mas impede declarar RBAC multiprojeto comprovado.

O catálogo pode conter diversas conversas dentro do mesmo armazenamento do serviço; `selected_repository` continua sendo metadado, não ACL. Risco: enumerar IDs, lista paginada e GET/DELETE de conversa sem evidência de permissão por recurso. Não executar nenhum desses casos em rede.

`tests/cycle011_d05_service_contract.test.mjs` mantém uma **fixture estrutural do algoritmo observado**, com casos offline de busca/ordenação/cursor e demonstração de que a fixture não tem identidade nem filtro de tenant. Ela não executa o código Python upstream nem constitui prova de vulnerabilidade ou RBAC no servidor instalado. Uma validação por código Python real em versão fixada será objetivo separado.

## Decisão

**NO-GO para descoberta e leitura multiprojeto.** Antes de operacionalizar: pin exato da versão instalada, política servidor por recurso, isolamento do catálogo, testes de negação entre projetos/revogação e gate humano de revisão independente.

**G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO.**

## ADM-CYCLE011D-06 — revisão adversarial da fixture e CI (2026-10-12)

- **HEAD avaliado:** `ec73f1ebc4ee9cf7197c101ed862247d6e7b4b91`. CI Observatório run `38216281989` **SUCCESS**; Canary Worker Inert SDK run `38216281822` **SUCCESS**. Job `contract` confirmou `CYCLE011-D05 contrato estrutural ConversationService (offline)` como SUCCESS.
- Comparação nova com `_search_conversations` upstream: a fixture JS reproduz somente parte de filtragem por estado, ordenação descendente por `created_at` e cursor por UUID. Não implementa `_reconcile_active_records`, `_refresh_execution_statuses`, ordenação alternativa `updated_at`, nem `_conversation_info` que pode retornar `None` e alterar o preenchimento da página. Logo, **não há equivalência completa com a execução Python**.
- A fixture deliberadamente recebe registros sintéticos dos projetos alpha/beta e não possui contexto autenticado. A exibição de itens de ambos os projetos prova somente o comportamento do **modelo sintético**; não prova vazamento do sistema instalado. Metadados de projeto na fixture não são prova de que o armazenamento real os possua no mesmo formato.
- O JEV.1 `jev_review_completion` classificou a conclusão de autorização real como `incomplete` (probabilidade 1,00, confiança 1,00), parecer consultivo. A CI GREEN não contradiz esse resultado: ela atesta apenas execução e aprovação dos testes offline.
- **Decisão adversarial:** evidência suficiente para documentar hipóteses de risco e lacunas, **insuficiente para comprovar RBAC, ACL ou revogação operacional**. Antes de ampliar os testes, fixar revisão de commit upstream e isolar as responsabilidades de cada camada. Manter `G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO · NO-GO operacional`.
- Este registro cria um **novo HEAD**; os workflows citados acima não validam automaticamente esse novo commit. Sem merge, GET real, operações destrutivas ou deploy.
