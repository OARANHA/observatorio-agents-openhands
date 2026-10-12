# ADR-CYCLE011-E01 — Autorização multiprojeto no Observatório

- **Status:** PROPOSTA — não aceita para implementação
- **Data:** 2026-10-12
- **Base verificada:** `main` `8774eab87b160617d7dcf5f06bbf98eeba281bc2`
- **Autoridade:** `docs/PROJECT_SOURCE.md` → `AGENTS.md` → ADRs vigentes → `docs/CANONICAL_STATE.md` → `MEMORY.md`
- **Escopo:** Observatório horizontal de Agentes/OpenHands, não VIGIAFAST ou qualquer projeto cliente

## Contexto e evidências
PRs #61–#67 investigaram, de forma estática/offline, `host.agentServer.request`, `AgentServerClient`, `HttpClient`, autenticação de sessão, rotas de conversa e `ConversationService`. `search_conversations` percorre catálogo persistido, filtra por estado, ordena e pagina; consultas e exclusão por UUID ocorrem em métodos públicos. Nos trechos examinados, não foi comprovada autorização por sujeito, projeto e recurso. **Não afirmar inexistência universal de ACL:** middleware, proxy, deployments distintos e controles externos não foram inspecionados. Versões públicas de código não demonstram versão instalada. Fixtures JavaScript e gates booleanos não executam o servidor Python original.

## Requisitos de segurança verificáveis
1. Identidade derivada da sessão autenticada no servidor (subject/tenant/roles), nunca de campos do navegador como `selected_repository`.
2. Referência autoritativa que vincule cada conversa a projeto, sujeito e permissão; política deny-by-default e separação leitura/escrita.
3. Consulta pontual, lote, contagem, listagem, cursor, eventos, anexos e exportações aplicam **a mesma política antes de devolver dados ou metadados**. Cursor opaco e limitado ao escopo, sem contagens globais.
4. Revogação de vínculo ou papel impede novas leituras em tempo verificável; invalidar caches, sessões delegadas e decisões pré-computadas conforme modelo de risco.
5. Permitir apenas endpoints/métodos/headers necessários; bloquear GET com body e operações de escrita na superfície do Observatório, salvo futura aprovação explícita.
6. Registrar decisão auditável sem tokens, títulos, conteúdo privado ou segredos; minimizar dados e cumprir políticas do usuário/organização.
7. Testes de negação entre projetos e após revogação, inclusive UUID conhecido, paginação, batch, eventos e associação declarada manualmente.
8. Revisão independente G11 e autorização explícita antes de chamadas reais; não confundir GREEN CI com prova operacional.

## Alternativas e comparação
| Critério | A — Reutilizar autorização já existente | B — Camada complementar de autorização | C — Não descobrir automaticamente |
|---|---|---|---|
| Quando escolher | Backend real demonstra identidade/ACL por recurso e revogação | Controles inexistentes/insuficientes; nova ADR de desenho e implementação aprovada | Evidência insuficiente ou custo/risco desproporcional |
| Mudança em arquitetura | Menor, via contrato oficial e allowlist | Backend/BFF adicional com validação server-side de sujeito/ACL | Mantém modo offline/consultas autorizadas já existentes |
| Vantagem | Menor duplicação, menor superfície nova | Fronteira única e verificável para projetos distintos | Menor risco de exposição transversal |
| Risco residual | Configuração/versão divergente, rotas fora da política | Drift ACL, cache stale, BFF privilegiado, maior operação | Cobertura funcional limitada |
| Dependências | Fingerprint instalado, middleware e testes negativos reais autorizados | Modelo de dados de permissões, identidade confiável, storage, observabilidade, revisão | UX clara de indisponibilidade e evidência manual |
| Esforço relativo* | Baixo–médio se comprovado; alto se exigir adaptação | Médio–alto; manutenção contínua | Baixo |
| Rollback | Desativar discovery e revogar permissões de leitura da integração | Feature flag fail-closed, desligar BFF, invalidar tokens/cache sem apagar evidências | Permanecer desativado |

*Estimativas qualitativas, não prazos/preços, pois instalação e controle disponíveis não foram verificados.

## Decisão proposta (não implementada)
**A preferencial sob prova:** reutilizar ACL existente se e somente se os controles forem comprovados para versão instalada e para todas as rotas utilizadas. **B condicional:** se A falhar, formular ADR posterior detalhando BFF, limites de privilégio, propagação de identidade, custódia das políticas e rollback; não programar B automaticamente. **C padrão seguro:** manter descoberta multiprojeto desativada até satisfazer os gates.

## Critérios de aceitação antes de qualquer GO
- Evidência rastreável de build/versão/commit do Canvas, Agent Server, SDK e middleware instalados **obtida com autorização específica e sem segredos**.
- Matriz sujeito×projeto×conversa×operação, testando permitido/negado e projeto diferente.
- `search/count/page/batch/get/events` exercitados em ambiente de teste autorizado, com dados sintéticos e política real; nenhuma listagem ou metadado vaza de projeto não autorizado.
- Revogação comprovada em cenário antes/depois, com limite temporal documentado e limpeza de cache.
- Controles contra headers arbitrários, métodos de escrita, GET com body, UUID forjado e projeto indicado pelo frontend.
- Revisão independente de segurança G11, evidência de isolamento P02 e só então decisão humana separada para G12.

## Reversão e condições de parada
Antes do GO, rollback é manter o feature flag de discovery em OFF — sem alterar instalação. Após eventual implementação autorizada, desabilitar ponte/BFF, invalidar credenciais delegadas e caches, preservando auditoria sem conteúdo sensível. Qualquer inconsistência em ACL, tenant ou versão resulta em **STOP / NO-GO**; nenhuma solução deve falhar aberta.

## Revisão adversarial pendente
Inspecionar se A abrange roteadores de eventos, batch, count e streams; se B se tornaria confused deputy por credencial global; se revogação cobre páginas já cacheadas, e se proteção de tenant existe também em armazenamento e logs. JEV.1 é **consultivo** e não substitui revisão independente.

**G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO · NO-GO operacional.** Sem GET real, merge, deploy, Canvas ou operações destrutivas por esta ADR.
