# OBS-EXPLORER-MONEY-HARDENING-001 — 2026-10-11

REAL NOW: base main `50009d1d040aaaaef2920026f173d0425c643a28`, PR #18 integrada.
PROVEN EVIDENCE: testes negativos reproduziram arredondamento de reserva
USD 0.005000001 para 0.005 sob precisão ambiente 2, aceitando orçamento
0.0050000009 insuficiente. Casos extremos numéricos também eram aceitos.
REUSE GATE: BudgetBook, Guard, RateCard e reconciliador SDK existentes.
DECISION: contexto Decimal privado (80 dígitos, Inexact/Rounded proibidos)
para reserva, liquidação, comparação de configuração SDK e reconciliação.
Representações monetárias limitadas a 64 caracteres, 30 dígitos, expoente
absoluto até 18, ordem até 12; inteiros positivos limitados a 1 bilhão.
São limites defensivos da prova, não tetos de modelo/provedor.

Verificação local: 115 testes descobertos, 98 aprovados, 17 opcionais ignorados;
diagnóstico estático e build/sintaxe JS aprovados, extension.js preservada.
O runner SDK recebe a mesma suíte adversarial; CI ainda por conferir no HEAD.
Revisão adversarial: contexto ambiente, excesso de precisão, insuficiência
subcentavo, mutação do contexto do chamador e extremos de expoente examinados.
O contexto original é restaurado; nenhum arredondamento permissivo foi adicionado.
Limitação: SDK reporta custo como float; igualdade exata pode recusar acúmulos
não representáveis. Manter recusa, não inserir tolerância financeira arbitrária.

GO somente para provas offline após ambas CIs/revisão favorável no HEAD.
NO-GO operacional: tarifas/modelo/caps reais, rede/worker operacional e autorização
LLM continuam ausentes. Sem inferência, provedores, credenciais ou deploy.

Achado adicional da revisão: delta monetário no adapter de rotas mocks ainda
herdava contexto ambiente e contabilizava 0.001234567 como 0.0012. Teste
RED reproduziu; mesmo contexto exato aplicado à subtração antes de settle.
