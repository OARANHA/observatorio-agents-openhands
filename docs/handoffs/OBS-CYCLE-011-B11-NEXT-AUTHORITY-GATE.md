# ADM-CYCLE011B-11 — Fechamento e próxima decisão arquitetural

Data: 2026-10-12. Origem: main `2abde4207ce6a6798520103d8ae9c98dd5b863a4` antes desta PR.

## Real now e proven evidence
PRs [#56](https://github.com/OARANHA/observatorio-agents-openhands/pull/56), [#57](https://github.com/OARANHA/observatorio-agents-openhands/pull/57), [#58](https://github.com/OARANHA/observatorio-agents-openhands/pull/58) e [#59](https://github.com/OARANHA/observatorio-agents-openhands/pull/59) estão integradas. As entregas foram: validação do GET individual; documentação de APIs de busca; pesquisa de Agent Server upstream; separação de autenticação de sessão, cookie workspace e RBAC. Testes offline rodaram nas CIs correspondentes; esta PR de consolidação ainda terá CI própria. Nenhuma dessas PRs ativou descoberta em produção.

## Lacunas persistentes
- A versão/runtime efetivos do Canvas do proprietário não foram verificados neste ciclo.
- `host.agentServer.request` não teve prova de listagem `/search` suportada na instalação.
- Não há contrato demonstrado de autorização servidor por projeto/conversa, nem prova de isolamento entre projetos.
- Metadado `selected_repository`, UUID e sessão autenticada não equivalem a autorização.
- A revisão Codex e o JEV são evidência adversarial, mas não cumprem por si sós G11 operacional formal.

## Próxima decisão recomendada (não autorizada por este documento)
**CYCLE011-C — dossiê de compatibilidade host/RBAC**, em duas fases:
1. **Offline:** inspecionar código correspondente à versão do host/Canvas e seus testes upstream; documentar o fluxo `request` → roteador → dependency de auth → autorização de recurso. Criar somente fixtures sintéticas de negação, duplicidade, projetos cruzados e paginação. Se não houver prova, encerrar com NO-GO sem escrever cliente de listagem.
2. **Gate humano separado:** solicitar autorização específica apenas se uma verificação controlada em ambiente próprio, com escopo/credenciais/retorno redigidos, tornar-se inevitável. Sem autorização, nenhuma chamada real.

Critério de aceitação para futura descoberta: identidade de operador/tenant comprovada pela autoridade servidor; política efetiva de ACL por recurso; versão de host conhecida; contrato de resposta minimizado; limite de páginas/volume; sem compartilhamento de tokens; revogação testada. Nada disso foi comprovado por esta rodada.

## Segurança e governança
**G11 NÃO PROVADO · G12 BLOQUEADO · P02 NÃO PROVADO · NO-GO operacional.**
Revisão adversarial + JEV usada para decisões offline conforme autorização do proprietário; não altera gate canônico operacional. Nenhum merge/deploy/Canvas/GET real autorizado em ADM-CYCLE011B-11.
