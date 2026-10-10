# Estado canônico — Observatório de Agentes (2026-10-10)

## REAL NOW — GitHub
- Repositório: `OARANHA/observatorio-agents-openhands`, criado inicialmente vazio.
- `main`: apenas README de bootstrap; SHA `d1cf8e9ef6afb70270129b188dbe315ecfe401f5`.
- Branch: `feat/canvas-observatorio-v03` e PR **#1** (aberta para revisão, não mesclada).
- Primeira revisão da branch `6a7a22bc875fc0b09d85912f2360521cceaf55f9`: workflow `CI Observatorio` run `38061597646` **completed/success**; job `contract`, etapas `Conferir geração` e `Contrato e sintaxe` concluíram com sucesso. Se o HEAD avançar, esse resultado não equivale automaticamente ao CI do novo SHA.

## PROVEN EVIDENCE
- Fonte OpenHands/demos usa manifesto `canvas-extension.json`, ESM e `activate(host)` / `registerPage`.
- Contrato da extensão, código ESM e origem V0.2 conferidos na branch; o app não usa `host.agentServer.request` nem `fetch`.
- Testes locais da V0.3 em host Canvas **simulado** (desktop e mobile), sintaxe e ciclo mount/unmount passaram. CI remoto prova contrato e geração reproduzível, **não** instalação no servidor real.
- Dados de VIGIAFAST/Wandora/ELUS/OpenHands Lab são **ilustrativos**, não um inventário real.

## INSTALAÇÃO REAL E DEFEITO VISUAL CONFIRMADOS PELO USUÁRIO
- A V0.3.0 foi instalada com Ref fixo \`c9e43d10bcd77c874ddb09aaef512707e9d310c0\`, inicialmente desabilitada, depois ativada pelo usuário no Canvas protegido por Cloudflare Access (screenshots de 2026-10-10).
- O menu do Observatório abriu e a visualização do sistema VIGIAFAST renderizou planetas em 3D no navegador do usuário. Não demonstra conexão com agentes reais.
- **Defeito**: a barra lateral nativa do OpenHands ficou visualmente vazia, mas seus links ainda reagiam ao mouse. O CSS compilado continha \`.ob-wrap:before{...position:fixed...}\`, cuja camada decorativa cobria o viewport em vez do painel.
- **Correção V0.3.1 proposta nesta PR**: \`position:absolute\` para o fundo pseudo-elemento, dentro do contêiner relativo e isolado do app. Adicionado teste de regressão. Reprodução local via Canvas simulado mostrou antes \`fixed\` e depois \`absolute\`, com os links da barra visíveis; navegação/lifecycle passaram localmente.
- **A revisão nova NÃO está aplicada no Canvas real**: a instalação ativa continua pinada em SHA anterior. CI do novo commit precisa ser verificada; não assumir resultado anterior.

## GAPS E GATES
- A compatibilidade visual corrigida ainda precisa ser verificada no Canvas real após atualizar explicitamente o aplicativo para novo SHA.
- A política de CSP/segurança do servidor, desempenho GPU real completo e dados de agentes reais ainda exigem verificações específicas.
- Integração com agentes reais requer inventário autoritativo, BFF somente leitura, RBAC por projeto/tenant, minimização e auditoria.
- Integração com agentes reais requer inventário autoritativo, BFF somente leitura, RBAC por projeto/tenant, minimização e auditoria.
- Não modificar VIGIAFAST, ELUS, Wandora, Agent Mesh, brokers, volumes, credenciais ou VPS sem autorização específica. Não realizar merge/deploy automáticos.
