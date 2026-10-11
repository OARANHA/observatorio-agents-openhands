# OBSERVATÓRIO DE AGENTES — Matriz de prontidão GO/NO-GO

**Data de referência:** 2026-10-11
**Repositório:** https://github.com/OARANHA/observatorio-agents-openhands
**Main verificada antes do fechamento 003:** `4c0f5f0f7559bbe8b2ab7476387fbe700894de9c` (histórico e SHA do próprio fechamento: handoff/PR).
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


### G03/G04 — expansão financeira sintética

Novas provas em tests/test_canary_accounting_hardening.py: custo sem tokens,
ledger corrompido antes/depois do transporte, reservas concorrentes e métricas
parciais. Reutiliza exatidão Decimal e hold sem refund; nenhuma tolerância
para float introduzida. Estado ainda PROVADO OFFLINE, sem tarifa/fatura real.
Achado adicional C: utils/model_info.py faz HTTP GET de proxy /v1/model/info;
utils/runtime_metadata.py cria task por loop/rota e resolver OpenRouter usa
httpx Client/AsyncClient. Esses destinos não são os quatro sinks; precisariam
de bloqueio de rede independente no worker futuro. Nada foi solicitado à API.


### G07/G10 — ciclo e saída supervisionados

TaskManager oficial + conversa mockada exercitam confirmação/Guard/Book/
terminal e encerramento. Supervisor real e killpg continuam nas dez provas
separadas de sandbox. A saída do worker é allowlist de nomes e valores
factuais fixos; extra payload e counters bool são recusados. Nunca serializar
objeto LLM, ambiente, prompt privado, exceção ou nome de cliente.
G07 continua PARCIAL: prova integrada sintética não cria filho operacional,
não registra code-explorer e não prova herança em delegação real.


### G10 — envelope sintético v1 (2026-10-11)

Contrato em [SYNTHETIC_EVIDENCE_SCHEMA.md](SYNTHETIC_EVIDENCE_SCHEMA.md):
campos fechados, hash de integridade e SHA declarado, sem autenticidade
independente ou anti-replay. Oito negativas/roundtrips offline. G10 PARCIAL;
G11 NÃO PROVADO. Nunca constitui autorização para canário real.


## Matriz ao fechar os incrementos A–H (2026-10-11)

Main de referência pré-PR documental: b95ea8c44f9fe95ee24fdec6e32c2bea00c8451a.
Baseline do anexo preservada acima; abaixo prevalece o estado atualizado.

| Gate | Antes | Depois e prova | Aceite ainda ausente |
|---|---|---|---|
| G01 | PROVADO | PROVADO: #23–#28, SHAs e runs no handoff noturno | Manter rastreabilidade de cada HEAD |
| G02 | PROVADO OFFLINE | Igual: 12 testes AST, 2 de superfície, SDK/Tools 1.53.0 | Drift transitivo/dinâmico fora do inventário |
| G03/G04 | PROVADO OFFLINE | Igual, mais fortes: 29 testes financeiros e hold incerto/concorrência/métricas parciais | Tarifas, tokenização, métrica e faturamento reais |
| G05 | PARCIAL | PARCIAL: dez probes DNS/TCP/Unix/RO/FD/env/descendentes/killpg GREEN no runner efêmero | Mesmo isolamento no ambiente futuro; kernel/canais/ameaças residuais |
| G06 | PARCIAL | PARCIAL: aliases novos recusados; stream/cache/fallback/refresh/extras negados nominalmente | Toda rota auxiliar/dependência/metadata HTTP e processo isolado futuro |
| G07 | PARCIAL | PARCIAL: 6 testes TaskManager oficial, ciclo mockado e contrato de saída fechado | Herança e cancelamento num único filho operacional, sem autorizar execução agora |
| G08 | NÃO PROVADO | PARCIAL DOCUMENTAL: modelos, preços e ressalvas oficiais datados | Modelo/snapshot/rota atual disponível, cap e orçamento efetivos; não selecionados |
| G09 | NÃO PROVADO | Igual: nenhuma conta ou credencial consultada | Identidade não produtiva, segregação, quotas e revogação autorizadas |
| G10 | PARCIAL | PARCIAL: envelope v1/8 testes, hash e SHA declarado, payload fechado | Assinatura/proveniência confiável, consumidor/anti-replay/retenção/redaction operacional |
| G11 | NÃO PROVADO | Igual: somente autorrevisões automatizadas identificadas | Revisor distinto e aceite de riscos |
| G12 | BLOQUEADO | Igual: zero LLM, registros/dispatches operacionais | Todos gates pertinentes e autorização separada para missão congelada |
| P01 | PARCIAL | Igual: #7 revisada estaticamente e mantida aberta/draft | DOM/visual/Canvas autorizado, CI e aprovação específica |
| P02/P03 | NÃO PROVADO | Igual: identidade/RBAC/memória sem prova operacional | Contratos segregados e validação pertinente |

