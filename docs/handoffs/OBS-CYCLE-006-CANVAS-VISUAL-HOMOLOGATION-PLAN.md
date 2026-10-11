# CYCLE006 — plano de homologação visual do Observatório V0.5.1 no Canvas

**Natureza:** plano documental e checklist de aceite, **NÃO é autorização de instalação, atualização, habilitação ou operação**. Criado após o merge da PR #43. Observatório é ferramenta horizontal, não um módulo do VIGIAFAST ou de qualquer cliente.

## 1. REAL NOW → PROVEN EVIDENCE → GAPS → REUSE GATE → DECISION

**REAL NOW (GitHub, 2026-10-11):**
- Repositório: `OARANHA/observatorio-agents-openhands`.
- `main` após merge da PR #43: `ac9c525a7e169fe253f0f488550686491939289a` (merge commit, pais `e06d3b01e60d9a5503e046dc0fe2eeb269f0e403` e `f50109d5c73c9d8e027ac9ad15ba0472e184283a`).
- Manifesto `canvas-extension.json`: versão `0.5.1`, página `observatorio`, entrada `extension.js`, uso de `host.registerPage`.
- PR #43 **integrada ao repositório**. PR #35 ainda **aberta**, PR #7 **draft/aberta**: candidatas anteriores com sobreposição de grafo. **Não fechar, mesclar ou descartar automaticamente**.
- **Última instalação comprovada em captura histórica do operador:** Observatório V0.4.2, ref `7212c51c38fc34cd195afb4db99ee35808e67cb5`. O estado **atual do Canvas não foi inspecionado neste ciclo**; não inferir que essa versão permanece instalada ou que a 0.5.1 já esteja habilitada.

