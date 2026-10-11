# OBS-CYCLE-004-EVENTS-MENTORSHIP

2026-10-11 · **NO-GO operacional** · ferramenta horizontal multiprojeto.
Método: REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION.

## Estado reconciliado e rastreabilidade

Main inicial: `242856c523b1880328b6bb985f6fcedf0a7c58c2` (#37 integrada).
Main final do código: 96ed4a3c5ce659aa55a4841716e7623d30aaeb64. SHA final da consolidação é o
`merge_commit_sha` da PR de fechamento: registrado após confirmação da ref
main na descrição dessa PR. Não tentar gravar um SHA de commit dentro dele
próprio; usar esse registro externo vinculável, sem autodeclaração circular.

| PR / incremento | HEAD exato | Merge confirmado | CIs no HEAD |
|---|---|---|---|
| [#38](https://github.com/OARANHA/observatorio-agents-openhands/pull/38), continuidade | 78d08d1129755a259137bf764458a7c26f63b339 | 7c152857fae2859b6dc7cb8977ebb3cd6fa54eaf | [principal38161220593](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38161220593), [SDK38161220592](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38161220592), GREEN |
| [#39](https://github.com/OARANHA/observatorio-agents-openhands/pull/39), gateway | 89f7e9f168a0e560640b7bb7cd6c58be458a0b7c | 9e25aa67eea7a15b9d61ed7f249202644b9ee1d8 | [principal38161636349](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38161636349), [SDK38161636333](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38161636333), GREEN |
| [#40](https://github.com/OARANHA/observatorio-agents-openhands/pull/40), Mentor DEMO | b3ee40f9f1a08f674ad456106e6bcc46e1f4ada0 | 96ed4a3c5ce659aa55a4841716e7623d30aaeb64 | [principal38162575498](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38162575498), [SDK38162575476](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38162575476), [DOM38162575506](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38162575506), GREEN |
| Consolidação deste handoff | HEAD/merge/CIs na descrição da PR de fechamento, reconciliados após criação | Somente após critérios offline | Sem usar CI de outro HEAD |

Logs reais completos inspecionados **antes** dos merges deste ciclo. Duas CIs
obrigatórias e DOM adicional pertinente; nenhuma troca de teste/sandbox por
GREEN. Revisões adversariais em contexto separado são **autorrevisões
automatizadas**, não homologação independente G11:
[#38 revisão5484300319](https://github.com/OARANHA/observatorio-agents-openhands/pull/38#pullrequestreview-5484300319),
[#39 revisão5484332648](https://github.com/OARANHA/observatorio-agents-openhands/pull/39#pullrequestreview-5484332648),
[#40 revisão5484351485](https://github.com/OARANHA/observatorio-agents-openhands/pull/40#pullrequestreview-5484351485).
Nota CI #40 teve dois IDs de jobs incorretos na prosa, embora o JSON da própria
nota e os logs conferidos antes do merge fossem corretos; retificação registrada
na PR, sem mudança de HEAD/resultados. Diff --check também detectou EOF extra na
fixture; normalizado com checksum/HTML regenerados e três CIs repetidas no HEAD
final antes do merge.

Diffs/leases de HEAD/main confirmados; nenhum handoff anterior removido.
O desvio histórico de logs tardios #34 permanece registrado no
[handoff CYCLE003](OBS-CYCLE-003-CONTINUITY.md); não foi reescrito como correto.

PR7 continua aberta/draft HEAD48f898d99a8979ef2c794513131506b028772666;
PR35 aberta HEAD811d5fa4c48aa9eb2cf618174b7d645039a590ac. Nenhuma foi alterada,
retargetada ou integrada. Canvas historicamente v0.4.2 instalado não foi
modificado; nenhuma DEMO deste ciclo foi instalada ali.

## Implementado/testado apenas offline

- Continuidade: uma intenção fictícia em mesma conversa; Guard/BudgetBook/
  tarifas e tokens sintéticos reutilizados. Aprovação literal, estado e schema
  fechados, zero retries, hold conservado, timeout/cancelamento, corrida. Sempre
  dispatch_allowed/operational_go/authenticity_proven=False.9 novos testes.
- Gateway: envelope/session existentes, enums públicos DEMO, sequência e replay
  locais, gaps/binding/janela/contabilidade/capacidade, prompt injection/campos
  privados recusados. Mock failed/unknown terminal sem retry; replay confirmado
  sem novo envio.10 novos testes. Cap interno agora aparece no summary após
  observação adversarial. Instância nova aceita receipt antigo: lacuna provada.
- Mentor: HTML independente da extensão, funções de identidade local PR35
  reutilizadas com origem/hash, contexto revisável/excluível, consentimento
  revogado ao mudar seleção, recomendação fixa e NO-GO. Node9/9 e Python2/2.
  DOM Chromium5/5PASS, zero skip: revisão/sem egress, teclado/Escape, vazio/erro,
  teardown/remount e mobile/foco.9Node também PASS nesse workflow. Capturas
  desktop/mobile finais examinadas: artefato11711135617 do HEADb3ee40f...,
  ZIP SHA2564f7e5ca0d9f0abe90fda3d7bdfca1fae29f3c5e740ee92df17186ad3bb6d9dfe.
  PNGs SHA256desktop b3f05e608d6f610fedbfec0cfd52975bd8140eb004ec7869dce416215ca1656b;
  mobile2371471c9fba6981cd3a2bc6ee44f450b575a4c1bdd69de627b7d359252f8202.
  Expires2026-10-14T18:09:12Z, evidência visual efêmera; não Canvas instalado.
  Mobile usa scroll interno; testes não certificam leitor de tela/contraste/RBAC.
- Testes completos locais finais:213 Python,185 PASS/28 skips SDK explicitamente
  disponíveis apenas no runner isolado. Node9 são executados também dentro de
  um teste Python: não somar como testes distintos sem declarar sobreposição.
- CI principal #38:201/173PASS/28SDKskip; #39:211/183PASS/28SDKskip.
  CI principal #40:213/185PASS/28SDKskip. Jobs: #38 principal114534363460/
  SDK114534363518; #39 principal114535598825/SDK114535598628; #40 principal
  114538394917/SDK114538394649/DOM114538394729. SDK dedicado em cada HEAD:
  125 PASS/zero skip; bwrap negativo real efêmero,
  SDK/Tools1.53.0, transports/stubs e worker inertes, zero actual_llm_calls /
  actual_agent_registrations / actual_task_dispatches. Os skips da principal
  estão documentados e cobertos pela suite dedicada; nenhum agente operacional.
- Estático `python3 -B scripts/check_team_sdk.py`, geração `node scripts/build.mjs`,
  sintaxe `node --check extension.js`, geração/sintaxe Mentor e diff --check PASS.

RED→GREEN: continuidade9/gateway9 por módulos ausentes; décimo gateway após
feedback de estado. MentorNode9 por modelo ausente. DOM inicial real4/5PASS em
HEADc5b1f0063a154667a5f2ab0b0575caaaaedf4eb0/run38162140153/job114537096182:
Tab escapou do diálogo Shadow DOM. Correção mantém teste de contenção e sandbox,
adiciona ciclo Tab/ShiftTab e assertiva de wrap reverso na mesma branch. Nenhum
RED financeiro/isolation foi reproduzido neste ciclo; não inventar correção.

## Slack conectado e resultado verdadeiro Slack → Work

Conector respondeu no workspace Wandora. `#observatorio-eventos` já existia.
Criado `#observatorio-aprovacoes` público para teste autorizado. Nomes/IDs de
usuários e conteúdo de históricos não foram publicados.

Schema Work de gatilho Slack foi consultado: mensagem nova em canais definidos,
`include_thread_replies=False`; condição semântica na tarefa, sem filtro de texto
no schema. Uma tentativa de criação de tarefa por evento, sem horário/polling,
foi recusada: serviço não reconhece aplicativo oficial no canal. Nome `@chatgpt`
na lista de membros não comprova vínculo. **Nenhuma tarefa criada, nenhuma
mensagem OBS-TEST-V1 enviada, nenhum disparo/execução Work comprovado.**
Não executar manualmente a tarefa como substituto de prova de evento.

Fixture preparada (não enviada):
`OBS-TEST-V1 | source=openhands-synthetic | event=needs_review | mission=DEMO-001 | status=blocked | Nenhum agente real executado.`

Dependência humana: instalar/reconectar
[app oficial](https://chatgpt.com/slack-ai-app-install) e adicionar ao canal.
Depois, dentro de autorização de teste: criar uma tarefa event-driven restrita,
sem respostas de thread, classificar apenas fixture exata, sem ações/Slack
writes/MCP/LLM de provedor; emitir uma mensagem, comprovar um disparo e ausência
de loop, desabilitar teste. A classificação Work não concede GO operacional.

## API e MCP: código confirmado, implantação desconhecida

Ver [contrato e fontes fixadas](../CYCLE004_CONTINUITY_CONTRACT.md): SDK/AgentServer
v1.53.0 commit54daf056bd863bb46f922a2fe9324dd736b37ff6; MCP público commit
235fd9359cbf56e5aa7cf46c3f0fe224ee242cdd. Nenhuma chamada à API implantada.

Já há sete tools públicos, incluindo **events**. Reutilizar esse diagnóstico,
não recriá-lo. Sua projeção não preserva event.id/seq: falta contrato de cursor/
ordem e prova de escopo. Result/títulos podem ser privados; não repassar ao Slack.
`stop` usa goal/stop, sem garantia de interrupção de conversa/LLM em voo.

POST events persiste mensagem antes de run; HTTP429 pode significar já salva.
`run=False` ainda é escrita e pode interromper goal loop. Role user deve ser
restrito na proposta futura; API oficial aceita outros papéis. Consulta e POST
não são atômicos; zero retry, estado incerto e revisão humana necessários.
Rejeitar confirmação no servidor não cancela terminalmente a missão: Guard e
supervisor existentes permanecem obrigatórios. Pause/interrupt são retomáveis.

**Ambos** sockets events legado e session com replay também recebem Message e
chamam send_message(...,True). Cursor de replay não torna socket somente leitura.
No receptor futuro, impedir envio de frames de mensagem após handshake; não
conectar/autorizar agora. Deltas/transientes não avançam cursor. Buscar eventos
com cursor desconhecido pode reiniciar busca; não aceitar reset silencioso.

Propostos apenas: metadados minimizados de cursor no events existente,
confirmation_state (binding API de pendências ainda a validar), send_message na
mesma conversa sob aprovação/GO separado. Nenhum patch aplicado ao MCP real.
Versão/API/RBAC/políticas/quotas/encerramento do ambiente implantado não provados.

## Gateway e ameaças

[Design completo](../CYCLE004_GATEWAY_DESIGN.md): stream/replay oficial → receptor
isolado → validação/minimização → outbox → Slack → Work orientação → humano →
eventual MCP autorizado. Nenhum desses serviços persistentes foi criado.
Fonte não confiável nunca vira comando, policy, system role ou autorização.
Faltam assinatura/origem/RBAC, store durável, outbox/transação, TTL/revogação,
rate limit real, tratamento de crash/ack perdido e reconciliação de lacunas.
Checksum é integridade acidental, não autenticidade; lock de instância não
resolve múltiplos processos; delivery mock não é prova Slack/Work.

Mitigações sintéticas testadas: conteúdo fechado, projeção sem privados, replay
local, falha incerta terminal, orientação sem dispatch, recusa/limites existentes
preservados. Eventos/prompts não confiáveis continuam dados, não instruções.

## Matriz antes → depois e decisões humanas

| Gates | Antes → depois | Evidência / pendência |
|---|---|---|
| G01 | PROVADO → PROVADO | GitHub/SHA/CI/logs/merges deste ciclo rastreáveis |
| G02–G04 | PROVADO OFFLINE → PROVADO OFFLINE | Reuso financeiro, SDK/stubs/Guard, zero operação |
| G05/G06 | PARCIAL → PARCIAL | Regressões offline preservadas; egress/transportes reais ainda requerem homologação |
| G07 | PARCIAL → PARCIAL | Recusa terminal sintética; stop remoto/cleanup/retomada não homologados |
| G08 | PARCIAL DOCUMENTAL → PARCIAL DOCUMENTAL | Sem conta/modelo/tarifa/quota escolhidos |
| G09/G11 | NÃO PROVADO → NÃO PROVADO | Credencial segregada/revisão independente ausentes |
| G10 | PARCIAL → PARCIAL | Gateway/order/replay/contexto sintéticos; autenticação/restart/atomicidade ausentes |
| G12 | BLOQUEADO → BLOQUEADO | NO-GO, autorização operacional separada ausente |
| P01 | PARCIAL → PARCIAL | Mentor DEMO/proveniência local, nenhuma fonte autenticada/instalação |
| P02/P03 | NÃO PROVADO → NÃO PROVADO | Hash local não é RBAC; memória persistente não testada |

Próximo plano de homologação:
1. Proprietário resolver vínculo oficial Slack; teste único de evento sintético,
   classificação e ausência de loop/ação, com evidências e desligamento do teste.
2. Revisão independente do pacote/gates. Decidir contexto permitido ao Mentor e
   identidade/escopo/RBAC sem assumir projeto pelo texto ou status de conversa.
3. Autorizar separadamente eventual missão no MCP para compatibilidade somente
   leitura e patch aprovado; resolver stop/cursor/API implantada antes de envio.
4. Homologar isolamento, origem/outbox/replay persistente, conta segregada, tarifas,
   tokens/custo/timeout/zero retries e parada real. Só então apresentar canário
   único code-explorer, orçamento e limites efetivos para GO humano separado.

Nenhum deploy, Core/Canvas/VPS/Docker/infra, credencial produtiva, provedor pago,
agente real, tarefa OpenHands ou outro projeto foi modificado/acionado. Quatro
PRs úteis bastam: última consolida os resultados, sem incremento artificial.
