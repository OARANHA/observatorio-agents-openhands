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
