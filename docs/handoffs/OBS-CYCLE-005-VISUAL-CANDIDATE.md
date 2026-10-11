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
