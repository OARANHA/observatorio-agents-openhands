# CANONICAL_STATE — Observatório de Agentes

## REAL NOW — última reconciliação da base em 2026-10-10/11
- Repositório: `OARANHA/observatorio-agents-openhands`.
- `main` lida antes desta PR de documentação: `7212c51c38fc34cd195afb4db99ee35808e67cb5`, resultante do **merge da PR #5**.
- Manifesto da versão **0.4.2**; app do Canvas via `host.registerPage`, UI Shadow DOM com WebGL2/fallback 2D.
- Evidência trazida pelo usuário: screenshot de **Apps** mostrou Observatório v0.4.2 habilitado, `Ref: 7212c51c38fc34cd195afb4db99ee35808e67cb5`. Outro screenshot mostrou, no Canvas, `OBSERVATÓRIO · Missão consultada`, uma lua real, UUID `69009100-f867-4032-ad17-9023e24ae4ee`, `finished`, origem/horários e **0 agentes comprovados**.
- Evidência independente anterior via MCP: a conversa sintética `OBS-REAL-001` retornou `finished` e a resposta `OBS-REAL-001|OK` para operações de leitura simples. Não afirmar que o frontend recebeu essa resposta final.
- Evidência trazida pelo usuário: em **Configurações → Contexto do agente**, a memória persistente foi ativada e a UI apresentou “Configurações salvas”. **Não houve prova de gravação, recuperação ou isolamento por projeto**; conversas antigas podem requerer reinicialização.
- Quatro sistemas originais do universo (VIGIAFAST, Wandora, ELUS, OpenHands Lab) continuam cenários **DEMONSTRATIVOS**; sistema `OBSERVATÓRIO` aparece após GET pontual de UUID e não persiste após reload.
- Sem descoberta de missões automática, monitoramento contínuo, grafo Obsidian operacional, agentes reais identificados, inventário multi-projeto verificado, controle de execução pela UI ou RBAC multi-tenant comprovado.

## IDENTIDADE E FRONTEIRAS — regra canônica
Consulte `docs/PROJECT_SOURCE.md` e `AGENTS.md`.
**ChatGPT coordena → OpenHands executa tarefas autorizadas → Observatório exibe o que for verificável → GitHub registra histórico e decisões**.
**VIGIAFAST e demais produtos são PROJETOS ATENDIDOS; não são donos, camadas-base ou sinônimos de OpenHands/Observatório.**
Nenhuma memória do OpenHands ou conteúdo dos projetos deve ser compartilhado transversalmente sem controle de escopo.

## PROVEN EVIDENCE x GAPS
- **Comprovado**: `main` da PR #5; CI do HEAD pré-merge aprovada; extensão 0.4.2 habilitada no screenshot; leitura manual de conversa real `finished` visível no Canvas; memória ativada nas configurações do usuário.
- **Não comprovado**: runtime atualizado automaticamente, correlação missão→agente, vínculo projeto validado no servidor, sucesso semântico de tarefas, memória recuperável em sessão posterior, grafo vivo, acesso de observação a todos os projetos.
- O projeto informado no formulário da consulta de conversa é **declaração manual**, não resultado autenticado da API.

## ROADMAP — não é estado presente
1. Refinar painel de consulta e geometria/legibilidade da lua (propostas).
2. Investigar contratos de leitura, identidade/projeto e permissões antes de ativar descoberta multiprojeto.
3. Projetar modo **Grafo** estilo Obsidian como vista adicional do Observatório, apenas com nós e arestas rastreáveis.
4. Avaliar memória nativa OpenHands após teste sintético de escrita e recuperação; **não duplicá-la** como recurso específico do VIGIAFAST.

## GATES
- Consultar estado atual e reutilizar o que funciona. Branch + PR + testes.
- Sem merge/deploy automáticos, sem acesso a dados reais de clientes, sem alterações em VPS, Docker, OpenHands Core ou projetos atendidos sem autorização separada.
- Documento vivo mantém decisões e evidências **com data**; não tratar notas históricas de propostas como estado atual.

