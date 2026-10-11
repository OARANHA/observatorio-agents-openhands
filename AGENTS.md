# AGENTS — regras operacionais do Observatório

## IDENTIDADE INEGOCIÁVEL
**Esta base é a ferramenta horizontal OBSERVATÓRIO, não o projeto VIGIAFAST.**
OpenHands = executor de missões de desenvolvimento autorizadas, com memória opcional e limites reais.
ChatGPT = coordenação, análise, revisão e delegação **conforme acessos e autorizações existentes**.
Observatório = **visão operacional multiprojeto** (universo/grafo), não orquestrador, não produto final de um cliente.
GitHub = documentação viva, código, testes, PRs e histórico dos projetos atendidos.
**VIGIAFAST, Wandora, ELUS e outros são projetos independentes atendidos**. Nunca converter requisito horizontal em funcionalidade de VIGIAFAST apenas porque o chat usa o projeto CRISEDIGITAL.

Leia PRIMEIRO `docs/PROJECT_SOURCE.md` → este arquivo → `docs/decisions/` → `docs/CANONICAL_STATE.md` e `MEMORY.md` → `docs/ARCHITECTURE.md` → `README.md` → código/testes → estado real.
Leia `docs/PROJECT_SOURCE.md` e `docs/CANONICAL_STATE.md` antes de sugerir nova função, agente, integração ou módulo.

## REALIDADE E GOVERNANÇA
- Separar **demo**, **consultado e autenticado**, **declarado manualmente**, **inferido** e **planejado**.
- Um UUID retornando `finished` não certifica sucesso da tarefa, um agente individual ou a associação a projeto.
- O switch de memória persistente do OpenHands não certifica que uma memória foi gravada, recuperada, segregada por projeto ou exibível num grafo. Fazer teste sintético antes de afirmações.
- Produto: aplicativo de visualização no OpenHands Canvas. Reutilizar Canvas, OpenHands e GitHub; não alterar OpenHands Core, VIGIAFAST, Wandora, ELUS, brokers ou VPS por implicação.
- Código do App roda em contexto autenticado. Nenhuma credencial, cookie, token, prompt ou dado privado enviado a GitHub/frontend; respeitar permissões e origem dos dados.
- Testar Shadow DOM, lifecycle, API, evidências e licenças. Branch + PR; **sem** merge, instalação, operação remota, deploy ou polling contínuo sem autorização adequada.
