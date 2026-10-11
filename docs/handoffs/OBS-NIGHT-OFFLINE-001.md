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
