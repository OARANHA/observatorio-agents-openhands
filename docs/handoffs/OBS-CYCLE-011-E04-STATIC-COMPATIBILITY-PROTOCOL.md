# ADM-CYCLE011E-04 — Inventário estático e protocolo de prova de autorização

Data: 2026-10-12. Base `main` `ca0479ad5bc84243e5f3bd958c78dd750fe68371`. **Somente inventário de fontes públicas.** ADR-CYCLE011-E01 mantém status PROPOSTA.

## REAL NOW → EVIDÊNCIA → LACUNA

| Componente | Evidência pública examinada | Instalação real |
|---|---|---|
| Agent Canvas | `OpenHands/OpenHands/config/defaults.json`: `agentCanvas=1.26.0` | NÃO COMPROVADA |
| Agent Server | mesmo `defaults.json`: `agentServer=1.54.0`, mínimo compatível `1.51.0` | NÃO COMPROVADA |
| TypeScript client | `OpenHands/OpenHands/package.json`: `@openhands/typescript-client=1.54.0` | NÃO COMPROVADA |
| Middleware de sessão | `openhands-agent-server/.../dependencies.py`: `check_session_api_key` verifica `X-Session-API-Key` contra `config.session_api_keys` **quando a lista está configurada** | Configuração efetiva NÃO COMPROVADA |
| Cookie de workspace | mesmo arquivo: `check_workspace_session` aceita header ou cookie para rotas estáticas de workspace; comentário explícito delimita seu escopo ao roteador | Uso real NÃO COMPROVADO |
| Consulta de conversa | `conversation_router.py` → `ConversationService`; busca e GET/DELETE por UUID em código público | ACL por conversa/projeto NÃO COMPROVADA |

Fontes exatas:
- https://github.com/OpenHands/OpenHands/blob/main/config/defaults.json
- https://github.com/OpenHands/OpenHands/blob/main/package.json
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/dependencies.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/conversation_router.py
- https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/conversation_service.py

**Atenção:** `main` público é mutável. Os números acima são declarações verificadas na consulta desta etapa, **não fingerprints instalados nem garantias de tag imutável**. A condição `if config.session_api_keys` demonstra que a presença/ausência de chaves configuradas modifica o comportamento; não inferir modo de autenticação real. Cookie de workspace não equivale a autorização por conversa/projeto.

## Protocolo verificável — SOMENTE PLANO, NÃO EXECUTAR

**Gate 0 — Aprovação separada:** definir operador, instalação, ambiente, escopo, proteção de dados e janela de testes. Sem aprovação, **parar** antes de qualquer leitura do ambiente.

**Gate 1 — Inventário autorizado sem segredos:** coletar manifestos de release, digests de imagens, commits do Canvas/servidor/cliente e configuração de roteamento **redigida**, usando canais aprovados e sem tokens, cookies ou material privado. Comparar com matriz pública por commit, não com números presumidos. Discrepância → NO-GO.

**Gate 2 — Proveniência de identidade:** demonstrar de onde nasce o sujeito autenticado (subject), tenant/projeto e papéis, em qual camada se aplica autorização por recurso e como a ponte Canvas preserva esse escopo. Chave de sessão, UUID, `selected_repository` e cookie de workspace isoladamente não servem.

**Gate 3 — Matriz de recursos em ambiente sintético autorizado:** dois sujeitos e dois projetos fictícios. Validar permissão e negação de `get/search/count/batch/events`; UUID cruzado, busca/cursor paginado, dados de anexos, método indevido, GET com corpo e headers arbitrários. Negativa não pode revelar existência/conteúdo/metadados de outro projeto. Nenhum teste desta matriz foi executado.

**Gate 4 — Revogação:** retirar vínculo projeto/sujeito e provar invalidação de autorização, páginas e caches com limite temporal documentado; se não for demonstrada → NO-GO.

**Gate 5 — Revisão independente G11:** revisão humana formal de evidências, riscos, configuração e runbooks; JEV.1 é apenas apoio. Só depois outra autorização para G12/canário, limitada e explícita.

## Hipóteses adversariais obrigatórias
- `check_session_api_key` condicionada à configuração de chaves não é uma ACL por recurso.
- Middleware de sessão no `/api` não garante filtro de tenant em `ConversationService`.
- Backend/BFF com chave ampla cria risco de `confused deputy`.
- Filtrar depois de paginação/contagem pode vazar metadados.
- Cache pré-revogação e solicitações concorrentes precisam de fail-closed.
- A implementação pública pode ser diferente da instalada; não reutilizar rota pública sem compatibilidade comprovada.

## REUSE GATE / DECISION

Alternativa A da ADR (reutilizar) só é candidata após provas dos Gates 1–5; B exige ADR própria e autorização explícita; C (descoberta desativada) é o comportamento seguro atual. **Não se escolhe A ou B com este inventário.**

**G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO · NO-GO operacional.** Sem GET real, acesso à instalação, alteração Canvas, merge ou deploy por este protocolo.
