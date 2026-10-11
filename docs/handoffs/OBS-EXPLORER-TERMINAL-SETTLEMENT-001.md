# OBS-EXPLORER-TERMINAL-SETTLEMENT-001 — 2026-10-11

REAL NOW: main `2e17e05804d3f2561f5fdc5b2506a870ffe881e3`, PR #20 integrada
após revisão favorável e ambas CIs GREEN no HEAD 370600016b1bfae565a8b45a6ab389c413c10527
(runs 38118001929 / 38118001931). Runner: 10 testes adversariais, 12 SDK/stubs,
worker inerte, zero inferência/registro/delegação.

PROVEN EVIDENCE: RED reproduziu segunda reserva com TokenCaps.max_calls=1,
liquidação exatamente no limite do Guard sem registro no Book, troca de Guard,
e ausência de erro específico na expiração. REUSE GATE: BudgetBook/Guard existentes.
DECISION: identidade única de Guard ligada ao Book; cancelar ambos em tentativa
de substituição. Limite efetivo de chamadas é o menor entre caps, Book e Guard.
Reserva preventiva considera também orçamento restante do Guard. Prazo expirado
nega liquidação, mantém reserva incerta e fecha missão. Nenhuma devolução de
reserva em erro/timeout ou nova tentativa é permitida.

Uso validado que esgota limite registra o custo exato uma vez, libera a reserva
já comprovada e fecha Book/Guard. Não confundir gasto comprovado com reserva
incerta. Recusa externa/timeout continuam erro, com retenção conservadora.
Depois da última chamada: nenhuma rota LLM mock nem ação terminal é aprovada.

Verificação local: 127 testes descobertos, 110 aprovados, 17 opcionais ignorados;
diagnóstico/build/sintaxe preservados. CIs deste HEAD ainda por conferir.
Revisão adversarial: limites menores que o Book, substituição de Guard para
resetar contador/prazo, replay de liquidação, custo exatamente no limite,
pré-reserva contra o Guard mais restritivo e bloqueio de ações subsequentes.
Limite: custo real e tokens continuam inexistentes; números são fictícios.
Guard float só pode tornar a prova mais restritiva, nunca autoriza preço/cap real.
NO-GO operacional mantido; sem transporte real, agente, credencial ou deploy.
