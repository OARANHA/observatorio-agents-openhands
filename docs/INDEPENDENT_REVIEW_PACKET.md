# Revisão independente e preparação de missão única

2026-10-11. **NO-GO OPERACIONAL.** Não executa, provisiona, registra, delega
ou implanta. Autorrevisão de PR não atende G11.

## Arquitetura e fontes

PROJECT_SOURCE → AGENTS → ADR-0001 (Proposto) → CANONICAL_STATE/MEMORY →
ARCHITECTURE → GO_NO_GO_MATRIX → handoffs. ChatGPT coordena dentro das
permissões; OpenHands executa missões autorizadas; Observatório visualiza;
GitHub registra. Nenhum novo orquestrador ou backend de autorização.

Examinar Guard/supervisor/terminal em canary_controls, Book/Decimal em
canary_budget, SyntheticTransportGate (exclusivo de fakes), canary_sdk,
probe_canary_worker (inerte), canary_audit_bundle e canary_evidence_session.
Fontes/dependências: [inventário SDK](SDK_TRANSPORT_INVENTORY.md) e
[egress auxiliar](SDK_AUXILIARY_EGRESS_INVENTORY.md).

## Ameaças para avaliação do revisor distinto

| Ameaça | Prova offline | Limite ainda pendente |
|---|---|---|
| HTTP auxiliar, hooks, imports e rotas fora dos sinks | AST/namespace/HTTP/thread/filho | Dependências/destinos dinâmicos e ambiente real |
| FDs/ambiente/arquivos herdados | snapshot RO/clearenv/close_fds/probes | Isolamento futuro; stdout é canal a minimizar |
| Recusa seguida de ações | callback/Guard/TaskManager mocks | Herança operacional e cancelamento do filho |
| Timeout/cleanup incompleto | killpg antes de reap bounded 1s | Falha não prova morte; finally SDK sequencial pode pular close |
| Métrica parcial/ausente/sub-reserva | Decimal/hold/binding/concorrência | Cobrança/tokenização/cap efetivos do provedor |
| Streaming adiado além do escopo | Iterator/AsyncIterator/awaitable negados | Gate de fakes não controla tasks de código hostil |
| Evidência alterada ou replay | hash/campos/session/janela | Não autentica origem/tempo; restart perde replay state |
| Vínculo e visibilidade multiprojeto | revisão #7/demo/manual separados | Não há backend RBAC ou identidade autenticada |

Revisor distinto confere HEAD/merge/runs/logs, reproduz provas pertinentes,
registra achados e aceite/rejeição por gate. Contagens GREEN não substituem
parecer nem autoridade operacional.

## Checklist de preparação — não preenchido nem aprovado

1. Ambiente efêmero identificado; RO público, estado temporário separado,
   rede/processos descendentes/FDs/env comprovados nele, sem segredos produtivos.
2. SDK/Tools 1.53.0 e transitivos congelados/revisados; origens de rede, hooks,
   MCP/ACP/remote/imports explicitamente permitidos ou negados, sem terminal host.
3. Guard único, Book preventivo, zero retries, chamadas/input/output/timeout
   efetivos, confirmação exata e recusa terminal; worker atual permanece inerte.
4. Proprietário escolhe modelo/snapshot/rota disponível, todas tarifas datadas,
   categorias thinking/cache/extras e tokenização. [Dossiê](PUBLIC_PROVIDER_DOSSIER.md)
   é pesquisa pública, não tarifa/cap de conta nem escolha autorizada.
5. Somente após autorização específica, responsável provisiona identidade
   não produtiva segregada, escopo mínimo e validade curta; segredo por canal
   aprovado, nunca Git/log/terminal. Conferir quota/cap/latência de corte reais.
6. Responsável define e valida revogação na conta autorizada; nenhuma credencial
   foi acessada/provisionada/revogada neste ciclo offline.
7. Revisor distinto aprova wiring/herança operacional de ferramentas nativas,
   uma delegação code-explorer sem resume; outros presets/ações ficam negados.
8. Protocolo operacional vincula autorização/commit/eventos, proveniência
   confiável, acesso segregado, redaction, retenção e descarte. Não promover
   receipts sintéticos a faturamento ou autenticidade.
9. Plano de interrupção: recusa, custo/uso incerto, limite, egress, falha de
   comunicação/cleanup encerram tudo, sem retry/resume/refund do hold incerto.
10. Parecer distinto e autorização humana explícita da missão congelada,
    orçamento e riscos residuais. Campo ausente ou gate não provado = NO-GO.

## Parada e rollback futuros — não executados

Supervisor autorizado tenta matar grupo e reap bounded; erro registra término
**não comprovado**, exigindo intervenção humana. Responsável interrompe o
processo, revoga identidade segregada, confere ausência de descendentes,
preserva evidência minimizada aprovada e elimina temporários sob política.
Não alterar Canvas/Core/projetos atendidos. Não declarar cleanup concluído
somente porque um worker devolveu erro.

## Modelo obrigatório de autorização única

ID; repo/commit/snapshot; ambiente; versões/rotas/endpoints; modelo/tarifas;
referência segura da identidade segregada (nunca chave); tarefa read-only;
comandos/aprovação; uma delegação sem retomada; input/output/chamadas/timeout/
custo; riscos de excesso aceitos; responsáveis por parada/revogação/retenção;
política de evidências; parecer distinto; validade e autorização explícita do
proprietário. Preencher formulário não inicia canário ou habilita serviço.

## Reprodução offline disponível

`python3 -B -m unittest discover -s tests -p 'test*.py' -v` e workflows
efêmeros existentes. Provas de egress SDK exigem netns e versões corretas;
não executá-las no host como substituto. Sem comando operacional neste pacote.
