# ADM-CYCLE011D-09 — Consolidação e decisão arquitetural de autorização por recurso

Data: 2026-10-12. Referência main: `9b59de97e6b9218941e7b46539d9bfccc37bd1fc`. Trabalho **somente documental/offline**.

## REAL NOW → PROVEN EVIDENCE

- PR [#65](https://github.com/OARANHA/observatorio-agents-openhands/pull/65), merge `18745a8ee780551d114b8a5008c321c815e69c97`: auditoria de autenticação de sessão, handlers de busca/GET/DELETE por UUID, catálogo e revogação; testes de **modelo booleano**, não implementação real.
- PR [#66](https://github.com/OARANHA/observatorio-agents-openhands/pull/66), merge `9b59de97e6b9218941e7b46539d9bfccc37bd1fc`: leitura de `ConversationService` e `_search_conversations`, metadados `meta.json`, catálogo por UUID/estado/paginação; testes **fixture JS aproximada**, não execução Python.
- Código upstream examinado: https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/conversation_service.py ; https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/dependencies.py ; https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/conversation_router.py .
- Declarações de versão em código público não comprovam a versão **instalada** no Canvas/Agent Server do proprietário. Sessão/chave e `selected_repository` não certificam autoridade por projeto.
- Revisões consultivas JEV.1 anteriores: D01 `block` e `incomplete`; D05 `deep_review` e `incomplete`. Não substituem gate independente G11.

## GAPS explícitos

1. Identidade autenticada estável (subject) ligada ao operador, tenant e papéis em cada pedido.
2. Prova de versão instalada exata, middleware/proxy efetivo e política de escopo por conversa/projeto no servidor.
3. Negação de consulta, busca, paginação, lote e exclusão com UUID válido mas não autorizado.
4. Revogação efetiva: associação removida invalida leitura/listagem e cache sem confiar só em flags fornecidas pelo cliente.
5. Evidência de que o backend usado pelo Canvas impõe o mesmo perímetro para todos os endpoints e métodos, inclusive headers arbitrários e GET com corpo.
6. Revisão independente G11 e autorização separada para qualquer teste real.

## REUSE GATE — decisão condicional, não implementação

**Caminho A — Reutilizar controles existentes (preferencial):** somente se forem identificados controles de autorização por **recurso** no backend efetivamente instalado, com versão/commit, identidade confiável, falha fechada e negação multiprojeto demonstradas. Evidência exigida: caminhos de código e execução de testes reproduzíveis com sujeitos distintos e revogação.

**Caminho B — Camada complementar dedicada (plano alternativo):** se a proteção por recurso não existir ou não puder ser provada, elaborar **nova ADR** para backend/BFF com identidade de servidor, mapeamento explícito de ACL conversa/projeto, allowlist estrita de operações, egress controlado, revogação, auditoria e sem transportar chaves/segredos ao frontend. Requer revisão de ameaça e aprovação humana antes de codificação/implantação. **Não implementar agora.**

**Caminho C — Permanecer sem descoberta automática:** se faltarem versão/identidade/ACL verificáveis, manter somente evidências offline e visualização de dados explicitamente autorizados no contrato atual. Nenhum fallback que enumere conversas a partir de sessão genérica.

## Matriz de aceitação para próxima autorização técnica

| Controle | Prova exigida | Falha fechada |
|---|---|---|
| Inventário de versão | release/commit do Canvas e Agent Server instalados, sem segredos | sem fingerprint, negar |
| Identidade | sujeito/tenant derivado de autenticação servidor, não do corpo JS | sem sujeito, negar |
| ACL por conversa | decisão por recurso e sujeito no servidor; caso de UUID cruzado | 403/404 sem metadados |
| Listagem/paginação | filtro autorizado antes de contar/paginar; sem cursor transversal | sem ACL, sem lista |
| Revogação | teste antes/depois de revogar associação e invalidar cache | leitura posterior negada |
| Métodos/headers | allowlist por propósito, GET sem body e sem headers arbitrários | método inválido negado |
| Independência | revisão G11 documentada separadamente da opinião JEV.1 | sem revisão, NO-GO |

## Decisão

**G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO · NO-GO operacional.** Esta consolidação não cria política de autorização, não atesta segurança operacional e não concede permissão para GET/DELETE real, descoberta, merge, deploy ou mudanças no Canvas. O próximo trabalho permitido, mediante ADM próprio, deve ser plano/ADR comparativo e verificação offline da versão de código público fixada, sem depender de mais fixtures booleanas.
