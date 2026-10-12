# CYCLE008-D — Proposta congelada para **uma** primeira missão OpenHands

**Data:** 2026-10-11 (Brasília) | **Estado:** PLANEJADA / **NÃO AUTORIZADA** / **NÃO EXECUTADA**
**Referência:** Issue #48 e `docs/handoffs/OBS-CYCLE-008-OPERATIONAL-PREFLIGHT.md`.
Este documento não concede autorização operacional e não cria fila ou executor novo.

## Objetivo único e evidência

**Objetivo:** um `code-explorer` ler **somente o arquivo público `AGENTS.md`** do Observatório num snapshot read-only e produzir um resumo verificável de três fatos: (1) as funções de ChatGPT, OpenHands e Observatório; (2) a separação entre projetos atendidos; (3) o requisito de autorização específica para operações reais.

**Repositório alvo:** `OARANHA/observatorio-agents-openhands` (público).
**Branch e commit de leitura:** `main` **pinada** em `5cedc0eada928fcd1f46cc50e2144d02822181be`; se a `main` mudar, manter o SHA ou recongelar mediante decisão explícita, nunca seguir HEAD silenciosamente.
**Blob público de entrada:** `AGENTS.md`, SHA Git `943a15490986d344012393007b3fb94450a64819` na base acima.
**Proveniência da demanda:** Issue #48, revisão posterior independente e uma futura autorização humana única assinada/registrada. `mission_id`, `evidence_id` e ID de execução **NÃO ATRIBUÍDOS**; não criar IDs operacionais fictícios.

## Proposta de escopo restrito

| Campo | Valor preparado / lacuna |
|---|---|
| Executor | OpenHands SDK/Tools 1.53.0 / `code-explorer` **candidato**, não selecionado operacionalmente |
| Ferramenta pretendida | Terminal oficial via `TaskToolSet` e `TerminalTool`/executor restrito existente |
| Único comando permitido na missão | `cat AGENTS.md` **proposto**; `ALLOWED` global atualmente também permite `pwd` e outros `cat`: enforcement do subset por missão **NÃO PROVADO** |
| Leitura/escrita | Snapshot de arquivo público, RO; nenhuma escrita, rede, `.git`, variável de ambiente, segredo, shell arbitrário, browser, MCP remoto ou acesso transversal |
| Número de delegações | Uma, sem `resume` e sem subagentes adicionais, **sujeito a prova efetiva** |
| Tentativas | Zero retries, zero fallback, nenhuma repetição após falha/incerteza |
| Ações terminais propostas | No máximo **uma** (`cat AGENTS.md`); limite efetivo do SDK/worker por missão ainda não certificado |
| Tempo total pretendido | **60 segundos**; prazo realmente imposto a todos processos/streams e cleanup ainda não homologado |
| Modelo/provider/snapshot/rota | **NÃO SELECIONADOS NEM COMPROVADOS** — bloqueio G08 |
| Tarifa/categorias de consumo | **NÃO COMPROVADAS** — preços públicos não equivalem a tarifa da conta |
| Teto monetário e quota | **NÃO DEFINIDOS**; não inventar USD. Sem G08/G09, não submeter orçamento ou gastar |
| Identidade/credencial segregada | **INEXISTENTE PARA ESTA MISSÃO**; sem chaves no repositório ou logs |
| Autorização operacional | **NÃO CONCEDIDA**; não há aprovação posterior nem G11 válido |
| Saída | Resumo pequeno de três itens com referência ao blob público; sem cópia de prompts privados, segredos ou resultado do SDK bruto |
| Retenção e prova | Schema, custodiante, prazo, autorização/identidade, hash com origem verificada e política de acesso **AINDA PENDENTES** |

**Regra de interpretação:** `finished` da conversa não certifica que o arquivo foi lido, o resumo é correto, a ferramenta respeitou as permissões ou que o agente pertence ao projeto. A comprovação exigiria cadeia auditável entre fonte pinada, autorização, processo supervisionado, comandos e conteúdo produzido, conferida por um revisor humano distinto.

## Critérios de aceite de execução futura

1. Comprovar o snapshot contendo exatamente o arquivo público esperado e digest/blob conferidos; ambiente de execução isolado comprovado (G05).
2. Garantir via política **efetiva** que `cat AGENTS.md` é o único comando permitido, mesmo quando o catálogo global inclui outros (G07). Teste adversarial de um comando globalmente permitido mas **fora do subset desta missão** deve resultar DENY terminal.
3. Garantir uma só delegação autorizada, sem processamento assíncrono/streaming/egress fora dos sinks controlados, sem retry/resume (G06/G07).
4. Congelar modelo, provider/rota/versão, todas as tarifas e limites de tokens/chamadas; validar orçamento preventivo exato e bloqueio financeiro independente, sem acesso a outros modelos (G08).
5. Usar identidade de teste segregada, quota real, revogação comprovada e autorização financeira explícita (G09).
6. Registrar autorização por missão, inputs mínimos, comando efetivo, output minimizado, tempos, estado de cleanup, custos/hold incerto e hash/proveniência autenticados; revisar retenção (G10).
7. Parecer independente e aceite de riscos pelo proprietário no HEAD exato e superfície autorizada (G11).
8. Proprietário aprova **especificamente** a missão congelada depois de todos os gates; somente essa nova autorização pode liberar G12. Uma PR aprovada ou CI verde não satisfazem G12.

## Cancelamento, revogação e rollback — futuros, não testados aqui

Ao primeiro desvio (negação, ferramenta extra, timeout, egress, corrida, custo não verificado ou falha da prova), cancelar Guard, impedir retry e `resume`, parar grupo supervisionado, confirmar `kill/reap` com evidência e registrar estado incerto se cleanup falhar. Acionar o custodiante para revogar a credencial segregada e confirmar ausência de descendentes. Preservar apenas evidências mínimas permitidas e descartar temporários conforme política homologada. Nunca declarar sucesso por callback ou exit code sem conteúdo e autorização verificados.

**Decisão: BLOQUEADO / NO-GO.** A missão está definida **somente como proposta**. Iniciar um agente real, selecionar provedor/custo, registrar identidade ou chamar SDK de execução exigiria autorização adicional e nova comprovação dos gates. Não houve operações reais nesta etapa.
