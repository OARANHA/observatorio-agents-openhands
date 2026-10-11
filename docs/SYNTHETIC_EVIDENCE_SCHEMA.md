# Evidências sintéticas — contrato v1

Data: 2026-10-11. Implementação: `scripts/canary_audit_bundle.py`.
Somente offline. `operational_go` e `authenticity_proven` são sempre `false`.
Reutiliza `synthetic_accounting_evidence()`, sem SDK, transporte, leitura de
ambiente, persistência ou registro de agentes.

| Campo obrigatório | Contrato |
|---|---|
| `schema` | `obs.synthetic.audit.v1` |
| `classification` | `synthetic` |
| `operational_go`, `authenticity_proven` | Booleano `false` exato |
| `evidence_id` | `SYNTHETIC-` seguido de UUID v4 canônico, gerado localmente |
| `observed_at_utc` | UTC local `YYYY-MM-DDTHH:MM:SSZ`; não atesta relógio externo |
| `source_claim` | `caller_declared_public_git_sha` |
| `source_sha` | SHA Git público declarado pelo chamador: 40 caracteres hex minúsculos |
| `target_sdk` | `1.53.0`, alvo descritivo; não comprova pacote instalado |
| `accounting` | Contrato existente `obs.synthetic.accounting.v1`, campos fechados |
| `sha256` | Digest do JSON canônico dos demais campos |

JSON canônico: `sort_keys=True`, separadores `,` e `:`, ASCII, sem NaN.
Leitor admite no máximo 8192 caracteres; rejeita chaves duplicadas, constantes
não JSON, campos ausentes/adicionais, tipos incorretos e versões desconhecidas.
Não há campos livres para prompts, URLs arbitrárias, objetos SDK, ambiente,
credenciais ou dados de clientes. Marcadores privados dos testes são fictícios
e são rejeitados; não são evidências publicadas.

Valores monetários são strings decimais não negativas, fixas, de até 64
caracteres; orçamento positivo, `budget = spent + held + uncommitted`, com
aritmética exata e contexto próprio. Contadores são inteiros exatos entre zero
e 10^18, excluindo booleanos; chamadas do Book não excedem as observadas pelo
Guard. Hold positivo admite apenas `open_reserved`/`closed_uncertain`; hold
zero admite `open_idle`/`closed_verified`. `closed_verified` descreve somente
a contabilização fictícia liquidada, nunca sucesso semântico ou operacional.
Falha ao construir evidência encerra Book/Guard, sem tentativa de transporte.

## Limites da prova

Checksum detecta alterações sem recomputação. Quem recomputa um hash pode
forjar um relato sintético válido; isto não é assinatura, proveniência
independente nem defesa contra replay. UUID não cria registro persistente.
Não existem store, consumidor, política de retenção, autenticação ou acesso
multitenant implementados por este contrato. SHA declarado requer conferência
externa com GitHub antes de qualquer uso como prova de origem.

Oito testes cobrem roundtrip, identidade, hash, alteração com hash recalculado,
claims operacionais, campos privados, finanças/tipos/estado, JSON duplicado ou
malformado, tamanho, origem inválida e hold incerto. A matriz G10 continua
PARCIAL e G11 não provado. Não há evidência operacional nova.
