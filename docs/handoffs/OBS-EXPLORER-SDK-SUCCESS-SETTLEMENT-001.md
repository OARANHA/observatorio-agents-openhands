# OBS-EXPLORER-SDK-SUCCESS-SETTLEMENT-001 — sucesso fictício SDK 1.53.0

Data: 2026-10-11. Branch: `test/explorer-sdk-success-settlement-offline-v1`. Base GitHub conferida `main = a21eb4e2250cf935de783b305f3d32d643bd0b1a`, PR #17 **integrada**. PR #7 do grafo é independente. Fonte de autoridade na sequência: `docs/PROJECT_SOURCE.md` → `AGENTS.md` → ADR-0001 (**Proposto**) → `docs/CANONICAL_STATE.md` / `MEMORY.md` → `docs/ARCHITECTURE.md` / `README.md` → código/testes/main/PR.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

**REAL NOW:** PRs #14–17 integradas. Runner do SDK 1.53.0 passou seis testes de **erro** com as quatro rotas públicas SDK reais interceptadas por transportes LiteLLM fictícios no Bubblewrap sem rede. Não existe chamada operacional LLM autorizada. O Observatório é ferramenta horizontal distinta de VIGIAFAST/Wandora/ELUS.

**PROVEN EVIDENCE:** inspeção da fonte SDK 1.53.0, `openhands-sdk/openhands/sdk/llm/llm.py`: `_validate_chat_response` e `responses`/`aresponses` chamam `Telemetry.on_response`; `_build_completion_result`/`_build_responses_result` devolvem `LLMResponse` com snapshot de métricas. `utils/telemetry.py` normaliza `Usage` (chat) e `ResponseAPIUsage` (responses) e atualiza `Metrics` com custo e tokens. `max_input_tokens` não equivale a teto efetivo de input imposto pelo provedor. Nada disso autoriza uso real.

**GAPS:** os testes #17 jamais receberam `ModelResponse` ou `ResponsesAPIResponse` bem-sucedido. Portanto não validaram normalização, acumulação, reconciliação nem liberação de uma reserva após uso verificado.

**REUSE GATE:** reaproveitar `SyntheticTransportGate` + `BudgetBook` + `Guard` existentes, a classe `LLM` real e `Telemetry` SDK 1.53.0, e o runner Bubblewrap da PR #17. Não alterar OpenHands Core, não criar agente, não criar conexão com provedor.

**DECISION:** somente adicionar integração **offline sintética** em `tests/test_sdk_real_transport_offline.py`, novo reconciliador reutilizando as métricas existentes `scripts/canary_sdk_success_probe.py` e gatilho de CI. **NO-GO** para qualquer execução LLM operacional.

## Estratégia da prova

1. O teste roda exclusivamente com SDK/Tools **1.53.0 instalado em venv efêmero**. `.github/workflows/canary-worker-inert.yml` o executa dentro de Bubblewrap `--unshare-all`, `--clearenv`, com namespace de rede comprovadamente diferente do host e sem interface externa. Import do LiteLLM usa `LITELLM_LOCAL_MODEL_COST_MAP=True`; `api_key` é apenas texto artificial que não funciona em provedores.
2. As quatro funções importadas `litellm_completion`, `litellm_acompletion`, `litellm_responses`, `litellm_aresponses` são substituídas **temporariamente** por funções locais que devolvem objetos **tipados** `ModelResponse`/`ResponsesAPIResponse`, com `Usage`/`ResponseAPIUsage` artificiais e texto fictício. Não há chamada remota, streaming ou modelo real. Cada destino passa pelo `SyntheticTransportGate`: `BudgetBook.reserve` ocorre antes do stub.
3. O SDK oficial deve consumir a resposta, invocar `Telemetry.on_response` e produzir `LLMResponse` com snapshot de tokens/custo. Para manter cálculo **estritamente sintético e determinístico**, o método `Telemetry._compute_cost` é substituído apenas no teste por cálculo local a partir do uso do próprio stub: USD 2 por milhão tokens de entrada e USD 8 por milhão tokens de saída. Isso **não testa** o algoritmo de preços real do LiteLLM ou de provedores.
4. Antes da chamada, `snapshot_success_start` registra os totais reais de `Metrics` do SDK. Depois, `settle_success_from_sdk_metrics` exige que o `LLMResponse.metrics` corresponda às métricas internas, obtém deltas de tokens/custo, compara preço **de novo** com `RateCard` via `Decimal` e só então chama `SyntheticTransportGate.settle` → `BudgetBook.settle`. Para 100 tokens de entrada e 100 de saída: reserva máxima **USD 0,005** (500 + 500) e liquidação sintética **USD 0,001** (0,0002 + 0,0008). Sem liquidação, o contexto fecha a missão como falha.
5. Cobertura: quatro rotas reais sync/async, duas chamadas com métricas acumulativas, ausência de uso, ausência de custo, sobrecobrança sintética e tokens acima de 500. Nos erros, missão e `BudgetBook` fechados e reserva incerta **não** é devolvida. O contexto descarta o patch no `finally`.
6. O runner genérico sem SDK deve **SKIP apenas os testes que precisam do SDK**; o runner isolado deve executá-los sem skips. GREEN depende do HEAD exato e da inspeção do log; nenhum polling contínuo.

## Limites reais da demonstração

- Só testamos **respostas fictícias bem-sucedidas** produzidas dentro do SDK real; não há inferência, faturamento, provedores ou credenciais verdadeiras.
- Validação de `LLMResponse.metrics` e `BudgetBook` não demonstra que preços, taxas extras, cotas da conta ou limites físicos de contexto/output são impostos pelo provedor. O valor esperado foi calculado com tarifa de teste; seu propósito é testar aritmética e reconciliação.
- `SyntheticTransportGate` é um instrumento para testes descartáveis, **não guard financeiro operacional** nem sandbox multi-tenant. Rotas de egress auxiliares, retries dentro de dependências e bypasses por código dinâmico não foram integralmente provados ausentes.
- O código não deve ser usado como justificativa para modificar VPS, Canvas, OpenHands Core, registrar/delegar agentes, habilitar workers ou fazer chamadas LLM. Para um futuro canário real: provas independentes de rede/identidade/caps reais, tarifas oficiais verificadas e autorização específica.

**Gate da PR #18: GO apenas para CI offline e revisão; NO-GO operacional. Sem merge automático, sem deploy.**
