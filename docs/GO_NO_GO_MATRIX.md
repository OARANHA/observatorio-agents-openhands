# OBSERVATÓRIO DE AGENTES — Matriz de prontidão GO/NO-GO

**Data de referência:** 2026-10-11  
**Repositório:** https://github.com/OARANHA/observatorio-agents-openhands  
**Main verificada:** `ba38f1a0dd29110c0b1dbbc7c0c0c51a07887510`  
**Fontes de autoridade:** `docs/PROJECT_SOURCE.md` → `AGENTS.md` → ADRs (ADR-0001: **Proposto**) → `docs/CANONICAL_STATE.md` → `MEMORY.md` → `docs/ARCHITECTURE.md` → código/CI.  
**Decisão atual:** **NO-GO operacional**.

## Legenda

- **PROVADO OFFLINE:** testes com stubs/simulações, sem demonstrar funcionamento operacional.
- **PARCIAL:** alguma prova ou código, mas faltam condições cumulativas.
- **NÃO PROVADO:** falta evidência pertinente.
- **BLOQUEADO:** iniciar somente depois de gates e autorização específica.

## Matriz

| ID | Gate | Estado | Evidência | Critério de aceitação que falta | Próximo trabalho seguro |
|---|---|---|---|---|---|
| G01 | Fonte canônica / GitHub | PROVADO | PRs #19–#22 integradas e dois workflows verdes no HEAD exato; main verificada | Preservar rastreabilidade de SHAs, decisões e provas em cada etapa | Matriz versionada e handoff |
| G02 | Compatibilidade SDK 1.53.0 | PROVADO OFFLINE | Testes na distribuição SDK real em runner efêmero, auditoria AST de sinks | Detectar drift de versão, aliases e entrypoints não inventariados | Inventário de rotas + testes anti-drift |
| G03 | Reservas e cálculo sintéticos | PROVADO OFFLINE | `BudgetBook`, `Guard`, `Decimal`, fechamento e reserva incerta, PRs #18–#22 | Casos extremos financeiros, concorrência e falsificação adicionais | Testes adversariais determinísticos |
| G04 | Identidade e integridade de métricas | PROVADO OFFLINE | Baseline por chamada, replay negado, binding de SDK e prova JSON sintética | Telemetria parcial, snapshots malformados e replay cruzado | Testes negativos |
| G05 | Isolamento de rede e arquivos | PARCIAL | `bwrap --unshare-all` no GitHub runner; namespace separado, sem interfaces externas | Evidência de negação DNS/TCP, escrita, leitura externa, vazamento de FDs/segredos, descendentes; validar ambiente futuro | Suite isolada de testes negativos |
| G06 | Egress interno / retries / streaming | PARCIAL | Quatro aliases LiteLLM e fallback/refresh induzidos testados | Inventário e negação de streaming, metadata HTTP, threads, retries ocultos e outros destinos | Auditoria estática + mocks adversariais |
| G07 | Worker e supervisor completos | PARCIAL | Worker inerte, TaskToolSet, terminal restrito e supervisor básico | Ciclo pai/filho completo simulado, herança de Guard/confirm/terminal, kill process-group e cleanup | Harness de integração 100% inerte |
| G08 | Modelo e tarifas verificadas | NÃO PROVADO | Tarifas usadas até aqui são sintéticas | Fontes oficiais vigentes, modelo/rota, preços cache/extras e limites efetivos | Dossiê público somente leitura |
| G09 | Credencial e quota segregadas | NÃO PROVADO | Nenhuma credencial operacional usada | Identidade isolada, teto real de conta/provedor, provisioning autorizado e revogação | Plano sem credenciais |
| G10 | Evidência auditável operacional | PARCIAL | `obs.synthetic.accounting.v1` minimizado, `operational_go=false` | Proveniência/autorização confiável, ID único, tempo, hashes, retenção, antifraude e redaction | Esquema offline + testes anti-vazamento |
| G11 | Revisão independente | NÃO PROVADO | PRs #19–#22 têm **autorrevisões automatizadas**, não revisão independente | Revisor distinto e aceite de riscos remanescentes antes de canário real | Pacote de revisão independente |
| G12 | Primeiro canário LLM real | BLOQUEADO | Nenhum LLM real, agente real ou despachos reais | Gates críticos concluídos + missão congelada + autorização explícita separada | Preparar plano, nunca executar |
| P01 | Grafo visual | PARCIAL | PR #7 ainda aberta; versão instalada v0.4.2 faz leitura pontual e mistura cenários DEMO identificados | Revisão isolada #7, proveniência verificável e compatibilidade com Canvas | Testes de contrato/UX com fixtures |
| P02 | RBAC e vínculos multiprojeto | NÃO PROVADO | UUID de conversa não comprova agente ou vínculo autenticado com projeto | Identidade, autorização por projeto e contrato read-only testados | Design + mocks multi-tenant |
| P03 | Memória persistente | NÃO PROVADO | Switch habilitado em UI, sem prova de gravação/leitura/segregação | Teste sintético autorizado na superfície adequada | Plano e fixtures, sem ativação real |

