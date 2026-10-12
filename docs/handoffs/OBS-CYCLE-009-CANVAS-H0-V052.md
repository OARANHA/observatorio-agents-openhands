# CYCLE009 — Canvas H0 / Grafo Estelar V0.5.2 pós-merge

**Data:** 2026-10-11 (Brasília). **Natureza:** handoff de reconciliação **somente leitura**. Não autoriza instalação, habilitação, consulta de dados privados, agentes, LLM, deploy nem mudanças de infraestrutura.

## REAL NOW — evidência verificada nesta rodada

- PR visual **[#45](https://github.com/OARANHA/observatorio-agents-openhands/pull/45)** integrada; `main` efetiva `08d9072240411c5c980faadaf39b0336349591ef`. Manifesto `canvas-extension.json` **0.5.2**, entrypoint `extension.js` e `host.registerPage`. Isso prova somente **GitHub**, não Canvas instalado.
- CI no HEAD pré-merge `da924b4bc1cfc1371ce0ba3e22ccffcdde358cd9`: [CI Observatório](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38185587019) SUCCESS (218 testes, 28 skips), [Graph DOM Offline](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38185587051) SUCCESS (24/24 Chromium) e [SDK inerte](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38185587032) SUCCESS. Log CI comprova `node scripts/build.mjs` e `git diff --exit-code -- extension.js`.
- Revisor estático nesta rodada: sem novo endpoint, dependência externa ou execução de agentes observados no diff. **Não** é homologação real, revisão humana independente G11 nem prova de segurança de execução real.
- MCP do target `vigia-openhands-read` retornou `healthy:true`. A capability de leitura não lista os Apps Canvas instalados, sua versão ou ref. A URL histórica `https://canvas.wandora.com.br` não ficou acessível pela ferramenta pública; o perfil conectado de browser não dispõe de sessão autenticada para esse domínio. **H0 INCOMPLETO; versão/ref instalada em 2026-10-11 desconhecida.**
- Capturas históricas do operador indicam V0.5.1 ativada com ref `5cedc0ea...`; NÃO atribuir esse estado ao Canvas atual até leitura autenticada. Não inventar rollback a partir desse screenshot.

## REUSE GATE — H0 somente leitura, operador autenticado

No **Canvas correto**, sem comandos remotos nem leitura de conteúdo de conversas:
1. Abrir **Customize → Apps** e localizar **Observatório de Agentes**; anotar **versão**, **Ref SHA exato**, estado enabled/disabled, URL da instância e versão do host quando disponível.
2. Conferir se a ref permite **voltar exatamente à versão encontrada**; registrar o procedimento de rollback antes de propor H1.
3. Registrar evidência minimizada da tela Apps, ocultando nomes/IDs de clientes, cookies, senhas, tokens, títulos e prompts. **Não** clicar em instalação, atualização, habilitação, GET de conversa ou controle de agente.
4. Se a versão/ref já corresponder à V0.5.2, não reinstalar. Se diferir, só propor H1 após evidência H0, revisão dos riscos do App no contexto autenticado e aprovação **para instância + SHA específicos**.
5. Mantendo gates anteriores: **H1** instalação inicial desabilitada; **H2** habilitação visual de DEMO requer autorização distinta; **H3** GET sintético requer sua própria autorização e UUID autorizado. **H4** missão real segue bloqueado.

## Decision

- **GitHub visual 0.5.2 integrado**, **Canvas atualização NÃO EXECUTADA**, **homologação visual P01 PARCIAL**, **H0 INCOMPLETO**.
- **G05/G06/G07/G10 PARCIAIS, G08/G09/G11 NÃO PROVADOS, G12 BLOQUEADO**, P02/P03 NÃO PROVADOS; ADR-0001 PROPOSTO. **NO-GO operacional.**
- Outras PRs #49–#52 permanecem independentes; merge da PR #45 não as integra, não cria filas de agentes operacionais, não promove autorização/custos.
- Fonte histórica de critérios V01–V12 e gates: [CYCLE006](OBS-CYCLE-006-CANVAS-VISUAL-HOMOLOGATION-PLAN.md). Para versão 0.5.2 usar o HEAD `08d907...` apenas quando H0 demonstrar necessidade e H1 for autorizado.

**Próxima ação:** obter evidência autenticada H0 (screenshot sanitizado ou sessão browser explicitamente autorizada), sem deployment. Depois comparar ref instalada versus `08d9072240411c5c980faadaf39b0336349591ef` e decidir H1 separadamente.

## ATUALIZAÇÃO H0 — evidência visual do próprio operador (capturas recebidas)

**Momento da captura:** fornecida pelo proprietário após o merge da PR #45. **Origem:** imagens da interface Canvas nesta conversa, NÃO sessão browser aberta pelo assistente.

- Tela de **Apps** em `https://canvas.wandora.com.br` mostra **Observatório de Agentes**, **Ativado**, versão **v0.5.2**, **Páginas: 1** e Ref **`08d9072240411c5c980faadaf39b0336349591ef`**, coincidente com o merge da PR #45.
- Tela **Grafo** mostra o título **Grafo estelar · conexões com origem**, a etiqueta **CONSTELAÇÕES · V0.5.2**, quatro nós **DEMO** (VIGIAFAST, WANDORA, ELUS, OPENHANDS LAB) e o hub **APENAS DEMO**. As ligações SVG estão visíveis. Seleção visual do nó **ELUS** atualiza o painel de inspeção com **NÓ DO GRAFO · DEMO** e descrição de projeto ilustrativo.
- Contadores na captura: **CONSULTAS OPENHANDS 00**, **PROJETOS EXEMPLO 04**, **RELAÇÕES CONFIRMADAS 00**. Isso **não prova** inventário real, autenticação de vínculo projeto–missão nem telemetria.
- **Ponto de UX para revisão:** o fim da descrição do grafo (`relação.`) aparece encostado ou parcialmente coberto pelo conjunto de filtros, em imagens de largura desktop similar; hipótese visual P2 a reproduzir com coordenadas/viewport, não regressão funcional comprovada.
- **H0 parcial cumprido pela evidência do operador:** identidade do App, versão, Ref e estado de habilitação comprovados **nas capturas**. **H2 observação visual parcial** (renderização/seleção/legenda), sem teste independente de teclado, touch, WebGL, leitor de tela, remount, rede ou cleanup.
- **Ainda pendente:** versão do host Canvas, prova de rollback para a Ref anterior à atualização, inspeção do runtime por sessão autorizada, V01–V12 completos, revisor distinto e testes de acesso por projeto. Não inferir que a atualização foi executada pelo assistente: o operador apresentou o App já ativo.
- **Decisão atualizada:** versão 0.5.2 já aparece instalada e ativada; **não clicar em Atualizar novamente** sem novo objetivo. P01 **PARCIAL**, G11 **NÃO PROVADO**, G12 **BLOQUEADO**, H3 não executado, **NO-GO operacional**. Este bloco mais recente substitui apenas as afirmações anteriores de 'instalação desconhecida', mantendo-as como registro histórico da tentativa de H0.
