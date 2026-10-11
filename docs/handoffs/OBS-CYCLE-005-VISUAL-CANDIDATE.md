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