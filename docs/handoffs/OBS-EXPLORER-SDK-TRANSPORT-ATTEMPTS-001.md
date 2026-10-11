# OBS-EXPLORER-SDK-TRANSPORT-ATTEMPTS-001 — investigação de tentativas internas

Data: 2026-10-11. Base reconciliada: `main` = `8e008325bb59562369b0a0e69a017eda3123eb89` (PR #15 integrada). Branch: `test/explorer-sdk-transport-attempts-v1`.

## Autoridade e estado real

Leituras na ordem obrigatória: `docs/PROJECT_SOURCE.md`, `AGENTS.md`, `docs/decisions/ADR-0001-canvas-extension.md` (**Proposto**), `docs/CANONICAL_STATE.md` e `MEMORY.md`, `docs/ARCHITECTURE.md`, `README.md`, código/testes/PRs. PR #7 do grafo segue separada. **Observatório é ferramenta horizontal**, não VIGIAFAST. PRs #12–15 estão integradas, mas nenhum agente/LLM/canário operacional foi autorizado.

**REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION**

- Código real SDK OpenHands **tag v1.53.0** inspecionado em `openhands-sdk/openhands/sdk/llm/llm.py` e `openhands-sdk/openhands/sdk/llm/utils/runtime_metadata.py`. O último SDK instalado em CI foi `openhands-sdk==1.53.0` + `openhands-tools==1.53.0`, sem inferência.
- A PR #15 cobriu reservas nos **nomes das quatro rotas públicas simuladas**, mas não tentativas de transporte internas da implementação SDK e LiteLLM.
- Reutilizar `Guard`, `BudgetBook`, `RateCard`, `TokenCaps` e os runners existentes. Não criar runtime alternativo nem modificar OpenHands Core/Canvas.
- **Decisão:** adicionar inventário de transporte **somente leitura** do SDK real e um teste isolado de **uma reserva por tentativa fictícia**, com falha terminal diante de segunda tentativa. **NO-GO operacional preservado.**

## Mapa verificado no código SDK 1.53.0

| Rota SDK | Ponto LiteLLM (módulo `openhands.sdk.llm.llm`) | Outros riscos |
|---|---|---|
| `completion` | `_transport_call` → `litellm_completion` | retry decorator, cache fallback, refresh 401, fallback model |
| `acompletion` | `_atransport_call` → `litellm_acompletion` | retry decorator + hard timeout, cache fallback, refresh 401, fallback síncrono em outra thread |
| `responses` | `litellm_responses` em `_one_attempt` | retry decorator, cache fallback, refresh 401, fallback model |
| `aresponses` | `litellm_aresponses` em `_one_attempt` | retry decorator + hard timeout, cache fallback, refresh 401, fallback síncrono |
| `resolve_runtime_metadata` / `aresolve_runtime_metadata` | `resolve_provider_metadata_sync` / `aresolve_provider_metadata` | **rede auxiliar sem reserva de LLM**, por exemplo consulta a metadados OpenRouter; o inventário de quatro sinks não cobre esse egress |

Fontes de código upstream para revisão humana: `https://github.com/OpenHands/software-agent-sdk/blob/v1.53.0/openhands-sdk/openhands/sdk/llm/llm.py`, `https://github.com/OpenHands/software-agent-sdk/blob/v1.53.0/openhands-sdk/openhands/sdk/llm/utils/runtime_metadata.py`. Analisar código, não confiar apenas em README.

A presença de `max_retries: 0` no kwargs de transporte e `LLM.num_retries=0` **não** demonstra ausência de novas tentativas por outros caminhos. Atualizar a conta/chave e realizar fallback também podem trocar instâncias/modelos.

## O que os testes novos realmente exercem

- `scripts/canary_transport_probe.py`: `SyntheticTransportGate` só opera em **módulo fictício** `canary_synthetic_litellm`. Envolve quatro sinks com nomes espelhados; cada transporte exige escopo lógico explícito, identidade da task/thread, única tentativa, `BudgetBook.reserve` **antes** da função fake e `BudgetBook.settle` com números fictícios. Segunda tentativa, task paralela, cancelamento, erro, uso ausente ou orçamento insuficiente abortam o mesmo Guard. O wrapper é restaurado em `finally`.
- `tests/test_canary_transport_attempts.py`: execuções sintéticas sync/async, retry na mesma rota, fallback cruzado, retry depois de erro, tentativa após liquidação dentro do mesmo escopo, chamadas separadas, concorrência, token/custo faltante, cancelamento, orçamento insuficiente, negativa fora de escopo e restauração. Contador no destino fake comprova que uma segunda tentativa não o alcançou **nesses testes**, e não que todo transporte de software desconhecido seja interceptado.
- `scripts/audit_canary_sdk_transport.py`: `ast` em **fonte instalada e versão 1.53.0** no runner, sem instanciar LLM. Exige quatro aliases exatos de LiteLLM, **um local de chamada conhecido por alias**, ausência de chamadas adicionais até fora da classe LLM, métodos de fallback e dois caminhos de metadados identificados.
- `tests/test_canary_sdk_transport_audit.py`: mutações de fonte artificial demonstram falha se aliases mudarem, sink duplicar, surgir chamada em outro escopo, houver chamada direta não revisada ou sumir inventário conhecido. No runner SDK o teste adicional audita o pacote instalado; CI comum sem SDK pode ignorar **apenas esse teste opcional**.
- Workflow `.github/workflows/canary-worker-inert.yml` já instala SDK/Tools 1.53.0 em venv efêmero e agora executa o inventário oficial e as provas negativas. Sem credenciais, sem provedor nem LLM.

## Limitações explícitas — não apresentar como prova geral de ausência de bypass

1. O teste dinâmico **NÃO faz monkeypatch no SDK real**, e seu módulo sintético não tem privilégios de segurança. Referências para funções originais capturadas antes do patch, importação dinâmica, bibliotecas externas, novos caminhos e código malicioso podem contornar um wrapper de Python. Ele não deve ser ativado em operação.
2. Auditoria AST por nomes não cobre `getattr` dinâmico, chamadas do LiteLLM dentro da dependência, redirects, SDK instalado alterado após teste, DNS/HTTP por metadata resolver, provedores ou outros serviços. A versão declarada do pacote não é uma prova de integridade imutável.
3. A prova de **uma tentativa por chamada lógica** não comprova que um request HTTP de provedor possa ser completamente controlado com monkeypatch em Python; um controle de saída de rede do processo/sandbox e inspeção dos hooks reais de transporte ainda são necessários.
4. O `BudgetBook` reserva o pior custo declarado para uma chamada sintética; não certifica limites físicos de input/output de um provedor, tarifas, taxas adicionais, disponibilidade na conta, quota monetária nem exatidão de fatura. Cancelamento depois de erro não retira um custo já incorrido.
5. **Critério para avançar:** demonstrar que o worker SDK real pode executar **inteiramente contra transporte stubado, sem rede**, com contador de requests e primeiro/segundo retry, mais uma política de **deny egress** independente cobrindo metadata HTTP e LiteLLM; validar modelo, tarifas oficiais, tokenização e limite do provedor; solicitar autorização humana específica para qualquer canário real.

Sem merge, deploy, alteração VPS/Docker/Canvas/OpenHands Core, registro/delegação ou LLM nesta branch. Nenhuma afirmação GREEN até ler a CI do HEAD.
