# OBS-EXPLORER-CANARY-PLAN-001 — preparação, sem execução LLM

Data: 2026-10-11. Ferramenta horizontal multiprojeto.
**Estado: preparado para avaliação; NO-GO para tarefa LLM até fechar os gates.**

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

- REAL NOW: main `789d442e586466ee7085a1724028d7e1edba7ec0`; PR #9
  integrada, HEAD de origem `680d3a151a4bbdb11c29fca4657515e10efb8785`.
- PROVEN EVIDENCE: snapshot local separado, detached HEAD no mesmo SHA,
  árvore Git limpa; diagnóstico estático e 27 testes aprovados. SDK/Tools
  1.53.0 já instalados em virtualenv isolado. Descoberta oficial não mutadora
  localizou code-explorer, tools=[terminal], limites/permission_mode ausentes;
  registry de agentes permaneceu vazio (0 → 0). Nenhum registro/delegação/LLM.
- GAPS: modelo/provedor e tarifas não definidos para esta execução; credencial
  autorizada não provisionada neste executor. Isolamento de terminal não
  homologado. Teste local de bwrap falhou: `open /proc/8/ns/ns failed: No such
  file or directory`; presença do binário não prova sandbox. Harness de
  confirmação/global budget ainda não implementado nem testado.
- REUSE GATE: usar register_builtins_agents(enable_browser=False), TaskToolSet,
  AlwaysConfirm e limites nativos; não copiar o Explorer nem criar runtime.
- DECISION: manter execução bloqueada e registrar plano/limites observados.
  Não usar openhands_start como atalho: a ferramenta exposta só recebe target
  e task, tem workspace fixo e 20 iterações; não demonstra montagem do snapshot,
  orçamento, callback de confirmação nem TaskToolSet configurado. Nenhuma
  alteração da VPS/Canvas é autorizada por esta preparação.

## Plano do canário proposto — requer autorização explícita

1. Fixar SDK/Tools 1.53.0 e snapshot no SHA acima; verificar hashes antes/depois.
   Montar snapshot somente leitura para o terminal, sem outros workspaces,
   sessões, .git/config com credenciais ou segredos; estado SDK em diretório
   separado. A separação Git atual é organização, não isolamento de segurança.
2. Provisionar modelo/provedor autorizado somente no processo controlador;
   terminal filho não pode herdar credenciais. Verificar tarifas e contabilização
   de custo real; nenhuma chave entra em Git, prompts ou relatórios.
3. Em processo descartável, registrar presets pela API oficial com navegador
   desabilitado e capturar nomes retornados e definição code-explorer. Essa API
   registra vários presets; isso não os executa. Não chamar register_file_agents
   nem habilitar Construtor/Verificador. Só code-explorer poderá ser delegado.
4. Configurar contexto pai SDK sem executar seu loop LLM, com terminal e
   TaskToolSet. Usar TaskToolSet para uma única TaskAction de subagent_type
   code-explorer, sem resume. Pai serve como contexto da ferramenta; somente
   uma conversa filha terá inferência. SubAgentScope(tools=True,mcp_servers=True)
   restringe capacidades relativas ao pai, não é allowlist de nomes de agentes.
5. AlwaysConfirm no pai, herdado pelo Explorer. Passar confirmation_handler
   explicitamente a TaskToolSet; exigir aprovação das ações filhas e rejeitar
   qualquer comando fora da lista fechada de leituras. Callback ausente NÃO
   constitui confirmação humana: no SDK 1.53.0 o manager continua o loop.
6. Tarefa sintética: ler somente docs/PROJECT_SOURCE.md, AGENTS.md,
   team/README.md e team/catalog.json; explicar a separação horizontal,
   identificar code-explorer como candidato nativo e listar evidências ainda
   ausentes. Citar caminhos/linhas, sem construir, testar, editar ou publicar.
   Allowlist proposta: pwd; cat dos quatro caminhos exatos; git rev-parse HEAD.
   Nenhum env/printenv, rede, shell composto, redirecionamento ou escrita.
7. Uma missão, uma delegação, zero retomadas/repetições. Capturar IDs pai/filho,
   task_id, subagent, estados, comandos aprovados/rejeitados, resposta sintética,
   custos/tokens, limites efetivos, horários e hashes. Avaliar o conteúdo;
   finished/completed isoladamente não prova sucesso semântico.
8. Encerrar processo e registrar somente evidências minimizadas. Não alterar
   catálogo para operacional nem integrar nós no Canvas neste primeiro teste.

## Orçamento e limites: proposta versus implementação comprovada

- **Estimativa monetária: dados insuficientes** até definir modelo/provedor,
  tarifas e tokenização. Não há estimativa verificável baseada na instalação
  existente. Fórmula: tokens de entrada × tarifa + tokens de saída × tarifa,
  incluindo chamadas auxiliares e custos de condensação quando houver.
- Proposta inicial para discussão: `max_budget_per_run=0.10` USD e
  `max_iteration_per_run=6` no contexto pai; code-explorer nativo não define
  limites próprios, então a tarefa filha os herda em TaskManager._create_task.
- Orçamento SDK compara custo acumulado nos pontos de controle do loop. Pode
  exceder 0.10 USD durante uma chamada já iniciada; não é garantia de cobrança
  máxima no provedor. Custo desconhecido/zero não autoriza prosseguir.
- Iterações SDK são **por chamada a run()**; o contador reinicia e TaskManager
  chama run() novamente nas confirmações. O valor 6 não é teto global da missão.
  Exigir contador global de chamadas e encerramento externo (proposta: até seis
  chamadas LLM totais, 120 segundos, num_retries=0), com testes sem LLM antes
  de execução. Estes controles ainda NÃO estão implementados/homologados.
- Definir max_output_tokens e teto de entrada conforme o modelo suportado;
  verificar suporte efetivo e contabilização antes de estimar pior caso.
- Exigir limite no provedor/credencial caso necessário teto financeiro rígido.
  Sem mecanismo comprovado, não declarar controle rígido de gastos.

## Fontes técnicas lidas — distribuição oficial instalada 1.53.0

- openhands/tools/preset/default.py: discover_builtin_agents,
  register_builtins_agents e habilitação de tools.
- openhands/tools/preset/subagents/code_explorer.md: terminal, sem limites
  próprios, instruções de leitura (instruções não são sandbox).
- openhands/tools/task/definition.py: TaskToolSet.create, confirmation_handler,
  SubAgentScope; TaskAction.max_turns é deprecated e ignorado.
- openhands/tools/task/manager.py: herança de limites/policy, conversa filha,
  confirmação, resultado e métricas. Callback None permite continuar.
- openhands/sdk/conversation/impl/local_conversation.py: orçamento contabilizado
  e iteration=0 em run(), inclusive reentradas para confirmação.
- openhands/sdk/llm/llm.py: max_output_tokens, num_retries e tarifas por token.

## Gate humano e próximo passo

Não houve chamada register_builtins_agents, execução TaskToolSet ou LLM.
Antes da autorização operacional: definir modelo/provedor/credencial, homologar
isolamento e callback fail-closed, contador global e gasto verificável em testes
sem LLM. Depois apresentar custo/limites concretos e obter autorização explícita
para a missão congelada. Nenhum merge, deploy, alteração remota ou polling de CI.
