# OBS-EXPLORER-SDK-REAL-OFFLINE-001 — canário SDK real com transportes stubados e egress negado

Data: 2026-10-11.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

**Identidade:** Observatório de Agentes é projeto horizontal independente do VIGIAFAST/Wandora/ELUS, segundo `docs/PROJECT_SOURCE.md` e `AGENTS.md`. A ADR-0001 permanece **Proposta**.

**BASE:** `main` confirmada em `7a6fdc2faa1fc41ff8d4c1d5696c4b65b0ca641d`, correspondente à PR #16 integrada; PR #7 (grafo) continua independente. Esta branch é `test/explorer-sdk-real-offline-egress-v1`.

**EVIDÊNCIA PR #16:** SDK/Tools 1.53.0 instalado no runner efêmero, inventário AST dos quatro sinks LiteLLM e experimentos fake com reserva por tentativa e negação de retry/fallback aprovados. Isso não significou acionar a classe LLM real.

**GAP:** o SDK 1.53.0 contém retry de tenacity, fallback após cache muito pequeno, refresh 401, fallback de modelo e descoberta de metadados de roteamento potencialmente via HTTP. Wrapper público e auditoria AST não bastam para garantir limite de custo. Além disso, `max_input_tokens` está descrito na própria classe LLM como não aplicado diretamente no runtime.

**REUSE:** `SyntheticTransportGate`, `BudgetBook`, `Guard`, runner Bubblewrap/AppArmor, testes e SDK/Tools 1.53.0 já existentes. Não reimplementar SDK, não usar provedores ou alterar OpenHands Core.

**DECISION:** acrescentar apenas prova de **integração negativa no SDK real**, sob namespace de rede descompartilhado, com todo sink LiteLLM substituído por stub local antes da primeira chamada de teste. **NO-GO operacional mantido.**

## Como a prova funciona

1. `tests/test_sdk_real_transport_offline.py` instala temporariamente callbacks em **todos os quatro aliases LiteLLM importados no módulo SDK real**, nunca em um sistema em execução. No teste se constrói o objeto oficial `openhands.sdk.llm.LLM` usando nome de modelo público para acionar formatação e um marcador de credencial literal artificial (não uma chave utilizável). Nenhuma chamada remota é autorizada.
2. Antes de cada stub, o `SyntheticTransportGate` exige `logical_call` no mesmo dono de thread/task e reserva antecipada de pior custo com taxas **exclusivamente fictícias**. O stub sempre interrompe localmente por exceção sentinela ou `RuntimeError`; portanto **não existe resposta LLM bem-sucedida e não há custo verificado**.
3. Exercita os quatro métodos públicos reais (`completion`, `acompletion`, `responses`, `aresponses`) e confirma se um sink stubado foi alcançado uma única vez e reservado previamente. Um método real chamado **sem reserva** deve falhar antes do stub.
4. Nos casos condicionados, força as ramificações oficiais de fallback de cache e refresh 401 depois da primeira exceção sintética. A segunda tentativa deve ser barrada **antes** de alcançar outro stub. É evidência desses ramos de código **nessa versão** e **nesse teste**, não de todas as rotas HTTP nem de cobranças reais.
5. O workflow `.github/workflows/canary-worker-inert.yml` instala o SDK/Tools **1.53.0** em venv no GitHub runner efêmero e então executa a suíte num **novo namespace de rede** usando `bwrap --unshare-all`; o teste exige diferença entre o namespace do runner e o isolado, interfaces sem links externos e falha se o SDK não estiver instalado. `--clearenv`, sem tokens/cookies e `persist-credentials: false`. Não altera a VPS.
6. O teste monta a raiz da máquina efêmera em modo leitura para assegurar bibliotecas Python e certificados disponíveis; **isso não é isolamento estrito de sistema de arquivos ou de segredos do runner**. O namespace de rede é a fronteira de egress usada nesta prova; não inferir sandbox multi-tenant.

## Critérios de CI e bloqueios

O runner de contrato, sem SDK, pode registrar testes opcionais como **SKIP**; apenas o job específico SDK 1.53.0, com os **testes reais executados sem skips**, comprovará compatibilidade. Não afirmar GREEN antes de conferir o HEAD e os logs reais.

Mesmo que essa CI aprove, continuam não demonstrados:
- Interceptação de toda tentativa HTTP interna do **LiteLLM** e dependências (incluindo API de metadados, proxies, DNS, redirects e transportes não instrumentados). Egress foi negado somente no teste descartável, não no ambiente de produção.
- Sucesso de uma chamada LLM com métricas/telemetria reais, teto efetivo de entrada/saída, tarifas de provedor, taxas extras, quota financeira ou disponibilidade de modelo.
- Segurança do monkeypatch de aliases Python como mecanismo operacional: referências previamente capturadas podem contorná-lo. Para canário operacional, isolamento independente e verificação de rede + todas as saídas devem ser comprovados, e um provedor/conta/modelo autorizados pelo proprietário.
- Registro/delegação de subagentes, alteração no Canvas ou qualquer trabalho real.

**NO-GO para chamada LLM/registro/delegação/deploy.** Sem merge automático. A próxima decisão exige leitura de logs e revisão adversarial, autorização humana explícita para eventual merge, e gate separado para qualquer teste LLM real.

## Incidente CI da PR #17 — RED e correção revisável

No HEAD `529f332614927e1702028f3be24c62b0b35c80b7`, a CI principal `CI Observatorio` run `38114870538` terminou **success**. A CI `Canary Worker Inert SDK` run `38114870551`, job `114397660431`, terminou **failure** exclusivamente no passo `SDK real contra stubs isolados de rede`.

O log mostrou **4/5** testes offline aprovados. `test_real_sdk_refresh_path_must_not_dispatch_twice` falhou com `AssertionError` em `openhands.sdk.llm.llm.LLM._get_api_key_value`, ao verificar que o campo `api_key` era `SecretStr`. A causa imediata foi uma **incompatibilidade na fixture**: o mock `_resolve_refreshed_api_key` forneceu texto simples, mas o contrato real de `_auth_refreshed_llm` exige `SecretStr`. Isso ocorreu **antes** da segunda tentativa stubada; a falha não demonstra bypass real nem prova de que o segundo transporte seria bloqueado. A correção na mesma branch faz o refresh fake retornar `pydantic.SecretStr`.

Outra evidência: o import do LiteLLM dentro do namespace isolado **tentou acessar** `raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json`, e o DNS falhou devido à rede isolada. Logo, dizer que o SDK não tentou rede seria incorreto. A opção documentada `LITELLM_LOCAL_MODEL_COST_MAP=True` foi agora configurada **antes do import**, via `bwrap --setenv`, para usar o mapa embutido sem essa consulta; o teste exige a flag. Isso ainda **não prova** que todos os outros módulos do LiteLLM/OpenHands deixam de tentar rede nem que a tabela embutida vale como tarifa real.

**Status pós-correção:** exigir nova CI no HEAD atualizado, sem polling. Enquanto ela não for examinada, permanecer `RED anterior corrigido no código, validação pendente`. Sem merge, deploy, LLM nem agentes e **NO-GO operacional**.
