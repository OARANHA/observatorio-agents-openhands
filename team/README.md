# Equipe de agentes do Observatório — primeira etapa

> **Estado: candidatos definidos em Git, não agentes implantados.** Este diretório guarda contratos para a operação **horizontal multiprojeto**. OpenHands executa missões autorizadas; ChatGPT coordena conforme acessos; Observatório exibe evidências; GitHub guarda código e documentação. VIGIAFAST, Wandora, ELUS e outros são projetos **atendidos**, nunca proprietários da infraestrutura.

## REUSE GATE — capacidades já existentes

1. **Explorador:** preferir o subagente nativo `code-explorer` do OpenHands. A documentação oficial afirma que ele é especialista em leitura de código. Não criar cópia do agente até que uma lacuna real seja comprovada.
2. **Construtor:** o OpenHands já dispõe de execução geral e ferramentas `terminal`/`file_editor`; o arquivo `../.agents/agents/observatorio-construtor.md` acrescenta um contrato restritivo de trabalho.
3. **Verificador:** revisar de maneira independente via `../.agents/agents/observatorio-verificador.md`. Avaliar reutilização das skills oficiais `code-review`, `qa-changes` e `security` **somente quando habilitadas/compatíveis e dentro do escopo**. Não copiar suas implementações.

Referências oficiais verificadas: [agentes definidos por arquivo](https://github.com/OpenHands/docs/blob/main/sdk/guides/agent-file-based.mdx), [delegação `TaskToolSet`](https://github.com/OpenHands/docs/blob/main/sdk/guides/task-tool-set.mdx) e [OpenHands Extensions](https://github.com/OpenHands/extensions).

## Como integrar no futuro (não executado)

A especificação atual do **Software Agent SDK** prevê:
- `register_builtins_agents()` para registrar agentes nativos como `code-explorer`;
- `register_file_agents(project_path)` para localizar `<project>/.agents/agents/*.md`;
- `TaskToolSet` no agente coordenador, delegando pelo identificador `subagent_type`.

Essas chamadas **não foram realizadas** neste slice. Não está demonstrado que a instalação específica do Canvas ofereça esse fluxo nem que carregue esses arquivos automaticamente. **A presença dos Markdown no Git não cria agentes em execução.** Os arquivos ficam inicialmente no repositório do Observatório, portanto seu alcance automático, se confirmado, é **somente esse workspace**. Para uso em todos os projetos, avaliar instalação oficial por **user-level** `~/.agents/agents/` ou pacote/plugin com controle de permissões; não copiar os arquivos para os outros repositórios sem autorização.

O campo `permission_mode: always_confirm` impõe confirmações quando o SDK respeita o contrato. **Não substitui** RBAC do servidor, bloqueio de rede, workspace isolado ou validação das ações no backend. O acesso de `terminal` não é intrinsecamente somente leitura. Não presumir equivalência entre prompt de papel e restrição de segurança.

## Fluxo de uma missão

**Porta 0 — Autoridade e escopo:** o operador autoriza objetivo, repositório, workspace, branch, teto de custo/iterações e ações permitidas. Sem autorização, parar.

**Porta 1 — Explorar:** `code-explorer` devolve relatório com fontes (caminhos e refs), reaproveitamentos e lacunas. Sem edição de arquivos.

**Porta 2 — Construir:** `observatorio-construtor` recebe contrato fechado, efetua somente operações confirmadas em workspace/branch autorizados e devolve diff/testes/evidências. Não criar PR/merge/deploy automaticamente.

**Porta 3 — Verificar:** `observatorio-verificador` inspeciona alterações e evidências sem alterá-las. Apresenta achados verificáveis, testes executados ou ainda não verificados.

**Porta 4 — Humano:** o proprietário decide abertura de PR, merge, deploy, mudança de escopo e operações sensíveis conforme cada permissão. Estado final é registrado com origem.

Os agentes **não** podem afirmar conclusão de tarefa só porque uma conversa OpenHands apresentou `finished`. O grafo deve distinguir `agent_role_definition`, `openhands_conversation_if_verified`, `manual_declaration` e `human_approved`.

## Contrato de dados

Fonte: [`catalog.json`](catalog.json). Cada papel declara identificador, tipo (nativo ou definido por arquivo), capacidades esperadas, entradas necessárias, resultados permitidos, estado de implantação **não verificado** e evidências exigidas.

As transições de missão são propostas, não automação. Nenhum webhook, polling, trigger, serviço em segundo plano, credencial, banco de dados, deploy ou operação remota é criado nesta entrega.

## Critérios de aceitação para próxima fase

1. O OpenHands instalado confirma, por leitura segura de sua versão/capacidades, suporte às APIs e ao registro dos subagentes.
2. Os arquivos são lidos pelo loader oficial do SDK **em ambiente de teste isolado**, registrando apenas metadados e nunca segredos.
3. Primeira missão sintética e limitada, iniciada somente com autorização explícita, demonstra delegação ao Explorador, depois ao Construtor e por fim ao Verificador.
4. Cada saída inclui fonte, escopo, observado_em, resultado e lacunas; o Observatório só exibe agente operacional depois de evidência real de delegação.
5. Nenhum agente acessa outro projeto, publica segredos, faz merge ou deploy sem autorização; testes de permissão e de falha são obrigatórios.

## Decisões e limites

JEV recomendou `deep_review` como rota **consultiva**, não como autorização. Context7 e a documentação oficial do GitHub confirmaram o formato de subagente. Não foi realizada prova de execução do SDK ou da delegação.

**Não confundir dois conceitos:** *skills* são conhecimentos/procedimentos carregados por agente; *subagentes* são delegados definidos por perfil. Para o primeiro time, usamos o agente nativo e definimos dois subagentes em Markdown, evitando implementar novo runtime.

## Diagnóstico local sem ativação

O loader SDK/Tools 1.53.0 foi validado em ambiente local isolado, sem registro
ou delegação. Use `python3 -B scripts/check_team_sdk.py` para contrato estático;
`--sdk` exige ambas as distribuições na versão exata 1.53.0.
Procedimento e provas em [SDK_DIAGNOSTIC.md](SDK_DIAGNOSTIC.md).
Registro e funcionamento na instalação Canvas continuam não comprovados.