**PROVEN EVIDENCE (offline no HEAD da PR #43, integrado sem alterar a árvore):**
- CI Observatorio: [38175631445](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38175631445), `SUCCESS`; 218 Python executados, 190 aprovados e 28 skips opcionais SDK.
- Graph DOM Offline: [38175631434](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38175631434), `SUCCESS`; **19/19** testes Chromium, sem falhas nem skips; testes com DOM real e fixtures sintéticas, **não** sessão do Canvas.
- Canary Worker Inert SDK: [38175631527](https://github.com/OARANHA/observatorio-agents-openhands/actions/runs/38175631527), `SUCCESS`; `actual_agent_registrations=0`, `actual_llm_calls=0`, `actual_task_dispatches=0`.
- Revisão adversarial automatizada Codex sobre HEAD `f50109d5...`, árvore `4fa1490b...`: A1–A5/R1–R3 resolvidos nos casos examinados, sem P0/P1 demonstrado; **APTA PARA CONSIDERAÇÃO DE MERGE**, não aprovação operacional.
- JEV consultivo avaliou a revisão offline como concluída; não substitui revisão/aceite formal G11.
- A versão 0.5.1 implementa o **Universo + Grafo 2D offline** com projetos e cenários DEMO, consulta pontual de estado de conversa pelo host quando acionada, links manuais rotulados, teclado/pan/zoom e fallback 2D. Não descobre contas/projetos/agentes automaticamente.

**GAPS:** versão e permissões atuais do Canvas, instalação 0.5.1, compatibilidade real `registerPage`, WebGL2/context loss/GPU, dispositivo touch, leitor de tela, vínculo RBAC por projeto, memória persistente, cancelamento de transporte e revisão G11 **não comprovados**. `finished` não significa missão bem-sucedida.

**REUSE GATE:** reusar **Apps nativo do OpenHands Canvas** e o código já integrado; não bifurcar Canvas, criar novo backend, nova autenticação, orquestrador ou credenciais no frontend.

**DECISION:** preparar aceite **somente visual**, inicialmente com informações demonstrativas e consulta sintética opcional autorizada separadamente. **NO-GO operacional / G12 BLOQUEADO** continua valendo. Nenhuma etapa deste documento deve ser executada sem o gate de autorização indicado.

## 2. Gates de autorização e responsabilidades

| Gate | Antes de executar | Limite |
| --- | --- | --- |
| H0 — levantamento somente leitura | Operador identifica URL/instância Canvas, versão, App atual, ref instalado, permissão e janela de manutenção; evidência minimizada | Não mexer em configuração; não usar sessão de outra pessoa |
| H1 — instalação desabilitada | Aprovação explícita do proprietário para **a instância identificada e o commit SHA exato**; confirmar backup/reversão para a ref realmente observada em H0 | Somente App Observatório, inicialmente **desabilitado**; nada de OpenHands Core/VPS |
| H2 — habilitação visual | Aprovação explícita após H1 e aceitação dos riscos de JavaScript no contexto autenticado | Navegar dados **DEMO**, sem GET a conversas reais ou execução de agentes |
| H3 — GET de conversa sintética | Aprovação própria para o UUID **sintético/teste**, ambiente e conta autorizados; nenhuma informação de cliente | Somente `GET /api/conversations/{UUID}`, uma consulta intencional e sem polling |
| H4 — operação real | Gates cumulativos G01–G11 provados + autorização humana G12 para missão congelada | **BLOQUEADO neste ciclo** |

G11 (revisor distinto + aceite de riscos) continua **NÃO PROVADO**; P01 **PARCIAL**; P02/P03 **NÃO PROVADOS**; ADR-0001 **Proposto**. H1/H2 são apenas proposta para homologação visual; não promovem G11 nem G12.

## 3. Procedimento proposto ao operador (NÃO executado)

1. **H0:** no Canvas autenticado pelo próprio operador, conferir em **Customize → Apps** a versão/ref **efetivamente instalada**, estado habilitado/desabilitado, URL da instância e compatibilidade conhecida; registrar evidência sanitizada (sem nomes de clientes, IDs reais, cookies, tokens, prompts).
2. Registrar a estratégia de rollback **para a ref efetivamente observada em H0**. A V0.4.2 (`7212c51...`) é evidência histórica, **não substituir automaticamente pela versão de H0**. Caso não haja rollback verificado, **STOP / NÃO INSTALAR**.
3. **Somente após H1:** adicionar/atualizar **somente** Observatório no gerenciador nativo de Apps. Fonte `https://github.com/OARANHA/observatorio-agents-openhands.git`, ref **fixa** `ac9c525a7e169fe253f0f488550686491939289a` (não `main` móvel), path **vazio** (manifesto `canvas-extension.json` na raiz); manter **desabilitado** até inspecionar a revisão.
4. **Somente após H2:** habilitar App, confirmar menu **Observatório**, abrir e checar compatibilidade do host, isolamento visual de Shadow DOM e ausência de interferência no menu nativo. Não usar conversas ou projetos privados na inspeção de UI.
5. **Somente após H3:** se houver conversa sintética autorizada e controle de acesso validado, executar **uma** consulta deliberada. Verificar UUID, estado, horário de origem/observação, associação de projeto manual **não atestada**, inexistência de inferência sobre agentes/êxito, comportamento negado/timeout e nenhum segredo exposto. Não reaproveitar UUID históricos sem nova aprovação.
6. Em falha relevante, **STOP**: desabilitar extensão e reverter à ref registrada em H0 **apenas conforme procedimento autorizado**. Revalidar a navegação nativa e registrar o resultado, sem afirmar rollback concluído antes de inspeção.

**Importante:** Apps executam JavaScript no contexto autenticado do Canvas. Shadow DOM é isolamento visual, **não** fronteira de autorização. Não copiar senhas/tokens para este projeto ou screenshots.

## 4. Checklist de aceite visual com evidências

| ID | Cenário | Critério observável | Evidência necessária | Status |
| --- | --- | --- | --- | --- |
| V01 | Ref e manifesto | Ref instalada coincide com SHA congelado, versão 0.5.1, entrypoint correto | Captura sanitizada do App/versão/ref | **PENDENTE H1** |
| V02 | Registro | Menu nativo mantém-se visível, Observatório aparece e abre sem erro de montagem | Tela + versão do host, sem dados privados | **PENDENTE H2** |
| V03 | DEMO versus consultado | Quatro exemplos visuais têm DEMO explícito, nada aparenta ser inventário real | Captura Universo e legenda | **PENDENTE H2** |
| V04 | Grafo e origem | Nós DEMO, conversa consultada e projeto manual claramente distintos, sem associação validada inventada | Captura grafo/painel com fixture permitida | **PENDENTE H2/H3** |
| V05 | Layout | Desktop 1440px, mobile 390px e tablet sem cortes/sobreposições; texto legível | Capturas sanitizadas por viewport | **PENDENTE H2** |
| V06 | Teclado e foco | Tab/Enter/Escape, busca, filtros, pan/zoom/reset com foco previsível | Checklist manual de teclado | **PENDENTE H2** |
| V07 | Movimento | Respeita `prefers-reduced-motion`, sem efeitos agressivos ou quebra ao alterar preferência | Checklist visual em configurações suportadas | **PENDENTE H2** |
| V08 | Renderização | WebGL2 real (se suportado), fallback 2D, perda/restauração de contexto, cleanup ao sair | Registro técnico sanitizado / device e browser | **PENDENTE H2** |
| V09 | Touch real | Rolagem vertical, pinch e pan/navegação não bloqueiam a página | Teste em dispositivo touch real | **PENDENTE H2** |
| V10 | Acessibilidade | Nomes acessíveis, contraste, ampliação de fonte e leitor de tela conforme dispositivo | Checklist de tecnologia assistiva | **PENDENTE H2** |
| V11 | GET positivo/negado | Apenas conversa sintética aprovada, resposta autorizada/negada distinguida, sem dado antigo após falha, timeout não anuncia cancelamento de rede | Log mínimo sem payload privado + captura | **PENDENTE H3** |
| V12 | Desmontagem/rollback | Remount sem duplicação, timers/recursos liberados na extensão e estratégia de reversão comprovada | Registro técnico e rollback autorizado quando aplicável | **PENDENTE H2/H3** |

**Pontos de parada:** ref/versão divergente; erro JS não recuperável; acesso não autorizado; GET expõe dados privados; tráfego externo não previsto; UI impede navegação do Canvas; falha de teardown; WebGL/contexto instável sem fallback; impossibilidade de reverter com segurança. O termo `resolved` em DOM synthetic não substitui prova em Canvas.

## 5. Pacote de evidência e aceite

Preencher apenas **depois** de testes executados e autorizados:

- Ambiente/instância (sem token), versão do Canvas, responsável e horário.
- SHA exato do App e versão do manifesto; ref anterior e plano de reversão.
- IDs V01–V12: **PASS / FAIL / BLOQUEADO / NÃO EXECUTADO** e links para evidências sanitizadas com retenção conhecida.
- Evidência de rede apenas com paths/verbos permitidos, sem conteúdos de conversas.
- Defeitos P0/P1/P2/P3, mitigação, decisão humana e riscos residuais.
- Resultado separado: **ACEITE VISUAL (GO/NO-GO)** e **ACEITE OPERACIONAL (NO-GO neste ciclo)**.
- Evidências de H1/H2/H3, quando aplicáveis, documentadas em repositório sem identificadores sensíveis.

**Sem preencher por antecipação.** Screenshots do Chromium sintético da CI não comprovam instalação, autorização por projeto ou WebGL real.

## 6. Seguimento administrativo das PRs anteriores

- **#43:** integrada à main, é a candidata visual V0.5.1 de referência.
- **#35:** permanece aberta; contém trabalhos visuais reutilizados pela #43. Fazer comparação de arquivos/SHAs e registrar divergências antes de eventual fechamento. Não aplicar merge para evitar retrocesso/duplicidade.
- **#7:** permanece draft; mesma cautela e comparação de escopo. Não fechar automaticamente.
- Eventual fechamento das PRs antigas exige autorização e comentário de rastreabilidade específico. Não modificar PRs nesta preparação.

## 7. Próxima decisão humana

Autorizar ou recusar **H0**, levantamento da instalação **somente leitura**; fornecer a instância do Canvas e seu contexto autorizado. Em seguida, se necessário, submeter **H1**, **H2** e **H3** como pedidos distintos. Não inferir a autorização de instalação a partir do merge da PR #43.

**Este documento não instala, habilita, consulta nem implanta nada.**
