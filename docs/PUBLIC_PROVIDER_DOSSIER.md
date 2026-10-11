# Provedores — homologação exclusivamente documental

Consultado em **2026-10-11 UTC**, somente páginas públicas oficiais.
Nenhuma conta, chave, quota privada, SDK de provedor ou endpoint de inferência
foi acessado. Pesquisa não seleciona modelo e não altera RateCard, allowlists
ou autorização. **G08 PARCIAL DOCUMENTAL; G09 NÃO PROVADO; NO-GO.**

## Amostras verificadas, sem recomendação operacional

Preços USD por milhão de tokens, rota padrão síncrona de API direta;
não equivalem a tarifa efetiva de uma conta, agregador, região ou contrato.

| Amostra | Entrada / saída | Contexto / saída máxima documentados | Ressalva |
|---|---|---|---|
| `gpt-4o-mini` | 0.15 / 0.60; entrada cache 0.075 | 128000 / 16384 | Snapshot público `gpt-4o-mini-2024-07-18`; disponibilidade e tier da conta não verificados |
| `claude-haiku-4-5-20251001` | 1 / 5; cache write 5m 1.25, 1h 2; read 0.10 | 200K / 64K | Active legacy; retirada não antes de 2026-10-15, não é promessa de disponibilidade futura |
| `gemini-2.5-flash` | Texto 0.30 / 2.50, saída inclui thinking | Entrada 1048576 / saída 65536 | Acesso limitado a usuários com uso anterior dos modelos 2.5; não assumir acesso em projeto novo |

Fontes diretas para cada linha:

- OpenAI: https://developers.openai.com/api/docs/models/gpt-4o-mini
- Anthropic: https://platform.claude.com/docs/en/models/haiku-4-5/overview
- Google modelo: https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash
- Google preços: https://ai.google.dev/gemini-api/docs/pricing

Google: áudio possui outra tarifa, cache textual 0.03 mais armazenamento
1 USD/milhão/hora; grounding e ferramentas têm cobranças adicionais.
Batch/flex/priority e rotas cloud não foram homologadas para o canário.
O cálculo sintético atual não autoriza cache, streaming ou extras; preços
documentais não tornam essas superfícies aceitas.

## Caps, quotas e ressalvas documentais

| Fonte oficial | Fato público | Prova de conta ainda ausente |
|---|---|---|
| [OpenAI prepaid billing](https://help.openai.com/en/articles/8264644-setting-up-and-managing-prepaid-api-billing) | Corte por saldo pode atrasar e produzir saldo negativo. Limite de recarga automática não é limite de uso API; compras manuais não entram nele. | Spend limit efetivamente imposto, saldo, tier, limites de requests/tokens e identidade segregada |
| [Anthropic rate/spend limits](https://platform.claude.com/docs/en/api/rate-limits) | Spend e rate limits são distintos. Limites de organização sempre se aplicam; workspaces podem ter limites menores, exceto workspace default. | Organização, workspace segregado, cap configurado e comportamento da rota escolhida |
| [Gemini billing](https://ai.google.dev/gemini-api/docs/billing) | Cap de projeto experimental admite excesso por latência de cerca de dez minutos; tarefas longas podem exceder. Conta faturada/offline não dispõe desses caps. Gastos agregam projetos da conta de billing. | Tipo de conta, projeto, cap efetivo, quota disponível e segregação financeira |

Não registrar valores de quota de uma tabela pública como se fossem os da
conta. Nenhuma configuração foi criada, alterada ou consultada em console.
Essas ressalvas impedem tratar saldo/cap público como teto instantâneo da
missão. O teto preventivo local e o cancelamento independente continuam
necessários, mas ainda não foram homologados contra um provedor real.

## Gate para futura decisão do proprietário

Congelar modelo/snapshot, provedor/rota/endpoints, contexto e saída, preços
de todas as categorias faturáveis, data e moeda. Verificar disponibilidade,
tokenização/thinking/cache, zero retries em todas as camadas e metadados
auxiliares. Confirmar identidade não produtiva, limites efetivos de conta,
revogação e risco de excesso financeiro antes de qualquer autorização real.
Emitir orçamento preventivo completo após esses dados, não estimativa fechada
a partir das amostras desta tabela. Nenhuma chamada gratuita está autorizada
pelo simples fato de existir free tier.

Gap concreto: `OFFICIAL_HOSTS['anthropic']` aceita `anthropic.com` e
`docs.anthropic.com`; a documentação pública atual consultada usa
`platform.claude.com`. A allowlist permanece restrita. Eventual atualização
precisa de revisão específica; não foi ampliada para obter GO ou CI verde.
RateCard `operator_verified` não foi produzido. Tarifas devem ser novamente
verificadas antes de uma missão futura (o código exige idade máxima de 30 dias).
