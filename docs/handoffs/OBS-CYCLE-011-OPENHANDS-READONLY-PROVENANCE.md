# CYCLE011 — descoberta e proveniência de dados OpenHands (fase A, somente leitura/offline)

**Data de referência:** 2026-10-11, Brasília.
**Natureza:** handoff e roteiro de investigação **sem implementação de nova API**, sem autorização de GET real, de registro de agentes, de execução de tarefas ou de atualização do Canvas.
**Estado:** preparação documental para próxima sessão GPT-6 (raciocínio médio); decisão arquitetural final ainda não aprovada.

## 1. Autoridade e escopo

Prioridade: `docs/PROJECT_SOURCE.md` → `AGENTS.md` → status dos ADRs em `docs/decisions/` → `docs/CANONICAL_STATE.md` → `MEMORY.md` → `docs/ARCHITECTURE.md` → `README.md` → código/testes/CI/GitHub/OpenHands real.

**Missão horizontal:** ChatGPT coordena → OpenHands executa **somente tarefas explicitamente autorizadas** → Observatório apresenta relações/estados comprovados → GitHub mantém trilha de evidências e documentação. VIGIAFAST, Wandora, ELUS e OpenHands Lab são projetos independentes atendidos, não módulos ou tenants comprovados no Observatório.

Use o fluxo **REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION**. Memória e screenshots são evidência com limites, não autoridade para a ação. Antes de qualquer código, usar `superpowers:brainstorming` e exigir aprovação do desenho apropriado; usar `wmemory-universal` para continuidade e `superpowers:verification-before-completion` para os resultados.

## 2. REAL NOW comprovado no GitHub em 2026-10-11