## Diagnóstico da equipe — integração local em 2026-10-11

Base GitHub reconciliada: `1fb8575bc55778130d8e8c6184e8939c54aa6bab`
(PR #8 integrada). Branch: `feat/observatorio-team-sdk-diagnostic-v1`.
O loader oficial SDK/Tools **1.53.0** carregou localmente as definições
Construtor/Verificador; preset `code-explorer` presente. Registry SDK vazio
antes/depois. **Nenhum agente registrado, executado ou delegado.**
20 testes unittest, diagnóstico estático/SDK, build e sintaxe JS aprovados.
Isso não comprova integração na sessão Canvas nem execução remota.
Relato histórico de OBS-TEAM-CANARY-001 veio do ZIP; MCP original não relido.
Evidências e limites: `docs/handoffs/OBS-TEAM-CANARY-001.md` e
`team/SDK_DIAGNOSTIC.md`. Catálogo segue não ativado; app instalado não atualizado.
Nenhum merge/deploy realizado. PR #7 do grafo continua separada.

## PR #9 — correção da revisão técnica em 2026-10-11

Revisão `5481728232` atendida a partir do HEAD `94d5123` na branch existente.
Validação estática reconhece o contrato restrito de seis campos, rejeita
chaves/ferramentas duplicadas, extras, sintaxe não suportada e iterações acima
12/10; confirmação permanece `always_confirm`. **27 testes aprovados**,
diagnóstico estático e loader local SDK/Tools 1.53.0 aprovados, build/sintaxe JS
preservados. Formato e limites em `team/SDK_DIAGNOSTIC.md`.
Não houve registro/delegação, mudança no runtime, merge ou deploy.

## Preparação do primeiro canário Explorer — 2026-10-11

PR #9 integrada à main `789d442e586466ee7085a1724028d7e1edba7ec0`,
confirmada por Git e metadados GitHub. Snapshot local separado/limpo preparado
nesse SHA. SDK/Tools 1.53.0: descoberta oficial code-explorer (terminal),
registry vazio antes/depois, 27 testes e diagnóstico estático aprovados.
**Nenhum registro, delegação ou tarefa LLM foi iniciado.**
Plano: `docs/handoffs/OBS-EXPLORER-CANARY-PLAN-001.md`.
Execução bloqueada até definir modelo/tarifas/credencial autorizada e homologar
isolamento, callback de confirmação e limite global. bwrap falhou localmente;
worktree não é sandbox. Orçamento/iterações do SDK têm limites documentados.
Aguardará autorização explícita após apresentar condições concretas.
Nenhuma mudança no Canvas/VPS/Core ou projetos atendidos; sem merge/deploy.

## Gates do primeiro Explorador — 2026-10-11

Main reconciliada em `789d442e586466ee7085a1724028d7e1edba7ec0` (PR #9 integrada).
PR #10 preservada aberta. Branch independente `feat/explorer-canary-gates-v1`
implementa controles e adaptadores oficiais SDK/Tools 1.53.0, com 45 testes
locais e construção inerte de specs. Nenhum agente, registro ou delegação
operacional, LLM, merge ou deploy. **NO-GO operacional**: bwrap e unshare
falham neste ambiente; sandbox efetivo, wiring completo do worker e tarifas/modelo
com orçamento preventivo ainda exigem prova. Evidências e critérios cumulativos:
`docs/handoffs/OBS-EXPLORER-CANARY-GATES-001.md`.

## PR #11 — parar a missão na primeira recusa (2026-10-11)

Revisão `5481809830`: False no TaskManager 1.53.0 rejeita a ação e chama run
novamente. Callback oficial e executor agora cancelam o Guard compartilhado
e lançam MissionCancelled, que sai do fluxo recuperável do SDK. Testes com
manager oficial/conversas mockadas comprovam um único run e limpeza no finally;
nenhuma chamada LLM ou ação adicional após recusa nos testes simulados.
52 testes descobertos: 50 aprovados e 2 opcionais ignorados sem SDK; os dois
opcionais aprovados no SDK/Tools 1.53.0 isolado. Não houve execução operacional.
As notas e o handoff PLAN-001 da PR #10 foram preservados nesta branch antes
de GATES-001; a branch #10 permanece intacta. Main continua `789d442`.
NO-GO mantido pelos gates de sandbox, worker completo e orçamento preventivo.
Detalhes, limites e ordem de integração humana em
`docs/handoffs/OBS-EXPLORER-CANARY-GATES-001.md`.


## Preparação do worker sintético OpenHands — 2026-10-11

Após o merge da PR #12, `main` foi reconfirmada em
`607a91f5fb88eb65b51cebd0db6941dc982dec00`. Seis provas
de Bubblewrap/AppArmor passaram no runner GitHub Actions, mas só para o
escopo isolado testado; não autorizaram inferência.
Branch `test/explorer-worker-wiring-inert-v1` prepara a PR #13,
sem mudar Canvas, VPS ou OpenHands Core. O worker **sintético**
usa SDK/Tools 1.53.0 para resolver TaskToolSet e a instância oficial do
terminal restrito, e invoca bwrap com dados artificiais. A TaskAction
code-explorer é apenas construída, nunca enviada ao TaskExecutor.
Novo workflow independente precisa de prova GREEN no HEAD exato antes
de qualquer conclusão. Limites e procedimento em
`docs/handoffs/OBS-EXPLORER-WORKER-INERT-001.md`.
**NO-GO** para registro de agentes, delegação real e qualquer LLM;
modelo, tarifas, orçamento preventivo e autorização continuam ausentes.

## Reserva preventiva offline do canário — 2026-10-11

Após o merge da PR #13, main foi conferida em `cf4a429fde6e8b4aecd7c1001166ee13f2d755c4`.
Branch `feat/explorer-offline-budget-gate-v1` prepara cálculo preventivo
com `Decimal`, exigência de fonte tarifária revisada, limites de tokens,
exatidão do modelo SDK e bloqueio de gasto de pior caso antes da chamada.
Testes usam exclusivamente tarifas fictícias e nenhum LLM. Documentação:
`docs/handoffs/OBS-EXPLORER-BUDGET-OFFLINE-001.md`.
**O novo `BudgetBook` ainda não foi conectado ao `guarded_llm`**; só provas
offline podem ser reivindicadas até a CI do HEAD exato. Modelo/provedor
autorizados, preços oficiais e limites do provedor ainda estão pendentes.
NO-GO operacional; sem merge, deploy, VPS ou Canvas nesta preparação.


## BudgetBook nas quatro rotas simuladas — 2026-10-11

Main reconfirmada antes do slice em `b16a1eddaa852ee92716a0162f09106ee73b4335`
(PR #14 integrada). A branch `feat/explorer-budget-sdk-boundary-mock-v1`
acrescenta adaptador **exclusivamente para classes LLM fictícias** nos nomes
oficiais `completion/acompletion/responses/aresponses` e vincula reserva
prévia `BudgetBook`, `Guard` e reconciliação de métricas. Recusa de
classe OpenHands LLM real é explícita; nenhum modelo, provedor ou preço
operacional foi homologado. O SDK v1.53.0 contém caminhos internos de
segunda tentativa não inteiramente cobertos pelo wrapper público; **NO-GO**
operacional continua, mesmo com CI verde. Testes e escopo:
`docs/handoffs/OBS-EXPLORER-BUDGET-SDK-MOCK-001.md`.
Nenhum merge/deploy/chamada LLM nesta preparação.

## Tentativas internas SDK/LiteLLM — preparação da prova sintética (2026-10-11)

Base reconciliada em `main` `8e008325bb59562369b0a0e69a017eda3123eb89`
(PR #15 integrada). Branch `test/explorer-sdk-transport-attempts-v1`
investiga os quatro aliases LiteLLM na fonte SDK 1.53.0 e o tráfego
auxiliar de metadados (`resolve_provider_metadata_sync` /
`aresolve_provider_metadata`). Testes sintéticos exigem uma única
tentativa de transporte por escopo lógico, reserva prévia e cancelamento
ao primeiro retry/fallback/concorrência. Auditoria AST do SDK instalado
deve falhar se a superfície nominal mudar. Essa prova **não cobre**
egress real, chamadas dinâmicas ou caminhos internos do LiteLLM; o módulo
novo recusa o SDK real e não é um mecanismo de produção.
Handoff: `docs/handoffs/OBS-EXPLORER-SDK-TRANSPORT-ATTEMPTS-001.md`.
A CI desta branch ainda precisa ser validada por logs do HEAD exato.
**NO-GO operacional** até controle independente de rede, teste SDK com
transporte stubado, modelo/tarifas/tokens e autorização específica.
Nenhuma chamada LLM, merge, deploy ou alteração na VPS/Canvas/Core.

## SDK 1.53.0 real com transporte fictício e egress negado — 2026-10-11

Base reconciliada: main `7a6fdc2faa1fc41ff8d4c1d5696c4b65b0ca641d`
(PR #16 integrada). Branch `test/explorer-sdk-real-offline-egress-v1`
propõe PR #17: invocar métodos públicos reais da classe SDK LLM 1.53.0
com quatro aliases LiteLLM stubados, compartilhando reserva preventiva
`SyntheticTransportGate`/`BudgetBook`. CI do runner SDK executará
os testes dentro de Bubblewrap com `--unshare-all` e verificará
namespace de rede separado, sem segredos, chamada a provedor ou LLM.
Falha ao tentar sem reserva e ao retornar para transporte em fallback
de cache/refresh (cenários induzidos). O modelo nominal nos testes é
identificador público com credencial artificial não válida; não executa
inferência. O namespace não é sandbox multi-tenant, e os testes
não cobrem todos os egress internos/HTTP de dependências nem validam
tarifas/tetos. Critérios e limites em
`docs/handoffs/OBS-EXPLORER-SDK-REAL-OFFLINE-001.md`.
**CI por comprovar no HEAD; NO-GO operacional**. Sem merge, deploy
ou alteração de VPS/Canvas/OpenHands Core nesta preparação.

## Correção do RED — SDK real com stubs (PR #17, 2026-10-11)

No HEAD `529f332614927e1702028f3be24c62b0b35c80b7`, CI principal
GREEN, mas workflow SDK run `38114870551` RED: quatro testes SDK offline
passaram e o caso refresh-401 falhou em `_get_api_key_value` porque
o mock devolveu `str` em vez de `pydantic.SecretStr`. O LiteLLM
também **tentou** baixar o mapa de custos durante import, bloqueado
pela rede descompartilhada. A branch da PR #17 foi corrigida para
`SecretStr` fake e `LITELLM_LOCAL_MODEL_COST_MAP=True` antes do import
via bwrap. CI do novo HEAD pendente; não alegar GREEN antecipadamente.
Handoff: `docs/handoffs/OBS-EXPLORER-SDK-REAL-OFFLINE-001.md`.
**NO-GO** para LLM/registro/delegação/deploy/merge implícito.

## Segunda falha CI da PR #17 — compatibilidade de coleta sem SDK (2026-10-11)

HEAD `6dfac7b9b3769005c3c3c563cb8ce74faf425e40`:
SDK runner `38115115662` GREEN, com 6/6 testes reais de método SDK
em transporte stubado/namespace isolado. CI principal `38115115652`
RED: `ModuleNotFoundError: No module named 'pydantic'` ao importar
`tests/test_sdk_real_transport_offline.py`. O runner principal
intencionalmente não instala SDK/Pydantic. Ajustado import de
`SecretStr` para ocorrer apenas junto da importação opcional do SDK.
Revalidar o HEAD posterior antes de merge. Contexto:
`docs/handoffs/OBS-EXPLORER-SDK-REAL-OFFLINE-001.md`.
**NO-GO operacional**.
