# OBS-CYCLE-005 — candidata V0.5.1 do grafo (offline)

2026-10-11. **PROPOSTO / PR DRAFT / NO-GO operacional**.

## REAL NOW / PROVEN EVIDENCE
- Main congelada para esta branch: `e06d3b01e60d9a5503e046dc0fe2eeb269f0e403` (PR #42 integrada). PR #35 em `811d5fa4c48aa9eb2cf618174b7d645039a590ac` e PR #7 em `48f898d99a8979ef2c794513131506b028772666`, ambas preservadas, sem merge.
- Reutilizados 12 arquivos visuais, testes e workflow da PR #35 sobre a main; arquivos comuns não tinham alterações adicionais na main desde o ancestral da #35 (verificado por SHA blob).
- Build original da #35 reproduzido byte a byte usando o algoritmo `scripts/build.mjs`. O gerado desta candidata ainda precisa CI no HEAD exato.
- Alterações locais: rótulos/legenda legíveis no mobile, pointerId primário e lostpointercapture no mapa, 2 cenários adicionais de Chromium (390px e GET liberado após teardown).

## GAPS / REUSE GATE / DECISION
- Rótulos DEMO/manual/GET por UUID mantidos distintos; projeto digitado é manual; `finished` não indica êxito nem agente associado. Identidade `local-view-not-tenant` é hash de visualização, **não RBAC**.
- Requisição GET pendente pode continuar na camada host; o teste só prova que não atualiza DOM desmontado. **Não afirmar cancelamento de rede**.
- Validar CI principal, SDK inerte e Graph DOM no HEAD; inspecionar logs e screenshots. A CI da PR #35 não homologa a candidata. Nenhuma CI deste commit foi observada ou declarada verde.
- Revisar mobile 390px/tablet/desktop, Shadow DOM, Canvas real, WebGL2/fallback, foco, Escape, pan, touch, zoom, reduced-motion, contraste e rollback somente sob autorização apropriada.
- ADR-0001 ainda Proposto; G11 independente não provado, G12 bloqueado, P02 RBAC não provado, P03 memória não provada. Mentor DEMO #40 permanece standalone na main. **Não realizar merge, instalação, deploy, agentes/LLM, VPS/MCP/Core ou automações**.

## Inspeção da CI e screenshots da candidata inicial (2026-10-11)
- HEAD anterior `e06f0539ee033a372b54b50bc07c5c556bfadbfc`: CI Observatorio run `38167440233` GREEN (218 testes Python: 190 PASS/28 skip SDK opcionais); Canary Worker Inert SDK run `38167440226` GREEN (125 testes dedicados em grupos; zero agente/LLM/dispatch real); Graph DOM Offline run `38167440241` GREEN (8/8, zero skip).
- Teste CLI que imprime `error: one of the arguments ... is required` é negativo esperado `test_no_implicit_run_mode`, registrado `ok`; não foi falha de job.
- A inspeção visual do artefato `11711998610` (390px) revelou `DEMONSTRAÇÃO` quebrado em duas linhas nos quatro nós DEMO, defeito não coberto pelo teste anterior. Capturas offline, não Canvas instalado.
- Correção subsequente na própria PR draft: rótulo sucinto `DEMO` preserva classificação explícita e cabe em uma linha, mantendo legendas/proveniência; teste Chromium confere quatro nós, texto e altura de uma linha. **Requer nova CI e nova revisão do screenshot no HEAD corrigido**.
- Não usar GREEN anterior para aprovar o HEAD corrigido; **NO-GO** operacional e G11/P02/P03 inalterados. Sem autorização de merge/Canvas.

## Passagem adversarial com JEV — preparação de revisão do HEAD a94d269c614d059879b367546a91f1856a312177 (2026-10-11)

**Natureza:** JEV typesafe `jev-1.13.0` é árbitro consultivo probabilístico, **não** revisor independente e não promotor do gate G11. A consulta anterior ao ciclo de correção classificou próximo passo como `block` 0,56 (confiança 0,41), e objetivo de integração como `incomplete` 0,64 (confiança 0,46); são julgamentos consultivos, não métricas objetivas de defeitos.

Nesta passagem foram submetidos **trechos reais do HEAD**, e o `jev_select_context` priorizou: origem/identidade 0,86, consulta GET 0,89, desmontagem 0,66, mobile 0,72, testes/rede 0,82. `jev_guard_action` considerou aceitável preparar **somente** patch reversível em branch e documentação (`allow` 0,67, confiança 0,56). Decisão final permaneceu sob política determinística/proprietário.

**Constatações de código (não inferidas exclusivamente do JEV):**
- Confirmado: CSS mobile tinha `max-width:105px;overflow:hidden;text-overflow:ellipsis` herdado do viewport intermediário e truncava `SIMULAR: CALMO`. A tela corrigida usa textos separados: desktop `SIMULAR: [estado]`, mobile `DEMO: [estado]` e `aria-label` completo. Novo teste Chromium sintético verifica os estados após clique, dimensões e overflow em 390px.
- Contrato `host.agentServer.request(GET /api/conversations/{UUID})` usa projeto declarado manualmente. Nomeação visual como “missão real” merece cautela: retorno da conversa **não** comprova execução/sucesso semântico nem vínculo autorizado; manter P02 NÃO PROVADO. Orientar o revisor a verificar textos de proveniência antes de Canvas.
- O `active=false` impede que GET tardio altere DOM desmontado no caso testado; não aborta request da camada host nem valida cancelamento de transporte.
- Fixture de navegador força fallback2D, não atesta WebGL2 real, dispositivo touch físico, tela leitora, Canvas autenticado ou sandbox do host. Contraste testado é pontual.
- O workflow do HEAD anterior `a94d269c614d059879b367546a91f1856a312177` comprovou 3 CIs GREEN (CI Observatorio `38167894448`, Graph DOM `38167894440` 8/8, Canary Worker `38167894511`), sem chamadas LLM/agentes reais; **esses resultados NÃO homologam o novo commit**.

**PENDÊNCIAS:** CI no novo HEAD, screenshot atualizado e análise de revisor distinto (G11). `ADR-0001` PROPOSTO, G12 BLOQUEADO, P02/P03 NÃO PROVADOS. Sem merge, deploy, Canvas, OpenHands ou credenciais.

## Remediação fatiada do parecer Codex — slice A1/A2 (2026-10-11)
- Codex, em sessão separada e somente leitura, examinou HEAD `1567c386f9326607aae31d36de0d59e156b66d24`: 5 achados P2 (A1–A5), 1 P3 (A6), nenhum P0/P1 demonstrado. Parecer geral **CORREÇÕES NECESSÁRIAS**; segunda revisão automatizada não basta para G11.
- JEV `jev-1.13.0` consultivo: recomendação `split_task` probabilidade 0,54 (confiança 0,39); preflight de remediação reversível `allow` probabilidade 0,75 (confiança 0,67); **não aprovação operacional**.
- **A1 P2 abordado:** antes de cada nova consulta, a observação existente e relações derivadas são retiradas da UI. Erro de API, contrato inválido ou entrada inválida não deixam a informação anterior parecendo atual. Novo teste sequencial GET sucesso → GET negado exige grafo sem nós consultados/manuais.
- **A2 P2 abordado:** Lua e painel usam `conversa consultada` e `estado recebido`, jamais `execução verificada`; teste de `execution_status='idle'` exige rótulos de conversa.
- **A3/A4/A5 P2 continuam PENDENTES nesta fatia:** prazo e cancelamento/ignorância de GET tardio, rollback quando montagem falha, gestos touch. Não afirmar correção sem código/testes específicos. **A6 P3 continua PARCIAL**; fixture Chromium força fallback2D.
- CI anterior do HEAD `1567c386f9326607aae31d36de0d59e156b66d24`: `38169408157`, `38169408183` 9/9, `38169408172` GREEN. Esses runs **NÃO validam o HEAD desta remediação**. São esperados 11 testes Chromium após as duas adições, a confirmar pelo runner.
- **G11 não provado, G12 bloqueado, P01 parcial, P02/P03 não provados. NO-GO operacional.** Sem merge/deploy/Canvas.

## Ciclo 005 — remediação A3/A4/A5 após 11/11 Chromium GREEN (2026-10-11)

- HEAD anterior `0ebb942c7e13199381966d96ed1e4be4e6f2d77d` conferido no GitHub: CI `38172263276` (218 Python, 28 SDK skips), Graph DOM Offline `38172263290` (**11/11**), SDK inerte `38172263281` GREEN; logs indicam zero operações LLM/agente/dispatch. Estes runs valem **somente para o HEAD anterior**.
- A3: prazo de **10 segundos na UI** com `Promise.race`, feedback de timeout, botão reabilitado, rejeição local na desmontagem e prevenção de atualização tardia. A requisição `host.agentServer.request` **não é cancelada no transporte**; suporte `AbortSignal` do host não comprovado. Teste adversarial com relógio sintético.
- A4: pré-checagem de `crypto.randomUUID`/`subtle.digest` antes de anexar e limpeza em erro síncrono depois do append (disposer leitura, RAF, observer, listener, DOM). Testes de nonce indisponível e falha do `ResizeObserver`.
- A5: `touch-action:pan-y pinch-zoom` no mapa; preserva pan vertical/pinch nativos previstos pelo CSS e pan teclado, com teste CSS/sintético. **Não testado em touchscreen físico**.
- A6: mais quatro testes DOM, total **15** esperados. Runner ainda força fallback2D, não valida WebGL2/Canvas instalado, leitor de tela ou autenticação tenant.
- Passagem JEV `jev-1.13.0` aconselhou `confirm` (0,62; confiança 0,49); histórico de autorização do proprietário cobre apenas patch na PR, nenhum merge/deploy/Canvas. Próxima CI e inspeção dos logs no **novo HEAD** aguardam aviso `green`/`red`; **não realizar polling**.
- ADR-0001 PROPOSTO, G11 NÃO PROVADO, G12 BLOQUEADO, P01 PARCIAL, P02/P03 NÃO PROVADOS. Sem agente/LLM real, VPS/MCP, deploy, Canvas ou merge.

## Acabamento de proveniência após screenshot da CI — 2026-10-11
- HEAD anterior `0b6ccf879f92cc4691cacbe977db67fb58f07a6f` verificou 3 GREEN (CI `38173719969`, DOM `38173719965` **15/15**, SDK inerte `38173719983` com zero operações reais). Captura do Graph DOM revelou instrução herdada `CONSULTA DE MISSÃO REAL` e texto `consulta real do OpenHands`; são claims semânticos acima da prova de consulta do estado da conversa.
- Correção visual/textual limitada: `Consultar conversa`, `estado de conversa consultado`, instrução `CONSULTA DE CONVERSA`, placeholder e ARIA precisos, sem mudar endpoint, RBAC, identity, timeout, WebGL ou motor do grafo. Contrato DOM de proveniência adicionado (16 testes Chromium esperados no novo HEAD).
- **GREEN anterior não valida o novo commit.** Retornar a PR ao Codex em sessão separada para reavaliar A1–A6 após nova CI. Revisão automatizada não promove G11. ADR-0001 PROPOSTO; G12 BLOQUEADO; P01 PARCIAL; P02/P03 NÃO PROVADOS. Sem merge/deploy/Canvas.

## Segunda revisão Codex — R1/R2/R3, remediação proposta em branch (2026-10-11)
- Codex em **segunda sessão de revisão automatizada** examinou HEAD `83957b69dfe3e35e87e4ba6a12b7768004187012`, tree `32fcfa47b13a61bfff333fdc8b5413230fbecade`. Parecer: **CORREÇÕES NECESSÁRIAS**, sem P0/P1 demonstrados; R1 e R2 P2, R3 P3. Reproduziu Python 218 (190 PASS/28 SDK skip), Node 23 PASS, build byte-a-byte; Chromium local não rodou por sandbox; confiou apenas no status público das runs, não nos logs. Nossa sessão já havia verificado os logs desse SHA; não confundir proveniências.
- Código analisado confirmou R1: timeout cobria GET, não `await onVerified`/WebCrypto, permitindo UI desabilitada e atualização tardia. Correção: `Promise.race` agora abrange GET e digest da identidade; `pending.valid` funciona como guarda de atualização, é desativado no timeout, no teardown e no `finally`. O callback só materializa dados se vigente. **Não cancela a requisição host nem o digest pendente.** Teste Chromium: digest sintético pendente → timeout → liberação tardia sem render.
- Confirmou R2: `wrapper.querySelectorAll` não atravessava Shadow DOM. Correção: `shadow.querySelectorAll('canvas')` no caminho de rollback. Teste negativo simula GPU com `WEBGL_lose_context` no ShadowRoot antes da falha de ResizeObserver; testa liberação explícita, não WebGL real nem garantia do GC.
- R3: `canvas-extension.json` + instrução de grafo vazio + métrica de Universo e painel sem conversa usam **conversa consultada**, não missão/execução real. Teste de manifesto, métrica pós-consulta e filtro vazio.
- JEV `jev-1.13.0` aconselhou `deep_review` 0,34 com confiança muito baixa 0,12; preflight de patch reversível `allow` 0,57, confiança 0,43. Juízo consultivo, não aprovação humana.
- A1 continua coberto em teste sucesso→negação; A2 textual agora inclui R3; A3 timeout abrange processamento, mas cancelamento de host não comprovado; A4 rollback prova mock ShadowRoot, não liberação WebGL física; A5 CSS/touch físico permanecem distintos; A6 cobertura em fixture. Esperados **19 testes Chromium** no novo HEAD; **CI ainda NÃO executada/verificada**. Não promover GREEN anterior.
- **G11 NÃO PROVADO, G12 BLOQUEADO, P01 PARCIAL, P02/P03 NÃO PROVADOS; ADR-0001 PROPOSTO.** Sem merge, Canvas, deploy, OpenHands real, credenciais ou infra.

## Fechamento efetivo da PR #43 e ponte CYCLE006 (2026-10-11)
- Pós-parecer Codex: R1, R2 e R3 resolvidos nos cenários revisados; sem novos defeitos comprovados. Testes do último HEAD `f50109d5c73c9d8e027ac9ad15ba0472e184283a`: `38175631445` (190/218 Python, 28 skip), `38175631434` (19/19 Chromium), `38175631527` (SDK inerte, zero operações reais), todos `success` e logs inspecionados. JEV consultivo considerou rodada offline concluída; não substitui G11.
- Proprietário **autorizou especificamente merge da PR #43 sem deploy/Canvas**. GitHub confirmou merge commit `ac9c525a7e169fe253f0f488550686491939289a`, árvore `4fa1490b4a6ea2984701e5a52dc70003abe2ac63`, `main` atualizada, PR fechada/merged.
- Última evidência histórica de instalação no Canvas é V0.4.2; versão/estado atual e homologação da V0.5.1 no Canvas **não comprovados**. PRs #35 e #7 ainda abertas.
- Plano seguinte apenas documental: `docs/handoffs/OBS-CYCLE-006-CANVAS-VISUAL-HOMOLOGATION-PLAN.md`, com gates H0–H4 e matriz V01–V12. **Nenhuma instalação, GET, login remoto, operação de agentes/LLMs ou alteração de infraestrutura foi executada** por este plano; G11 não provado, G12 bloqueado, P01 parcial, P02/P03 não provados.