- `main` de `OARANHA/observatorio-agents-openhands`: `ec9f061469d0376e17c687b4b191a40478e557ee`, merge confirmado da [PR #54](https://github.com/OARANHA/observatorio-agents-openhands/pull/54), manifesto e etiqueta visual V0.5.3.
- CI comprovada no HEAD `86a454d6485cdaf9a8ba0ba1fb9f9a972fbdf668`: [principal #38192037359](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38192037359) SUCCESS (218 testes, 28 skipped); [Chromium #38192037357](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38192037357) SUCCESS (25/25); [SDK inerte #38192037325](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38192037325) SUCCESS, zero LLM/agentes/dispatch reais. Estes resultados **não** são aprovação operacional.
- O proprietário mostrou uma captura da página do Grafo com a etiqueta V0.5.3 e aceitou a correção de espaçamento. **Não há nova captura da tela Apps com Ref exata V0.5.3 nesta etapa**: versão/ref atualmente instalada não foi confirmada por readback independente no host. Não inferir G11 ou homologação completa.
- PRs [#49](https://github.com/OARANHA/observatorio-agents-openhands/pull/49), [#50](https://github.com/OARANHA/observatorio-agents-openhands/pull/50), [#51](https://github.com/OARANHA/observatorio-agents-openhands/pull/51), [#52](https://github.com/OARANHA/observatorio-agents-openhands/pull/52): OPEN/DRAFT, HEADs antigos baseados em `5cedc0ea...`, não mescladas à main atual. Não presumir merge automático, nem integrar SDK/worker nesta trilha visual.

## 3. PROVEN EVIDENCE — contrato já existente e REUSE GATE

A extensão **já dispõe** de `mountRealRead` em `scripts/extension-template.txt`. Ela usa o Canvas autenticado para uma consulta **pontual, opt-in, por UUID informado manualmente**:

```js
const item = await host.agentServer.request({
  method: 'GET',
  path: '/api/conversations/' + id
});
```

O código existente apenas aceita o objeto após conferir:
- `item.id === id` (UUID previamente validado no frontend);
- `typeof item.execution_status === 'string'`;
- `item.updated_at` somente quando string; `observedAt` vem do relógio local da interface.
- `project` é texto livre fornecido pelo operador e marcado **manual/não atestado**. Essa correspondência **não foi provada** pelo servidor.
- `graphIdentityForObservation()` gera IDs de **visualização local/efêmera** com WebCrypto. `scope: 'local-view-not-tenant'` **não é identidade de tenant ou autorização**.
- A exibição tipa vínculos **fonte consultada → conversa consultada** como observação; **conversa → projeto** como declaração manual. Os demais projetos/planetas permanecem **DEMO**.
- Cancelamento/desmontagem, prazo local e falha de resposta tardia já são tratados na UI; prazo local **não prova cancelamento da requisição no host**.

**NÃO reconstruir** a leitura existente, a UI, o host Canvas, o sistema de agentes do OpenHands ou os mecanismos de autorização oficiais.

## 4. GAPS — questões que exigem prova antes de expandir

| Pergunta | Estado nesta rodada | Prova mínima aceitável |
| --- | --- | --- |
| Qual contrato de leitura o OpenHands Agent Server **realmente disponibiliza** para conversa, lista de conversas, estado, tarefas e agentes? | **NÃO PROVADO** além da chamada pontual já presente no código | Fonte oficial com commit/tag/versão + contrato/testes; na instância, somente após autorização H3 |
| É possível enumerar conversas por projeto/tenant com autorização do servidor? | **NÃO PROVADO** | API + política RBAC + teste negativo de escopo (fixture), sem inferir projeto de texto manual |
| Existe inventário oficial de agentes/missões e relação missão→agente? | **NÃO PROVADO** | Modelo e IDs documentados + resposta autorizada; `finished` ≠ sucesso |
| É possível atribuir conversa a repo/projeto real sem input do operador? | **NÃO PROVADO** | Vínculo autenticado no servidor, não hash local/URL/título/prompt |
| Quais eventos são observáveis sem acionar uma execução? | **NÃO PROVADO** | Regras de leitura, egress e proteção de rotas; não experimentar websockets/events por analogia |
| Isolamento multiprojeto, leitura RBAC, retenção, sanitização e auditoria? | **NÃO PROVADO** | Testes negativos + trilha de fonte, data e permissão em ambiente aprovado |
| Atualização do Canvas ou GET real da conversa sintética? | **NÃO AUTORIZADO NESTE CICLO** | Decisão humana separada com instância, UUID, identidade, minimização e rollback |

## 5. CYCLE011-A — próximos passos autorizados apenas offline

1. **Inventário:** conferir `main`, branch/PRs, testes e geração de `extension.js`; inspecionar implementação do `host.agentServer.request` no código da extensão e fontes oficiais da versão do Agent Server/Canvas **sem chamar endpoints reais**. Documentar caminhos, verbos, formatos e evidência exacta de origem; marcar APIs não localizadas como **DESCONHECIDAS**.
2. **Matriz de confiança:** para cada campo candidato, registrar origem, tipo, identidade, permissão do servidor, atualização, classificação (**DEMO / CONSULTADO / MANUAL / INFERIDO / DESCONHECIDO**), retenção/risco e UI permitida. Campos inicialmente visíveis: `id`, `execution_status`, `updated_at` opcional, `observedAt` local, `project` manual.
3. **Threat modeling:** negar no novo escopo leitura de prompts, títulos privados, conteúdo de conversas, cookies/tokens, listagem sem autorização, `fetch` externo, `WebSocket`, escrita, auto-polling, cache persistente e quaisquer comandos de agentes. Definir tratamento fail-closed de 401/403, 404, timeout e shape divergente **somente com fixtures**.
4. **REUSE GATE:** escolher entre (a) reforçar contrato de consulta pontual existente (preferível para slice mínimo) e (b) estudar inventário permitido futuro. Não projetar BFF ou endpoints paralelos enquanto contratos oficiais, RBAC e necessidade não estiverem comprovados.
5. **Especificação e TDD (dependentes da aprovação de desenho):** obter a aprovação da abordagem no novo chat antes de escrever código de comportamento. Depois implementar **apenas fixtures/testes offline e funções pequenas de validação**, respeitando a hierarquia de skill Superpowers, test-first RED → GREEN e regressão do código existente. Não mudar manifest/versão sem mudança realmente necessária.
6. **Entrega:** branch isolada + PR **Draft**, documentação viva incremental e atualização de `OARANHA/wmemory` privado; CI de um HEAD congelado verificada quando o operador disser GREEN/RED, **sem polling**. Não fazer merge por inferência do aceite visual anterior.

## 6. Condições de aceite da fase A

- Existe matriz com **fatos, hipóteses e desconhecidos separados**, ancorada em fonte verificável.
- O contrato **já existente** é reutilizado, não reimplementado.
- Contratos não observados não são inventados; nenhuma listagem de projetos/agentes é declarada operacional.
- Nenhum request real, novo token, LLM, agente, automação, custo de provedor, deploy ou alteração do Canvas.
- Permanecem **G05/G06/G07/G10 PARCIAIS; G08/G09/G11 NÃO PROVADOS; G12 BLOQUEADO; P01 PARCIAL; P02/P03 NÃO PROVADOS; NO-GO operacional.** G11 revisões independentes e G12 canário real têm gate separado.
- Qualquer consulta H3 com UUID sintético já existente **precisa de autorização específica posterior**, mesmo que seja somente GET. Não chamar sem essa autorização.

## 7. Handoff à próxima sessão

Abrir GPT-6 em **raciocínio médio** com GitHub, `wmemory-universal` e `superpowers` conectados. Usar este handoff como ponto de localização, **não** como substituto da leitura de fontes canônicas e do código real. Iniciar pela prova de contrato offline e desenho aprovado; relatar bloqueios. Não fazer polling contínuo de CI. Não tocar em outros projetos ou infraestrutura.
