# OBS-EXPLORER-WORKER-INERT-001 — integração simulada do worker

Data: 2026-10-11.

## REAL NOW

- Repositório horizontal: OARANHA/observatorio-agents-openhands, não VIGIAFAST.
- Base reconciliada antes da branch: main `607a91f5fb88eb65b51cebd0db6941dc982dec00`; PR #12 integrada; PR #7 (grafo) permanece separada.
- Documentos canônicos lidos: PROJECT_SOURCE, AGENTS, ADR-0001 (status **Proposto**), CANONICAL_STATE, MEMORY, ARCHITECTURE, README e handoffs PLAN-001, GATES-001, SANDBOX-GHA-001.
- Provas anteriores: PR #12 passou seis testes isolados no GitHub Actions, após carregar perfil específico AppArmor do Bubblewrap no runner efêmero. Isso não prova execução de subagentes.

## REUSE GATE E DECISÃO

Reusar `canary_controls.py` (snapshot, Guard, confirmação, terminal restrito, supervisor), `canary_sdk.py` (TaskToolSet/TerminalTool/TaskAction) e as APIs oficiais SDK/Tools 1.53.0. Não criar um novo runtime OpenHands, não copiar o Explorer, não registrar agentes.

**GO somente para testes sintéticos de wiring e supervisão em GitHub Actions; NO-GO para tarefas LLM/delegação real, deploy ou alterações em VPS/Canvas/Core.**

## O que a PR implementa — código não é execução comprovada

- `scripts/probe_canary_worker.py` tem apenas os modos explícitos `--supervise-synthetic-worker` e `--synthetic-child`, sem modo operacional.
- Um processo controlador chama `supervise` para o worker inteiro, com ambiente vazio, stdin fechado, FDs fechados, grupo próprio e timeout de 60 segundos.
- No filho sintético: cria apenas quatro arquivos públicos artificiais, aplica `snapshot`, cria um Guard, monta o terminal oficial com `TerminalTool.create(executor=RestrictedExecutor())`, registra **somente a instância de ferramenta** no registry local do processo e exige que `resolve_tool` retorne a **mesma instância**. Não registra subagentes.
- Monta `TaskToolSet` pelo `task_spec` oficial, resolve seu `TaskTool` e valida que o `TaskManager` recebeu callback de aprovação ligado ao mesmo Guard.
- A única chamada real de terminal prevista é `cat AGENTS.md` sobre conteúdo sintético no Bubblewrap, autorizada pelo callback. O output bruto dos arquivos não é publicado no relatório, apenas um resumo estrutural.
- `explorer_action` constrói uma `TaskAction` nativa para code-explorer mas **não** chama `TaskExecutor`, `start_task`, `Conversation`, `run()` nem qualquer API de LLM.
- A confirmação negativa sintética dispara `MissionCancelled` e testa que novas ações de terminal e reserva de LLM são impedidas. Contagem esperada de chamadas LLM/registro de agente/delegação real: zero.
- `tests/test_canary_worker_wiring.py` verifica supervisão, não utilização de fallback e identidade da ferramenta. Testes opcionais do `TaskManager` oficial são reaproveitados.

## CI planejada e limites

Workflow `.github/workflows/canary-worker-inert.yml`: runner `ubuntu-24.04`, permissões `contents:read`, checkout sem credenciais persistidas, AppArmor perfil restrito do Bubblewrap, venv efêmero SDK/Tools == 1.53.0, até 15 minutos. Nenhum token de provedor, segredo de cliente, registro remoto de agente, deploy ou chamada LLM.

**A aprovação da CI depende dos logs do HEAD exato.** Qualquer falha em import/assinatura/registro do SDK, sandbox, callback ou supervisor resulta em RED e manutenção de NO-GO. Não transformar erro em skip.

Mesmo se GREEN, a prova termina no **wiring inerte** e não valida ciclo de delegação real, vazamento por APIs não observadas, limites preventivos de custo, disponibilidade do modelo, tokens máximos ou sandbox contra todos os ataques. Próximo gate exige implementação controlada do worker operacional, orçamento preventivo e autorização humana separada.

Histórico documental anterior preservado; nenhum merge ou deploy autorizado por esta PR.
