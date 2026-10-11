# SDK 1.53.0 — inventário offline e limites

2026-10-11 UTC. Leitura dos arquivos da distribuição oficial instalada no
venv isolado do Work; hashes via stdlib, sem importar SDK, ler ambiente ou
executar LLM. `audit_canary_sdk_transport.py` valida aliases/métodos via AST;
doze testes passam no SDK oficial e no workflow do runner.

| Fonte SDK instalada | SHA-256 observado localmente |
|---|---|
| `openhands/sdk/llm/llm.py` | `a3261d1d021eebeb81114acdf3e36c38ea08e0bbb1d037def25c0ad8995f92d3` |
| `openhands/sdk/llm/utils/retry_mixin.py` | `609b84dd4185a49d51101d0876341f5bb1b5aefc160c6b7192e16d4f11170ed3` |
| `openhands/sdk/llm/utils/model_info.py` | `5a3d11614dfc129122b157355c308d62038796f3e9d45bfd765f855baac2f0ab` |
| `openhands/sdk/llm/utils/runtime_metadata.py` | `ffe99aa7d144f8e247ed638eb506b60d1c4e531e455906209949860847f8747a` |
| `openhands/sdk/llm/streaming.py` | `5d96f396448a238842f0de3bd6f165c3830464dd20a4e8ff3fdfbc3824caabbe` |

Metadados observados no mesmo venv: SDK/Tools 1.53.0, LiteLLM 1.103.4,
httpx 0.28.1, tenacity 9.1.4, pydantic 2.14.0. São observações locais,
não um lock transitivo imposto a todos os runners. Workflows fixam apenas
SDK/Tools; nova resolução transitiva exige conferir versões/superfície.

| Caminho | Risco | Controle/prova existente e limite |
|---|---|---|
| completion/acompletion/responses/aresponses | Tentativas adicionais, sync/async e mutação | Quatro sinks, uma reserva/chamada lógica, segunda tentativa/owner distinto recusados; stubs não provam toda requisição interna |
| RetryMixin/Tenacity | Retry oculto ou configuração alterada | Zero retries nominal e negativas no sink; dependências fora do sink exigem barreira de rede independente |
| fallback e refresh de chave | Rota alternativa e nova tentativa após erro | Flags negadas no preflight, testes reais contra stubs; nenhuma chave real |
| streaming/cache/extra_body | Métrica parcial, novas taxas ou superfície | Negados pela configuração sintética; não há suporte operacional homologado |
| model_info/runtime_metadata/OpenRouter resolver | HTTP auxiliar e tarefas por loop, cache positivo/negativo | Inventariados por leitura; não são os quatro sinks LiteLLM. Precisam de política própria antes de worker real |
| threading/asyncio/imports/plugins | Execução fora do owner e drift dinâmico | Owner de thread/task e AST nominal; AST não é análise geral de egress nem isolamento de código hostil |

Reutilizar APIs oficiais, Guard, Book e supervisor. Nenhuma modificação no
OpenHands Core/distribuição oficial. A prova SDK com `/` RO e netns isolado
certifica rede no runner, não filesystem mínimo do processo futuro; o terminal
mínimo é exercitado por probes separados. Não expandir permissões para validar
metadados remotos. G02 PROVADO OFFLINE, G06 PARCIAL, NO-GO operacional.
