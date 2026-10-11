# OBS-EXPLORER-OFFLINE-EVIDENCE-001 — ciclo autorizado 2026-10-11

## REAL NOW → PROVEN EVIDENCE

Base main `732351094565da35159943212782c71941784f64`, PR #21 integrada.
Ciclo autorizado pelo proprietário: desenvolver/revisar/merge de quatro
incrementos offline após ambas CIs GREEN no HEAD exato e sem conflitos.
Permissão não abrange provedores, inferência, deploy, agentes ou infraestrutura.

| PR | HEAD revisado e testado | CIs confirmadas |
|---|---|---|
| #19 | 925ff17ebac7c64d6c847b3e80bbdf5fec8837e3 | 38117751430 / 38117751606 |
| #20 | 370600016b1bfae565a8b45a6ab389c413c10527 | 38118001929 / 38118001931 |
| #21 | 69c02bffa66bd066387b65243e5d8518bcc4b10a | 38118252923 / 38118252958 |

Essas três PRs foram integradas sequencialmente após revisão adversarial
**automatizada por autorrevisão**, não por revisor humano independente.
GitHub confirmou ausência de conflitos; merges usaram expected_head_sha.
Logs do runner SDK conferidos: 4/10/16 testes adversariais respectivamente,
12 testes de SDK 1.53.0 com stubs em namespace de rede separado e worker
inerte com zero registros, delegações e inferência reais. A CI principal
ignorou somente os testes dependentes do SDK: 115/121/127 descobertos, 17 skips.
Não confundir essas provas sintéticas com agentes operacionais.

## REUSE GATE → DECISION do quarto incremento

Reutilizar validate_sdk_config no baseline e na liquidação, exigindo modelo,
retries, max_output_tokens e tarifas nominais idênticos ao contrato sintético.
Mudança durante a resposta fictícia fecha Book/Guard e retém reserva.
Nada é enviado ao provedor; ler campos SDK não comprova aplicação de token caps.

Novo `scripts/canary_accounting_evidence.py` gera esquema fixo
`obs.synthetic.accounting.v1`, contendo apenas valores monetários, contadores
e tokens observados pelo Guard. Nenhuma serialização de LLM, baseline, modelo,
URL, prompt, exceção, chave, ambiente ou atributo extra. `operational_go` sempre
False, mesmo que o chamador injete atributo True. Dados inválidos fecham a prova.
Modelo/tarifa não sintéticos são recusados para esse relatório.

`verified_spent_usd` é valor já liquidado no Book; `held_usd` é pior caso ainda
reservado, inclusive após falha incerta. `book_uncommitted_usd` é saldo aritmético
do Book, **não** disponibilidade autorizada no Guard ou provedor. Tokens são
observação local do Guard, não fatura. Estado closed_uncertain mantém reserva;
closed_verified não afirma sucesso semântico, sandbox ou registro de agentes.
Relatório não declara ausência de tráfego por simples inspeção desses contadores.

CLI é demo fechada sem argumentos, SimpleNamespace + transportes locais:
`python3 -B scripts/canary_accounting_evidence.py`.
Uma chamada fictícia com 100+100 tokens, gasto inventado USD 0.001, Book USD 0.01,
saldo Book 0.009, nenhum hold e missão fechada por max_calls=1.
Nenhum objeto LLM/Agent/Conversation real é construído por essa demo.

Verificação local final: **133 testes descobertos, 116 aprovados e 17 opcionais
ignorados**, diagnóstico estático, demo JSON e build/sintaxe JS aprovados.
O runner SDK executa também os novos testes e a demo; CI deste HEAD por conferir.
Revisão adversarial: overrides/mutação nominal, ausência de tarifa, reservas
incertas, ledger negativo/NaN/excessivo, booleanos como contadores, atributos
privados e tentativa de promover GO. Não adicionar tolerância monetária.

## GAPS e decisão operacional

**NO-GO operacional permanente neste ciclo.** Ainda pendentes:

1. Modelo/provedor/credencial separada autorizados e tarifas oficiais revisadas.
2. Caps físicos de input/output, extras, cache e quota financeira do provedor.
3. Cobertura independente de todos os egress e retries das dependências;
   isolamento do runner não é prova de runtime Canvas ou sandbox multi-tenant.
4. Worker operacional completo com herança comprovada do executor/confirm policy,
   supervisor externo e parada global nas fronteiras não simuladas.
5. Plano/custo concretos e autorização explícita separada para uma delegação real.

SDK float pode causar recusa exata após acúmulos não representáveis; é limitação
conservadora, não motivo para tolerância automática. Referências Python não
protegem contra código hostil no processo. Revisão humana independente continua
recomendada antes de qualquer decisão operacional. Nenhum deploy ou outro projeto.

Achado adicional da revisão: contador Guard adulterado acima do limite era
serializado. RED reproduziu; relatório agora nega limites inválidos e contadores
fora dos limites, abortando a prova em vez de emitir evidência enganosa.
