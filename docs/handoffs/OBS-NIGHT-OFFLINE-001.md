# OBS-NIGHT-OFFLINE-001 — 2026-10-11

## REAL NOW → PROVEN EVIDENCE

Base ba38f1a0dd29110c0b1dbbc7c0c0c51a07887510, main confirmada.
Matriz do anexo versionada em ../GO_NO_GO_MATRIX.md; oito CIs históricas
reconfirmadas. PR #7 aberta/draft, excluída de merges; PR #10 preservada.
A–H são prioridades, não obrigação de criar oito PRs artificiais.

## GAPS → REUSE GATE → DECISION

Manter NO-GO. Reutilizar controles existentes. Primeiro incremento inclui
somente matriz/documentação e ampliação do filtro de CI para docs/testes
canary. Nenhuma mudança de runtime, permissões ou política de confirmação.
Validação do HEAD e autorrevisão serão registradas na PR real. Autorrevisão
serve ao merge offline autorizado, não atende G11 de revisão independente.

Riscos remanescentes: isolamento futuro não homologado, todos egress de
dependências não cobertos, tarifas/conta/quota/caps não aprovados, worker
operacional não conectado, evidência operacional e autorização ausentes.


## Provas negativas de isolamento — preparação noturna (2026-10-11)

PR #23 integrada abc1997e7999a91e9a8c71933bb581437097ad51; CIs 38120273244
e 38120273294 GREEN, logs sem skips no SDK e autorrevisão registrada.
Suite de sandbox ampliada de seis para dez probes: DNS sem resolver do host,
socket Unix abstrato do host negado, FD herdável fechado pelo supervisor,
descendente com ambiente limpo/RO/DNS negado e tmpfs separado. Não muda
sandbox_argv nem allowlist. CI efêmera é obrigatória, sem skip/fallback.
Local: bwrap indisponível para namespaces; resultado RED não certifica
isolamento. Provas do novo HEAD ainda dependem do runner. NO-GO mantido.


## SDK superfície e rotas inertes — 2026-10-11

PR #24 integrada 05f88c1790b13c19e23a74fadc80cbaa22f0de23; CIs 38120541286 /
38120541272 e sandbox 38120541278 GREEN, dez probes reais sem skips,
autorrevisão registrada. Auditoria AST agora nega aliases LiteLLM extras,
imports duplicados, módulos renomeados e duplicação de método executável;
property getter/setter oficial preservado. REDs reproduzidos e corrigidos.
Baseline/settlement sintéticos negam streaming, cache, fallback, refresh hook
e extra_body antes do transporte ou após mutação, retendo hold incerto.
139 testes locais: 122 PASS/17 opcionais skip; AST no SDK 1.53.0: 12 PASS.
Não garante todo egress de dependências; CI do novo HEAD por conferir. NO-GO.


## Financeiro adversarial — 2026-10-11

PR #25 integrada em 2329f85123f04667bbd39ce1ce4a4021e3cbb9c2; CIs 38120804684
e 38120804699 GREEN, logs/revisão registrados. Negativas financeiras novas
reproduziram RED: saldo/contadores negativos financiavam reserva; custo com
zero tokens era liquidado. Invariantes agora são verificadas antes de reserva
e liquidação; uso zero mantém hold incerto e cancela, sem refund/retry.
Concorrência determinística: só uma reserva, segunda encerra missão inteira.
Métricas parciais negadas antes do stub; ausência de usage vira GateError.
144 testes locais: 127 PASS/17 opcionais skip. CI deste HEAD por conferir.
Proteção contra código hostil no mesmo processo continua fora da garantia.
NO-GO operacional mantido.


## Ciclo supervisionado inerte — 2026-10-11

PR #26 integrada d32483da5300c17d4e556c7f3b7d7166e196a32a, CIs 38121045562 /
38121045552 GREEN. Quatro cenários novos percorrem _run_task oficial com
conversa mockada, FakeLLM, Book/Guard compartilhados e terminal com saída
fictícia: leitura seguida de recusa, aprovação ausente, expiração durante
aprovação e última chamada global. Depois da parada nenhum novo stub ou
subprocesso roda; pause/close no finally, sem recuperação por task.set_error.
Nenhum Agent/Conversation real, start_task, TaskExecutor dispatch ou registro.
Contrato do pai rejeita bool como contador e campos extras potencialmente
privados antes de imprimir JSON (RED reproduzido). 149 testes locais: 128
PASS/21 opcionais SDK skip; manager oficial local: 6 PASS. CI por conferir.
Worker continua inerte; não certifica wiring operacional ou cgroup. NO-GO.


## Evidência sintética versionada — 2026-10-11

