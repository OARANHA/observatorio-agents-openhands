# CANONICAL_STATE — Observatório de Agentes

## REAL NOW — última reconciliação da base em 2026-10-10/11
- Repositório: `OARANHA/observatorio-agents-openhands`.
- `main` lida antes desta PR de documentação: `7212c51c38fc34cd195afb4db99ee35808e67cb5`, resultante do **merge da PR #5**.
- Manifesto da versão **0.4.2**; app do Canvas via `host.registerPage`, UI Shadow DOM com WebGL2/fallback 2D.
- Evidência trazida pelo usuário: screenshot de **Apps** mostrou Observatório v0.4.2 habilitado, `Ref: 7212c51c38fc34cd195afb4db99ee35808e67cb5`. Outro screenshot mostrou, no Canvas, `OBSERVATÓRIO · Missão consultada`, uma lua real, UUID `69009100-f867-4032-ad17-9023e24ae4ee`, `finished`, origem/horários e **0 agentes comprovados**.
- Evidência independente anterior via MCP: a conversa sintética `OBS-REAL-001` retornou `finished` e a resposta `OBS-REAL-001|OK` para operações de leitura simples. Não afirmar que o frontend recebeu essa resposta final.
- Evidência trazida pelo usuário: em **Configurações → Contexto do agente**, a memória persistente foi ativada e a UI apresentou “Configurações salvas”. **Não houve prova de gravação, recuperação ou isolamento por projeto**; conversas antigas podem requerer reinicialização.
- Quatro sistemas originais do universo (VIGIAFAST, Wandora, ELUS, OpenHands Lab) continuam cenários **DEMONSTRATIVOS**; sistema `OBSERVATÓRIO` aparece após GET pontual de UUID e não persiste após reload.
- Sem descoberta de missões automática, monitoramento contínuo, grafo Obsidian operacional, agentes reais identificados, inventário multi-projeto verificado, controle de execução pela UI ou RBAC multi-tenant comprovado.

## IDENTIDADE E FRONTEIRAS — regra canônica
Consulte `docs/PROJECT_SOURCE.md` e `AGENTS.md`.
**ChatGPT coordena → OpenHands executa tarefas autorizadas → Observatório exibe o que for verificável → GitHub registra histórico e decisões**.
**VIGIAFAST e demais produtos são PROJETOS ATENDIDOS; não são donos, camadas-base ou sinônimos de OpenHands/Observatório.**
Nenhuma memória do OpenHands ou conteúdo dos projetos deve ser compartilhado transversalmente sem controle de escopo.

## PROVEN EVIDENCE x GAPS
- **Comprovado**: `main` da PR #5; CI do HEAD pré-merge aprovada; extensão 0.4.2 habilitada no screenshot; leitura manual de conversa real `finished` visível no Canvas; memória ativada nas configurações do usuário.
- **Não comprovado**: runtime atualizado automaticamente, correlação missão→agente, vínculo projeto validado no servidor, sucesso semântico de tarefas, memória recuperável em sessão posterior, grafo vivo, acesso de observação a todos os projetos.
- O projeto informado no formulário da consulta de conversa é **declaração manual**, não resultado autenticado da API.

## ROADMAP — não é estado presente
1. Refinar painel de consulta e geometria/legibilidade da lua (propostas).
2. Investigar contratos de leitura, identidade/projeto e permissões antes de ativar descoberta multiprojeto.
3. Projetar modo **Grafo** estilo Obsidian como vista adicional do Observatório, apenas com nós e arestas rastreáveis.
4. Avaliar memória nativa OpenHands após teste sintético de escrita e recuperação; **não duplicá-la** como recurso específico do VIGIAFAST.

## GATES
- Consultar estado atual e reutilizar o que funciona. Branch + PR + testes.
- Sem merge/deploy automáticos, sem acesso a dados reais de clientes, sem alterações em VPS, Docker, OpenHands Core ou projetos atendidos sem autorização separada.
- Documento vivo mantém decisões e evidências **com data**; não tratar notas históricas de propostas como estado atual.

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
