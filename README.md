# Observatório de Agentes — OpenHands Agent Canvas

Extensão experimental **instalável como App do OpenHands Canvas**, reutilizando o protótipo V0.2: universo central, sistemas solares por projeto, planetas, informações de agentes, WebGL2 e fallback 2D.

**V0.4.0: dados exclusivamente demonstrativos.** Não existe conexão a OpenHands/Agent Mesh real, monitoramento de clientes ou execução de tarefas. Nomes e estados não são inventário factual.

## Instalar (somente após revisão e autorização da mudança no Canvas)
Em **Customize → Apps → Add app**, preencher:
- **App source:** `https://github.com/OARANHA/observatorio-agents-openhands.git`
- **Ref:** `main` para atualizações manuais após PR revisada e integrada (ou SHA fixo para congelar uma revisão).
- **Path:** deixar **vazio**: o manifesto está na raiz.

Instale **desabilitado**, revise antes de habilitar. A entrada no menu é **Observatório**.

⚠️ Apps executam JS confiável no mesmo contexto autenticado do Agent Server. A extensão atual não utiliza `host.agentServer.request`, `fetch`, cookies ou outras credenciais. Instalar uma revisão futura exige nova revisão de segurança. **A instalação V0.3.0 já foi testada pelo usuário no Canvas real.** A V0.3.1 foi exibida no Canvas real; a correção V0.3.2 ainda precisa ser validada nele.

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

## Desenvolver
Sem npm/CDN em runtime. Fonte: `source/observatorio-v02.html`. Regenerar `extension.js` usando `node scripts/build.mjs`. Verificar `node --check extension.js` e `python3 -m unittest discover -s tests -p test_contract.py`.

## Arquitectura
O `canvas-extension.json` registra uma página via `activate(host)` e `host.registerPage('observatorio', ...)`, como documentado em [OpenHands/demos](https://github.com/OpenHands/demos). A interface usa Shadow DOM para isolamento visual e limpa RAF/ResizeObserver/GPU ao desmontar.

A futura observabilidade real exige agregador read-only, inventário confiável, RBAC por projeto/tenant e dados minimizados. Não acessar perfis de clientes, conteúdo de conversas ou segredos no navegador.

Consulte `docs/PROJECT_SOURCE.md`, `docs/CANONICAL_STATE.md`, `docs/ARCHITECTURE.md` e `AGENTS.md`.
