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
