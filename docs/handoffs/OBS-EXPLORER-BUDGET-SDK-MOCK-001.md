# OBS-EXPLORER-BUDGET-SDK-MOCK-001 — quatro rotas com pré-reserva sintética

Data: 2026-10-11. Base da branch: `b16a1eddaa852ee92716a0162f09106ee73b4335` (PR #14 integrada). Branch `feat/explorer-budget-sdk-boundary-mock-v1`.

## Autoridade e reconciliação

A ordem canônica consultada foi `docs/PROJECT_SOURCE.md`, `AGENTS.md`, `docs/decisions/ADR-0001-canvas-extension.md` (**Proposto**), `docs/CANONICAL_STATE.md`, `MEMORY.md`, `docs/ARCHITECTURE.md`, `README.md`, código, testes e PRs. O projeto Observatório é horizontal, distinto de VIGIAFAST, Wandora e ELUS. PR #7 do grafo continua separada.

**REAL NOW:** a `main` acima inclui PRs #9, #11, #12, #13 e #14, com `BudgetBook` offline mas sem integração às rotas LLM.

**PROVEN EVIDENCE:** SDK/Tools 1.53.0 efetivamente verificados em runners anteriores, sem chamadas LLM; seis testes de sandbox e worker sintético passaram nas PRs #12/#13; pré-reserva offline teve 10 testes aprovados na PR #14.

**GAPS:** orçamento não havia sido ligado às quatro rotas, e o SDK 1.53.0 contém retentativas internas em `completion`/`acompletion` (por exemplo fallback de cache e atualização de credenciais), além de dependências de transporte externas. Interceptar apenas os métodos públicos NÃO comprova ausência de mais de um request de cobrança na mesma chamada. Sem modelo/tarifas oficiais nem prova de teto de tokens do provedor.

**REUSE GATE:** reutilizar `BudgetBook`, `RateCard`, `TokenCaps`, `validate_sdk_config`, `Guard` e `_metrics`. Não alterar SDK/Core, não publicar segredos e não iniciar agentes.

**DECISION:** aceitar somente PR com provas de integração **mock-only**, mantendo o primeiro canário real em **NO-GO**.

## Implementação proposta

- `scripts/canary_budget_boundary.py`: contexto explícito `synthetic_budgeted_llm_routes` que envolve `completion`, `acompletion`, `responses` e `aresponses` em classe fictícia com métodos de mesma forma síncrona/assíncrona. Exige cartão `synthetic`, provedor `synthetic`, marcador de transporte fictício e **recusa a classe LLM real do SDK** por origem do módulo.
- Antes de cada função fictícia, compara `model`, `num_retries=0`, `max_output_tokens`, taxas por token, rejeita `stream` e `caching_prompt` e quaisquer kwargs adicionais ainda não revisados, lê métricas anteriores e exige `BudgetBook.reserve`. Apenas então deixa a função fake retornar.
- Depois da função, reconcilia deltas de métricas com a `Reservation` pelo `BudgetBook.settle`, compartilhando o mesmo `Guard`.
- Falha em qualquer ponto, inclusive `BaseException`/cancelamento assíncrono, chama `book.abort(guard)`. Resultado incerto nunca libera outra reserva. Segunda chamada concorrente ou fallback via método envelopado cancela a missão em vez de executar a segunda chamada.
- A substituição dos métodos é temporária e restaura exatamente as implementações originais no `finally`, até se o teste falhar. Este mecanismo é de processo descartável e nunca deve ser aplicado no servidor OpenHands ou em sessões com outros usuários.
- `tests/test_canary_budget_boundary.py`: modelos 100% fictícios, casos de sucesso e negação em quatro rotas, clonagem, recusa por orçamento, reentrada, falta de métricas, sobrecobrança, exceção durante chamada, configurações divergentes, restaurar métodos e bloqueio de classe SDK real.
- `tests/test_canary_budget_sdk_surface.py`: consulta as assinaturas oficiais da classe `openhands.sdk.llm.LLM` 1.53.0, quando instalada, e demonstra que essa classe é recusada sem criar LLM nem acessar provedor. No runner sem SDK, testes opcionais são SKIP; o workflow separado com SDK 1.53.0 deve comprovar a execução de ambos sem SKIP.
- Workflow `.github/workflows/canary-worker-inert.yml` foi ampliado para disparar com esse slice e validar API oficial no runner efêmero. CI principal testa mocks sem instalar SDK.

## Limites obrigatórios antes do primeiro canário real

1. Este módulo é **mock-only e não é usado no worker operacional**. A classe real `LLM` é explicitamente recusada. Nenhum provedor pode ser acionado neste slice.
2. A instrumentação futura precisa garantir **uma reserva por tentativa de transporte**, inclusive quando o SDK faz retries internos, credencial refresh, cache-fallback, redirects ou novas chamadas por ferramentas. Proibir ou instrumentar esses caminhos no nível correto do SDK, verificar contagem de transportes e impedir bypasses.
3. Limites reais de entrada precisam cobrir contexto do SDK, system prompt, tool schemas e tokens de resposta; não são provados pela comparação de campos do LLM nem pelas flags `TokenCaps`.
4. Preços e variantes de cobrança dependem de prova **externa** de fornecedor/modelo/data, provedor/conta e teto efetivo. Não confundir URL/flag `operator_verified` com homologação. Sem provedor real neste PR.
5. Orçamento preventivo em código continua sendo estimativa: só um limite contratual do provedor/conta comprovado e contabilização de todas as classes de uso ajudam a restringir custo real absoluto.
6. A CI GREEN valida somente o que os testes realmente executarem, não autoriza registro de agentes, delegação, deploy, alteração da VPS/Canvas/OpenHands Core ou chamadas LLM.

## Critério de revisão

Reconciliar HEAD e main, ler os logs exatos do job de contrato e do runner SDK, identificar quantos testes passam/ignoram e examinar diferenças na PR. Sem polling contínuo. PR abre sem merge e sem deploy. Próximo gate depende de autorização humana específica.
