# Transitivos e reconstrução de sessão — ciclo003

Base ef09e283ef27ad2b6aa02973cee71a27925b22c7; ferramentas inertes, NO-GO.
Leitura estática oficial local LiteLLM1.103.4 METADATA exige aiohttp>=3.14.2,
httpx>=0.28.0; requests é extra CLI, não foi adicionado para testes artificiais.
httpcore compõe HTTPx. Fonte litellm/llms/custom_httpx/aiohttp_transport.py
LiteLLMAiohttpTransport.handle_async_request reconstrói sessão e chama de novo
_make_aiohttp_request após RuntimeError('Session is closed'), fora do RetryMixin
SDK. _get_proxy_settings também pode ler proxy do ambiente; o futuro worker
precisa manter clearenv/barreira independente. Nenhuma credencial lida.

Novo teste no netns existente: httpcore.ConnectionPool(retries=0) e transporte
LiteLLMAiohttpTransport real com aiohttp.ClientSession tentam localhost:9,
sem chave, timeout0.3, trust_env=False, sem mocks de resposta; falha exigida.
Outro teste chama esse transporte oficial contra sink falso guardado: induz
Session is closed, observa reconstrução oficial de sessão e nega reentrada
antes do segundo sink. Uma chegada, hold incerto/Guard fechado e sessões
fechadas; não invoca SDK LLM, agente ou provedor. É gate de fakes/teste,
não proteção financeira operacional do SDK ou toda dependência.

Inventário stdlib de nove distribuições efetivamente presentes usa mecanismo
importlib.metadata sem importar SDK ou transportes. Emite somente nomes
fixos, versões numéricas e SHA256 de METADATA público; não inclui URL,
Requires-Dist, ambiente, caminho local, extras, credencial ou texto livre.
SDK/Tools diferentes de1.53.0, ausência/malformação de metadata e versões
potencialmente privadas/prerelease são falha minimizada. Hash não autentica
origem; inventário não é lock transitivo nem SBOM completo/certificação.

Três testes de contrato RED→GREEN, sem dependências externas. Suite local
192 testes:164 PASS/28 SDK opcionais skip. Duas provas transitivas SDK ainda
precisam do runner isolado; não importar dependências do SDK no host. Workflow
SDK mantém todos controles e adiciona inventário/teste pertinente; não alarga
rede, retries ou permissões. G02 offline, G06 PARCIAL, G12 BLOQUEADO.
