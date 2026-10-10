# Observatório de Agentes — OpenHands Agent Canvas

Extensão experimental **instalável como App do OpenHands Canvas**, reutilizando o protótipo V0.2: universo central, sistemas solares por projeto, planetas, informações de agentes, WebGL2 e fallback 2D.

**V0.3.1: dados exclusivamente demonstrativos.** Não existe conexão a OpenHands/Agent Mesh real, monitoramento de clientes ou execução de tarefas. Nomes e estados não são inventário factual.

## Instalar (somente após revisão e autorização da mudança no Canvas)
Em **Customize → Apps → Add app**, preencher:
- **App source:** `https://github.com/OARANHA/observatorio-agents-openhands.git`
- **Ref:** SHA ou branch **revisada** (não instalar automaticamente de `main`).
- **Path:** deixar **vazio**: o manifesto está na raiz.

Instale **desabilitado**, revise antes de habilitar. A entrada no menu é **Observatório**.

⚠️ Apps executam JS confiável no mesmo contexto autenticado do Agent Server. A extensão atual não utiliza `host.agentServer.request`, `fetch`, cookies ou outras credenciais. Instalar uma revisão futura exige nova revisão de segurança. **A instalação V0.3.0 já foi testada pelo usuário no Canvas real.** A correção visual V0.3.1 ainda precisa ser atualizada e verificada no Canvas.

## Correção da barra lateral do Canvas (V0.3.1)
A camada visual \`.ob-wrap::before\` da extensão anterior usava \`position: fixed\` e escondia a navegação nativa do OpenHands, embora os links continuassem recebendo hover. O CSS gerado agora usa \`position: absolute\`, limitado ao painel. **Não basta clicar Atualizar sem confirmar o SHA da versão corrigida**, pois a instalação anterior foi fixada num commit imutável.

## Desenvolver
Sem npm/CDN em runtime. Fonte: `source/observatorio-v02.html`. Regenerar `extension.js` usando `node scripts/build.mjs`. Verificar `node --check extension.js` e `python3 -m unittest discover -s tests -p test_contract.py`.

## Arquitectura
O `canvas-extension.json` registra uma página via `activate(host)` e `host.registerPage('observatorio', ...)`, como documentado em [OpenHands/demos](https://github.com/OpenHands/demos). A interface usa Shadow DOM para isolamento visual e limpa RAF/ResizeObserver/GPU ao desmontar.

A futura observabilidade real exige agregador read-only, inventário confiável, RBAC por projeto/tenant e dados minimizados. Não acessar perfis de clientes, conteúdo de conversas ou segredos no navegador.

Consulte `docs/PROJECT_SOURCE.md`, `docs/CANONICAL_STATE.md`, `docs/ARCHITECTURE.md` e `AGENTS.md`.
