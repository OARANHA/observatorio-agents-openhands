# CYCLE008-B — Evidências read-only com proveniência fechada (offline)

**Data:** 2026-10-11 (Brasília) | **Issue:** #47 | **Base congelada:** `main` `5cedc0eada928fcd1f46cc50e2144d02822181be`.
**Status:** candidato em PR Draft separada; não integrado, instalado nem operacional.

## Autoridade e REUSE GATE

1. `docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/decisions/ADR-0001-canvas-extension.md` (**PROPOSTO**) → `docs/CANONICAL_STATE.md` → `MEMORY.md` → `docs/ARCHITECTURE.md` → `docs/GO_NO_GO_MATRIX.md` → `docs/INDEPENDENT_REVIEW_PACKET.md`.
2. `source/observatorio-v02.html` já usa consulta opt-in via `host.agentServer.request(GET /api/conversations/{UUID})`. `graphIdentityForObservation` e `validGraphIdentity` distinguem projeções DEMO/manual/consultado; não atestam vínculo tenant/repositório nem resultado.
3. `scripts/canary_evidence_session.py` implementa janela, SHA declarado, lock, replay e parada terminal para **contabilidade sintética**. `scripts/canary_audit_bundle.py` valida o envelope sintético, não autenticidade externa. `scripts/mission_plan_v1.py` está em PR #49 independente, não integrada, e nunca despacha.
4. `scripts/evidence_read_contract_v1.py` não replica supervisor, SDK, fila, autorização ou BFF. É uma projeção somente de fixtures para UI, acrescentando invariantes de proveniência não presentes nos contratos contábeis; não importa SDK nem faz rede ou I/O.

## Contrato v1 e recusa por padrão

- Envelope fechado `obs.synthetic.evidence.read.v1` com `classification=synthetic`, `source={repository,base_sha,issue}`, `record_id` UUID, `subject_id` digest opaco de fixture e `observed_at_utc` em janela declarada. O digest **não** autentica a fonte e não deve ser calculado com dados pessoais reais.
- `DEMO`, `PLANNED`, `CONSULTED`, `MANUAL` e `INFERRED` são estados sintéticos distintos; `VERIFIED` é **reservado e rejeitado**. `CONSULTED` com `canvas_get_fixture` **não prova GET real**; `MANUAL` e `INFERRED` mantêm relação `manual_unverified` ou `inferred_unverified`. `finished` é só estado de uma conversa ilustrativa, **não sucesso da tarefa**.
- Entradas e projeções exigem `authenticity_proven=false`, `agent_identity_proven=false`, `task_success_proven=false`, `operational_go=false`, `dispatch_allowed=false`; `authorization=not_granted`, `redaction=metadata_only`, `retention=ephemeral_process_only`.
- Projeção `obs.synthetic.evidence.view.v1`: somente tipo, estado, relação, UUID de fixture, digest local (não assinado) e flags falsas. Não devolve payload original, prompt, saída LLM nem `subject_id`.
- Campos extras, spoofing de repo/SHA/issue, tempo fora da janela, ordenação temporal regressiva, repetição por ID, digest ou assunto/instante, capacidade e qualquer promoção de `VERIFIED` recusam e fecham a instância. Replay é **somente em memória**, perdido no restart; a janela e o SHA são informados pelo chamador e não atestados pelo servidor.

## Testes e limites

- Fixture `tests/fixtures/evidence_read_v1.synthetic.json` vinculada ao SHA histórico e à Issue #47, sem dado de cliente ou credencial.
- Executar offline: `python -B -m unittest discover -s tests -p 'test_evidence_read_contract_v1.py' -v`. Nove testes isolados verificam classificação, permissões negadas, `finished != sucesso`, schema fechado, SHA/issue/repo, replay, janela temporal, concorrência, capacidade e ausência de imports de execução.
- Esses testes locais não validam toda a suíte CI nem a API do Canvas. O frontend e OpenHands não foram alterados. Hash local não é assinatura, `CONSULTED` em fixture não é consulta real, P02/RBAC multi-tenant e integridade operacional continuam **NÃO PROVADOS**.

## Decisão

G05/G06/G07/G10 = **PARCIAIS**; G08/G09/G11 = **NÃO PROVADOS**; G12 = **BLOQUEADO**; P01 **PARCIAL**, P02/P03 **NÃO PROVADOS**; ADR-0001 **PROPOSTO**. **NO-GO operacional**.

PR #45 (visual) e PR #49 (missões planejadas) permanecem independentes; nenhuma instalação Canvas, merge, VPS, SDK Core, agente, LLM, credencial ou custo real foi usado. Para evidência operacional, exigir origem confiável, autorização server-side por projeto e revisão independente antes de desenhar BFF real.
