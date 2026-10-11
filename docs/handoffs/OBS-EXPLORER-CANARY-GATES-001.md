# OBS-EXPLORER-CANARY-GATES-001 — 2026-10-11

## REAL NOW

`main` reconfirmada em `789d442e586466ee7085a1724028d7e1edba7ec0`
(PR #9 integrada). PR #10 permanece aberta, branch `docs/explorer-canary-plan-v1`,
HEAD `f52b635290ba9e542e2bbb01a9d5a657fed11452`. Seu handoff
`OBS-EXPLORER-CANARY-PLAN-001.md` foi lido; esta implementação é independente,
na branch `feat/explorer-canary-gates-v1`. Não incorpora nem altera a PR #10.
Observatório permanece ferramenta horizontal; nenhum projeto atendido foi alterado.

## PROVEN EVIDENCE

### Sandbox

Bubblewrap 0.9.0 instalado. Probe sem tarefa nem LLM:
`bwrap --unshare-user --ro-bind / / /bin/true` falhou antes do comando com
`bwrap: open /proc/8/ns/ns failed: No such file or directory`.
`/proc/self/ns/mnt` e `/proc/self/ns/user` existem; `/proc/8/ns` não existe.
Alternativa `unshare --user --map-root-user --mount --net /bin/true` falhou com
`write failed /proc/self/uid_map: Operation not permitted`.
Tracing por `strace` também bloqueado: `PTRACE_TRACEME: Operation not permitted`.
Não foi possível determinar a causa completa entre kernel/runtime/mapeamento
PID; não atribuir isso a uma configuração específica da VPS ou Docker.

`canary_controls.snapshot` copia somente quatro arquivos públicos revisados
(PROJECT_SOURCE, AGENTS, team/README e team/catalog), sem `.git`, credenciais,
links simbólicos ou diretório de estado dentro da origem. Estado novo separado
com modo 0700. `sandbox_argv` monta somente `/usr` e snapshot em leitura,
usa `--unshare-all`, ambiente limpo, capabilities removidas, `/tmp` efêmero e
argv fixo sem shell. O subprocesso recebe `env={}`, nenhum stdin e FDs fechados.
**Construção do comando testada não prova isolamento em execução.**

A alternativa por namespaces (`unshare`) não funciona aqui. Landlock/seccomp
sozinhos não demonstram todos os requisitos de rede/processos/filesystem.
Um runner efêmero com namespaces habilitados seria alternativa futura sujeita
à autorização e probes negativos; não foi criado. Não houve alteração de Docker.
Falha de sandbox resulta em erro, sem fallback para terminal do host.

### SDK e harness

SDK/Tools 1.53.0 inspecionados no ambiente isolado, sem credenciais.
APIs oficiais reutilizadas: `Tool`, `TaskToolSet`, `TaskAction`,
`TerminalTool.create(executor=...)`, `ToolExecutor`, `TerminalObservation`.
Construção inerte real de TaskToolSet, TerminalTool com executor restrito e
TaskAction code-explorer aprovada. Nenhum `Conversation`, `run()`, registro de
agente ou execução de TaskAction realizada.

`sdk_bindings` expõe a função oficial `register_builtins_agents`, sem chamá-la.
Ela registra múltiplos presets; o futuro worker deve restringir despachos a
`explorer_action`, reservar uma única delegação e usar apenas code-explorer.
`SubAgentScope` restringe ferramentas/MCP, não os nomes de agentes.
O executor restrito deve substituir a ferramenta terminal via API oficial
`register_tool` apenas no futuro processo dedicado; não é instalado agora.
Sem esse wiring comprovado, permanece NO-GO. Não há CLI que inicie LLM.

O callback é explicitamente passado a TaskToolSet: ausência de callback no SDK
poderia permitir continuação automática. Nosso callback nega aprovação ausente,
valor diferente de True, ação desconhecida, input interativo e comando fora da
lista exata. Executor repete a validação mesmo se chamado diretamente.
Apenas `pwd` e os quatro `cat` são permitidos; pipelines, redirects, expansão,
rede, `env` e caminhos adicionais são negados. Prompt não é limite de segurança.

Guard global compartilhado cobre completion/responses síncronos e assíncronos,
mesmo em cópias de LLM e novos run(): defaults de **6 chamadas**, **120 segundos**,
**US$ 0,10 contabilizados**, zero retries. Registro somente code-explorer, uma vez.
Deadline monotônico, cancelamento terminal e encerramento do grupo de subprocesso
por SIGKILL no supervisor. Timeout real testado com `/bin/sleep`, sem agente.
Métodos da classe LLM são envolvidos somente no processo dedicado e restaurados;
nenhum arquivo do SDK/Core é alterado. Rotas aninhadas são contadas conservadoramente,
possivelmente duas vezes. Timeout de uma chamada em voo exige supervisor externo
sobre todo o worker; Guard sozinho não interrompe uma conexão bloqueada.

### Tokens, custos e modelos

Contabilidade usa deltas de `llm.metrics.accumulated_cost` e
`accumulated_token_usage.prompt_tokens/completion_tokens` por chamada.
Métricas ausentes, inválidas ou custo zero impedem continuação; modelos gratuitos
não são suportados neste gate. Rates explícitos oficiais existem em
`LLM.input_cost_per_token/output_cost_per_token`; `num_retries=0` é obrigatório.
`max_output_tokens` e timeout devem ser fixados na futura configuração revisada.
Nenhuma configuração privada foi lida ou publicada.

LiteLLM 1.103.4 instalado contém `litellm/cost.json`, mas nenhum registro com o
par de tarifas positivas requerido foi encontrado; não há tabela vigente validada.
`quote` valida estimativas com catálogo público fornecido offline; testes usam
modelo sintético. Catálogo não certifica disponibilidade na conta. Obter lista
pública oficial do provedor e tarifas com data, selecionar um modelo específico,
validar disponibilidade mediante configuração separada autorizada, sem credencial
produtiva e sem chamada LLM de descoberta. Não usar catálogo desatualizado como prova.

US$ 0,10 é limite **entre chamadas**, não teto financeiro absoluto: a última
chamada pode ultrapassá-lo. Sem tarifa confiável e teto de tokens verificável,
nenhum orçamento real pode ser autorizado. Para GO exigir teto preventivo por
chamada + orçamento reservado para a pior resposta e limite do provedor, se disponível.

### Verificação reproduzível

- `python3 -B -m unittest discover -s tests -p 'test*.py' -v`: **45 testes**, incluindo
  18 novos de gates (mocks, prazo global, interrupção, zero retries, aprovação,
  contabilidade, snapshot e uma ação oficial inerte).
- `python3 -B scripts/check_team_sdk.py`: contrato estático válido, sem registro/delegação.
- `node scripts/build.mjs`; `node --check extension.js`;
  `git diff --exit-code -- extension.js`: geração e sintaxe preservadas.
- SDK 1.53.0: construção de specs/ação/executor inertes em ambiente limpo.

Os testes provam controles locais, não operação de agente, isolamento de sandbox
bem-sucedido, integração no Canvas, registro ou delegação real.

## GAPS → REUSE GATE → DECISION

**NO-GO para o primeiro canário real. GO apenas para revisão dos controles.**
Reutilizar SDK/Tools, builtins e TaskToolSet; não construir runtime alternativo.
Critérios cumulativos para GO operacional:

1. Sandbox executável no runner autorizado; testes negativos de escrita no snapshot,
   rede, credenciais/FDs, leitura externa e sobrevivência de descendentes comprovados.
2. Worker dedicado inteiro supervisionado; terminal oficial substituído pelo executor
   restrito e callback fail-closed observado com TaskToolSet real sem LLM inicialmente.
3. Todas as rotas de chamadas/fallback verificadas no modelo escolhido, zero retries,
   uma delegação e Guard compartilhado em todo o ciclo (incluindo confirmações).
4. Modelo, tarifas vigentes, tokens máximos, orçamento preventivo e credencial sintética
   separada definidos. Não há estimativa financeira real aprovada nesta missão.
5. Aprovação explícita humana para uma tarefa sintética com LLM, plano e limites finais.
6. Evidência minimizada de registry antes/depois, tipo code-explorer, ID de delegação,
   confirmações, tokens/custos e término; sem prompts privados ou segredos.

Risco residual: monkeypatch de fronteira pública precisa revalidação em qualquer
atualização de SDK e não protege código que contorne essas APIs; concorrência não
faz parte do canário. Snapshot deve vir de checkout público congelado, sem modificações
concorrentes durante a cópia. Estado/logs devem ser eliminados após revisão autorizada.
Não tratar esse harness como plataforma geral de execução.
