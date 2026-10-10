# ADR-0001 — Observatório como App Canvas
**Status:** Proposto, sujeito à revisão de PR.

O requisito é aparecer no menu OpenHands Agent Canvas (`New Chat / Customize / Automate / Observatório`) como o exemplo Vibe Kanban, porém em experiência de sistema solar.

**Escolha:** manifesto + ESM com `registerPage`, V0.2 em Shadow DOM, somente demonstração estática.

**Rejeitados:** fork completo do Canvas, portal externo como caminho único, cópia do Kanban/cron manager.

**Consequências:** compatibilidade e segurança devem ser validadas antes de instalar; integração real requer BFF de leitura RBAC.
