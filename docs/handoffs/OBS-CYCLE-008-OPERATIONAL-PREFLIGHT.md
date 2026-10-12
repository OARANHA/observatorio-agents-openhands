# CYCLE008-C — Pré-voo independente do primeiro agente OpenHands

**Issue:** #48 | **Data da avaliação:** 2026-10-11 (Brasília)
**Base auditada:** `main` `5cedc0eada928fcd1f46cc50e2144d02822181be`.
**Decisão:** **NO-GO**. Este documento NÃO habilita, registra, despacha, provisiona nem autoriza agentes.

## Fontes, reuso e limites de prova

Autoridade: `docs/PROJECT_SOURCE.md` → `AGENTS.md` → ADR-0001 (**PROPOSTO**) → `docs/CANONICAL_STATE.md` → `MEMORY.md` → `docs/ARCHITECTURE.md` → `docs/GO_NO_GO_MATRIX.md` → `docs/INDEPENDENT_REVIEW_PACKET.md`.

REUSE GATE — antes de adicionar infraestrutura:
- `scripts/canary_controls.py`: `ALLOWED`, `Guard`, confirmação/cancelamento terminal, `snapshot`, `sandbox_argv` e `supervise`. Os comandos efetivamente previstos incluem `pwd` e leitura `cat` de quatro arquivos públicos; não há um executor operacional autorizado.
- `scripts/canary_sdk.py`: contrato SDK/Tools **1.53.0**, `TaskToolSet`, `task_spec`, `terminal_tools` e `explorer_action` com `code-explorer`. `guarded_llm` sozinho não controla todo egress do SDK/dependências.
- `scripts/probe_canary_worker.py`: exercício de registry/ferramenta terminal/TaskManager oficial **somente em ambiente sintético**, sem `start_task` real, agente registrado nem LLM.
- `scripts/canary_budget.py`: `RateCard`, `TokenCaps`, `BudgetBook` e `Decimal`, dependentes de modelo, tarifas e caps efetivos antes de qualquer modo live.
- `scripts/canary_continuity_contract.py`: continuação inerte; não executa, não retoma agente e conserva reservas incertas.
- `scripts/canary_evidence_session.py` e `scripts/canary_event_gateway.py`: evidência/gateway **sintéticos**, replay apenas em memória, sem persistência, autenticação ou entrega Slack real.
- PR #49, ainda Draft na avaliação: `SyntheticMissionPlanQueue` é proposta offline `authorization=not_granted`, nunca executor. PR #50, separada, contém proposta de metadados sintéticos para a Issue #47; não autentica projetos.
- Contratos oficiais TaskManager/TaskToolSet foram caracterizados em testes e arquivos atuais; sua presença **não** representa delegação operacional autorizada. Nenhum orquestrador paralelo ou BFF fictício será criado.

## Matriz de evidências — não elevar gates por CI

| Gate | Estado | Evidência verificada no código/documentação | Prova ainda exigida para GO | Responsável/gate humano |
|---|---|---|---|---|
| **G05** isolamento | PARCIAL | `sandbox_argv` com bwrap/unshare; probes de runner isolado documentados em `docs/GO_NO_GO_MATRIX.md` | isolamento rede, caminhos, descendentes, namespaces/FDs, segredos e stdout no ambiente real específico; snapshot RO mínimo | responsável pelo ambiente + revisor |
| **G06** retries/egress | PARCIAL | `guarded_llm`, `SyntheticTransportGate`, auditorias AST, mocks HTTP/stream descritos no pacote de revisão | egress negado na rede de execução, redirects/imports/hook/streaming, reentradas e caminhos auxiliares reais | revisor distinto |
| **G07** supervisor | PARCIAL | `Guard`, `mission_confirmation`, `supervise`, `task_spec`, `terminal_tools`, worker inerte | provar herança do mesmo Guard, confirmação exata, subset de comandos, cancelamento/killpg/reap e cleanup em processo operacional; resultado tardio | operador + revisor |
| **G08** modelo/preço | NÃO PROVADO | `PUBLIC_PROVIDER_DOSSIER.md` traz pesquisa pública; `RateCard` sintético | seleção expressa de provider/modelo/snapshot/rota, disponibilidade, token bounds, tarifa efetiva incl. cache/thinking/extras e orçamento preventivo validado | proprietário + financeiro |
| **G09** conta/segredo/quota | NÃO PROVADO | nenhuma conta, credencial ou quota operacional confirmada | identidade não produtiva segregada, canal secreto, spend/rate cap efetivos, prazo e procedimento de revogação testado sem expor chave | proprietário + operador de segurança |
| **G10** trilha íntegra | PARCIAL | `canary_audit_bundle`, `SyntheticEvidenceSession`, contratos de read-only sintéticos | origem e autorização autenticadas; link único missão→execução→issue/SHA, clock confiável, hashing assinado/protocolo de retenção/replay e acesso RBAC | custodiante + revisor |
| **G11** revisão | NÃO PROVADO | CI e autorrevisões automatizadas não satisfazem revisão distinta | parecer independente no HEAD/ambiente/modelo/permissões e aceite explícito dos riscos residuais | revisor distinto + proprietário |
| **G12** canário real | BLOQUEADO | nenhum despacho operacional autorizado nesta tarefa | G05–G11 demonstrados cumulativamente e autorização **específica e posterior** para missão congelada; sem auto-merge ou auto-execução | proprietário |

