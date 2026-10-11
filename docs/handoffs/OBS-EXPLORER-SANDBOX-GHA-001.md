# OBS-EXPLORER-SANDBOX-GHA-001 — prova efêmera no GitHub Actions

Data: 2026-10-11. Base inicial da branch: 6811dc88057ae7507423d6160a14881f2cc69b3e (merge da PR #11).

## Autoridade e escopo

Observatório é ferramenta horizontal. Respeitar docs/PROJECT_SOURCE.md, AGENTS.md, ADRs e os handoffs OBS-EXPLORER-CANARY-PLAN-001 e OBS-EXPLORER-CANARY-GATES-001.

Autorização recebida: preparar uma PR para testes de isolamento em um runner temporário do GitHub Actions, sem deploy, sem VPS, sem OpenHands Core/Canvas e sem LLM. Esta PR não concede autorização para registrar/delegar agentes nem para o canário operacional.

## REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

- REAL NOW ao criar a branch: main no merge 6811dc8, PR #11 integrada e #10 encerrada como absorvida. O primeiro canário continua NO-GO.
- PROVEN EVIDENCE anterior: o harness implementa snapshot mínimo, argv restrito, execução bwrap, Guard compartilhado e supervisor de processos; bwrap e unshare não funcionaram no executor anterior.
- GAPS: comportamento real de isolamento em runner GitHub Actions ainda não comprovado. Resultado de CI deve ser lido no HEAD exato e registrado separadamente; escrever workflow não é prova de execução.
- REUSE GATE: reusar scripts/canary_controls.py e os testes unittest; não criar novo agente, runtime ou executor.
- DECISION: adicionar job separado que falha se qualquer prova de sandbox falhar. Não converter indisponibilidade em sucesso ou skip.

## Matriz de provas do job

O workflow .github/workflows/canary-sandbox.yml usa ubuntu-24.04 efêmero, até oito minutos, token GitHub somente para leitura e checkout sem persistir credenciais. Instala apenas bubblewrap dos repositórios Ubuntu do runner. Não usa secrets, SDK, modelo de IA ou provedor LLM.

Em scripts/probe_canary_sandbox.py:

1. Confirmar que bwrap inicializa usando sandbox_argv do harness e executa leitura permitida.
2. Proibir escrita em arquivo existente e criação de arquivo no snapshot, verificando SHA-256 depois.
3. Demonstrar invisibilidade de arquivo sintético fora do snapshot, pasta .git e variável sintética de ambiente herdado.
4. Demonstrar que rede do sandbox não alcança um listener 127.0.0.1 efêmero no host. Nenhuma requisição à internet.
5. Rejeitar comandos não presentes na allowlist, sem fallback.
6. Com processo sintético sem sandbox, comprovar que o supervisor mata o grupo e descendente após timeout.

Os passos de apt são apenas preparação temporária do runner; a etapa de rede verifica conectividade local da sandbox, não bloqueio de egress da VM GitHub inteira.

## Critério de aceite e limites

- Job GREEN com seis provas passando e nenhuma ignorada = sandbox bwrap deste runner aprovado **para as propriedades exercitadas**, não significa isolamento geral, proteção contra todas as evasões ou prontidão operacional.
- Job RED por user namespaces, AppArmor, ausência do binário ou falha de prova = NO-GO; investigar sem fallback para shell do host.
- CI principal e teste de contratos continuam independentes. Não publicar conteúdo de arquivos, segredos, caminhos privados nem ambiente em logs.
- A prova de encerramento de grupos cobre descendentes que não escapam da sessão/grupo. Não demonstra isolamento cgroup contra processos maliciosos destacando sessões.
- Mesmo GREEN, permanecem bloqueios: worker completo realmente conectado ao TaskToolSet, controles de custo preventivos, modelo/tarifas verificadas e autorização separada do canário com LLM.

## Entrega

Branch e PR para revisão, sem merge/deploy. Após o primeiro job, conferir UMA vez o status do HEAD e o relatório de falhas/sucessos. Não fazer polling contínuo.
