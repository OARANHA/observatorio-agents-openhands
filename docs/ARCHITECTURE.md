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
