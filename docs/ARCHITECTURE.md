# Arquitetura

```
OpenHands Agent Canvas -> Apps -> Observatório (registerPage)
  -> Shadow DOM -> WebGL2 com fallback 2D
  -> catálogo demonstrativo local (nenhum endpoint remoto)
```

- UI não importa bibliotecas externas, não consulta tokens ou APIs; nenhuma ação operacional.
- O teardown remove a raiz e cancela animação, observação de tamanho e contexto GPU quando disponível.
- Planeta é representação de um **papel de agente fictício**; não deduzir agente real de conversa/LLM.
- Futuro: BFF autenticado somente de leitura -> escopo servidor por projeto/tenant -> provedores OpenHands/Agent Mesh -> agregado minimizado e auditado com `observed_at`.
- Sem inferir CPU, tokens, ETA, progresso, colaboração ou estado do agente sem evento comprovado.
- Revisar políticas CSP, conexões e fonte Git fixada antes da primeira instalação real.


## V0.4.2 proposta — primeira leitura operacional

O Observatório conserva a experiência demonstrativa V0.4.1, mas inclui o painel **☾ CONSULTA DE MISSÃO REAL**. Após inserção manual do UUID, consulta pontualmente `GET /api/conversations/{id}` por `host.agentServer.request`, usando a autenticação do Canvas. Mostra somente ID, estado, horário de atualização do servidor, origem e horário da observação pelo navegador. Não lista conversas, mostra resultados/segredos, executa comandos nem faz polling.

O projeto é preenchido pelo operador: associação explícita, **não validada pelo Agent Server**. A lua representa apenas a execução consultada; nenhum agente real é inferido. O acesso do Canvas não substitui RBAC por projeto/tenant. Uso interno sintético apenas, sem dados reais de clientes. **Não verificado no Canvas instalado**: aguarda CI, revisão e autorização para instalação. Testes previstos: `node scripts/build.mjs`, `node --check extension.js` e `python3 -m unittest discover -s tests -p test_contract.py`.


## Ajuste da PR #5 — lua real dentro do Multiverso (2026-10-10)

Depois de consultar manualmente um UUID via Canvas Host, a UI cria **em memória** o quinto cartão `OBSERVATÓRIO` (projeto explicitamente informado pelo operador) e abre seu sistema solar: **uma lua de execução OpenHands verificada**, zero planetas de agentes comprovados e painel lateral com UUID, status, origem, atualização do servidor e hora da consulta. Os quatro sistemas originais permanecem DEMO; o cartão real exibe `OPENHANDS REAL`.

- Evidência operacional: missão sintética OBS-REAL-001 terminou em `finished`; resposta do MCP `openhands_result` continha `OBS-REAL-001|OK`. A execução real não é embutida no Git ou frontend; somente o UUID inserido pelo usuário é consultado pelo Canvas autenticado.
- `host.agentServer.request(GET /api/conversations/{uuid})` é lido sob a sessão Canvas. Não expor resposta final, prompts nem títulos. A associação `project` é **declarada**, nunca inferida ou certificada.
- Zero sincronização automática, zero histórico persistido, nenhuma credencial no JS, nenhum agente novo, nenhuma ação start/stop. Sem dados reais de clientes nem RBAC multi-tenant homologado.
- Após reload do Canvas, **é necessário consultar o UUID novamente**. Para vinculação automática e durável, precisaríamos de inventário seguro do lado do servidor: fora deste primeiro slice.
- Mudança não instalada nem mesclada. Requer CI, revisão, validação no Canvas e autorização específica. Em caso de API incompatível, não mostrar uma lua como atividade comprovada.
