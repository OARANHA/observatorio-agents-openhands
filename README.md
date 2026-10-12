# Observatório de Agentes — OpenHands Agent Canvas

> **FERRAMENTA HORIZONTAL DA OPERAÇÃO (não é módulo do VIGIAFAST).** ChatGPT coordena, OpenHands executa tarefas autorizadas, Observatório apresenta atividades comprovadas, e GitHub mantém o histórico e a documentação. **VIGIAFAST, Wandora, ELUS e demais são projetos atendidos**, não proprietários da plataforma. Regra canônica: [`docs/PROJECT_SOURCE.md`](docs/PROJECT_SOURCE.md), [`AGENTS.md`](AGENTS.md), [`docs/CANONICAL_STATE.md`](docs/CANONICAL_STATE.md).

**Estado vigente:** versão 0.4.2 do Observatório foi instalada no Agent Canvas (ref `7212c51c38fc34cd195afb4db99ee35808e67cb5`) e a consulta de uma conversa OpenHands sintética real foi exibida como lua (`finished`); informação comprovada em screenshots do operador. Quatro sistemas originais seguem DEMO, e o projeto informado na consulta é manual. **O Grafo V0.5.1 foi integrado ao código da `main` na PR #43, mas sua instalação no Canvas NÃO foi comprovada**; a última instalação documentada continua sendo a V0.4.2. A memória persistente foi ativada no Canvas, mas gravação e recuperação ainda não foram validadas.


Extensão experimental **instalável como App do OpenHands Canvas**, reutilizando o protótipo V0.2: universo central, sistemas solares por projeto, planetas, informações de agentes, WebGL2 e fallback 2D.

**Histórico V0.4.1:** dados exclusivamente demonstrativos. **V0.4.2:** agrega uma leitura pontual de estado via API autenticada do Canvas; os agentes/nomes ilustrativos permanecem DEMO e não são inventário factual.

## V0.5.1 — Universo e Grafo integrados ao repositório, instalação ainda pendente

