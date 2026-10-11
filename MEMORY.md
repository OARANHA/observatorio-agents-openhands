# MEMORY — Observatório multiprojeto

## NORTE INEGOCIÁVEL
**OpenHands e Observatório são ferramentas horizontais da nossa operação de desenvolvimento. Não fazem parte do VIGIAFAST.**
**ChatGPT coordena → OpenHands executa missões autorizadas → Observatório visualiza atividades verificáveis → GitHub conserva código e documentação canônica.**
**VIGIAFAST, Wandora, ELUS e outros são projetos atendidos**, nenhum é dono das ferramentas. Confirmado repetidamente pelo proprietário; leia a ADR-0002 antes de discutir arquitetura.

## O que existe de fato
- OpenHands Agent Canvas v1.26.0 mostrado em screenshot; app Observatório 0.4.2 instalado/habilitado, ref `7212c51c38fc34cd195afb4db99ee35808e67cb5` (PR #5 integrada).
- Primeira prova real: `OBS-REAL-001` consulta UUID `69009100-f867-4032-ad17-9023e24ae4ee`, `finished`, lua visível; **0 agentes individualmente identificados**. Vínculo ao projeto digitado pelo operador, não autenticado como associação.
- Cenários de VIGIAFAST, Wandora, ELUS e OpenHands Lab na UI continuam demonstrações, não operadores implantados.
- Memória persistente ativada em Configurações → Contexto do agente do Canvas; configuração salva conforme print, **sem teste de persistência/recuperação/segregação ainda**.

## Direção
- Evoluir a experiência astronômica para **Universo + Grafo interativo estilo Obsidian**, com nós/conexões de fontes reais. Grafo operacional vivo é **objetivo**, não estado atual.
- Memória nativa OpenHands é auxiliar, **distinta da documentação canônica de cada projeto**, sem pressupor sincronização; não recriar memória isolada para VIGIAFAST.
- Não inventar agentes/atividades, não fazer merge/deploy automaticamente, não expor dados reais ou misturar escopos de projetos.

## Retomada
`docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/decisions/ADR-0002-horizontal-operations.md` → `docs/CANONICAL_STATE.md` → `docs/ARCHITECTURE.md` → estado real do código e integrações.
