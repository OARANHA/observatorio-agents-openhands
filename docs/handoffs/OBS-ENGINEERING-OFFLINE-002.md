# OBS-ENGINEERING-OFFLINE-002


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

## Plano de incrementos

1. Supervisor: startup minimizado; killpg seguido de reap bounded; erro de
cleanup terminal. Testes mocks de falhas e hold incerto, sem SDK operacional.
2. Egress: reutilizar namespace runner com provas HTTP auxiliares locais,
threads/async/subprocess; inventário público de fontes, sem provedor.
3. Auditoria: consumidor sintético com replay/ordem/relógio e falha segura,
sem autenticação alegada; pacote de revisão independente e plano congelado.
4. Produto: contratos read-only com fixtures; DOM quando disponível, sem
merger da #7 ou alteração de instalação. Cada PR terá suite/duas CI/logs/
autorrevisão/expected SHA e confirmação main antes de seguinte incremento.

Retenção: não publicar stderr/stdout parcial ou texto de exceções. Cleanup
concede até 1s adicional ao timeout; falha exige NO-GO, não nova tentativa.


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