A PR [#43](https://github.com/OARANHA/observatorio-agents-openhands/pull/43) integrou a candidata V0.5.1 à `main` no commit `ac9c525a7e169fe253f0f488550686491939289a`. A suíte sintética Chromium passou em **19/19** cenários, com UI demonstrativa, consulta de conversa opcional pelo Canvas host, proveniência manual/consultada distinta e controles de teclado/mobile. **Isso NÃO indica que o Canvas instalado já esteja na V0.5.1, nem valida GPU real, RBAC, memória ou operação de agentes.**

Antes de qualquer atualização, seguir [Plano de homologação visual — CYCLE006](docs/handoffs/OBS-CYCLE-006-CANVAS-VISUAL-HOMOLOGATION-PLAN.md). Inicialmente, conferir a instalação real **somente leitura**; atualização/instalação e habilitação exigem autorizações específicas. PRs #7 e #35 continuam abertas e não devem ser mescladas automaticamente.

## Instalar (somente após revisão e autorização da mudança no Canvas)
Em **Customize → Apps → Add app**, preencher:
- **App source:** `https://github.com/OARANHA/observatorio-agents-openhands.git`
- **Ref:** preferir **SHA fixo** após autorização explícita; para homologar V0.5.1 a referência proposta é `ac9c525a7e169fe253f0f488550686491939289a`. `main` é móvel e não deve ser usado como prova de versão testada.
- **Path:** deixar **vazio**: o manifesto está na raiz.

Instale **desabilitado**, revise antes de habilitar. A entrada no menu é **Observatório**.

⚠️ Apps executam JS confiável no mesmo contexto autenticado do Agent Server. A extensão 0.4.2 **usa** `host.agentServer.request` para um GET explícito de conversa com UUID; não utiliza `fetch` bruto, cookies lidos pelo app ou credenciais embutidas. Instalar uma revisão futura exige nova revisão de segurança. **A instalação V0.3.0 já foi testada pelo usuário no Canvas real.** A V0.3.1 foi exibida no Canvas real; a correção V0.3.2 ainda precisa ser validada nele.

## Correção da barra lateral do Canvas (V0.3.1)
A camada visual \`.ob-wrap::before\` da extensão anterior usava \`position: fixed\` e escondia a navegação nativa do OpenHands, embora os links continuassem recebendo hover. O CSS gerado agora usa \`position: absolute\`, limitado ao painel. **Não basta clicar Atualizar sem confirmar o SHA da versão corrigida**, pois a instalação anterior foi fixada num commit imutável.

## Correção de sobreposição na visualização solar (V0.3.2)
A nota descritiva ficava parcialmente escondida pelo painel inferior porque ambos usavam posições absolutas independentes. Agora eles dividem um contêiner vertical, com a nota acima das métricas. O universo oculta a nota; dispositivos móveis mantêm o comportamento responsivo. O teste de regressão valida o CSS e o DOM efetivamente gerados.

## Realismo progressivo e atividade visual (V0.4.0)
- O botão **SIMULAR: CALMO / ATIVIDADE / ATENÇÃO / FALHA** permite avaliar os estados sem alegar conexão com agentes ou tarefas reais.
- Universo: rotação lenta das órbitas, cartões com brilho contextual e contagem **DEMO**.
- Sistema solar: brilho WebGL por estado e até duas pequenas luas ilustrativas em movimento por planeta ativo; labels 2D acompanham os cenários.
- Respeita `prefers-reduced-motion`, mantém Shadow DOM e não adiciona dependências, requests, tokens ou persistência.
- O modelo de demonstração é interno à fonte; **não** corresponde a eventos operacionais. A integração real exige novo projeto de contrato de leitura e controle de acesso.

## Correção das órbitas no Universo (V0.4.1)
A V0.4 girava o SVG inteiro do cartão, deformando visualmente a inclinação das órbitas e recortando seu desenho. Agora as elipses permanecem inclinadas em -17° como no protótipo original; somente um traço luminoso percorre a órbita externa, com velocidade por cenário e suporte a movimento reduzido. O teste de regressão verifica o CSS e SVG efetivamente compilados.

## Desenvolver
Sem npm/CDN em runtime. Fonte: `source/observatorio-v02.html`. Regenerar `extension.js` usando `node scripts/build.mjs`. Verificar `node --check extension.js` e `python3 -m unittest discover -s tests -p test_contract.py`.

## Arquitectura
O `canvas-extension.json` registra uma página via `activate(host)` e `host.registerPage('observatorio', ...)`, como documentado em [OpenHands/demos](https://github.com/OpenHands/demos). A interface usa Shadow DOM para isolamento visual e limpa RAF/ResizeObserver/GPU ao desmontar.

A futura observabilidade real exige agregador read-only, inventário confiável, RBAC por projeto/tenant e dados minimizados. Não acessar perfis de clientes, conteúdo de conversas ou segredos no navegador.

Consulte `docs/PROJECT_SOURCE.md`, `docs/CANONICAL_STATE.md`, `docs/ARCHITECTURE.md` e `AGENTS.md`.


## V0.4.2 — consulta operacional (implementada, validada visualmente)

O Observatório conserva a experiência demonstrativa V0.4.1, mas inclui o painel **☾ CONSULTA DE MISSÃO REAL**. Após inserção manual do UUID, consulta pontualmente `GET /api/conversations/{id}` por `host.agentServer.request`, usando a autenticação do Canvas. Mostra somente ID, estado, horário de atualização do servidor, origem e horário da observação pelo navegador. Não lista conversas, mostra resultados/segredos, executa comandos nem faz polling.

O projeto é preenchido pelo operador: associação explícita, **não validada pelo Agent Server**. A lua representa apenas a execução consultada; nenhum agente real é inferido. O acesso do Canvas não substitui RBAC por projeto/tenant. Uso interno sintético apenas, sem dados reais de clientes. **Verificado pelo operador no Canvas**: UI 0.4.2 mostrou uma conversa sintética `finished` como lua. Os demais vínculos, memória e agentes ainda não foram homologados. Testes previstos: `node scripts/build.mjs`, `node --check extension.js` e `python3 -m unittest discover -s tests -p test_contract.py`.


## Ajuste da PR #5 — lua real dentro do Multiverso (2026-10-10)

Depois de consultar manualmente um UUID via Canvas Host, a UI cria **em memória** o quinto cartão `OBSERVATÓRIO` (projeto explicitamente informado pelo operador) e abre seu sistema solar: **uma lua de execução OpenHands verificada**, zero planetas de agentes comprovados e painel lateral com UUID, status, origem, atualização do servidor e hora da consulta. Os quatro sistemas originais permanecem DEMO; o cartão real exibe `OPENHANDS REAL`.

- Evidência operacional: missão sintética OBS-REAL-001 terminou em `finished`; resposta do MCP `openhands_result` continha `OBS-REAL-001|OK`. A execução real não é embutida no Git ou frontend; somente o UUID inserido pelo usuário é consultado pelo Canvas autenticado.
- `host.agentServer.request(GET /api/conversations/{uuid})` é lido sob a sessão Canvas. Não expor resposta final, prompts nem títulos. A associação `project` é **declarada**, nunca inferida ou certificada.
- Zero sincronização automática, zero histórico persistido, nenhuma credencial no JS, nenhum agente novo, nenhuma ação start/stop. Sem dados reais de clientes nem RBAC multi-tenant homologado.
- Após reload do Canvas, **é necessário consultar o UUID novamente**. Para vinculação automática e durável, precisaríamos de inventário seguro do lado do servidor: fora deste primeiro slice.
- PR #5 integrada; extensão 0.4.2 instalada e verificada em screenshot do Canvas. Requer autorização específica para qualquer **nova** atualização; não implica telemetria completa ou sincronização. Em caso de API incompatível, não mostrar uma lua como atividade comprovada.

## V0.5.2 — candidata Grafo Estelar (não instalada)

A V0.5.2 propõe uma linguagem cósmica no grafo: estrelas CSS locais, nós em órbitas de constelações e conexões SVG curvas sem alterar o significado dos dados. Os rótulos `DEMO`, fonte consultada e vínculo manual continuam explícitos. Esta candidata é preparada **somente em branch/PR draft** e requer revisão e CI; o Canvas do operador permaneceu em **V0.5.1** conforme captura fornecida (ref `5cedc0eada928fcd1f46cc50e2144d02822181be`). Não instalar a V0.5.2 sem nova autorização específica.

Detalhes: [CYCLE007 — Grafo Estelar](docs/handoffs/OBS-CYCLE-007-STELLAR-GRAPH-V052.md). A integração no Canvas não é validada por screenshots do runner Chromium.
