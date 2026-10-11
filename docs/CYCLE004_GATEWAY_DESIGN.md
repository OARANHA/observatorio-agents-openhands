# Gateway CYCLE004 — modelo sintético em memória

**Não é servidor, cliente Slack, integração OpenHands ou autenticação.**
Não instalado. Nenhum webhook/token/secret provisionado. NO-GO operacional.
Reutiliza envelope audit v1 e `SyntheticEvidenceSession`, sem recriar SDK.

## Contrato implementado e testes

`scripts/canary_event_gateway.py`: conversa UUID declarada, SHA público declarado,
janela UTC explícita e 1–64 registros; schema fechado, source exclusivamente
`openhands-synthetic`, mission DEMO-001. Eventos mínimos: needs_review/blocked,
task_finished/finished e task_failed/error. Conteúdo livre, prompt, credenciais,
menções, links e campos desconhecidos são recusados. Não é parser de evento real.

Sequência sintética local começa em zero; não é cursor do servidor. Cada receipt
é validado pelo envelope e consumidor existentes: checksum, contabilidade,
origem declarada, janela, ausência de regressão e limite. Checksum NÃO autentica.
Replay idêntico confirmado é ignorado sem segunda tentativa; replay conflitante,
salto/regressão ou binding incorreto bloqueiam a instância. Lock cobre apenas
esta instância no processo. Não protege outros processos nem reinício.

A saída de alerta deriva somente de enums fixos e contém OBS-TEST-V1, DEMO-001 e
aviso de nenhum agente real executado. Não inclui UUID, cursor, source SHA,
accounting, títulos, conteúdo de ações ou dados de cliente. Resultado sempre
`operational_go=False`, `authenticity_proven=False`, `actions_allowed=False`.

O parâmetro **mock_outcome** é string de teste, não callback/transport: success,
failed ou unknown. Falha/incerteza simula uma única tentativa e bloqueia qualquer
redelivery/retry. Nenhuma mensagem foi efetivamente enviada. Não há persistência;
instância nova aceita novamente o mesmo receipt (lacuna explicitamente testada).
Limite de registros/janela é teto sintético, não rate limit do Slack nem relógio
confiável. Não alegar exactly-once, assinatura de origem ou recuperação durável.

9 testes RED (módulo ausente) → GREEN: projeção minimizada, replay exato/conflito,
gaps, binding, prompt injection/campos privados, falha/resultado incerto, janela,
checksum/regressão/capacidade, concorrência e lacuna de reinício. Suite completa
local:210 testes,182 PASS/28 skips SDK explícitos. Sem transporte/provedor/agente.

## Design futuro — depende de autorização separada

Fluxo: OpenHands autorizado → receptor isolado → validador/minimizador → outbox
→ Slack → Work **somente orientação** → humano → eventual MCP autorizado.
Orientação jamais é aprovação automática. O Observatório apenas apresenta os
vínculos e atividades; continua horizontal, sem primazia Wandora/VIGIAFAST/ELUS.

Receptor deve reutilizar stream/replay oficialmente suportado na versão
implantada, sem apostar em webhook inexistente. Frames transientes/deltas não
avançam cursor. Só evento durável identificado pode entrar após validação da
fonte/escopo. Stream com lacuna ou cursor desconhecido entra em reconciliação;
não resetar silenciosamente para início. Recusa de confirmação exige Guard
terminal e supervisor, não `goal/stop` isolado. Conferir fontes no
[CYCLE004_CONTINUITY_CONTRACT](CYCLE004_CONTINUITY_CONTRACT.md).

Antes de qualquer implementação conectada:

- Provar API/versão implantada, TLS/origem, autenticação da fonte e RBAC por
  projeto, segredo segregado com revogação e ausência de segredo em URL/log.
- Definir event_id durável, sequência, TTL, nonce, store de replay e outbox
  transacionais. Persistir somente campos minimizados e política de retenção.
- Definir allowlist de eventos/canais, quotas por escopo, tamanho/frequência e
  backpressure. Falha/429/timeout não autoriza retry cego: reconciliação manual.
- Separar estado received/validated/projected/uncertain/confirmed; identificar
  qual confirmação existe. Ack de Slack não prova disparo Work nem execução.
- Testar crash entre persistência/envio/ack, eventos fora de ordem, replay entre
  reinícios, corrida entre workers, assinatura expirada e revogação de escopo.
- Manter sem execução de comandos, provider fallback, autorização por texto,
  leitura de histórico privado ou loops de automação. Human GO obrigatório.

Nenhum desses componentes persistentes/operacionais foi instalado ou criado.
Slack → Work permanece bloqueado pelo app oficial não reconhecido; não trocar
por polling. Autorrevisão automatizada não cumpre G11. G12 segue BLOQUEADO.