PR #27 integrada em dd441990b72fed8917a8bf9ec279ddb0a5f688ca; CIs
38121276910 e 38121276933 GREEN no HEAD ab157d165c8eeb998d10b79b9b50df056ff7e836,
logs e autorrevisão registrados. Esquema obs.synthetic.audit.v1 reutiliza
relatório contábil fechado; JSON limitado, campos/tipos estritos, duplicatas
negadas, hash canônico e origem SHA explicitamente declarada, não autenticada.
Oito testes novos: RED inicial (contrato ausente), GREEN após implementação.
157 testes locais: 136 PASS/21 opcionais SDK skip; SDK manager já comprovado
em CI. Sem persistência, assinatura, credenciais ou payload livre.
Ver docs/SYNTHETIC_EVIDENCE_SCHEMA.md. CI deste incremento por conferir; G10
continua parcial, G11 não provado e NO-GO operacional mantido.


## Fechamento documental noturno — 2026-10-11

REAL NOW: main b95ea8c44f9fe95ee24fdec6e32c2bea00c8451a confirmada após PR #28.
PR #10 permanece aberta HEAD f52b635290ba9e542e2bbb01a9d5a657fed11452;
PR #11 integrada; #7 aberta/draft, HEAD 48f898d99a8979ef2c794513131506b028772666.
Nenhum handoff foi removido. ADR-0001 continua Proposto. Observatório horizontal.
PROVEN EVIDENCE: seis PRs offline integradas, duas CIs GREEN no HEAD exato,
logs examinados e autorrevisões favoráveis registradas antes de cada merge.
| PR | HEAD exato | Merge confirmado | CI Observatorio | Canary Worker Inert SDK |
|---|---|---|---|---|
| [#23](https://github.com/OARANHA/observatorio-agents-openhands/pull/23) | `9c089f60b54c12b11a9397b82118093a9a9a9803` | `abc1997e7999a91e9a8c71933bb581437097ad51` | [38120273244](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120273244) | [38120273294](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120273294) |
| [#24](https://github.com/OARANHA/observatorio-agents-openhands/pull/24) | `37b75fcbf98e7e1408967bca61de33479cd49a4a` | `05f88c1790b13c19e23a74fadc80cbaa22f0de23` | [38120541286](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120541286) | [38120541272](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120541272) |
| [#25](https://github.com/OARANHA/observatorio-agents-openhands/pull/25) | `5bc943516af3faacd52d56ee6f0fccef51c7226f` | `2329f85123f04667bbd39ce1ce4a4021e3cbb9c2` | [38120804684](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120804684) | [38120804699](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120804699) |
| [#26](https://github.com/OARANHA/observatorio-agents-openhands/pull/26) | `c596aea62ff200e7025eaa9b0ac681ae23080cf8` | `d32483da5300c17d4e556c7f3b7d7166e196a32a` | [38121045562](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121045562) | [38121045552](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121045552) |
| [#27](https://github.com/OARANHA/observatorio-agents-openhands/pull/27) | `ab157d165c8eeb998d10b79b9b50df056ff7e836` | `dd441990b72fed8917a8bf9ec279ddb0a5f688ca` | [38121276910](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121276910) | [38121276933](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121276933) |
| [#28](https://github.com/OARANHA/observatorio-agents-openhands/pull/28) | `b4774202dad4a49c9bcacdaaf18a969a104cd69b` | `b95ea8c44f9fe95ee24fdec6e32c2bea00c8451a` | [38121795712](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121795712) | [38121795824](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121795824) |

PR #24 tem também Sandbox Probe [38120541278](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120541278), GREEN.
Suite atual: 157 testes, 136 PASS/21 opcionais SDK skip no Python sem SDK.
No runner SDK, 81 testes dedicados PASS, dez probes reais de isolamento PASS,
worker inerte com zero chamadas LLM, zero registros e zero dispatches reais.
Geração determinística/node --check/diagnóstico estático passam.

GAPS: G05/G06/G07/G10 permanecem PARCIAIS operacionalmente; G08 passa de
NÃO PROVADO a PARCIAL DOCUMENTAL, sem homologação de modelo/rota/conta.
G09/G11 não provados; G12 bloqueado. Dossiê público em
`docs/PUBLIC_PROVIDER_DOSSIER.md` e revisão estática em
`docs/GRAPH_PR7_REVIEW.md`. REUSE GATE: BudgetBook, Guard, supervisor e SDK/Tools oficiais preservados;
não recriar OpenHands nem transformar mocks em agentes operacionais.
DECISION: finalizar este ciclo com PR documental única para G/H/consolidação,
não criar oitava PR artificial. Seu próprio HEAD/CI/merge serão registrados
na revisão e descrição GitHub após verificação, sem antecipar resultados.
**NO-GO operacional permanece.** Próximos gates exigem ambiente autorizado,
modelo/rota/conta segregados, revisão distinta e autorização expressa da missão.
