# OBS-CYCLE-003 — continuidade factual

Referência: 2026-10-11 UTC. Repositório horizontal OARANHA/observatorio-agents-openhands.
**NO-GO operacional preservado.** Nenhuma chamada LLM, registro/delegação operacional, provedor, credencial de produção, deploy ou alteração de infraestrutura.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

Main inicial ebd967cad24603f06e08b5e141e7e9b7ac6fe34e; main reconciliada antes desta PR documental: 4c0f5f0f7559bbe8b2ab7476387fbe700894de9c. O SHA de integração desta própria documentação e suas CIs serão registrados na descrição da PR de fechamento, evitando referência circular ao próprio commit. PR #10 fechada sem merge, handoffs preservados. PR #7 draft intocada: HEAD 48f898d99a8979ef2c794513131506b028772666. PR #35 aberta, não instalada.

| PR | HEAD exato | Merge | CIs principal / SDK / adicional |
|---|---|---|---|
| [#34](https://github.com/OARANHA/observatorio-agents-openhands/pull/34) | 07f70bdec04d8a9e7c63a12f12722c5df3df4f9c | ef09e283ef27ad2b6aa02973cee71a27925b22c7 | 38153082909 / 38153082928 |
| [#35](https://github.com/OARANHA/observatorio-agents-openhands/pull/35) | 811d5fa4c48aa9eb2cf618174b7d645039a590ac | NÃO integrada | 38154748675 / 38154748638 / DOM 38154748641 |
| [#36](https://github.com/OARANHA/observatorio-agents-openhands/pull/36) | 23333c603e1ad122cf7e85b8a942006403b148a7 | 4c0f5f0f7559bbe8b2ab7476387fbe700894de9c | 38153945729 / 38153945715 |

Todos esses runs terminaram GREEN; logs completos examinados. Autorrevisões automatizadas, **não revisão independente**. Na #34 ocorreu desvio de ordem: o helper leu o aviso da API em vez do payload dos logs; merge ocorreu antes da inspeção efetiva. Logs reais confirmados depois (187 testes principal:161 PASS/26 skips opcionais; 120 dedicados sem skips). Retificação registrada na review 5483943978. Helper corrigido para exigir payload real com grupos de log antes de revisão/merge; #36 cumpriu a ordem correta. Não apresentar #34 como cumprimento integral pré-merge.

## Segurança e provas sintéticas

- #34: UTC canônico usa ASCII, rejeitando dígitos Unicode aceitos por regex/strptime. Sete métodos adicionados; oito subcasos RED corrigidos, calendários/UUID/receipts. TaskManager oficial caracterizado com pausa/saída parcial/erro e falha de close; cleanup pode pular eviction. Sessão nova aceita receipt antigo: prova de lacuna de restart, não de proteção persistente. Ver ../CYCLE003_SECURITY_FINDINGS.md.
- #36: inventário minimizado de nove distribuições via metadata, versões/hash, SDK/Tools 1.53.0 obrigatório; não importa dependências nem revela metadata inteira. Não é lockfile/SBOM completo. CI #36 registrou LiteLLM1.105.0/httpx0.28.1/httpcore1.0.9/aiohttp3.14.3/tenacity9.1.4/pydantic2.13.5/anyio4.12.1; não presumir versões transitivas iguais à inspeção local histórica LiteLLM1.103.4. LiteLLM tem reconstrução/reenvio de sessão fora do RetryMixin: teste sintético demonstra duas tentativas no transport e apenas uma chegada ao sink; Guard terminal nega a segunda. httpcore e aiohttp transport reais negados em namespace sem rede, sessions fechadas. Ver ../CYCLE003_TRANSITIVE_TRANSPORT.md.
- #36: 192 testes principal:164 PASS/28 skips SDK opcionais; runner SDK 125 testes dedicados sem skips relevantes. Zero LLM/registro/dispatch reais. Este fechamento não acrescenta código operacional.

## Produto visual

#35 reaplica o patch público da #7 sobre main em branch independente, preservando handoffs/segurança. IDs compostos por contexto local/conversa/projeto manual; hash não comprova tenant/RBAC. Oito contratos novos e seis baseline congelados. Build corrige substituição literal de tokens $, foco restaurado após rerender; pan por teclado/pointer limitado e reset sem comparação textual frágil.

CI final: principal 197 testes (169 PASS/28 skips SDK opcionais), SDK 125 dedicados sem skips, DOM seis cenários Chromium sandboxed PASS. Fixtures sintéticas: teclado/foco, busca/vazio, GET simulado/proveniência/erro, mobile/reduced-motion/zoom/pan/reset, escape/contraste pontual, teardown/remount. Screenshots no artifact graph-synthetic-screenshots do run 38154748641. Primeiro DOM 4 PASS/2 RED; segundo 5 PASS/1 RED; ambos corrigidos na mesma branch. O terceiro run 38154029442 foi GREEN, mas inspeção visual dos screenshots identificou sobreposição mobile: quarto run 38154748641 GREEN valida fluxo normal e assertions geométricas heading/toolbar/map. Screenshot final examinado confirma separação em390px. Artifact11708530687, ZIP SHA256 69cfd5df87cae8ac6b76052917abf01b6be2baf3bf4e844b05726e321d15e68e, expira2026-10-14; provas reproduzíveis no código/workflow, não confundir retenção temporária com arquivo persistente. Browser local ausente; download oficial falhou, sem reduzir sandbox.

Não comprovados: Canvas real, fonte autenticada, RBAC, teardown durante await, touch/lostpointercapture, contraste integral/zoom elevado, tablet581–870/suporte :has futuro/overlay consulta e isolamento de rede Chromium (interceptação Playwright não equivale a namespace). active/destroyed bloqueiam aplicação tardia, não cancelam GET em trânsito. **Não integrar #7 ou #35 nem instalar Canvas sem decisão específica.** Avaliação visual detalhada permanece na branch #35: docs/CYCLE003_VISUAL_EVALUATION.md.

## Matriz e decisões

G01 provado; G02–G04 provados offline; G05–G07/G10 parciais; G08 parcial documental (dossiê histórico, sem validação de conta); G09/G11 não provados; G12 bloqueado. P01 parcial; P02 RBAC não provado; P03 memória persistente não provada. P03 não significa acessibilidade: a associação em tabelas históricas P02/P03 com DOM era imprecisa e não promove memória.

Faltam revisor independente, ambiente futuro autorizado, proveniência/autorização confiável, replay persistente, inventário transitivo completo, cleanup resiliente e conta/modelo/rota/tarifa/quota segregados. Nenhum desses gates é fechado por mocks. Reutilizar Guard/BudgetBook/SDK oficiais existentes; não criar stack paralela ou reduzir controles.

Próximos trabalhos seguros: revisão independente do pacote e do diff #35; caracterização de teardown assíncrono/touch; testes adicionais de drift transitivo e cleanup. Decisões do proprietário: homologação/integração visual; aceite de riscos e provisionamento separado; somente depois, autorização explícita da missão operacional congelada. Quatro PRs úteis bastam; não criar incrementos artificiais.

## Prompt de retomada

Retome OARANHA/observatorio-agents-openhands. Leia PROJECT_SOURCE, AGENTS, ADRs/status, CANONICAL_STATE, MEMORY, ARCHITECTURE/README, matriz, pacote independente e este handoff. Reconcilie main e PRs #7/#35/fechamento antes de agir. Priorize revisão independente e lacunas offline de transporte/cleanup/teardown. Preserve NO-GO; não fazer merge #7/#35, instalar Canvas, usar credenciais ou executar LLM/agentes sem autorização específica. Consulte CIs pontualmente no HEAD exato, leia logs reais e registre autorrevisão como automatizada.
