# Fonte de autoridade — Observatório de Agentes

## Natureza e escopo (decisão permanente do proprietário)
**OpenHands e Observatório são ferramentas de trabalho horizontais para coordenar e acompanhar múltiplos projetos. Não fazem parte do VIGIAFAST e não são módulos, backends ou serviços desse produto.**
VIGIAFAST, Wandora, ELUS e quaisquer projetos futuros são **projetos atendidos**, sem primazia arquitetural.
A coordenação é do ChatGPT dentro das ferramentas e permissões efetivamente disponíveis; não presumir autonomia, acesso a dados ou execução sem autorização.

**Contrato de coordenação: ChatGPT planeja e valida → OpenHands executa tarefas autorizadas → Observatório apresenta relações e atividades verificáveis → GitHub registra código, decisões, PRs e evidências dos projetos.**
O Observatório **não** é o orquestrador nem substitui GitHub, OpenHands ou documentação canônica. O grafo estilo Obsidian é uma evolução planejada, não capacidade implantada.

Autoridade sobre essa separação: este arquivo, `AGENTS.md` e `docs/CANONICAL_STATE.md`. Em caso de ambiguidade, essa delimitação prevalece sobre exemplos visuais de produtos.

## Ordem de retomada em todo chat
1. `docs/PROJECT_SOURCE.md` (este arquivo)
2. `AGENTS.md`
3. `docs/decisions/`: ler ADRs e respeitar **status** individual
4. `docs/CANONICAL_STATE.md` e `MEMORY.md`
5. `docs/ARCHITECTURE.md` e `README.md`
6. Código, testes, PRs, SHA de `main`, ambiente e execuções pertinentes

Método: **REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION**.
Documentação é regra de projeto, **não prova de deploy, integração ou execução**; reconfirmar estado operacional antes de alegá-lo.

## Segurança e limites
- Não divulgar segredos, sessões, títulos de conversas ou dados de clientes; minimizar dados operacionais.
- Não inferir que uma conversa representa um agente, vínculo autenticado a repositório, execução bem-sucedida ou memória efetivamente recuperada.
- Memória do OpenHands, histórico de conversas e documentação canônica são mecanismos **distintos**. O switch de memória ativado não prova armazenamento/recuperação nem isolamento por projeto.
- Multi-projeto exige identidades e autorização por escopo; nenhuma descoberta/ação transversal automática sem contrato e permissões demonstrados.
- Não alterar OpenHands Core, VPS, Docker, Canvas instalado, VIGIAFAST ou outros projetos por implicação; branch + PR para alterações no Observatório. Merge/deploy/operações destrutivas somente com aprovação específica. Sem polling contínuo de CI.