**Portas de produto:** P01 PARCIAL; P02/P03 NÃO PROVADOS. Um grafo visual e um `finished` não são prova de sucesso, associação autenticada, RBAC nem memória funcional. ADR-0001 permanece PROPOSTO.

## Testes offline reproduzíveis, sem despacho

- Suite principal: `python3 -B -m unittest discover -s tests -p 'test*.py' -v`. Necessidades de SDK/bwrap ficam restritas a runners efêmeros e configuração explícita; skips opcionais não homologam operação.
- Verificações de canário **somente inerte**: `scripts/probe_canary_worker.py` e os workflows existentes, com contadores `actual_llm_calls=0`, `actual_agent_registrations=0`, `actual_task_dispatches=0`. Os sucessos históricos permanecem associados ao SHA exato da PR de origem, não são retestados automaticamente por este documento.
- Um teste negativo crítico ainda a preparar: fornecer ação `cat team/catalog.json` à missão proposta com subset exclusivo `cat AGENTS.md`. **A allowlist global atual permitiria esse comando:** uma política *por missão* comprovada deve negá-lo, mesmo sendo globalmente permitido. Não executar esse teste em trabalhador operacional.
- Outro teste negativo: simular recusa após um output fictício e assegurar que não haja segunda execução, entrega tardia nem sucesso inferido pelo estado da conversa.
- Nenhum teste desta PR de documentação é prova nova de isolamento real. Nenhuma CI nova foi consultada ou promovida para GO.

## Riscos residuais e critério de parada

1. LLM/LiteLLM egress indireto fora do wrapper, streaming/retries, refresh e tasks auxiliares não completamente homologados.
2. Controladores atuais têm parte do estado somente em memória; reinício desfaz replay e não demonstra identidade.
3. Limites locais não asseguram cobrança e bloqueio efetivo de conta; um cap nominal pode exceder por latência no provedor.
4. Worker futuro requer subset por missão mais estrito que `ALLOWED`, herança de Guard e supervisão de descendentes.
5. Visualização não tem autoridade para aprovar comandos ou inferir sucesso.
6. Parada: primeira recusa, incerteza de custo/uso, erro de verificação/egress, deadline ou falha de cleanup encerram a missão; sem retry ou resume. Se kill/reap falhar, registrar término como **não comprovado** e escalar ao operador; revogar identidade segregada e verificar descendentes e artefatos sob política autorizada.
7. Não publicar logs brutos, saída de ferramentas, prompts, chaves, sessões ou dados de cliente no GitHub.

**Recomendação técnica:** manter NO-GO; exigir os ensaios de subset de comando, cadeia de prova e ambiente efêmero antes de qualquer autorização de canário. Não criar fila nova: aproveitar SDK/TaskManager oficial após gate. Ver missão candidata separada em `docs/handoffs/OBS-CYCLE-008-FIRST-REAL-MISSION.md`.

**Sem merge, deploy, instalação Canvas, VPS, Docker, OpenHands Core, credenciais, agente ou LLM real nesta PR.**
