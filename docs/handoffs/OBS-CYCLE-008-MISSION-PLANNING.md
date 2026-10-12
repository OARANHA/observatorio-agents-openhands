# CYCLE008-A — Contrato de missão planejada e fila sintética inerte

**Issue:** #46. **Base verificada:** `main` `5cedc0eada928fcd1f46cc50e2144d02822181be`. **Status:** candidata offline para revisão; PR Draft, sem merge. **Separada da PR #45** (Grafo Estelar V0.5.2).

## Autoridade e REUSE GATE

1. `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/decisions/ADR-0001-canvas-extension.md` (**Proposto**) → `docs/CANONICAL_STATE.md` → `MEMORY.md` → `docs/ARCHITECTURE.md` → `docs/GO_NO_GO_MATRIX.md`.
2. **Reusar, nunca duplicar executor:** `scripts/canary_controls.py` fornece `GateError`, `ALLOWED`, `Guard`, confirmação e supervisor restrito; `scripts/canary_sdk.py` integra `TaskToolSet`/SDK oficial (inicialização controlada); `scripts/canary_budget.py` calcula limites offline; `scripts/canary_evidence_session.py` tem anti-replay **efêmero** para evidência sintética; `scripts/canary_continuity_contract.py` bloqueia continuidade não aprovada. Estes componentes **não foram executados como agentes reais nesta PR**.
3. **Nova responsabilidade mínima:** `scripts/mission_plan_v1.py` apenas valida envelopes fechados e conta intenções planejadas **em memória**. Não cria agente, conversa, tarefa real, credencial, artefato operacional, publicação ou requisição de rede; nunca faz ligação automática issue → OpenHands.

## Formato `obs.synthetic.mission.plan.v1`

O arquivo `tests/fixtures/mission_plan_v1.synthetic.json` é um exemplo sintético e **não contém autorização**. Campos obrigatórios e fechados:
- `mission_id`: UUID opaco sintético, sem título, prompt ou identidade real;
- `source`: repositório GitHub, issue e SHA fixo da base, checados por igualdade literal ao escopo injetado;
- `objective_id=inspect_public_contracts`: intenção classificada, **não** uma instrução de agente;
- `classification=synthetic`, `state=planned`, `authorization=not_granted`, `operational_go=false`, `dispatch_allowed=false`;
- `tools`: 1–4 nomes exatos de comandos **já** permitidos no catálogo `canary_controls.ALLOWED`, sem novos comandos e sem duplicatas;
- `max_actions`: inteiro 1–6; `timeout_seconds`: inteiro 1–120; `retries=0`;
- `budget_usd=null`: **nenhuma** tarifa, conta, autorização ou limite financeiro real demonstrado;
- `evidence_id=null`: não fabricar prova; `redaction=deny_private_fields`, `retention=ephemeral_process_only`.

Estados **futuros conceituais**: `planned → approved → executing → verified|failed|blocked`. Somente `planned` é aceito aqui; os demais exigem gates, backend autorizado, evidência externa e revisão humana. **Nenhuma transição está implementada**.

O recibo `obs.synthetic.mission.plan.receipt.v1` traz somente `planned_offline`, contagem e flags `operational_go=false`, `dispatch_allowed=false`, `authenticity_proven=false`; não inclui ferramentas, credenciais, instruções, ID da missão nem qualquer prova falsa de execução.

## Regras de parada, testes e limites

- `SyntheticMissionPlanQueue` recebe fonte/issue/SHA validados, aceita no máximo 16 propostas locais (default 8), bloqueia IDs repetidos e encerra definitivamente a instância ao primeiro erro. O replay protection **some ao reiniciar processo**. Não é persistência nem autorização.
- Testes offline em `tests/test_mission_plan_v1.py`: ausência/elevação de autorização, falta de campos/extra fields, scope/SHA/issue divergentes, comandos não permitidos, action/time/retry limites, tipos bool indevidos, repetição/capacidade, concorrência idêntica, classificação live, redaction/credencial e configuração inválida. Não chamar SDK.
- Execução local proposta: `python -m unittest tests/test_mission_plan_v1.py` (ou `python -m unittest discover -s tests -p 'test_mission_plan_v1.py'`), sem Internet, sem credenciais, sem subprocesso de agente.
- Qualquer pedido para utilizar esses planos como fila real é **NEGADO** até que G05–G11 sejam demonstrados e G12 tenha autorização humana **específica** com objetivo, modelo, preço, credencial, custo, número de ações, escopo, rollback e evidência. Mesmo com CI GREEN, não liberar.
- Próximas tarefas #47/#48 são independentes e permanecem **planejadas**, não executadas.

## Superfície futura de aprovação (somente proposta)

Quando houver autoridade operacional, mostrar ao responsável: título curto da missão, repositório/SHA/issue verificados, ferramentas permitidas, limites reais auditados, impacto/dados, evidência requerida, cancelamento e opções **Aprovar**, **Recusar**. A UI não pode inferir aprovação de um clique em grafo ou do estado `finished` de uma conversa.

**GO/NO-GO:** G05/G06/G07/G10 PARCIAIS, G08/G09/G11 NÃO PROVADOS, G12 BLOQUEADO, P02/P03 NÃO PROVADOS. **NO-GO operacional.** Nenhum código aqui ativa trabalho de agentes.
