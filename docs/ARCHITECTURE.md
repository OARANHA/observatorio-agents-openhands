# Arquitetura — Observatório horizontal multiprojeto

**Decisão vinculante:** `docs/decisions/ADR-0002-horizontal-operations.md`.

## Papéis e fronteiras
```text
          OPERADOR HUMANO (autoriza/valida)
                        |
      ChatGPT — coordenação técnica dentro dos acessos disponíveis
         |                              |
         v                              v
 OpenHands — tarefas autorizadas     GitHub — código, ADRs, testes, PRs
 memória auxiliar do agente          documentação viva POR PROJETO
         |                              |
         +-------- fontes verificáveis --+
                        |
                        v
   Observatório — visualização transversal no OpenHands Canvas
   (consultas pontuais reais + cenários marcados como DEMO)
                        |
     Projetos atendidos: VIGIAFAST | Wandora | ELUS | demais
```
O Observatório não é filho, módulo, gestor de clientes nem runtime do VIGIAFAST. Também não é executor de tarefas, e não controla OpenHands por meio de imagens de planetas/luas.

## Estado técnico real — v0.4.2
```text
OpenHands Agent Canvas -> Apps -> Observatório (registerPage)
    -> Shadow DOM (WebGL2 + fallback 2D)
       -> catálogo demo: 4 sistemas
       -> leitura opt-in: host.agentServer.request(GET /api/conversations/{UUID})
          -> estado da conversa, ID, horários; projeto digitado pelo operador
          -> 1 lua de conversa, 0 agentes comprovados
```
- Consulta autenticada pelo próprio Canvas, sem ler cookies, sem token embutido, sem fetch externo, sem polling e sem operação de escrita.
- O frontend apenas observa dados aprovados pela API. Nem `finished` nem o título da conversa provam sucesso, identidade do agente, vínculo com repo ou aprovação de uma ação.
- O teardown limpa elementos de UI, timers RAF, resize observers e contexto GPU; desenvolvimento e regeneração: `source/observatorio-v02.html` -> `node scripts/build.mjs` -> `extension.js`.
- O modo Grafo estilo Obsidian para conexões entre projetos, agentes, missões, memória, decisões, PRs e artefatos é **planejado**; não há hoje API de arestas confiáveis nem sincronização multi-repositório.

## Memória não é telemetria
Memória persistente do OpenHands (ativada na configuração do Canvas por screenshot) = notas potenciais consumíveis por conversas posteriores, dependendo de workspace/configuração. **Não equivale** a inventário de agentes, proveniência de decisões, log auditável, informação compartilhável entre projetos ou confirmação de funcionamento. Validar escrita/leitura e isolamento antes de integrar ao grafo. Documentação canônica por projeto permanece no repositório correspondente.

## Segurança e evolução
Identidade e autorização por projeto/tenant, política de minimização, origem e horários auditáveis, exclusão de segredos/prompts/dados de clientes e verificação de isolamento precedem descoberta de missões ou expansão de grafo. Preferir API autenticada read-only e inventário real; nunca usar associações livres digitadas como vínculo comprovado.
Mudanças via PR e testes; implantação Canvas somente com autorização. Não modificar OpenHands Core, VPS, brokers nem outros projetos por implicação.
