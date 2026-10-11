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

## PR #18 — reconciliação de resposta fictícia bem-sucedida (2026-10-11)

Main confirmada em `a21eb4e2250cf935de783b305f3d32d643bd0b1a`
(PR #17 integrada). Branch
`test/explorer-sdk-success-settlement-offline-v1` acrescenta
provas estritamente **offline** de sucesso nas quatro rotas SDK LLM
1.53.0 com stubs LiteLLM, namespace de rede negado, preço fictício,
métricas geradas pelo SDK e liquidação `BudgetBook` após verificação
independente em `Decimal`. Cobertura proposta: acumulação, ausência
de uso/custo, sobrecobrança e teto de tokens. **Cálculo sintético** no
teste substitui a função de tarifação LiteLLM; nenhuma tarifa real
ou limite efetivo de provedor foi certificado.
Handoff: `docs/handoffs/OBS-EXPLORER-SDK-SUCCESS-SETTLEMENT-001.md`.
CI no HEAD desta PR precisa ser conferida antes de qualquer parecer.
**NO-GO operacional**, sem inferência, merge automático, deploy,
registro/delegação, alteração de VPS, Canvas ou OpenHands Core.

## Precisão monetária sintética — 2026-10-11

Base `50009d1` (PR #18 integrada). Contexto Decimal independente e exato,
limites defensivos de representações e testes de sub-reserva implementados.
115 testes descobertos: 98 aprovados, 17 opcionais ignorados localmente.
CI/revisão do HEAD ainda por conferir; NO-GO operacional permanece.
Handoff: `docs/handoffs/OBS-EXPLORER-MONEY-HARDENING-001.md`.

## Vínculo de métricas por chamada — 2026-10-11

PR #19 integrada em main `91f8bed`, duas CIs e revisão favoráveis no HEAD exato.
Baseline agora vinculado à identidade de LLM/Metrics e geração de chamada,
cache não precificado negado antes do stub. 121 testes descobertos: 104
aprovados/17 opcionais ignorados localmente; CI deste incremento por conferir.
NO-GO operacional permanece. Handoff METRICS-BINDING-001 em docs/handoffs.

## Encerramento e liquidação sintéticos — 2026-10-11

PR #20 integrada em main `2e17e05`, ambas CIs e revisão favoráveis.
Book exige Guard único e reserva contra orçamento mais restritivo; limites
de chamadas de TokenCaps são efetivos. Uso verificado no último limite é
contabilizado uma vez antes do encerramento, sem ações seguintes. Erros
expirados mantêm reserva incerta. Local: 127 testes, 110 pass/17 opcionais skip.
CI/revisão deste HEAD por conferir. NO-GO operacional mantido.
Handoff TERMINAL-SETTLEMENT-001 em docs/handoffs.

## Ciclo offline autorizado — quarto incremento (2026-10-11)

PRs #19, #20 e #21 integradas sequencialmente com revisão adversarial
automatizada favorável e duas CIs GREEN no HEAD exato. Main `7323510`.
Permissão explícita do proprietário vale somente para os quatro incrementos
offline; não autoriza agentes/LLM, provedores, deploy ou infraestrutura.
Configuração nominal SDK comparada antes/depois da resposta fictícia; evidência
JSON mínima distingue gasto liquidado e hold incerto, sempre operational_go=false.
133 testes locais: 116 pass/17 opcionais skip; CI deste HEAD por conferir.
Histórico, runs e critérios NO-GO em handoff OFFLINE-EVIDENCE-001.
NO-GO operacional preservado; nenhuma integração operacional foi comprovada.


## Retomada noturna — matriz verificável (2026-10-11)

Main reconfirmada ba38f1a0dd29110c0b1dbbc7c0c0c51a07887510; PRs #19–#22
integradas, oito runs reconfirmados success no HEAD exato. PR #7 aberta/draft
em 48f898d99a8979ef2c794513131506b028772666, não integrar. PR #10 aberta;
seu handoff preservado. ADR-0001 continua Proposto. Anexo do proprietário
versionado em docs/GO_NO_GO_MATRIX.md com referências GitHub verificadas.
Nova autorização: até oito PRs estritamente offline, merges condicionados
a duas CIs e revisão adversarial registrada; não autoriza LLM/registro/
delegação/provedor/infra/deploy. NO-GO operacional mantido.
Workflow SDK inclui docs/memória/testes canary para evitar que PR documental
seja considerada elegível sem a segunda CI; testes existentes não removidos.
CI deste incremento ainda precisa ser comprovada no HEAD.


## Provas negativas de isolamento — preparação noturna (2026-10-11)

PR #23 integrada abc1997e7999a91e9a8c71933bb581437097ad51; CIs 38120273244
e 38120273294 GREEN, logs sem skips no SDK e autorrevisão registrada.
Suite de sandbox ampliada de seis para dez probes: DNS sem resolver do host,
socket Unix abstrato do host negado, FD herdável fechado pelo supervisor,
descendente com ambiente limpo/RO/DNS negado e tmpfs separado. Não muda
sandbox_argv nem allowlist. CI efêmera é obrigatória, sem skip/fallback.
Local: bwrap indisponível para namespaces; resultado RED não certifica
isolamento. Provas do novo HEAD ainda dependem do runner. NO-GO mantido.


## SDK superfície e rotas inertes — 2026-10-11

PR #24 integrada 05f88c1790b13c19e23a74fadc80cbaa22f0de23; CIs 38120541286 /
38120541272 e sandbox 38120541278 GREEN, dez probes reais sem skips,
autorrevisão registrada. Auditoria AST agora nega aliases LiteLLM extras,
imports duplicados, módulos renomeados e duplicação de método executável;
property getter/setter oficial preservado. REDs reproduzidos e corrigidos.
Baseline/settlement sintéticos negam streaming, cache, fallback, refresh hook
e extra_body antes do transporte ou após mutação, retendo hold incerto.
139 testes locais: 122 PASS/17 opcionais skip; AST no SDK 1.53.0: 12 PASS.
Não garante todo egress de dependências; CI do novo HEAD por conferir. NO-GO.


## Financeiro adversarial — 2026-10-11

PR #25 integrada em 2329f85123f04667bbd39ce1ce4a4021e3cbb9c2; CIs 38120804684
e 38120804699 GREEN, logs/revisão registrados. Negativas financeiras novas
reproduziram RED: saldo/contadores negativos financiavam reserva; custo com
zero tokens era liquidado. Invariantes agora são verificadas antes de reserva
e liquidação; uso zero mantém hold incerto e cancela, sem refund/retry.
Concorrência determinística: só uma reserva, segunda encerra missão inteira.
Métricas parciais negadas antes do stub; ausência de usage vira GateError.
144 testes locais: 127 PASS/17 opcionais skip. CI deste HEAD por conferir.
Proteção contra código hostil no mesmo processo continua fora da garantia.
NO-GO operacional mantido.


## Ciclo supervisionado inerte — 2026-10-11

PR #26 integrada d32483da5300c17d4e556c7f3b7d7166e196a32a, CIs 38121045562 /
38121045552 GREEN. Quatro cenários novos percorrem _run_task oficial com
conversa mockada, FakeLLM, Book/Guard compartilhados e terminal com saída
fictícia: leitura seguida de recusa, aprovação ausente, expiração durante
aprovação e última chamada global. Depois da parada nenhum novo stub ou
subprocesso roda; pause/close no finally, sem recuperação por task.set_error.
Nenhum Agent/Conversation real, start_task, TaskExecutor dispatch ou registro.
Contrato do pai rejeita bool como contador e campos extras potencialmente
privados antes de imprimir JSON (RED reproduzido). 149 testes locais: 128
PASS/21 opcionais SDK skip; manager oficial local: 6 PASS. CI por conferir.
Worker continua inerte; não certifica wiring operacional ou cgroup. NO-GO.


## Evidência sintética versionada — 2026-10-11

PR #27 integrada em dd441990b72fed8917a8bf9ec279ddb0a5f688ca; CIs
38121276910 e 38121276933 GREEN no HEAD ab157d165c8eeb998d10b79b9b50df056ff7e836,
logs e autorrevisão registrados. Esquema obs.synthetic.audit.v1 reutiliza
relatório contábil fechado; JSON limitado, campos/tipos estritos, duplicatas
negadas, hash canônico e origem SHA explicitamente declarada, não autenticada.
Oito testes novos: RED inicial (contrato ausente), GREEN após implementação.
157 testes locais: 136 PASS/21 opcionais SDK skip; SDK manager já comprovado
em CI. Sem persistência, assinatura, credenciais ou payload livre.
Ver docs/SYNTHETIC_EVIDENCE_SCHEMA.md. CI deste incremento por conferir; G10
continua parcial, G11 não provado e NO-GO operacional mantido.


## Fechamento documental noturno — 2026-10-11

REAL NOW: main b95ea8c44f9fe95ee24fdec6e32c2bea00c8451a confirmada após PR #28.
PR #10 permanece aberta HEAD f52b635290ba9e542e2bbb01a9d5a657fed11452;
PR #11 integrada; #7 aberta/draft, HEAD 48f898d99a8979ef2c794513131506b028772666.
Nenhum handoff foi removido. ADR-0001 continua Proposto. Observatório horizontal.
PROVEN EVIDENCE: seis PRs offline integradas, duas CIs GREEN no HEAD exato,
logs examinados e autorrevisões favoráveis registradas antes de cada merge.
| PR | HEAD exato | Merge confirmado | CI Observatorio | Canary Worker Inert SDK |
|---|---|---|---|---|
| [#23](https://github.com/OARANHA/observatorio-agents-openhands/pull/23) | `9c089f60b54c12b11a9397b82118093a9a9a9803` | `abc1997e7999a91e9a8c71933bb581437097ad51` | [38120273244](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120273244) | [38120273294](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120273294) |
| [#24](https://github.com/OARANHA/observatorio-agents-openhands/pull/24) | `37b75fcbf98e7e1408967bca61de33479cd49a4a` | `05f88c1790b13c19e23a74fadc80cbaa22f0de23` | [38120541286](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120541286) | [38120541272](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120541272) |
| [#25](https://github.com/OARANHA/observatorio-agents-openhands/pull/25) | `5bc943516af3faacd52d56ee6f0fccef51c7226f` | `2329f85123f04667bbd39ce1ce4a4021e3cbb9c2` | [38120804684](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120804684) | [38120804699](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120804699) |
| [#26](https://github.com/OARANHA/observatorio-agents-openhands/pull/26) | `c596aea62ff200e7025eaa9b0ac681ae23080cf8` | `d32483da5300c17d4e556c7f3b7d7166e196a32a` | [38121045562](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121045562) | [38121045552](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121045552) |
| [#27](https://github.com/OARANHA/observatorio-agents-openhands/pull/27) | `ab157d165c8eeb998d10b79b9b50df056ff7e836` | `dd441990b72fed8917a8bf9ec279ddb0a5f688ca` | [38121276910](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121276910) | [38121276933](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121276933) |
| [#28](https://github.com/OARANHA/observatorio-agents-openhands/pull/28) | `b4774202dad4a49c9bcacdaaf18a969a104cd69b` | `b95ea8c44f9fe95ee24fdec6e32c2bea00c8451a` | [38121795712](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121795712) | [38121795824](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38121795824) |

PR #24 tem também Sandbox Probe [38120541278](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38120541278), GREEN.
Suite atual: 157 testes, 136 PASS/21 opcionais SDK skip no Python sem SDK.
No runner SDK, 81 testes dedicados PASS, dez probes reais de isolamento PASS,
worker inerte com zero chamadas LLM, zero registros e zero dispatches reais.
Geração determinística/node --check/diagnóstico estático passam.

GAPS: G05/G06/G07/G10 permanecem PARCIAIS operacionalmente; G08 passa de
NÃO PROVADO a PARCIAL DOCUMENTAL, sem homologação de modelo/rota/conta.
G09/G11 não provados; G12 bloqueado. Dossiê público em
`docs/PUBLIC_PROVIDER_DOSSIER.md` e revisão estática em
`docs/GRAPH_PR7_REVIEW.md`. REUSE GATE: BudgetBook, Guard, supervisor e SDK/Tools oficiais preservados;
não recriar OpenHands nem transformar mocks em agentes operacionais.
DECISION: finalizar este ciclo com PR documental única para G/H/consolidação,
não criar oitava PR artificial. Seu próprio HEAD/CI/merge serão registrados
na revisão e descrição GitHub após verificação, sem antecipar resultados.
**NO-GO operacional permanece.** Próximos gates exigem ambiente autorizado,
modelo/rota/conta segregados, revisão distinta e autorização expressa da missão.


## Novo ciclo de engenharia offline — 2026-10-11

REAL NOW: main b0ce4333d8c5e4ce22e32f3ebc1aeba7d08c838f confirmada.
GitHub agora confirma PR #10 CLOSED, merged=false, closed_at 04:11:36Z,
HEAD f52b635290ba9e542e2bbb01a9d5a657fed11452. Notas anteriores sobre aberta
são históricas e superadas; PLAN-001 preservado. #7 aberta/draft HEAD
48f898d99a8979ef2c794513131506b028772666, excluída de merges.
PROVEN EVIDENCE: supervisor tinha reap sem timeout e erros crus de startup/
cleanup. Sete negativas/lifecycle reproduzem falhas e passam após correção;
reap agora limitado a 1s adicional, sem retries/output parcial/fallback.
GAPS: cleanup falho não prova processo encerrado; SDK _run_task finally é
sequencial, falha de metrics/pause pode pular close e substituir cancellation.
Teste oficial novo é obrigatório em CI; fonte disponível, executável do venv
local indisponível neste ciclo (não reivindicar teste SDK local).
165 testes locais: 143 PASS/22 opcionais SDK skip. NO-GO mantido.
REUSE GATE: Guard/Book/terminal/supervisor oficial e código existente.
DECISION: até seis PRs offline condicionadas aos gates; priorizar lifecycle,
egress auxiliar, auditoria/replay e contratos visuais. Não habilitar worker.
Handoff novo: docs/handoffs/OBS-ENGINEERING-OFFLINE-002.md.


## Egress auxiliares e respostas adiadas — 2026-10-11

PR #30 integrada em 84b48a3198daa8f3191522709eaa6aa4ace363b4, CIs
38144819354 principal, 38144819359 SDK e 38144819350 sandbox GREEN.
Logs SDK comprovam 7 supervisor/7 TaskManager sem skips; cleanup sequencial
oficial falho não reabre Guard, mas pode pular close (risco G07 preservado).
Gate de fakes agora rejeita Iterator/AsyncIterator/awaitable sem consumi-los;
três REDs→GREEN, hold incerto preservado. Novas provas HTTPx/urllib/SDK
model_info em threads/subprocess só serão comprovadas no netns do runner.
171 locais: 146 PASS/25 opcionais SDK skip. AST de fontes SDK disponível
em docs/SDK_AUXILIARY_EGRESS_INVENTORY.md; não certifica dependências.
G05/G06/G07 PARCIAIS. Sem provedor, credencial, registro/delegação. NO-GO.


## Sessão de evidências e pacote de revisão — 2026-10-11

PR #31 integrada f749f5918b86ab0ce6624d220e4354e2e69ef5d2. Runs
38145217813 / 38145217812 GREEN; logs SDK: 15 testes reais com stubs e
HTTP auxiliar/threads/filho e 3 deferred negativos PASS, nenhum provedor.
Consumidor SyntheticEvidenceSession reutiliza envelope v1: cap 1–64, SHA/
janela declarados, UUID/hash replay, tempo/finanças/counters regressivos
negados. Recusa/cap/receipt fechado são terminais. Oito testes: contrato
ausente RED; parada tardia no cap RED corrigida; 179 locais, 154 PASS/25
opcionais SDK skip. CI deste incremento pendente. Pacote em
docs/INDEPENDENT_REVIEW_PACKET.md: ameaças/checklists/conta/limites/revisão,
parada/revogação e autorização única; não provisiona nada. Sem autenticação
fictícia; replay só em memória, perdido no restart. G10 PARCIAL, G11 NÃO
PROVADO e G12 bloqueado. NO-GO operacional mantido.


## Fechamento offline do ciclo de engenharia 002 — 2026-10-11

Main inicial b0ce4333d8c5e4ce22e32f3ebc1aeba7d08c838f; PR #10 fechada
sem merge, handoff preservado. PR #7 permanece draft, HEAD
48f898d99a8979ef2c794513131506b028772666; não integrada ou instalada.
Três incrementos já integrados com SHA esperado, duas CIs e logs:

| PR | HEAD | Merge | CI principal / SDK |
|---|---|---|---|
| #30 | 5b9c8d3f2ed3f7b35496e3887374173260b5ec22 | 84b48a3198daa8f3191522709eaa6aa4ace363b4 | 38144819354 / 38144819359 |
| #31 | 79bac7d57a09cbe21b0c04dc514f9f1bd88842c6 | f749f5918b86ab0ce6624d220e4354e2e69ef5d2 | 38145217813 / 38145217812 |
| #32 | b1d27cc51cac4813bd18f948a473167b2ffb9574 | 70ab4b35a452660f13c9c6e50e38159b1a6c56bf | 38145670004 / 38145670090 |

Todas GREEN; sandbox adicional #30 run38144819350 GREEN. SDK sem skips
relevantes: 15 transport/stubs auxiliares; supervisor 7; TaskManager 7;
sessão sintética 8. Não houve registro/delegação/chamada LLM real.
Quarto incremento independente: fixture congelada de graphModel da #7,
extraída sem alteração e hashes declarados em tests/fixtures/. Seis testes
Node executam o modelo com entradas fictícias, sem DOM, host ou rede.
Preservam DEMO/manual/consultado, não inventam agente/sucesso e demonstram
colisão dos IDs entre vistas. Esse teste PASS caracteriza lacuna aberta,
não prova RBAC. Wrapper Python: RED por reporter Node variável; corrigido
com TAP explícito, sem enfraquecer assertions. Suite local: 180 testes,
155 PASS/25 SDK opcionais skip; mais 6 subtestes Node PASS. Geração e
sintaxe JS e diagnóstico estático válidos, sem ativação. CI deste quarto
incremento ainda pendente no momento desta documentação.

| Gate | Antes → depois | Prova adicional / limite mantido |
|---|---|---|
| G05/G06 | PARCIAL → PARCIAL | HTTP auxiliar negado no netns; inventário AST não cobre todas dependências/dynamic imports |
| G07 | PARCIAL → PARCIAL | kill/reap bounded e cancelamento terminal; cleanup sequencial oficial pode pular close |
| G10 | PARCIAL → PARCIAL | replay/ordem/cap em memória; hash não autentica, restart perde replay |
| G11 | NÃO PROVADO → NÃO PROVADO | pacote independente preparado; autorrevisões não são review independente |
| G12 | BLOQUEADO → BLOQUEADO | autorização específica de missão real ausente |
| P01 | PARCIAL → PARCIAL | contratos do modelo congelado testados; fonte autenticada não foi consultada |
| P02/P03 | NÃO PROVADO → NÃO PROVADO | colisões caracterizadas; DOM/RBAC/contraste/foco não homologados |

Demais gates sem promoção. NO-GO operacional preservado. Ver
docs/INDEPENDENT_REVIEW_PACKET.md para checklist executável offline e
campos da autorização futura: conta segregada, modelo/rota/tarifa/quota,
provisionamento/revogação, limites globais, parada/rollback, janela e
responsável. Nenhuma conta/credencial foi escolhida ou provisionada.
Navegador local indisponível; nenhuma instalação foi tentada. Sem deploy,
Canvas, infraestrutura, provider ou outros projetos. Revisões favoráveis
automáticas são autorrevisões, não certificação humana independente.
Quatro PRs úteis bastam: não criar duas artificiais para atingir seis.


## Ciclo 003 — correção de UTC sintético (2026-10-11)

Main reconciliada ebd967cad24603f06e08b5e141e7e9b7ac6fe34e; #33 integrada,
#7 aberta/draft HEAD48f898d99a8979ef2c794513131506b028772666 e #10 fechada
sem merge. Nova autorização até oito PRs offline; evolução visual isolada,
sem merge #7/Canvas. Envelope e janela admitiam dígitos Unicode via \d;
negativas RED→GREEN agora exigem ASCII. 187 testes locais:161 PASS/26 SDK
skip esperados; teste TaskManager PAUSED/close/hold aguarda runner dedicado.
Replay aceita receipt em instância nova: prova de lacuna, sem store criado.
Ver docs/CYCLE003_SECURITY_FINDINGS.md. G07/G10 parciais, G11 não provado,
G12 BLOQUEADO. Não houve agente/LLM/provedor/credencial ou mudança Core.


## Fechamento do ciclo 003 — 2026-10-11

Main pré-fechamento 4c0f5f0f7559bbe8b2ab7476387fbe700894de9c; #34/#36 integradas, #35 visual aberta e #7 draft intocada. CIs dos HEADs GREEN, evidência/limites e desvio de inspeção tardia dos logs #34 registrados em [OBS-CYCLE-003-CONTINUITY](handoffs/OBS-CYCLE-003-CONTINUITY.md). SDK/transportes reais só em provas inertes; DOM Chromium com fixtures na #35, sem instalar esta versão no Canvas. Autorrevisão automatizada não substitui G11. G12 BLOQUEADO/NO-GO; P03 memória persistente NÃO PROVADA. SHA do merge desta documentação na descrição da PR de fechamento.

## Ciclo 004 — continuidade inerte (2026-10-11)

Main inicial 242856c523b1880328b6bb985f6fcedf0a7c58c2; #7/#35 preservadas abertas.
Slack Wandora consultado; canal de aprovações criado para teste. Gatilho Work
recusado por vínculo do aplicativo oficial, sem tarefa criada/mensagem enviada.
Fontes SDK v1.53.0 e MCP públicas fixadas; MCP já possui events. Stop usa goal/stop,
sem prova de cancelamento de missão. Contrato sintético reutiliza Guard/book,
reserva fictícia, recusa terminal, zero dispatch; 9 negativas/concurrency verdes.
Ver [contrato/evidências](CYCLE004_CONTINUITY_CONTRACT.md) e
[plano](plans/OBS-CYCLE-004-PLAN.md). Código público não comprova API implantada,
tools expostos, autorização nem agentes operacionais. NO-GO/G12 bloqueado;
G11 e P03 sem promoção. Nenhum handoff anterior removido.

## Ciclo 004 — gateway fictício (2026-10-11)

#38 integrada, merge7c152857fae2859b6dc7cb8977ebb3cd6fa54eaf; duas CIs/logs antes
do merge, revisão automatizada registrada. Novo gateway em memória reutiliza
envelope/session v1: schema fechado, alertas enum DEMO, replay/gaps, lock e
incerteza terminal sem retry. Dez testes novos;211 locais/183PASS/28SDKskip.
Nenhum envio Slack/SDK/MCP, store ou servidor. Ver
[CYCLE004_GATEWAY_DESIGN](CYCLE004_GATEWAY_DESIGN.md). Restart perde replay;
origem não autenticada, estado sintético, sem exactly-once. G11/G12/P03 intactos.

## Ciclo 004 — Mentor DEMO separado (2026-10-11)

#39 integrada merge9e25aa67eea7a15b9d61ed7f249202644b9ee1d8, ambas CIs/logs antes
do merge. Mentor só em tools/mentor-demo: HTML independente, contexto revisável
por campos fechados, consentimento da simulação, recomendação fixa, sem envio.
Identidade local da PR35 reutilizada com hash/proveniência, sem integrar #35 ou
mudar extensão/Canvas. Node9PASS, Python213/185PASS/28SDKskip; DOM aguardando prova
runner. Ver [CYCLE004_MENTOR_DEMO](CYCLE004_MENTOR_DEMO.md). Sem ChatGPT presente,
autorização ao agente, RBAC comprovado ou recuperação de memória. NO-GO vigente.

## Fechamento CYCLE004 — eventos e mentoria (2026-10-11)

Handoff [OBS-CYCLE-004-EVENTS-MENTORSHIP](handoffs/OBS-CYCLE-004-EVENTS-MENTORSHIP.md)
consolida fontes oficiais fixadas, #38/#39/#40 e PR de documentação, HEADs/CIs/
logs/merges e limites. Slack Wandora consultado/aprovações de teste criado; Work
recusou gatilho por app oficial não reconhecido, nenhuma tarefa/mensagem/disparo.
MCP público já possui events; stop usa goal/stop; ambos sockets podem iniciar run.
Contratos/gateway/Mentor apenas sintéticos/inertes, sem patch MCP ou instalação.
Mentor DOM inicial4/5RED no focoTab, corrigido mantendo sandbox/testes; prova final
no handoff. Matriz GO/NO-GO atualizada sem promover G11/G12/P02/P03. #7/#35 abertas,
sem alterações; todos os handoffs preservados. SHA final da consolidação na PR.

#40 integrada96ed4a3c5ce659aa55a4841716e7623d30aaeb64, HEADb3ee40f...:3CIs
GREEN,213Python/185PASS/28SDKskip,125SDK/9Node/5DOMPASS semskip dedicado. Logs
reais e capturas fictícias examinados antes do merge; nenhuma instalação.
Main pré-consolidação96ed4a3c5ce659aa55a4841716e7623d30aaeb64.
