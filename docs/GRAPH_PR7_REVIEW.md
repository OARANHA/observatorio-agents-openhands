# PR #7 — revisão estática separada do ciclo SDK

Data: 2026-10-11. [PR #7](https://github.com/OARANHA/observatorio-agents-openhands/pull/7)
aberta/draft, HEAD `48f898d99a8979ef2c794513131506b028772666`.
[Autorrevisão automatizada registrada](https://github.com/OARANHA/observatorio-agents-openhands/pull/7#pullrequestreview-5482290665).
Não equivale a review independente, homologação visual ou instalação.
Não foi feito merge, deploy, acesso ao Canvas nem consulta de conversa real.

## Contratos encontrados no código

`graphModel()` separa nós DEMO, fonte/conversa consultada e projeto manual;
arestas fonte→conversa e conversa→projeto têm proveniências diferentes.
`safe()` escapa dados exibidos, `finished` não cria sucesso semântico ou
identidade de agente. Reutiliza a consulta pontual existente via host Canvas,
sem descoberta, polling ou API paralela de inventário.

## Lacunas e critérios de aceitação

| Tema | Achado estático | Evidência futura necessária |
|---|---|---|
| Terminologia | Manifest descreve grafo operacional; breadcrumb chama mapa operacional | Texto refletir leitura pontual de conversa e estados demonstrativos, sem implicar agentes ativos |
| Identidade horizontal | `real-origin`, `real-mission`, `manual-project` são IDs locais de uma vista; nome do projeto é abreviado para exibição | Identidade autenticada de fonte/tenant/repositório/conversa, independente do rótulo e sem colisão entre projetos |
| RBAC | Sessão do host autoriza consulta; vínculo com projeto é declaração, não autorização segregada | Contrato read-only por projeto/tenant, negação cruzada, erro sem criação de nó real e ausência de bypass de permissões |
| Foco e teclado | Clique recria `graph-surface.innerHTML`, removendo o botão focado; painel já tem `aria-live="polite"` | Teste DOM de foco após seleção/filtro/zoom, keyboard-only, resultado vazio e anúncio sem duplicação |
| Acessibilidade visual | CSS/labels existem; testes atuais inspecionam strings | Medir contraste, zoom, largura estreita, nomes/estado selecionado e navegação num navegador com fixtures públicas fictícias |

Não afirmar ausência de aria-live: a região lateral já o possui. Sua presença
não certifica anúncio correto ou preservação de foco. Estas lacunas não são
bugs operacionais demonstrados no Canvas; são riscos e provas faltantes.

A API GitHub reportou `mergeable=false` numa consulta posterior ao avanço de
main; `git merge-tree --write-tree` entre refs locais então atuais produziu
árvore limpa. A divergência de metadados não autoriza merge nem afirma
conflito confirmado. Reconciliar refs/CI na retomada própria da PR #7.
Não houve resolução de conflitos ou alteração da branch visual neste ciclo.

Decisão: P01 PARCIAL, P02/P03 NÃO PROVADOS. Aprovação específica do proprietário
continua necessária para merge da #7 e qualquer alteração no Canvas instalado.
Próxima frente segura: fixtures DOM e contratos de identidade/proveniência,
sem implantar backend RBAC fictício nem declarar memória persistente pronta.


## Provas de modelo congelado — ciclo 002

Seis contratos Node em tests/graph_model_contract.mjs executam apenas
graphModel, snapshot HEAD48f898d99a8979ef2c794513131506b028772666.
Fixture/proveniência em tests/fixtures/pr7_graph_model*; SHA256 da origem
e extração declarados, não assinatura/autenticação remota. Inputs fictícios.
Sem observação: cinco nós/quatro arestas DEMO; com observação sintética:
fonte→conversa consultada e conversa→projeto manual distintos; finished
não gera agente/success; IDs resolvem dentro da vista. Conversas/projetos
distintos reutilizam IDs, comprovando lacuna multiprojeto. Nada alterado
na #7 ou no runtime da main. Contratos caracterizam baseline, não homologam
HEAD futuro da #7. DOM/foco/teclado/contraste não testados: navegador ausente.
PR #7 continuou aberta/draft na reconciliação, mergeable=true então; estado
histórico divergente acima não determina autorização. P02/P03 NÃO PROVADOS.
