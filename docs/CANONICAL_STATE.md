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

## GAPS E GATES
- A extensão **NÃO foi instalada nem habilitada** no OpenHands/Canvas da VPS.
- Compatibilidade com a instalação Canvas real, segurança/CSP no servidor, renderização 3D GPU real e dados de agentes reais não foram demonstrados.
- Próximo gate: revisão final e autorização explícita para instalar **desabilitado**, fixando SHA; só então teste visual no navegador autenticado.
- Integração com agentes reais requer inventário autoritativo, BFF somente leitura, RBAC por projeto/tenant, minimização e auditoria.
- Não modificar VIGIAFAST, ELUS, Wandora, Agent Mesh, brokers, volumes, credenciais ou VPS sem autorização específica. Não realizar merge/deploy automáticos.