Fontes: [handoff noturno](handoffs/OBS-NIGHT-OFFLINE-001.md),
[dossiê público](PUBLIC_PROVIDER_DOSSIER.md), [revisão #7](GRAPH_PR7_REVIEW.md),
[esquema sintético](SYNTHETIC_EVIDENCE_SCHEMA.md). Autoridade noturna permite
merges estritamente offline; não substitui a autorização específica de G12.
Nenhum GREEN deste ciclo muda a decisão operacional **NO-GO**.

Inventário de fontes/hashes e dependências: [SDK_TRANSPORT_INVENTORY.md](SDK_TRANSPORT_INVENTORY.md).


## Novo ciclo de engenharia offline — 2026-10-11

REAL NOW: main b0ce4333d8c5e4ce22e32f3ebc1aeba7d08c838f confirmada.
GitHub agora confirma PR #10 CLOSED, merged=false, closed_at 04:11:36Z,
HEAD f52b635290ba9e542e2bbb01a9d5a657fed11452. Notas anteriores sobre aberta
são históricas e superadas; PLAN-001 preservado. #7 aberta/draft HEAD
48f898d99a8979ef2c794513131506b028772666, excluída de merges.
PROVEN EVIDENCE: supervisor tinha reap sem timeout e erros crus de startup/
cleanup. Sete negativas/lifecycle reproduzem falhas e passam após correção;
reap agora limitado a 1s adicional, sem retries/output parcial/fallback.
GAPS: cleanup falho não prova processo encerrado; SDK _run_task finally é
sequencial, falha de metrics/pause pode pular close e substituir cancellation.
Teste oficial novo é obrigatório em CI; fonte disponível, executável do venv
local indisponível neste ciclo (não reivindicar teste SDK local).
165 testes locais: 143 PASS/22 opcionais SDK skip. NO-GO mantido.
REUSE GATE: Guard/Book/terminal/supervisor oficial e código existente.
DECISION: até seis PRs offline condicionadas aos gates; priorizar lifecycle,
egress auxiliar, auditoria/replay e contratos visuais. Não habilitar worker.
Handoff novo: docs/handoffs/OBS-ENGINEERING-OFFLINE-002.md.


## Egress auxiliares e respostas adiadas — 2026-10-11

PR #30 integrada em 84b48a3198daa8f3191522709eaa6aa4ace363b4, CIs
38144819354 principal, 38144819359 SDK e 38144819350 sandbox GREEN.
Logs SDK comprovam 7 supervisor/7 TaskManager sem skips; cleanup sequencial
oficial falho não reabre Guard, mas pode pular close (risco G07 preservado).
Gate de fakes agora rejeita Iterator/AsyncIterator/awaitable sem consumi-los;
três REDs→GREEN, hold incerto preservado. Novas provas HTTPx/urllib/SDK
model_info em threads/subprocess só serão comprovadas no netns do runner.
171 locais: 146 PASS/25 opcionais SDK skip. AST de fontes SDK disponível
em docs/SDK_AUXILIARY_EGRESS_INVENTORY.md; não certifica dependências.
G05/G06/G07 PARCIAIS. Sem provedor, credencial, registro/delegação. NO-GO.


## Sessão de evidências e pacote de revisão — 2026-10-11

PR #31 integrada f749f5918b86ab0ce6624d220e4354e2e69ef5d2. Runs
38145217813 / 38145217812 GREEN; logs SDK: 15 testes reais com stubs e
HTTP auxiliar/threads/filho e 3 deferred negativos PASS, nenhum provedor.
Consumidor SyntheticEvidenceSession reutiliza envelope v1: cap 1–64, SHA/
janela declarados, UUID/hash replay, tempo/finanças/counters regressivos
negados. Recusa/cap/receipt fechado são terminais. Oito testes: contrato
ausente RED; parada tardia no cap RED corrigida; 179 locais, 154 PASS/25
opcionais SDK skip. CI deste incremento pendente. Pacote em
docs/INDEPENDENT_REVIEW_PACKET.md: ameaças/checklists/conta/limites/revisão,
parada/revogação e autorização única; não provisiona nada. Sem autenticação
fictícia; replay só em memória, perdido no restart. G10 PARCIAL, G11 NÃO
PROVADO e G12 bloqueado. NO-GO operacional mantido.


## Fechamento offline do ciclo de engenharia 002 — 2026-10-11

Main inicial b0ce4333d8c5e4ce22e32f3ebc1aeba7d08c838f; PR #10 fechada
sem merge, handoff preservado. PR #7 permanece draft, HEAD
48f898d99a8979ef2c794513131506b028772666; não integrada ou instalada.
Três incrementos já integrados com SHA esperado, duas CIs e logs:

| PR | HEAD | Merge | CI principal / SDK |
|---|---|---|---|
| #30 | 5b9c8d3f2ed3f7b35496e3887374173260b5ec22 | 84b48a3198daa8f3191522709eaa6aa4ace363b4 | 38144819354 / 38144819359 |
| #31 | 79bac7d57a09cbe21b0c04dc514f9f1bd88842c6 | f749f5918b86ab0ce6624d220e4354e2e69ef5d2 | 38145217813 / 38145217812 |
| #32 | b1d27cc51cac4813bd18f948a473167b2ffb9574 | 70ab4b35a452660f13c9c6e50e38159b1a6c56bf | 38145670004 / 38145670090 |

Todas GREEN; sandbox adicional #30 run38144819350 GREEN. SDK sem skips
relevantes: 15 transport/stubs auxiliares; supervisor 7; TaskManager 7;
sessão sintética 8. Não houve registro/delegação/chamada LLM real.
Quarto incremento independente: fixture congelada de graphModel da #7,
extraída sem alteração e hashes declarados em tests/fixtures/. Seis testes
Node executam o modelo com entradas fictícias, sem DOM, host ou rede.
Preservam DEMO/manual/consultado, não inventam agente/sucesso e demonstram
colisão dos IDs entre vistas. Esse teste PASS caracteriza lacuna aberta,
não prova RBAC. Wrapper Python: RED por reporter Node variável; corrigido
com TAP explícito, sem enfraquecer assertions. Suite local: 180 testes,
155 PASS/25 SDK opcionais skip; mais 6 subtestes Node PASS. Geração e
sintaxe JS e diagnóstico estático válidos, sem ativação. CI deste quarto
incremento ainda pendente no momento desta documentação.

| Gate | Antes → depois | Prova adicional / limite mantido |
|---|---|---|
| G05/G06 | PARCIAL → PARCIAL | HTTP auxiliar negado no netns; inventário AST não cobre todas dependências/dynamic imports |
| G07 | PARCIAL → PARCIAL | kill/reap bounded e cancelamento terminal; cleanup sequencial oficial pode pular close |
| G10 | PARCIAL → PARCIAL | replay/ordem/cap em memória; hash não autentica, restart perde replay |
| G11 | NÃO PROVADO → NÃO PROVADO | pacote independente preparado; autorrevisões não são review independente |
| G12 | BLOQUEADO → BLOQUEADO | autorização específica de missão real ausente |
| P01 | PARCIAL → PARCIAL | contratos do modelo congelado testados; fonte autenticada não foi consultada |
| P02/P03 | NÃO PROVADO → NÃO PROVADO | colisões caracterizadas; DOM/RBAC/contraste/foco não homologados |

Demais gates sem promoção. NO-GO operacional preservado. Ver
docs/INDEPENDENT_REVIEW_PACKET.md para checklist executável offline e
campos da autorização futura: conta segregada, modelo/rota/tarifa/quota,
provisionamento/revogação, limites globais, parada/rollback, janela e
responsável. Nenhuma conta/credencial foi escolhida ou provisionada.
Navegador local indisponível; nenhuma instalação foi tentada. Sem deploy,
Canvas, infraestrutura, provider ou outros projetos. Revisões favoráveis
automáticas são autorrevisões, não certificação humana independente.
Quatro PRs úteis bastam: não criar duas artificiais para atingir seis.


## Estado factual consolidado do ciclo 003

Esta seção prevalece sobre snapshots históricos acima; detalhes/SHAs/runs e desvio procedimental #34 em [handoff](handoffs/OBS-CYCLE-003-CONTINUITY.md).

| Gates | Antes → depois | Evidência e limite |
|---|---|---|
| G01 | PROVADO → PROVADO | Reconciliado GitHub; #34 teve inspeção real de logs após merge, desvio explicitamente retificado |
| G02–G04 | PROVADO OFFLINE → PROVADO OFFLINE | UTC ASCII, contratos financeiros/metrics existentes e SDK 1.53.0 preservados |
| G05/G06 | PARCIAL → PARCIAL | httpcore/aiohttp negados no netns; resubmissão transitive bloqueada pelo Guard; inventário incompleto |
| G07 | PARCIAL → PARCIAL | TaskManager pausa/saída parcial/close falho caracterizados; cleanup/restart ainda têm lacunas |
| G08 | PARCIAL DOCUMENTAL → PARCIAL DOCUMENTAL | Dossiê público anterior preservado; sem validação de conta/modelo/tarifa efetivos |
| G09/G11 | NÃO PROVADO → NÃO PROVADO | Nenhum provisionamento/review independente; autorrevisão automatizada identificada |
| G10 | PARCIAL → PARCIAL | UTC/UUID mais estritos; replay em memória não persiste no restart, hash não autentica |
| G12 | BLOQUEADO → BLOQUEADO | NO-GO; autorização operacional separada ausente |
| P01 | PARCIAL → PARCIAL | #35 seis cenários DOM sintéticos GREEN; #7 intocada, #35 aberta, sem Canvas instalado |
| P02 | NÃO PROVADO → NÃO PROVADO | IDs locais compostos não comprovam tenant/RBAC/autorização |
| P03 | NÃO PROVADO → NÃO PROVADO | Memória persistente não testada; não confundir com acessibilidade DOM |

Não promover nenhum gate operacional por GREEN sintético. Ver handoff para prioridades e decisões humanas.
