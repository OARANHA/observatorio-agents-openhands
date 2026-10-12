# ADM-CYCLE011C-04 — Ponte pública Canvas host → Agent Server (estático)

Data: 2026-10-12. Main inicial `b886d5664dadc9a47d634f17ef9f4cc1c44aa1c7`. Sem chamadas reais, merge ou deploy.

## PROVEN EVIDENCE (código público)

- `OpenHands/OpenHands/src/components/features/canvas-extensions/canvas-extensions-runtime.tsx`: disponibiliza `host.agentServer.request(request)` chamando `CanvasExtensionsService.requestAgentServer(request, backend)`.
- `src/api/canvas-extensions-service.ts`: rejeita `path` que não comece por `/` e paths iniciados por `//`; escolhe `getClientForBackend(backend)` quando há backend, senão `getClient()`; encaminha `method`, `path`, `body` e `headers` ao `client.request`.
- `src/types/canvas-extension.ts`: interface expõe `GET|POST|PUT|PATCH|DELETE`, `path`, `body`, `headers`. **Não é interface somente GET**.
- `specs/canvas-extensions.md`: registra `apiVersion: "1"`, helper autenticado para backend proprietário, carregamento habilitado pelo operador; alerta que extensões rodam no contexto de requisições autenticadas e revisão de instalação não inventa permissões granulares.
- O Agent Server upstream (`openhands-agent-server/.../api.py`, `dependencies.py`) valida inicialização e sessão; **isso não prova** ACL multiprojeto.

Fontes públicas:
- https://github.com/OpenHands/OpenHands/blob/main/src/components/features/canvas-extensions/canvas-extensions-runtime.tsx
- https://github.com/OpenHands/OpenHands/blob/main/src/api/canvas-extensions-service.ts
- https://github.com/OpenHands/OpenHands/blob/main/src/types/canvas-extension.ts
- https://github.com/OpenHands/OpenHands/blob/main/specs/canvas-extensions.md

## REUSE GATE / análise adversarial

**Atenção:** validação de path raiz não equivale a allowlist de endpoints; helper genérico aceita escrita e `headers`, então código de extensão não confiável pode solicitar operações além de leitura. Não interpretar backend proprietário como tenant/repositório autorizado. `client.request` e autenticação de sessão não evidenciam, nesses trechos, política de autorização por conversa, projeto ou revogação.

A revisão identifica riscos de extensão habilitada em contexto autenticado, desvio de rota, métodos de escrita, cabeçalhos arbitrários e promoção de metadados a autorização. O Observatório deve manter a sua política própria **somente GET pontual aprovado**; não ampliar a superfície só porque a API host oferece métodos adicionais.

**Versões:** código observado no ramo público do OpenHands, **sem fingerprint da versão instalada do Canvas**, pacote frontend em uso, versão Agent Server ou hashes de distribuição efetiva. Compatibilidade operacional NÃO PROVADA. Não confundir artefatos de código consultados com sessão instalada.

## Modelo offline e decisão

`tests/cycle011_c04_canvas_host_bridge.test.mjs` codifica invariantes **sintéticos**, independentes do runtime: método GET pontual, path exato UUID, nenhum body/header, nenhuma descoberta/listagem e autorização separada; não exerce a ponte nem implementa RBAC.

**G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO · NO-GO operacional.** Próxima investigação, se autorizada: fingerprint **não sensível** da instalação por via documental e auditoria da política `client.request`/proxy/autorização por recurso no código da versão correspondente, sem consulta real.

## Fechamento técnico adversarial ADM-CYCLE011C-05 — 2026-10-12
- HEAD validado `0c13c2cbea9496b980c6c803fd6c2ee8b46ebe09`: CI Observatório run `38208610920` SUCCESS; Canary Worker Inert SDK run `38208610935` SUCCESS.
- Job `contract`: a etapa `CYCLE011-C04 ponte host - gates offline` efetivamente executou com SUCCESS, juntamente com verificações de contrato anteriores.
- Revisão adversarial: a interface host admite métodos de escrita, body e headers; a checagem de caminho relativo no service não é allowlist de endpoints, nem atesta ACL de projeto. Os testes adicionados só verificam uma política hipotética restritiva; não medem o código real do host nem as permissões instaladas.
- Resultado: apto a uma decisão posterior de integração **somente documental/offline**; G11 NÃO PROVADO, G12 BLOQUEADO, P02 NÃO PROVADO, NO-GO operacional.
- Este fechamento produz novo HEAD documental e os workflows acima não o validam. Sem merge, GET real ou deploy.
