# Avaliação independente de branch visual — ciclo003

Main base ebd967cad24603f06e08b5e141e7e9b7ac6fe34e. PR #7 permanece
aberta/draft HEAD48f898d99a8979ef2c794513131506b028772666, intocada.
Reuso: patch dos cinco arquivos visuais da #7 sobre main atual; documentação,
segurança e handoffs da main preservados. Nenhum merge da #7 ou Canvas.
Nova branch feat/cycle003-visual-evaluation. Este código de evolução visual
não está instalado e não será integrado automaticamente: decisão específica
necessária. Manifest/registerPage/Shadow DOM/WebGL2/fallback2D e teardown
reutilizados, consulta pontual host.agentServer.request(GET) preservada.

## Identidade e testes

IDs compostos SHA256 via WebCrypto, com nonce local por mount, domínio de tipo,
contexto, UUID e declaração manual. O contexto é LOCAL, não tenant autenticado;
nem hash nem nonce comprovam RBAC ou anonimização. Não publica projeto/UUID
brutos nos IDs. Origem permanece igual na mesma vista, conversa/projeto
mudam sem colisão trivial; IDs de outra vista/tipo negados e contexto ausente
omite os nós consultados. Demonstrações continuam prefixo demo, nenhum agente
ou sucesso inferido. Identidades são efêmeras, não garantem vínculo durável.

Oito contratos Node RED→GREEN, inclusive mistura de contexto (RED específico)
negada. Build revelou bug de substituição literal $' pelo String.replace;
node --check RED e teste existente RED; callback replacement preserva fonte,
sintaxe/regeneração GREEN. Local185 tests:160 PASS/25 SDK opcionais skip,
além dos oito contratos novos e seis baseline congelados. Ajustes dos antigos
asserts refletem IDs dinâmicos e versão0.5.1, não removem proteção de origem.

## Navegador e interação — estado em preparação

Playwright instalado1.62.1, browser executável ausente. Uma tentativa oficial
install chromium --only-shell falhou: arquivo download inválido/ZIP truncado.
Nenhuma proteção do sistema alterada. Teste local de DOM falhou por browser
indisponível; não é homologação. Workflow pertinente Graph DOM Offline instala
Playwright1.58.0 fixado e Chromium oficial em runner Ubuntu22.04, com
chromiumSandbox=true, retries de teste zero, fixtures públicas interceptadas,
requests inesperados abortados e denunciados. Não usa sessão real do Canvas.
Docs oficiais: https://playwright.dev/docs/release-notes e
https://playwright.dev/docs/api/class-browsertype (consulta2026-10-11).

Seis cenários reais de DOM preparados: abertura/teclado/seleção/desmarcação/foco;
sistema/universo/busca/filtro/vazio; GET mockado/manual/erro; mobile/movimento
reduzido/zoom/pan/reset; escape/contraste de label no fundo declarado/pt-BR;
teardown RAF/observer/remount sem reads duplicadas. Foco/pan/contraste aguardam
RED da CI para confirmar defeitos e correções. Não alegar testes visualmente
aprovados ou WebGL2 real: fixture força fallback2D, contraste não é auditoria
completa e screenshot ainda ausente. Sem polling contínuo; duas CIs existentes
mais workflow DOM precisam ser examinadas no HEAD final.

## Checklist futuro no Canvas — não executado

Autorização específica e SHA congelado; confirmar manifest/registerPage e versão;
Shadow DOM sem afetar host; WebGL2 e fallback2D com GPU/context loss; teclado/foco
nos filtros e seleção; layout desktop/mobile e pan; labels DEMO/manual/consultado;
GET autorizado sem mistura tenant, erros sem nó novo; cancelamento consulta ao
teardown; RAF/resize/GPU liberados; comparação screenshot sanitizada e contraste;
nenhum request/parâmetro adicional, nenhum agente real ou ação de escrita.
P01 PARCIAL/P02 e P03 NÃO PROVADOS. NO-GO operacional/G12 BLOQUEADO.


## RED real do navegador e correção proposta

HEAD0c0707761606b1582620247edd268b1062d13fc7, Graph DOM run38153324520
job114511095537: seis cenários executados, quatro PASS e dois RED. Confirmou
foco perdido (activeElement sem node após Enter) e pan ausente. Testes
navegação/busca/vazio, GET mockado/erro/proveniência, escape/contraste simples
e teardown/remount passaram em Chromium com sandbox obrigatório. Não é Canvas.
Correção na mesma branch: capturar/restaurar foco por identidade ou fallback
mapa, toggle seleção e Esc; remover anúncio duplicado do painel; mapa focável
com setas/pointer e pan bounded±140px, reset com zoom. Fundos opacos e fontes
legíveis preservam contraste ao destacar seleção sem reduzir texto dimmed.
Novo HEAD precisa reexecutar todos cenários: não antecipar GREEN. Workflow
publica apenas duas screenshots sintéticas, retenção3dias, sem trace/payload.


HEADa80f22429f5afe009813e34928080cdef3b88bdf: run38153679215, cinco DOM
PASS/um RED. Foco/toggle/teclado passaram; o RED restante foi comparação
textual de CSS normalizado pelo Chromium (espaço no translate), não prova
de falha no reset. Assertion agora confere DOMMatrixReadOnly [scaleX,scaleY,
translateX,translateY]=[1,1,0,0]; controles não foram afrouxados. Teste reforça
pan real com setas até teto140px e arrasto pointer de40px; rerun pendente.
