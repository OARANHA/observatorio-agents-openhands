# Mentor DEMO — interface independente, sem instalação

2026-10-11. Base reconciliada após #39:
`9e25aa67eea7a15b9d61ed7f249202644b9ee1d8`. #7 e #35 permanecem intocadas.

`tools/mentor-demo/index.html` é HTML autossuficiente gerado por
`scripts/build_mentor_demo.mjs`, fora do build/manifest/activate da extensão.
Não modifica o Canvas instalado, não consulta AgentServer, não envia mensagem
Slack/MCP/ChatGPT e não simula presença real do ChatGPT na conversa. Não há
SDK, provider, token, histórico ou agente registrado. CSP bloqueia conexões,
formulários e recursos externos. A recomendação é texto fixo local.

## Reuse gate e classificação

Reutilizadas **sem alteração** funções `graphIdentityForObservation` e
`validGraphIdentity` de `source/observatorio-v02.html`, snapshot público da
PR35 HEAD811d5fa4c48aa9eb2cf618174b7d645039a590ac; apenas exports ESM acrescentados.
`identity-provenance.json` registra origem, transformação e SHA-256, verificado
por teste. Não integra o grafo/patch da PR35 nem muda source/extension.js.
A identidade continua `local-view-not-tenant`: hash da visão local não autentica
RBAC, projeto, conversa/agente ou memória persistente.

Duas fixtures públicas `synthetic/alpha` / `synthetic/beta`, UUIDs fictícios,
paused e needs_review; tudo marcado DEMO/fonte sintética/projeto declarado.
Nenhuma informação é classificada como consultada/autenticada. Observação e
identidade imutáveis; seleção só project/status/event. Campos livres, notas,
prompts, credenciais e dados privados não entram. Não há input para conteúdo real.

## Revisão de contexto e ciclo assíncrono

Chamar Mentor abre diálogo modal; contexto exato em JSON visível. Estado e evento
começam selecionados; projeto é opt-in. Usuário pode excluir todos. Classificação,
origem e NO-GO permanecem. Alteração da seleção revoga o checkbox de revisão.
Aprovação literalmente True refere-se **apenas à simulação da orientação**,
nunca execução OpenHands/GO. Sem revisão, geração é recusada.

Modelo faz uma recomendação fictícia por instância. Solicitação concorrente,
cancelamento, segunda solicitação inválida ou close terminam a simulação.
Teardown invalida geração; resposta tardia não aparece em remount. Cancelar/Escape
não envia nada. UI fornece estados vazio/erro, foco/teclado, status anunciado,
contexto responsivo, targets44px e prefers-reduced-motion. Mutação hostil no mesmo
processo/browser não é fronteira de segurança; não reutilizar como autorização.

## Evidência disponível e limites

- 9 testes Node RED por modelo ausente → GREEN: revisão obrigatória, minimização,
  aprovação literal, teardown/corrida assíncrona, identidade local segregada,
  configuração fechada, fixture imutável e hash da reutilização.
- 2 testes Python executam contrato Node, geração idêntica e sintaxe dos módulos.
  Suite local:213 testes,185 PASS/28 skips SDK explícitos. Node9/9 sem skip.
- Cinco testes Chromium previstos em `tests/browser/mentor_dom.mjs`: contexto/
  consentimento/sem egress, teclado/Escape, vazio/erro, teardown/remount pendente,
  mobile/foco. Workflow efêmero `Mentor Demo Offline DOM` reutiliza o padrão
  Playwright1.58.0 + Chromium com sandbox obrigatório da avaliação PR35.
  Navegador local indisponível; PASS/resultado/QA visual **só após runner**,
  registrar no handoff/PR. Dependências apenas de teste efêmeras.

Capturas contêm fixtures públicas, retenção curta3dias, não são Canvas instalado.
Testes automáticos não homologam leitor de tela, RBAC, fonte autenticada, integração
Mentor/Work ou memória. P03 permanece NÃO PROVADA; G11 não cumprido por autorrevisão.
Próxima etapa visual real exige escolha humana de escopo/contrato de contexto,
revisão independente e autorização específica de instalação. **NO-GO operacional.**
