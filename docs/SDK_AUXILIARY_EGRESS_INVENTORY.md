# Inventário auxiliar de egress — 2026-10-11

Leitura AST local de 307 arquivos Python oficiais SDK/Tools; nenhum import desses arquivos, request ou agente. Lista nominal de chamadas explícitas: não é análise completa de aliases, dispatch dinâmico, imports indiretos ou dependências. Fontes disponíveis, launchers locais do venv ausentes; execução SDK somente comprovada por CI.

| Módulo oficial | Chamadas explícitas e linhas locais |
|---|---|
| `sdk/agent/acp_agent.py` | `asyncio.create_subprocess_exec:2550, asyncio.create_subprocess_exec:3047, threading.Thread:4669` |
| `sdk/agent/acp_file_credentials.py` | `threading.Thread:149` |
| `sdk/conversation/impl/remote_conversation.py` | `threading.Thread:181, importlib.import_module:99, asyncio.run:225` |
| `sdk/credential.py` | `httpx.AsyncClient:88, httpx.AsyncClient:117` |
| `sdk/git/utils.py` | `subprocess.run:29` |
| `sdk/hooks/executor.py` | `subprocess.run:102, subprocess.run:552, subprocess.Popen:513` |
| `sdk/llm/auth/openai.py` | `asyncio.run:960` |
| `sdk/llm/llm.py` | `importlib.import_module:3340` |
| `sdk/llm/utils/image_inline.py` | `httpx.Client:175` |
| `sdk/llm/utils/model_info.py` | `httpx.get:103` |
| `sdk/llm/utils/providers/openrouter.py` | `httpx.Client:175, httpx.AsyncClient:192` |
| `sdk/llm/utils/runtime_metadata.py` | `asyncio.create_task:203, asyncio.run:240` |
| `sdk/llm/utils/unverified_models.py` | `importlib.import_module:13` |
| `sdk/mcp/utils.py` | `asyncio.create_task:350` |
| `sdk/secret/secrets.py` | `httpx.get:128` |
| `sdk/security/grayswan/analyzer.py` | `httpx.Client:130` |
| `sdk/security/toolshield_helpers.py` | `asyncio.run:363` |
| `sdk/skills/execute.py` | `subprocess.run:66` |
| `sdk/skills/utils.py` | `subprocess.run:398` |
| `sdk/utils/async_executor.py` | `threading.Thread:198` |
| `sdk/utils/command.py` | `subprocess.Popen:101, threading.Thread:131, threading.Thread:134` |
| `sdk/workspace/base.py` | `httpx.Client:152` |
| `sdk/workspace/remote/async_remote_workspace.py` | `httpx.AsyncClient:62` |
| `sdk/workspace/remote/base.py` | `httpx.Client:100` |
| `sdk/workspace/repo.py` | `subprocess.run:364, subprocess.run:397` |

## Classificação e aceite

LLM síncrono/assíncrono, retry/fallback/refresh/cache/streaming continuam inventariados em SDK_TRANSPORT_INVENTORY.md e na auditoria AST existente. Quatro aliases LiteLLM não controlam os destinos acima. Credenciais URL, remote workspace/conversation, hooks, plugins e ACP ficam fora do canário proposto; não foram instanciados ou executados. Import dinâmico de transformers em llm.py e marketplace/conversation remota impede alegação de fechamento universal por AST.

Provas negativas adicionais no runner: SDK model_info faz GET auxiliar sem chave para localhost:9 e retorna None quando negado; essa tolerância é gap, não falha segura do SDK inteiro. Httpx sync/async/stream e urllib em thread/subprocess falham em namespace independente, antes de qualquer tráfego a provedor. Apenas endpoint local fictício, nenhum host público. Provas não cobrem todos destinos/redirects/plugins/dependências.

SyntheticTransportGate rejeita Iterator, AsyncIterator e awaitable como resposta imediata sem consumir chunks. Três REDs reproduzidos; hold incerto/Guard fechado. Não cancela arbitrariamente tasks criadas por código hostil; não é sandbox e permanece exclusivo de fakes. G05/G06 PARCIAIS, NO-GO operacional.
