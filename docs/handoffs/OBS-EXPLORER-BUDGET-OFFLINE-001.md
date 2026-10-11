# OBS-EXPLORER-BUDGET-OFFLINE-001 — reserva preventiva sem LLM

Data: 2026-10-11.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

- **REAL NOW:** base reconciliada antes da branch `cf4a429fde6e8b4aecd7c1001166ee13f2d755c4` (PR #13 integrada), PR #7 do grafo ainda separada. Observatório é ferramenta horizontal; não pertence ao VIGIAFAST.
- **PROVEN EVIDENCE:** PR #12 demonstrou seis provas de sandbox no runner temporário; PR #13 montou TaskToolSet, terminal restrito e supervisor em worker **inerte**, com SDK/Tools 1.53.0 e zero LLM/agentes/delegações.
- **GAPS:** o Guard de `canary_controls.py` contabiliza custo **após** cada chamada; esse mecanismo isolado permite ultrapassar o orçamento durante uma chamada. Não há provedor/modelo autorizado, tarifas reais conferidas, garantia de limite de entrada/saída ou controle independente de fatura.
- **REUSE GATE:** usar `Guard` compartilhado, métricas e limites oficiais do SDK; não criar outro executor, alterar OpenHands Core ou inventar valores atuais de provedor.
- **DECISION:** acrescentar somente cálculo e reserva **offline**, sem ligar ainda às APIs LLM. Continua NO-GO operacional.

## Política de preços e modelo

O módulo `scripts/canary_budget.py` define `RateCard`, `TokenCaps`, `BudgetBook` e `validate_sdk_config`.

- **Preço:** strings decimais USD por milhão de tokens, convertidas com `Decimal` (sem arredondamento precoce). Invalida custo zero, NaN, infinito, variante de cobrança desconhecida, modelo vazio e fonte não homologada.
- **Proveniência:** `operator_verified` é uma declaração que exigirá **revisão humana real**, URL HTTPS de host oficial exato, e conferência de até 30 dias. Verificação de hostname/data é filtro, **não comprova** que a página contém aquelas tarifas, a existência do modelo nem disponibilidade/limite na conta. Não há tabela tarifária real fornecida nesta PR.
- **Cobrança:** simulação considera somente tarifa padrão de entrada e saída, sem cache, lote, tools, vídeo, áudio, taxas ou outros custos. Na ausência de prova de cobertura de todas as classes de cobrança, a operação real fica bloqueada.
- **Tokens:** limites inteiros positivos para entrada e saída, soma dentro da janela de contexto, `num_retries=0`, máximo de chamadas. Futuro modo real exige evidência de que o tokenizer limita **todo** o prompt construído pelo SDK e de que o provedor impõe o teto de saída; flags declaradas não substituem testes.
- **SDK:** `validate_sdk_config` faz comparação **inerte** de `model`, `num_retries`, `max_output_tokens`, `input_cost_per_token` e `output_cost_per_token`. Campos observados no código oficial SDK 1.53.0, mas isso não certifica que o provedor os respeitará.
- **Concorrência:** reserva única em voo; segunda chamada paralela cancela o Guard. Resultado incerto cancela e **não devolve** a reserva para novas chamadas.
- **Liquidação:** compara tokens usados com os tetos e cobrança reportada com a tarifa mínima teórica e teto reservado. Dados ausentes, divergências e estouros bloqueiam a missão.

## Exemplo 100% sintético — NÃO são tarifas de um modelo comercial

- Modelo fictício: `fake/explorer`; valores artificiais: entrada **US$ 2,00/milhão**, saída **US$ 8,00/milhão**.
- Reservar 500 tokens de entrada e 500 de saída: `(500×2 + 500×8)/1.000.000 = US$ 0,005`.
- Orçamento artificial de US$ 0,01: primeira reserva pode ocorrer, mas uma requisição cuja pior resposta ultrapasse o saldo restante é **recusada antes do provedor**.
- Testes simulam liquidação e negação: sem tokens consumidos por LLM, sem chave de API, sem faturamento real.

## Limites e próximos gates

1. `BudgetBook` é **projeto de preflight**; **não está instalado** nos quatro métodos `LLM.completion / acompletion / responses / aresponses`. O `guarded_llm` atual permanece apenas pós-chamada, e portanto não há teto preventivo operacional.
2. Conectar a reserva ao processo worker supervisionado **antes de cada rota** e provar que fallback, cópias de LLM, uso de ferramentas, reentrada e tentativas extras também estão bloqueados; testar sem fornecedor.
3. Com a escolha **separada** de provedor/modelo: verificar página oficial, versão tarifária, disponibilidade na conta, limites técnicos de input/output, max_output_tokens, possíveis tarifas adicionais e rate-limits sem divulgar credenciais.
4. Verificar orçamento com teto real exigível do provedor, se o usuário precisar limite monetário absoluto. Mesmo uma estimativa de pior caso pode falhar diante de cobranças ocultas, diferenças de tokenização ou provedor que não honre limites.
5. Só depois pedir autorização humana específica para chamada sintética real e custo concreto. Nenhum merge/deploy implícito.

## Testes e evidências

`tests/test_canary_budget.py` traz dez testes de configuração/tokenização declarada, custo estimado, reserva anterior à chamada, orçamento exato, liquidação, restrição de origem, expiração, concorrência e falha terminal. Simulação local de dez testes passou com stub compatível com o Guard existente; **somente a CI GitHub no HEAD exato valida a integração real contra o repositório**. A CI principal já descobre `test*.py`, sem instalar SDK nem usar LLM.

Histórico preservado em MEMORY e CANONICAL_STATE. A branch/PR não toca Canvas, VPS, Docker, OpenHands Core ou projetos atendidos. **NO-GO operacional continua.**
