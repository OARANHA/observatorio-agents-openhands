# Ciclo 003 — validação de evidências e lifecycle offline

2026-10-11. Base local `ebd967cad24603f06e08b5e141e7e9b7ac6fe34e`.
Frente isolada `fix/cycle003-evidence-validation`. **NO-GO operacional**.
Projeto horizontal Observatório; ADR-0001 continua Proposto. Nenhuma mudança
em Canvas, VPS, SDK/Core ou projetos atendidos.

## REAL NOW → PROVEN EVIDENCE

O envelope v1 e a sessão efêmera usavam `\d` para timestamps. Em Python esse
padrão admite dígitos Unicode; `datetime.strptime` também admite alguns deles.
Exemplo reproduzido: `2026-10-11T12:00:0٠Z` era aceito com digest recalculado.
Assim duas grafias diferentes representavam o mesmo horário, contrariando o
formato fechado de UTC. Isso não demonstra bypass de UUID/replay nem acesso
operacional: UUID/hash e origem continuam declarações sintéticas.

Testes escritos antes da correção produziram RED: cinco subcasos do envelope,
dois parâmetros de janela e um receipt aceitos sem o `GateError` esperado.
A correção mínima troca `\d` por `[0-9]` nos dois validadores, preservando
`strptime` para calendário e exceções minimizadas. Depois: 9 testes do
envelope e 10 da sessão GREEN. Os testes novos também verificam que receipt
recusado encerra a sessão sem incrementar registros.

Caracterizações adicionais, sem novos mecanismos:

- 2000 e 2024 aceitam 29/02; 1900 e 2026 recusam; segundo 60 recusado.
- UUID sem variante RFC, v5 e grafia maiúscula recusados após rehash.
- Janela inclui os extremos do dia bissexto; calendário inválido e janela
  invertida recusados.
- Mesma evidência pode ser aceita por instância nova depois de a anterior
  parar por replay. Teste PASS demonstra a lacuna de restart já documentada;
  não demonstra proteção persistente. Nenhum store/auth foi introduzido.

Malformed JSON, chaves duplicadas, tamanho acima de 8192, campos privados,
contadores/finanças, replay concorrente e cap permanecem cobertos pelas
negativas existentes. Não foi encontrado outro defeito que justificasse
alteração de produção nesta investigação delimitada.

## REUSE GATE — TaskManager oficial 1.53.0

Leitura estática de `openhands/tools/task/manager.py` instalado confirmou:
`_run_task` marca status não FINISHED como erro e `_run_stop_detail` pode
incorporar resposta parcial; o `finally` chama métricas e eviction em sequência.
Em `_evict_task`, pause precede close e a cópia sem conversation só ocorre
depois de ambos. Falha de close pode substituir retorno e impedir eviction.
Fontes somente lidas; nenhum import SDK foi executado no host.

Novo teste opcional usa o TaskManager oficial com conversation mockada PAUSED,
resposta parcial fictícia e fechamento normal/falho. Diferencia erro do worker
da exceção de cleanup, exige ausência de resultado bem-sucedido, uma única
execução e caracteriza eviction pulada na falha. Reutiliza SyntheticTransportGate
para preparar uma reserva incerta: Book/Guard já fechados antes do ciclo SDK
permanecem fechados, retêm a mesma Reservation e recusam nova chamada.
Isso não prova que TaskManager feche Book/Guard sozinho nem morte de processo.
O SDK/Core não foi alterado, e resposta parcial não foi promovida a evidência
operacional. Minimização futura do canal de erro é requisito de integração.

## Reprodução e limites

RED, antes da mudança de regex:

```sh
python3 -B -m unittest discover -s tests -p 'test_canary_audit_bundle.py' -v
python3 -B -m unittest discover -s tests -p 'test_canary_evidence_session.py' -v
```

GREEN final local:

```sh
python3 -B -m unittest discover -s tests -p 'test*.py'
git diff --check
```

187 testes descobertos: **161 PASS, 26 opcionais SDK ignorados**; diff sem
erros de whitespace. Envelope final 10 testes e sessão 12 incluídos na suite.
A saída argparse do caso negativo de worker é esperada e o teste passa.
O novo teste TaskManager não foi executado localmente: depende da distribuição
SDK/Tools 1.53.0 no runner isolado existente. GREEN desse teste e CI do HEAD
exato precisam de logs próprios antes da integração; não alegar prova SDK local.

G07/G10 permanecem PARCIAIS, G11 NÃO PROVADO e G12 BLOQUEADO. Hash não
autentica, janela não certifica relógio e replay continua somente em memória.
Sem provider, LLM, agente, registro, delegação, credencial, deploy ou merge
nesta frente; nenhuma fonte externa ou dependência foi executada.