## Critério cumulativo de GO operacional

**NÃO** alterar para GO apenas porque os testes sintéticos estão verdes. G05, G06, G07, G08, G09, G10 e G11 devem estar comprovados no **ambiente autorizado de execução real**, e G12 exige autorização humana expressa para a missão congelada, inclusive modelo, rota, credencial, custo, limite de ações, parada, retenção e rollback. P01–P03 são trilha separada do produto visual: não impedem preparar os testes de SDK, mas não são capacidades já implantadas.

## Trilhas seguras para o Work

1. Versionar a matriz, criar índice de evidências e checklist com responsáveis.
2. Testes negativos de isolamento/egress no runner efêmero; nunca na VPS sem aprovação.
3. Mapear os caminhos internos do SDK 1.53.0: aliases, streaming, retries, refresh, metadata, threads, cache, tool calls; testes sintéticos fail-closed.
4. Fortalecer Decimal/float, uso parcial, cache, custos extras, falhas de telemetria, orçamento preventivo e concorrência sintética.
5. Criar harness inerte do ciclo completo TaskManager/TaskToolSet com supervisor e sem LLM/Agent/Conversation operacionais.
6. Propor evidências minimizadas versionadas e testes de vazamento (tokens, prompts, IDs privados, ambiente).
7. Pesquisar **apenas** fontes oficiais públicas de preços e caps, com URL e data; não acessar contas nem selecionar credenciais.
8. Avaliar PR #7 separadamente, sem merge automático e sem deploy do Canvas; desenhar contratos read-only RBAC com mocks.
9. Entregar matriz atualizada + relatório executivo: evidência por gate, riscos residuais, PR/HEAD/CI, itens que exigem ação humana.

## Governança de execução

- Primeiro confirmar estado real (`main`, PRs, branches, documentos e ADRs); trabalhar apenas no repositório do Observatório em branches/PRs pequenas.
- Reutilizar recursos do SDK e OpenHands; não copiar ou alterar OpenHands Core.
- Testes RED→GREEN; duas CIs no **HEAD exato** e logs inspecionados; evitar polling contínuo de CI. Não reduzir gates para obter GREEN.
- Documentar status factuais; **autorrevisão automatizada NÃO é revisão independente**.
- Sem provedores ou LLM reais, sem agentes reais, sem deploy, sem VPS/Docker/Canvas instalado, sem outros projetos, sem credenciais e sem despesas externas autorizadas.
- O ciclo de autorização de merges #19–#22 está encerrado. **Qualquer novo lote de merges necessita autorização expressa adicional**; o Work pode receber essa autorização em uma mensagem específica do usuário, com limites e critérios claros.
- Se uma frente travar, continuar as independentes e deixar o bloqueio documentado.

## Evidências consultadas

- PRs #19–#22, registros dos workflows, SHA de `main`; PR #7 aberta.
- `docs/handoffs/OBS-EXPLORER-CANARY-GATES-001.md`.
- `docs/handoffs/OBS-EXPLORER-CANARY-PLAN-001.md`.
- `docs/handoffs/OBS-EXPLORER-OFFLINE-EVIDENCE-001.md`.
- `scripts/canary_budget.py`, `scripts/canary_controls.py`, `scripts/canary_transport_probe.py`, `scripts/canary_sdk_success_probe.py`, `scripts/canary_accounting_evidence.py`, `scripts/probe_canary_worker.py`.

## Reconciliação versionada — ciclo noturno, 2026-10-11

Origem: OBSERVATORIO_MATRIZ_GO_NO_GO_2026-10-11.md, anexo do proprietário,
7655 bytes declarados. Matriz acima preservada como baseline; a linha sobre
nova autorização é histórica: a missão noturna autoriza até oito PRs offline
e merges somente sob os sete critérios cumulativos definidos pelo proprietário.
Nenhuma autorização operacional foi concedida.

REAL NOW: main ba38f1a0dd29110c0b1dbbc7c0c0c51a07887510 confirmada por Git;
PR #7 aberta/draft, HEAD 48f898d99a8979ef2c794513131506b028772666, sem merge.
PR #10 aberta, HEAD f52b635290ba9e542e2bbb01a9d5a657fed11452;
PR #11 integrada. Todos os handoffs existentes foram preservados.

PROVEN EVIDENCE: metadados GitHub reconfirmados nesta retomada:

