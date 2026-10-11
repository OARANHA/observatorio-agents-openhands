# MEMORY — Observatório multiprojeto

## NORTE INEGOCIÁVEL
**OpenHands e Observatório são ferramentas horizontais da nossa operação de desenvolvimento. Não fazem parte do VIGIAFAST.**
**ChatGPT coordena → OpenHands executa missões autorizadas → Observatório visualiza atividades verificáveis → GitHub conserva código e documentação canônica.**
**VIGIAFAST, Wandora, ELUS e outros são projetos atendidos**, nenhum é dono das ferramentas. Confirmado repetidamente pelo proprietário; leia `docs/PROJECT_SOURCE.md` e `AGENTS.md` antes de discutir arquitetura.

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
`docs/PROJECT_SOURCE.md` → `AGENTS.md` → `docs/CANONICAL_STATE.md` → `docs/ARCHITECTURE.md` → estado real do código e integrações.

## Diagnóstico da equipe — integração local em 2026-10-11

Base GitHub reconciliada: `1fb8575bc55778130d8e8c6184e8939c54aa6bab`
(PR #8 integrada). Branch: `feat/observatorio-team-sdk-diagnostic-v1`.
O loader oficial SDK/Tools **1.53.0** carregou localmente as definições
Construtor/Verificador; preset `code-explorer` presente. Registry SDK vazio
antes/depois. **Nenhum agente registrado, executado ou delegado.**
20 testes unittest, diagnóstico estático/SDK, build e sintaxe JS aprovados.
Isso não comprova integração na sessão Canvas nem execução remota.
Relato histórico de OBS-TEAM-CANARY-001 veio do ZIP; MCP original não relido.
Evidências e limites: `docs/handoffs/OBS-TEAM-CANARY-001.md` e
`team/SDK_DIAGNOSTIC.md`. Catálogo segue não ativado; app instalado não atualizado.
Nenhum merge/deploy realizado. PR #7 do grafo continua separada.

## PR #9 — correção da revisão técnica em 2026-10-11

Revisão `5481728232` atendida a partir do HEAD `94d5123` na branch existente.
Validação estática reconhece o contrato restrito de seis campos, rejeita
chaves/ferramentas duplicadas, extras, sintaxe não suportada e iterações acima
12/10; confirmação permanece `always_confirm`. **27 testes aprovados**,
diagnóstico estático e loader local SDK/Tools 1.53.0 aprovados, build/sintaxe JS
preservados. Formato e limites em `team/SDK_DIAGNOSTIC.md`.
Não houve registro/delegação, mudança no runtime, merge ou deploy.
