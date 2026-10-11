# Ciclo 004 — continuidade na mesma conversa (inerte)

2026-10-11. **NO-GO operacional.** Main inicial
`242856c523b1880328b6bb985f6fcedf0a7c58c2`. Não há conexão a AgentServer,
credenciais escolhidas, mensagens enviadas ao OpenHands ou MCP modificado.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

Slack Wandora foi consultado pelo conector. `#observatorio-eventos` já existia;
`#observatorio-aprovacoes` foi criado dentro da autorização de teste. O serviço
Work recusou a criação do gatilho Slack porque não reconhece seu aplicativo
oficial em `#observatorio-eventos`, embora a lista de membros contenha o nome
`@chatgpt`. Nome não comprova vínculo do aplicativo. Não foi criada automação,
nem enviada a mensagem OBS-TEST-V1. Não substituir o gatilho por polling.
Intervenção futura: instalar/reconectar [aplicativo oficial](https://chatgpt.com/slack-ai-app-install)
e adicioná-lo ao canal; então testar uma única mensagem fictícia e comprovar
um disparo, ausência de ações e ausência de loop. Sem prova Slack → Work agora.

### Fontes públicas fixadas (código, não ambiente implantado)

- SDK/AgentServer OpenHands **v1.53.0**, commit
  [`54daf056bd863bb46f922a2fe9324dd736b37ff6`](https://github.com/OpenHands/software-agent-sdk/tree/54daf056bd863bb46f922a2fe9324dd736b37ff6).
- MCP público, main reconciliada por ref, commit
  [`235fd9359cbf56e5aa7cf46c3f0fe224ee242cdd`](https://github.com/OARANHA/Remote-Ops-MCP/tree/235fd9359cbf56e5aa7cf46c3f0fe224ee242cdd).
  Ler `src/agent/openhands.ts` e `src/tools/index.ts`; nenhum tool operacional foi chamado.
- Consultados `event_router.py`, `event_service.py`, `conversation_router.py`,
  `models.py`, `api.py`, `dependencies.py`, `sockets.py`, `session_socket.py`,
  `session_protocol.py` no diretório `openhands-agent-server/openhands/agent_server/`;
  `conversation/request.py`, `conversation/state.py`, `event/base.py` no SDK.
- SDK/Tools 1.53.0 é o alvo das provas existentes. A versão realmente implantada
  do AgentServer **não foi consultada**. Versão de Canvas não substitui essa prova.

| Contrato no código oficial fixado | Evidência / implicação |
|---|---|
| `POST /api/conversations/{id}/events` | `SendMessageRequest`: `role`, lista `content`, `run=False` por padrão. A API oficial aceita outros papéis; proposta local restringe `user`. É escrita mesmo com `run=False`: persiste a mensagem e pode parar o goal loop. |
| Mensagem salva antes de `run` | HTTP 429 pode significar mensagem **já salva** sem execução. Não reenviar automaticamente. Resultado incerto requer reconciliação humana; zero retries. |
| `POST .../{id}/run` | Pode executar LLM. Não foi chamado. Estado concorrente e capacidade podem negar; envio durante run pode solicitar rerun. Consulta prévia não garante atomicidade. |
| `POST .../{id}/events/respond_to_confirmation` | Aceitar pode iniciar run. Rejeitar rejeita ações pendentes; não prova cancelamento terminal da missão. Guard global existente continua obrigatório. |
| `POST .../{id}/pause` / `interrupt` | Pause espera chamada atual; interrupt solicita cancelamento e espera até 5s no serviço. Ambos são estados retomáveis; não equivalem a Guard terminal nem morte comprovada do worker. |
| `POST .../{id}/goal/stop` | Para controlador de objetivo; não é garantia de interrupção de conversa ou LLM em voo. É a rota usada por `openhands_stop` no snapshot MCP. |
| `GET .../{id}/events/search` | `next_page_id` é o ID do **primeiro item não retornado**; próxima busca é inclusiva. Cursor inexistente reinicia busca. Evento ilegível pode ser ignorado com aviso pelo servidor: detectar lacunas fora dele. |
| `/sockets/session/{id}` | Frames duráveis possuem `seq` (índice do log); replay usa `after_seq` exclusivo. Deltas/transientes/progresso não avançam cursor. Há limites de fila/frame provisórios e desconexão do consumidor lento. |
| `/sockets/events/{id}` legado | Também recebe mensagens que podem iniciar execução. Não presumir canal somente leitura. |
| Autenticação | HTTP valida chave de sessão somente quando configurada. WebSocket suporta query/header e primeiro frame; não inferir isolamento por projeto ou RBAC. Proposta recusa segredo em URL. |

Nenhum webhook de saída com contrato de entrega foi comprovado nas fontes
inspecionadas. WebSocket/replay oficial existe, mas não é ponte Slack instalada.
Não usar eventos/deltas como instruções privilegiadas. Não coletar conteúdo
bruto, prompts, outputs, títulos, tokens de autenticação ou dados de clientes.

### Reuse gate MCP

Já existem **sete** tools no código público: health, list, status, result,
**events**, start, stop. `events` já minimiza conteúdo e exige `openhands.read`;
seu cursor admite hífen (o `-` final da classe regex é literal). Não há falha de
hífen constatada. A projeção atual elimina `event.id`, timestamp e sequência:
serve a diagnóstico, não comprova ordem/replay/correlação. Não recriar events.
`result` e títulos de list podem ser privados; não são payloads Slack.
Start é escrita não idempotente com custo; stop exige confirmação exata e
capacidade de execução, mas a semântica descrita precisa ser reconciliada com
`goal/stop`. Disponibilidade desses tools no MCP implantado não foi comprovada.

## Especificação de patch futuro — NÃO implementado no Remote-Ops-MCP

1. Preservar os tools existentes; acrescentar metadados sanitizados de identidade
   e cursor ao caminho events após teste de compatibilidade na versão implantada.
   Identidade de conversa não autentica projeto/agente. Vincular escopo por
   autorização verificada externa, não por texto do agente.
2. Propor `openhands_confirmation_state`: leitura minimizada de estado,
   quantidade/IDs opacos de ações pendentes, digest e versão da política.
   A ligação exata a uma API suportada para pendências ainda precisa ser validada;
   não anunciar esse tool como existente ou autorizado.
3. Propor `openhands_send_message`: conversa existente, papel **user** apenas,
   texto revisado limitado (sem anexos/URLs executáveis), `run=False` obrigatório
   inicialmente. Nunca criar nova conversa, nunca modificar política, usar role
   system/tool, retomar missão cancelada ou enviar a running/terminal.
   Aprovação humana vinculada a conversa, estado, conteúdo/digest, cursor,
   orçamento reservado, prazo e nonce de uso único. Aprovação de Mentor/Slack
   **não** concede autorização operacional. GO separado ainda exigido.
4. Uma consulta seguida de POST não é transação: TOCTOU, crash após append,
   resposta perdida e HTTP 429 mantêm resultado incerto. Sem idempotência
   comprovada no servidor, nenhuma promessa de exactly-once e nenhum retry.
5. Corrigir a documentação/semântica de stop somente em futura missão autorizada
   no MCP. `interrupt` também exige Guard terminal, supervisor e confirmação de
   encerramento; não afirmar cancelamento financeiro ou refund por HTTP 200.

## Implementação local entregue

`scripts/canary_continuity_contract.py` é modelo **puramente sintético**, sem
SDK, I/O, cliente HTTP ou dispatch. Reutiliza `SyntheticTransportGate`, Guard,
BudgetBook, tarifas/tetos fictícios e envelope audit v1. Permite um preparo
inerte para uma conversa declarada idle/paused, mensagem pública fixa DEMO-001,
AlwaysConfirm, zero retries, aprovação literalmente True e contabilidade
compatível. Recusa fecha book/Guard; corrida ou segundo preparo não libera a
reserva. Close mantém hold incerto. Resultado sempre `operational_go=False`,
`dispatch_allowed=False`, `authenticity_proven=False`.

Não verifica estado remoto, frescor do cursor, dono do workspace, assinatura,
autorização real ou integridade contra código hostil no mesmo processo. Não
intercepta todas as rotas de SDK. Não aplicar como middleware operacional.
9 testes RED por módulo ausente → GREEN: recusa, estado, schema/conteúdo fechado,
contabilidade vinculada, orçamento insuficiente, timeout/cancelamento, corrida,
reserva conservada, ausência de import de transporte. Autorrevisão ≠ G11.

## Ameaças e critérios futuros

Prompt injection/privacidade: evento é dado não confiável; campos fechados,
sem texto livre no alerta; revisão humana do contexto. Falsificação: checksum
não autentica; fonte assinada e escopo ainda ausentes. Replay: dedupe efêmero não
sobrevive reinício. Concorrência: lock local não substitui transação remota.
Loops: alerta não chama MCP/LLM nem produz instrução automática. Custo: reserve
antes da tentativa, hold quando incerto, supervisor independente. Cancelamento:
primeira recusa é terminal e não pode ser revertida por mensagem seguinte.

GO operacional exige separadamente: versão/API implantadas, autorização humana,
conta segregada/modelo/tarifa/quota, limites efetivos incluindo chamadas extras,
isolamento/egress, parada comprovada, fonte/cursor duráveis, RBAC multiprojeto,
revisão independente e plano de revogação. **Todos continuam pendentes conforme
matriz; estes testes não promovem G11/G12 ou P03.**
