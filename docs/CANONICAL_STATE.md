# Estado canônico — Observatório de Agentes (2026-10-10)

## REAL NOW
- Repositório `OARANHA/observatorio-agents-openhands`, produto App do OpenHands Agent Canvas.
- `main` verificada em `15b742ad25e8a0795b530f67df8df92ca004f936` com manifesto V0.3.2 e extensão `extension.js` gerada de `source/observatorio-v02.html`.
- PR #2 da V0.3.2 mesclada na `main`; CI do HEAD da PR foi reportada `success`, e o usuário apresentou a versão corrigida em screenshot do Canvas.
- V0.4.0 é trabalho proposto em branch separada; validar CI e revisão antes do merge e da instalação.

## PROVEN EVIDENCE
- A UI do Observatório abre dentro do Canvas, com universo 2x2, sistemas solares WebGL2 e fallback 2D, painel de inspeção e navegação nativa intacta.
- V0.3.2 resolveu a sobreposição anterior da nota explicativa com métricas.
- Fonte/gerador e testes de contrato conferidos; o produto ainda opera somente com dados demonstrativos locais.
- V0.4.0 define cenários **SIMULAR** (calmo, atividade, atenção, falha) e animações responsivas que jamais devem ser relatadas como trabalho real de agentes. Modo calmo é o padrão.
- Renderização progressiva reaproveita órbitas e shaders WebGL2 atuais, sem dependências remotas ou credenciais.

## GAPS, REUSE GATE E DECISÃO
- CI da V0.4.0 e validação visual no Canvas real, inclusive navegadores e dispositivos móveis, ainda necessárias; não inventar resultados.
- Nenhuma nova API, persistência, coleta, contagem real de tarefas ou conexão MCP neste slice.
- Futuro uso de estados reais requer backend de leitura autenticado com autorização por projeto/tenant e origem/horário de observação verificáveis.
- Não modificar Canvas Core, VPS, volumes, credenciais ou serviços, não fazer deploy/merge automáticos e não consultar CI repetidamente.
