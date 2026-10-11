# Diagnóstico de subagentes OpenHands — execução segura

Este arquivo é um **procedimento de diagnóstico local** para a equipe horizontal do Observatório; não instala, registra ou inicia agentes. VIGIAFAST, Wandora, ELUS e outros projetos são atendidos, não pertencem ao Observatório.

## Relato histórico OBS-TEAM-CANARY-001 (ZIP fornecido, 2026-10-11)

Os itens abaixo são evidências relatadas no pacote fornecido pelo proprietário. O resultado MCP original não foi relido nesta integração; não são novas observações do runtime remoto.

- OpenHands SDK / Tools / Agent Server `1.53.0` reportados pela missão sintética.
- Importações de `TaskToolSet` e `register_builtins_agents` funcionaram no workspace `/projects/mcp-coordination-lab`.
- `code_explorer.md` encontrado no preset do pacote, mas seu **registro nessa sessão não foi comprovado**.
- A pasta `.agents/agents` estava ausente; workspace continha somente `.git`.
- Nenhuma delegação foi tentada. Conversa `a075c791-b4cc-4f89-9bbb-d5d9b3042411` terminou em `finished`, que não equivale a agente operacional.
- O relato de que `register_file_agents` “não existe” foi **corrigido por leitura do código oficial `v1.53.0`**: está em `openhands.sdk.subagent.registry` e é exportado por `openhands.sdk.subagent`.

Código upstream: https://github.com/OpenHands/software-agent-sdk/blob/v1.53.0/openhands-sdk/openhands/sdk/subagent/__init__.py

## Reuso e três portas de validação

1. **Arquivo válido**: conferir os dois Markdown e a política de confirmação sem SDK (teste estático, não atesta compatibilidade integral YAML).
2. **Loader SDK**: dentro de workspace local, com OpenHands instalado, chamar apenas `load_project_agents`. Confirmar nomes carregados e arquivo builtin; não registrar.
3. **Delegação real**: requer missão nova com autorização, orçamento, workspace e ferramenta de delegação efetivamente habilitada. A delegação `TaskToolSet` cria conversa **filha interna** gerenciada pelo SDK; isso não é sinônimo de chamar `POST /api/conversations` do Canvas. Ainda não testada.

## Rodar depois de obter workspace autorizado

Da raiz do repositório em ambiente isolado:

```bash
python3 -B scripts/check_team_sdk.py
python3 -B scripts/check_team_sdk.py --sdk  # somente se SDK ja instalado
python3 -B -m unittest discover -s tests -p 'test*.py' -v
```

`--sdk` exige `openhands-sdk==1.53.0` e `openhands-tools==1.53.0`; outra versão retorna `versao_incompativel` antes do loader.

O padrão não importa o SDK, requer só stdlib; `--sdk` não registra agentes, não cria arquivos nem delega. O resultado JSON contém apenas estado e nomes dos agentes conhecidos, sem conteúdo de clientes. Código de saída 1 significa contrato ausente/inválido ou diagnóstico SDK não conclusivo. Imports SDK podem possuir efeitos próprios da biblioteca; executar preferencialmente em ambiente isolado.

## Bloqueios antes de ativar

- Provisionar o repositório certo num workspace de teste; o workspace vazio não serve para validação de arquivos.
- Registrar agentes e habilitar a ferramenta de delegação **somente após nova autorização expressa**, com limites reais no servidor (RBAC, isolamento, confirmação de ações e controle de custo). Texto do prompt não é sandbox.
- Não alterar Canvas, OpenHands Core, VPS ou outros projetos nesta fase. Nenhum merge/deploy automático.
- Não alterar `team/catalog.json` para status operacional sem registro e delegação comprovados.

## Prova local desta integração — 2026-10-11

Em clone isolado da branch `feat/observatorio-team-sdk-diagnostic-v1`, base
`1fb8575bc55778130d8e8c6184e8939c54aa6bab`, Python 3.12.14:

- Instalados SDK e Tools **1.53.0** em virtualenv fora do repositório; nenhuma instalação na VPS/Canvas.
- `python -B scripts/check_team_sdk.py --sdk`: saída 0, nomes `observatorio-construtor` e `observatorio-verificador`, preset `code_explorer.md` presente.
- Loader real executado novamente com funções de registro interceptadas para falhar se chamadas: registro SDK vazio antes e depois (0 → 0).
- Processo sem credenciais herdadas, HOME de teste e mapa de custos local do LiteLLM. Nenhuma conversa, Agent, LLM ou TaskToolSet foi instanciado.
- `python3 -B -m unittest discover -s tests -p 'test*.py' -v`: **20 testes aprovados**; CI usa stdlib e mocks, não instala SDK.
- `node scripts/build.mjs`, `node --check extension.js` e `git diff --exit-code -- extension.js`: saída 0; bundle preservado.

A prova valida parsing/carregamento local, não registro, ferramentas habilitadas,
execução ou delegação no OpenHands instalado. Agent Server não foi instalado nem
validado localmente. O catálogo permanece não ativado. A autorização desta tarefa
abrange integração, commits e PR, não merge/deploy ou missão com custo LLM.
