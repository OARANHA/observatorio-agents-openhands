# CYCLE011-A — Incremento A: validação de consulta pontual

Data: 2026-10-11. Estado: implementação proposta em PR Draft; **sem prova de integração operacional**.

## Decisão
Reutilizar `host.agentServer.request({method:'GET',path:'/api/conversations/'+id})`, sem criar endpoint, BFF, registro, polling ou coleta automática.

## Contrato local
- UUID continua sujeito à validação existente antes da chamada; a resposta só pode promover observação quando `item.id === id`.
- `execution_status` deve ser string não vazia, com no máximo 128 caracteres e sem caracteres ASCII de controle. **Não existe enum comprovado nesta etapa**: strings válidas no formato não garantem semântica operacional nem sucesso.
- `updated_at` somente aparece quando for string ISO 8601 com data/hora, fuso explícito e data parseável. Ausente ou inválido não impede mostrar estado; não é substituído pelo horário de observação.
- O objeto reduzido `{status, updatedAt}` impede carregar campos arbitrários para a observação.
- A consulta continua opt-in, única por UUID, sem armazenamento persistente. O timeout local não interrompe necessariamente a requisição no host.
- `project` continua **MANUAL**, `local-view-not-tenant` continua só identidade visual; `finished` não comprova tarefa bem-sucedida. DEMO e CONSULTADO permanecem distintos.

## Testes sintéticos
Arquivo `tests/point_read_validation.test.mjs`: metadados mínimos, ID divergente, status inválido, controles, timestamp ausente/malformado. Rodar `node --test tests/point_read_validation.test.mjs`, `node scripts/build.mjs`, `node --check extension.js`, `python3 -m unittest discover -s tests -p test_contract.py` e a suíte Chromium, se disponível.

## Fora do escopo
RBAC, listagem de conversas, inventário de agentes, relação projeto/repositório, API autenticada, eventos, retorno de tarefa, LLM, deploy e Canvas. Permissões de leitura e erros HTTP 401/403/404 dependem da interface host; a UI conserva a mensagem genérica, falhando de modo fechado.

**G11 NÃO PROVADO; G12 BLOQUEADO; P02/P03 NÃO PROVADOS; NO-GO operacional.** A CI da PR requer conferência no HEAD exato quando o proprietário informar GREEN/RED.

## Correção de cobertura CI — 2026-10-12
A execução inicial dos três workflows da PR #56 ficou GREEN no commit `f69b6e49277d1893c5d6521dad7e5cbb03d891c6`, porém a inspeção de `.github/workflows/ci.yml` provou que o novo teste JavaScript não estava na lista de comandos executados. A CI passou a executar `node --test tests/point_read_validation.test.mjs` em uma etapa específica. **O novo HEAD ainda requer resultado da CI; o GREEN anterior não valida essa alteração.** Sem polling contínuo, merge ou deploy.

## Revisão adversarial da PR #56 — 2026-10-12
Revisão própria, **não independente para G11**. Foi reproduzido offline que `Date.parse('2026-02-30T00:00:00Z')` normaliza uma data de calendário inexistente. Adicionada regressão JavaScript e validação explícita de dia do mês, ano bissexto, relógio e deslocamento UTC. Prova pontual no JS do validador: seis entradas inválidas rejeitadas e 2024-02-29 aceito; fonte e artefato gerado iguais na função alterada. **A suíte CI do novo HEAD não foi conferida.** Revisão de outras superfícies e G11 independente permanecem pendentes. Sem merge/deploy.
