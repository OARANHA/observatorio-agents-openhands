# CYCLE008-E — G07: escopo de comandos de uma missão (somente inerte)

**Data:** 2026-10-11 (Brasília) | **Base:** `main` `5cedc0eada928fcd1f46cc50e2144d02822181be` | **Issue:** #48.
**Estado:** implementação offline em PR Draft; **G07 permanece PARCIAL e G12 BLOQUEADO**.

## Autoridade, problema e REUSE GATE

Após `docs/PROJECT_SOURCE.md` → `AGENTS.md` → ADR-0001 (PROPOSTO) → `docs/CANONICAL_STATE.md` → `MEMORY.md` → `docs/ARCHITECTURE.md` → `docs/GO_NO_GO_MATRIX.md`:

- O `ALLOWED` existente em `scripts/canary_controls.py` inclui `pwd` e leitura de quatro arquivos públicos. A missão proposta em `docs/handoffs/OBS-CYCLE-008-FIRST-REAL-MISSION.md` permitiria **somente** `cat AGENTS.md`.
- O controle legado `confirm` e `mission_confirmation` exige aprovação humana por comando, usa `Guard` compartilhado e cancela terminalmente na primeira recusa. Contudo, o código não impunha uma lista exata **por missão** independente do avaliador humano.
- Não foi criado um autorizador, executor, fila ou SDK paralelo. `bind_mission_command_scope(guard, commands, approval)` encapsula o **callback existente** e retorna uma função para ser passada simultaneamente a `task_spec` e `terminal_tools` existentes. O `Guard` permanece o mesmo.
- Reutiliza `ALLOWED`, `Guard`, `MissionCancelled`, `GateError`, `TaskManager`/`TaskToolSet` e `TerminalTool`. Recusa comando globalmente conhecido mas fora do subconjunto, **antes** de chamar a aprovação humana, e cancela o Guard.
- Uma política inválida, vazia, mutável após o vínculo, com comandos repetidos/desconhecidos, ou aprovação ausente, falha fechada. A captura do subconjunto em `frozenset` impede que mudanças na lista fornecida ampliem a missão já vinculada. A aprovação continua sendo explicitamente `True`.

## Implementação estritamente sintética

- Novo `scripts/canary_command_scope.py`, independente de rede, provedores, LLM, browser, agentes ou persistência.
- Novo `tests/test_canary_command_scope.py`, sete cenários de contrato. No laboratório isolado do implementador, RED ocorreu por ausência do módulo e GREEN após implementação mínima: **7/7 PASS** com stub local de `Guard`/catálogo; essa prova local **não cobre SDK nem suite completa**.
- `scripts/probe_canary_worker.py` liga o novo callback à função `assemble_inert_tools` existente e tenta negar `cat team/catalog.json`: comando **globalmente permitido**, porém **fora do escopo** da missão. A prova SDK real com ferramentas *inertes* fica a cargo do workflow efêmero no novo HEAD; não foi reexecutada localmente.
- Saída do worker continua sem campos novos, com `actual_llm_calls=0`, `actual_agent_registrations=0` e `actual_task_dispatches=0`. Nenhum caminho operacional novo foi introduzido.

## Gaps e decisão

- **G07 PARCIAL:** o vínculo é opt-in; futuras integrações não podem chamar diretamente callbacks legados sem o novo escopo. É necessário comprovar ligação obrigatória à missão autorizada e o mesmo Guard em TaskManager/Terminal/worker real, além de limite total de **uma ação** no processo supervisor.
- `snapshot()` ainda copia a lista pública global; a candidata real deseja um único blob público. O controle do *subset* de comandos não é o controle físico do snapshot nem prova de que o processo não acessa outros arquivos montados.
- SDK 1.53.0, arquitetura do Canvas, G05/G06 isolamento/egress, G08/G09 modelo/preço/conta e G10 evidência operacional não foram validados por esta alteração.
- **G05/G06/G07/G10 PARCIAIS; G08/G09/G11 NÃO PROVADOS; G12 BLOQUEADO; P02/P03 NÃO PROVADOS; NO-GO operacional.**

**Sem agente real, SDK start/delegação, LLM, rede, credenciais, migração, deploy, merge, alterações de Canvas/VPS/Core/outros projetos.** CI e revisão independente somente após confirmação no HEAD exato. Sem polling contínuo.
