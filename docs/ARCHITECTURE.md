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
