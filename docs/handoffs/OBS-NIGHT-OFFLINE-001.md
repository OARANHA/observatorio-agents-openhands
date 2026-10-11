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
