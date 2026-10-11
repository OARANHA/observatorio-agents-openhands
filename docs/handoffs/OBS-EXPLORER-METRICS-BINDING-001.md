# OBS-EXPLORER-METRICS-BINDING-001 — 2026-10-11

REAL NOW: main `91f8bedb347985beddda9320b3db83d95cbfdce7`, PR #19 integrada
após revisão adversarial favorável e CIs 38117751430/38117751606 aprovadas
no HEAD 925ff17ebac7c64d6c847b3e80bbdf5fec8837e3. Logs do runner confirmam
4 testes monetários, 12 testes SDK real contra stubs sem rede e worker inerte
com zero registros, delegações e chamadas LLM. Não é operação de agentes.

PROVEN EVIDENCE: testes RED mostraram baseline fora do escopo, uso de outro
objeto LLM, reutilização em chamada seguinte e cache divergente no snapshot
aceitos. REUSE GATE: SyntheticTransportGate/BudgetBook/Guard existentes.
DECISION: SDKBaseline imutável vinculado por identidade à missão, LLM, Metrics
e geração do escopo lógico. Exigir criação antes do transporte, uma vez;
consumir baseline somente após liquidação válida, descartar ao sair do escopo.
Negar baseline forjado/reutilizado, troca de Metrics e cache ausente, inválido
ou não zero, incluindo snapshot da resposta. Sem preço para cache, não inferir zero.

Local: 121 testes descobertos, 104 aprovados, 17 opcionais ignorados.
Diagnóstico estático/build/sintaxe aprovados. CI do novo HEAD ainda por conferir.
Revisão adversarial: identidade/geração, baselines forjados, reentrada,
cache negativo/bool/ausente, troca de objeto e retenção de reserva incerta.
Limite: referências Python não são autenticação de provedor nem proteção
contra código hostil no processo. Classes reais só usadas com stubs no runner
isolado existente. NO-GO operacional mantido; nenhuma rede/provedor/LLM.
