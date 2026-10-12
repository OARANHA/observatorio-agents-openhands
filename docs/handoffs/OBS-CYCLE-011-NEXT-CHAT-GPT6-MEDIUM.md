# Prompt de retomada — CYCLE011-A (GPT-6, raciocínio médio)

**Cole esta missão em um novo chat GPT-6 com raciocínio médio. Conecte GitHub, `wmemory-universal` e `superpowers` quando disponíveis.** Este arquivo é um roteiro, NÃO é evidência de estado atual nem autorização operacional.

> MISSÃO: você é arquiteto e pesquisador técnico do projeto horizontal **Observatório de Agentes**, não do VIGIAFAST. Investigue fontes oficiais do OpenHands, inventarie contratos permitidos de leitura e prepare um próximo slice mínimo de dados comprováveis, reutilizando a extensão atual. Execute somente atividades offline nesta fase.

## Fontes obrigatórias e hierarquia

1. Conector GitHub: `https://github.com/OARANHA/observatorio-agents-openhands`.
2. Skill `wmemory-universal/agent-memory-repo`: verificar que `OARANHA/wmemory` permanece privado; ler `MEMORY.md`, `OPERATING_RULES.md` e **somente** `projects/observatorio-agents-openhands.md`. Memória não supera a autoridade local.
3. Skills Superpowers: `using-superpowers`, `brainstorming` (determinar spike/bounded/architectural e cumprir gate), `verification-before-completion`; `test-driven-development` e `writing-plans` **somente depois de aprovação de design e quando efetivamente implementar**.
4. Ler **nesta ordem**: `docs/PROJECT_SOURCE.md` → `AGENTS.md` → ADRs de `docs/decisions/` (com status) → `docs/CANONICAL_STATE.md` → `MEMORY.md` → `docs/ARCHITECTURE.md` → `README.md` → `docs/GO_NO_GO_MATRIX.md` → `docs/handoffs/OBS-CYCLE-011-OPENHANDS-READONLY-PROVENANCE.md` → código/testes/GitHub/CI.
5. Revalidar `main`, PRs/HEADs/estado de merge/workflows; não confiar em SHAs aqui como atualidade.

## Histórico útil a reconfirmar

- Última `main` **confirmada quando este prompt foi preparado**: `ec9f061469d0376e17c687b4b191a40478e557ee` (PR #54 merged); manifesto V0.5.3.
- A CI do HEAD da PR #54 `86a454d6485cdaf9a8ba0ba1fb9f9a972fbdf668` passou: Observatório #38192037359, Chromium 25/25 #38192037357, SDK inerte #38192037325.
- O proprietário mostrou a tela **Grafo** V0.5.3 corrigida e disse “está ok”. Não inferir ref instalada pela tela de Apps, RBAC, H3, telemetria ou homologação operacional.
- PRs #49–#52 ainda OPEN/DRAFT durante a última reconciliação, sem merge na main visual.
- Contrato já existente em `scripts/extension-template.txt`: `host.agentServer.request({method:'GET',path:'/api/conversations/'+id})`, acionado manualmente por UUID; aceitação restrita a `item.id === id`, `execution_status` string, `updated_at` opcional; `observedAt` é horário local; `project` digitado pelo operador não é vínculo autenticado.
- `graphIdentityForObservation` usa IDs temporários WebCrypto (`local-view-not-tenant`), não autenticação/tenant. `finished` não comprova sucesso de tarefa; conversa não comprova agente. Quatro sistemas continuam DEMO. Não inventar listas de missões ou agentes.

## Objetivo do ciclo — somente investigação offline e documentação

Produzir uma **matriz verificável de capacidades de leitura** do OpenHands compatíveis com o Canvas/Agent Server no contexto do projeto, sem GET real:
- localizar implementações/contratos oficiais, versões e métodos; distinguir provado no repositório local, confirmado por fonte upstream, hipótese e desconhecido;
- para cada campo: entidade, origem, endpoint/método comprovado (se houver), autenticação e identidade necessárias, escopo de permissão demonstrado/não demonstrado, sensibilidade, timestamps, confiabilidade, classificação `DEMO|CONSULTADO|MANUAL|INFERIDO|DESCONHECIDO`, exibição segura e testes;
- determinar se há dados **documentados e autorizáveis** sobre conversa, tarefa, agente, projeto/repositório e arestas de grafo; onde inexistentes, registrar **NÃO PROVADO**, não fazer inferências;
- inspecionar diffs relevantes e identificar menor slice de **reuso** de contrato pontual já presente; não criar novo BFF, coletor, API paralela ou orquestrador;
- modelar falhas 401/403, 404, timeout/response tardia, shape divergente, replay, dados privados, cross-project, XSS e permissões, sempre com fixtures offline;
- distinguir atualização da UI de dados falsos, eventos reais e chamadas que iniciem execução; proibir `POST`, `WebSocket`, streaming, polling, scraping, token/cookie/fetch externo;
- criar um **esboço de desenho** e recomendação com alternativas/custos e um plano TDD com arquivos e critérios mínimos, **parando para aprovação de desenho antes de implementar novo comportamento** se a habilidade Superpowers exigir.

## Restrições inegociáveis

**NO-GO operacional**: sem chamar o OpenHands autenticado, GET H3, outros endpoints reais, descoberta em produção, registro/despacho de agentes, LLM/provedor, tokens, projetos privados, alteração do Canvas, deploy/VPS/Docker, OpenHands Core, outro repo, custo ou merge indiscriminado. O histórico do GET sintético não autoriza novos GETs. Não confundir READ-ONLY com permissão para acessar dados pessoais. Sem polling contínuo de CI; proprietário informará GREEN/RED. Nenhum merge sem autorização específica, sem revisão e sem CI no HEAD certo. `G11 NÃO PROVADO; G12 BLOQUEADO; P02/P03 NÃO PROVADOS`.

## Entregáveis esperados

1. **REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION**, com SHAs reais, proveniência dos contratos e limites.
2. Inventário e matriz de confiança com status explicável a gestor não técnico, focado em português brasileiro.
3. Proposta do menor slice offline, testes negativos, critérios de aceite e dependências que demandam nova autorização.
4. Handoff/documentação viva em branch e PR **Draft**, respeitando autoria/conflitos; atualização do `OARANHA/wmemory` privado somente com fatos verificados e SHA condicional. Não tocar nos demais projetos.
5. Final: link da PR, HEAD, arquivos, comandos/testes **efetivamente** executados, alterações não executadas, riscos, próximos gates e pergunta objetiva para aprovação do desenho, se necessária.

Aguarde nova autorização antes de H3, aplicação no Canvas ou qualquer canário real. **Não recomece trabalho já existente.**
