# Handoff verificável — OBS-TEAM-CANARY-001

Data: 2026-10-11. Projeto: **Observatório horizontal multiprojeto**.

Relato histórico do ZIP fornecido (MCP original não relido nesta integração): estado operacional informado após o relatório: `finished`, conversa `a075c791-b4cc-4f89-9bbb-d5d9b3042411`. **Este estado atesta o encerramento, não sucesso de subagentes.**

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

- REAL NOW: o repositório `OARANHA/observatorio-agents-openhands` mantém definições candidatas do Construtor e Verificador. O Canvas com app v0.4.2 instalado em ref anterior não recebeu deploy desta missão.
- PROVEN EVIDENCE: OpenHands SDK / Tools / Agent Server 1.53.0; interfaces `TaskToolSet` e `register_builtins_agents` importáveis; preset `code-explorer` localizado; workspace sintético vazio (apenas `.git`), sem definições do projeto.
- GAPS: registro efetivo, ferramenta de delegação da sessão, execução do subagente, compatibilidade no runtime instalado, isolamento real e orçamento não demonstrados. Nenhuma chamada real a TaskToolSet ou registro.
- REUSE GATE: reusar `openhands.sdk.subagent.load_project_agents` para descobertas sem mutação; `register_file_agents` **existe** em `openhands.sdk.subagent` no código oficial v1.53.0. Não duplicar subagente Explorer.
- DECISION: testar contratos em CI sem SDK; permitir diagnóstico SDK somente em workspace isolado, mediante decisão separada para agentes ativos e delegação. Nenhuma mudança no runtime nesta entrega.

Referência upstream: https://github.com/OpenHands/software-agent-sdk/blob/v1.53.0/openhands-sdk/openhands/sdk/subagent/registry.py

O loader foi validado localmente nesta integração; a instalação remota e a delegação continuam não comprovadas. Qualquer registro/delegação limitada requer autorização específica. `finished` não justifica status operacional no catálogo ou planetas reais no Observatório.

## Integração GitHub — 2026-10-11

- REAL NOW: `main` e branch de integração reconciliadas na base `1fb8575bc55778130d8e8c6184e8939c54aa6bab`; PR #8 de contratos integrada. PR #7 do grafo permanece aberta e independente.
- PROVEN EVIDENCE: SDK/Tools 1.53.0 instalados em virtualenv local isolado; loader carregou as duas definições e localizou preset nativo. Registry vazio antes/depois, sem chamadas de registro/delegação.
- GAPS: registro, disponibilidade das ferramentas e delegação no runtime remoto ainda não demonstrados; CI não valida SDK real.
- REUSE GATE: aproveitados quatro arquivos do ZIP; README de aplicação manual omitido. Mantidos catálogo, agentes Markdown, extensão e workflow existente.
- DECISION: diagnóstico exige versão exata 1.53.0, usa erros sem mensagens potencialmente privadas e exibe somente nomes esperados. Evidências históricas do canário identificadas como relato do pacote.

Validação completa: **20 testes unittest**, diagnóstico estático, diagnóstico SDK real,
build reprodutível e sintaxe JS aprovados. Detalhes em `team/SDK_DIAGNOSTIC.md`.
Dois testes novos de versão incompatível/SDK ausente falharam antes da correção e
passaram depois. Revisão técnica pelo próprio integrador, sem iniciar subagentes,
conforme restrição da missão. CI remoto será consultado uma vez após abertura da
PR; o resultado do HEAD exato fica no relatório de entrega, não antecipado aqui.

## Plano e limites executados

1. Reconciliar refs, PRs e autoridades antes de aplicar arquivos.
2. Revisar ZIP, integrar diagnóstico e testes; corrigir compatibilidade comprovada.
3. Validar loader 1.53.0 sem registro; executar suite/build e registrar evidências.
4. Publicar commits organizados, abrir PR para main e consultar CI uma vez.

Sem merge, deploy, mudanças no Core/Canvas/VPS ou outros projetos, dados de
clientes, credenciais, registro de agentes ou tarefas com custo de LLM.
