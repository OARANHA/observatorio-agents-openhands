# Plano de execução CYCLE004 — aprovado pelo escopo do proprietário

Até quatro PRs úteis, sequenciais, exclusivamente neste repositório:
1. Fontes oficiais fixadas e contrato sintético de continuidade na mesma conversa.
2. Gateway em memória com mocks, minimização, ordem, dedupe e falha incerta.
3. Mentor DEMO isolado, contexto revisável, identidade composta, sem Canvas/ChatGPT real.
4. Consolidação de evidências/handoff somente se necessária após os resultados.

TDD das alterações de comportamento; reaproveitar Guard/BudgetBook/envelopes e
contratos visuais congelados. Nenhum servidor, cliente de rede, SDK operacional
ou instalação. PR7/35 preservadas. Slack → Work bloqueado por vínculo do app:
continuar offline, sem polling substituto. Cada merge exige diff final, revisão
adversarial automatizada registrada, duas CIs GREEN no HEAD exato e logs reais
lidos antes do merge, lease de SHA e confirmação da main. Evidência sintética
sempre marcada; manter NO-GO operacional. Handoff final em
`docs/handoffs/OBS-CYCLE-004-EVENTS-MENTORSHIP.md`.