| PR | HEAD exato | Merge | CI Observatorio | Canary Worker Inert SDK |
|---|---|---|---|---|
| [19](https://github.com/OARANHA/observatorio-agents-openhands/pull/19) | 925ff17ebac7c64d6c847b3e80bbdf5fec8837e3 | 91f8bedb347985beddda9320b3db83d95cbfdce7 | [38117751430](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38117751430) | [38117751606](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38117751606) |
| [20](https://github.com/OARANHA/observatorio-agents-openhands/pull/20) | 370600016b1bfae565a8b45a6ab389c413c10527 | 2e17e05804d3f2561f5fdc5b2506a870ffe881e3 | [38118001929](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38118001929) | [38118001931](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38118001931) |
| [21](https://github.com/OARANHA/observatorio-agents-openhands/pull/21) | 69c02bffa66bd066387b65243e5d8518bcc4b10a | 732351094565da35159943212782c71941784f64 | [38118252923](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38118252923) | [38118252958](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38118252958) |
| [22](https://github.com/OARANHA/observatorio-agents-openhands/pull/22) | ebb6b3fdd66be2382dca3117d10eb229bb56a338 | ba38f1a0dd29110c0b1dbbc7c0c0c51a07887510 | [38118729307](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38118729307) | [38118729256](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38118729256) |

Oito runs completed/success; autorrevisões automatizadas, sem revisão independente.
G01 é prova de estado GitHub, não prova operacional. Demais status da matriz
permanecem iguais nesta primeira versão. Cada incremento deve registrar teste,
fonte, SHA e limites; uma evidência ausente nunca vira PASS por declaração.

GAPS: todos os critérios operacionais G05–G12 permanecem pendentes;
não é possível validar isolamento futuro na VPS/Canvas sem autorização.
REUSE GATE: reutilizar BudgetBook, Guard, supervisor, SDK oficial e workflows.
DECISION: avançar testes inertes; decisão final operacional permanece NO-GO.

Responsáveis: Work produz provas offline e autorrevisão; proprietário escolhe
modelo/rota/conta e autoriza missão congelada; revisor distinto avalia riscos
operacionais. Nenhum responsável substitui permissões reais da plataforma.
Um merge offline exige ambos workflows GREEN no HEAD exato, inspeção de logs,
revisão registrada, ausência de conflitos, proteção preservada e lease de SHA.
Os registros das novas PRs são anexados ao handoff do ciclo após confirmação.


### G05 — provas propostas neste incremento

Teste: scripts/probe_canary_sandbox.py, dez probes obrigatórios. O executor
real/supervisor existente é reutilizado; só o harness de prova substitui
argv final por Python. DNS usa domínio .invalid; TCP e Unix tentam somente
listeners sintéticos locais. Marcadores de ambiente/arquivo são fictícios.
CI ainda por comprovar; G05 continua PARCIAL, sem validação do ambiente futuro.
Limites: não testa evasão do kernel, processos hostis que criam nova sessão
fora do PID namespace, canais pela própria stdout ou isolamento multi-tenant.
A prova SDK que monta / inteiro RO continua sendo apenas isolamento de rede
de um runner sem credenciais de produção; não é o filesystem mínimo do terminal.


### G02/G06 — inventário nominal de SDK/Tools 1.53.0

| Caminho oficial instalado | Superfície | Prova e limite |
|---|---|---|
| llm/llm.py completion/acompletion | _transport_call/_atransport_call → aliases LiteLLM | AST, quatro rotas stubadas; sem prova de todos requests internos |
| llm/llm.py responses/aresponses | aliases Responses, fluxo stream | baseline sintético nega stream; não há streaming operacional homologado |
| llm/utils/retry_mixin.py | Tenacity, num_retries e before_sleep | num_retries=0 e segunda tentativa negada no sink; transporte de dependência fora do gate continua gap |
| llm/llm.py _handle_error/_ahandle_error | fallback_strategy, inclusive thread no async | atributo negado no preflight; owner de thread/task exige mesma execução |
| llm/llm.py _resolve_refreshed_api_key/_auth_refreshed_llm | refresh 401 tenta novamente | hook negado nominalmente; teste real com stubs nega segunda tentativa |
| llm/llm.py resolve_runtime_metadata/aresolve_runtime_metadata | cache positivo/negativo e HTTP auxiliar | AST inventaria nomes; nenhum catálogo remoto consultado |
| llm/streaming.py | chunks e métricas agregadas | apenas inventário; stream permanece não homologado |

A auditoria não executa SDK LLM e não certifica ausência de imports dinâmicos,
plugins, redirects ou tráfego LiteLLM/httpx. Funções novas exigem revisão.
Aliases desconhecidos eram aceitos no baseline: RED → negação. Getter/setter
is_subscription da distribuição oficial não é duplicação de método; teste
positivo protege compatibilidade. G06 continua PARCIAL operacionalmente.
