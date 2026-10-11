// Gerado por scripts/build.mjs. Edite source/observatorio-v02.html e regenere.
// V0.5: Universo + Grafo de relações verificáveis; nenhuma operação de escrita.
const STYLE = ":host{display:block;min-width:0;width:100%;color-scheme:dark;--paper:#e6efff;--muted:#94a6c4;--gold:#ffd27c;--teal:#57efc5;--border:rgba(140,181,240,.19);--glass:rgba(9,19,41,.78)}\n.ob-wrap{position:relative;isolation:isolate;min-height:720px;width:100%;overflow:hidden}\n:host{color-scheme:dark;--paper:#e6efff;--muted:#94a6c4;--gold:#ffd27c;--teal:#57efc5;--border:rgba(140,181,240,.19);--glass:rgba(9,19,41,.78)}\n*{box-sizing:border-box}.ob-wrap{margin:0;min-height:100%;background:#050a16;color:var(--paper);font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif}button{font:inherit;color:inherit}button:focus-visible{outline:2px solid #79d5ff;outline-offset:4px}#starfield{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:.85}.ob-wrap:before{content:\"\";position:absolute;inset:0;background:radial-gradient(ellipse at 43% 34%,rgba(41,70,122,.24),transparent 53%),radial-gradient(ellipse at 90% 91%,rgba(75,32,112,.16),transparent 48%),linear-gradient(#050a16,#060c1c);pointer-events:none}.app{position:relative;z-index:1;min-height:720px;display:flex;flex-direction:column}.topbar{height:76px;display:flex;align-items:center;gap:20px;padding:0 28px;border-bottom:1px solid var(--border);background:rgba(4,10,23,.78);backdrop-filter:blur(18px)}.brand{display:flex;align-items:center;gap:12px;min-width:270px}.brand-logo{width:36px;height:36px;border:1px solid #569df6;border-radius:100%;display:grid;place-items:center;color:#a6dcff;box-shadow:0 0 23px #317ff15b;font-size:24px}.brand strong{display:block;letter-spacing:.22em;font-size:15px;font-weight:650}.brand small{display:block;margin-top:3px;letter-spacing:.18em;color:#7ba1cc;font-size:9px}.tabs{display:flex;align-items:center;gap:8px}.tab{border:1px solid transparent;background:none;padding:13px 15px;font-size:11px;letter-spacing:.11em;color:#92a8c6;border-radius:6px;cursor:pointer}.tab:hover,.tab.active{color:#f5e3b4;background:#c8a45c10;border-color:#d9ad4b35}.top-right{margin-left:auto;display:flex;align-items:center;gap:15px}.demo{font-size:10px;letter-spacing:.07em;color:#e6be83;padding:9px 11px;border-radius:999px;background:#78501a26;border:1px solid #e3b3644a;white-space:nowrap}.top-link{font-size:12px;border:1px solid var(--border);background:#0e1d36;border-radius:9px;padding:10px 12px;cursor:pointer}.main{display:grid;grid-template-columns:76px minmax(0,1fr) 315px;min-height:calc(100vh - 76px);flex:1}.rail{border-right:1px solid var(--border);background:rgba(5,12,26,.68);display:flex;flex-direction:column;align-items:center;padding:23px 0;gap:15px}.railbutton{border:1px solid transparent;background:transparent;border-radius:14px;width:45px;height:45px;cursor:pointer;color:#769abf;font-size:22px;display:grid;place-items:center}.railbutton:hover,.railbutton.active{background:#1934579c;color:#85d5ff;border-color:#5389bd5a}.rail-bottom{margin-top:auto;font-size:10px;writing-mode:vertical-rl;letter-spacing:.14em;color:#6584ab}.scene-column{min-width:0;position:relative;overflow:hidden}.scene-heading{position:absolute;z-index:8;top:28px;left:38px;right:34px;display:flex;align-items:flex-start;justify-content:space-between;gap:16px;pointer-events:none}.scene-heading h1{font-size:26px;letter-spacing:.025em;font-weight:550;margin:5px 0 6px}.scene-heading p{color:var(--muted);font-size:12px;margin:0;max-width:530px;line-height:1.55}.eyebrow{font-size:10px;color:#77c9e9;letter-spacing:.19em;text-transform:uppercase}.scene-actions{pointer-events:auto;display:flex;align-items:center;gap:6px}.smallbutton{min-width:35px;height:34px;padding:0 10px;border:1px solid var(--border);border-radius:9px;background:#13274499;color:#c6dbfa;cursor:pointer}.smallbutton:hover{background:#234770}.scene{height:calc(100vh - 76px);min-height:675px;position:relative;overflow:hidden}.scene:before{content:\"\";position:absolute;inset:0;background:radial-gradient(ellipse at 47% 55%,#1b34592a,transparent 51%);pointer-events:none}.universe{position:absolute;inset:0;display:grid;grid-template-columns:repeat(2,minmax(210px,1fr));gap:24px;align-content:center;padding:115px min(7vw,85px) 115px}.universe.hidden,.solar.hidden{display:none}.system-tile{position:relative;min-height:220px;border-radius:22px;background:linear-gradient(145deg,rgba(20,39,69,.68),rgba(8,17,37,.78));border:1px solid #7998c03a;text-align:left;cursor:pointer;overflow:hidden;padding:22px;transition:transform .25s,border-color .25s,box-shadow .25s}.system-tile:hover{transform:translateY(-3px);border-color:#b2d3ff77;box-shadow:0 12px 54px #05284955}.system-tile .system-name{position:absolute;z-index:2;left:23px;bottom:42px;font-size:15px;font-weight:650;letter-spacing:.08em}.system-tile .system-sub{position:absolute;z-index:2;left:23px;bottom:23px;font-size:11px;color:#8ba5c9}.system-tile svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.system-tile .sys-open{position:absolute;right:22px;bottom:22px;border:1px solid #699bcc4d;padding:6px 10px;border-radius:8px;color:#c2dbf5;font-size:11px}.solar{position:absolute;inset:0;transform-origin:center}.solar-background{position:absolute;inset:0}.orbit-layer{position:absolute;inset:0;overflow:visible;pointer-events:none}.orbit-layer ellipse{fill:none;stroke:rgba(151,175,221,.26);stroke-width:.9}.orbit-layer ellipse:nth-child(even){stroke:rgba(207,172,116,.19)}.sun{position:absolute;z-index:3;left:50%;top:53%;transform:translate(-50%,-50%);border:0;background:none;cursor:pointer;width:116px;height:116px}.sun-core{position:absolute;inset:15px;border-radius:100%;background:radial-gradient(circle at 39% 38%,#fff9d9 0%,#ffe1a0 12%,#ffb338 33%,#f28017 60%,#a7430c 86%);box-shadow:0 0 11px 4px #ffd08c,0 0 45px 9px #f0a1328a,0 0 120px 38px #ff8c1942;animation:sunPulse 5s ease-in-out infinite alternate}.sun-core:after{content:\"\";position:absolute;inset:-18px;border:1px solid #ffbc5b71;border-radius:50%;box-shadow:0 0 18px #ffad4170}.sun-label{position:absolute;top:118px;left:50%;transform:translateX(-50%);background:#101c2cdb;border:1px solid #eabb6c77;padding:9px 13px;border-radius:9px;font-size:11px;white-space:nowrap;letter-spacing:.13em;color:#ffe0ab}.sun-label small{display:block;font-size:9px;letter-spacing:.12em;color:#ad9e8b;padding-top:4px}.planet-slot{position:absolute;z-index:5;transform:translate(-50%,-50%);background:none;border:none;padding:0;cursor:pointer;min-width:70px;text-align:center}.planet-sphere{display:block;position:relative;margin:auto;width:var(--size,50px);height:var(--size,50px);border-radius:50%;background:radial-gradient(circle at 28% 23%,#ffffff90,transparent 18%),radial-gradient(circle at 66% 66%,#000b22a8,transparent 66%),radial-gradient(ellipse at 30% 30%,var(--light),var(--mid) 51%,var(--dark) 90%);box-shadow:inset -11px -10px 18px #050718bc,0 0 20px var(--glow),0 0 40px color-mix(in srgb,var(--glow) 25%,transparent);transition:filter .25s,transform .25s}.planet-sphere:after{content:\"\";position:absolute;inset:4px;border:1px dashed #ffffff4b;border-radius:50%;transform:rotate(-23deg);opacity:.45}.planet-slot:hover .planet-sphere,.planet-slot.selected .planet-sphere{transform:scale(1.14);filter:brightness(1.25)}.planet-ring{position:absolute;left:50%;top:50%;width:calc(var(--size,50px) * 1.5);height:calc(var(--size,50px) * .48);border:2px solid var(--ring,#8bcaf4);border-radius:50%;transform:translate(-50%,-50%) rotate(-24deg);box-shadow:0 0 13px var(--glow);opacity:.8;pointer-events:none}.planet-label{display:block;font-size:10px;font-weight:650;letter-spacing:.11em;color:#e4efff;background:#0a1526dc;border:1px solid #50688970;border-radius:7px;margin:11px auto 0;padding:7px 9px;white-space:nowrap;box-shadow:0 7px 18px #03070d99}.planet-status{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:7px;box-shadow:0 0 8px currentColor;background:currentColor;color:var(--status-color)}.scene-bottom{position:absolute;z-index:9;bottom:24px;left:30px;right:30px;display:flex;flex-direction:column;align-items:flex-start;gap:12px;pointer-events:none}.solar-note{position:static;font-size:11px;color:#6d8aaf;border:1px solid #2d48655b;background:#06132691;border-radius:10px;padding:10px 13px;max-width:min(100%,280px)}.solar-note.hidden{display:none}.metrics{position:static;width:100%;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid var(--border);background:#091527da;backdrop-filter:blur(14px);border-radius:13px;overflow:hidden}.metric{padding:15px 18px;border-right:1px solid var(--border)}.metric:last-child{border:0}.metric small{display:block;color:#7893b9;letter-spacing:.11em;font-size:9px}.metric strong{display:block;font-size:20px;margin-top:6px;font-weight:550}.metric span{font-size:10px;color:#8ba6c8}.rightpanel{border-left:1px solid var(--border);background:linear-gradient(180deg,#0b172de8,#071121f2);padding:25px 22px;position:relative;min-width:0}.panel-top{display:flex;justify-content:space-between;align-items:center;gap:10px}.panel-kicker{font-size:10px;letter-spacing:.17em;color:#89accf}.panel-icon{color:#6fcad7;font-size:19px}.agent-hero{margin:25px 0 21px;height:180px;border:1px solid #45668d55;border-radius:14px;position:relative;display:flex;align-items:center;justify-content:center;overflow:hidden;background:radial-gradient(circle at center,#23446e66,transparent 60%),linear-gradient(160deg,#10213c,#081329)}.agent-hero:before,.agent-hero:after{content:\"\";position:absolute;border:1px solid #5684af66;border-radius:50%;width:240px;height:78px;transform:rotate(-24deg)}.agent-hero:after{width:204px;height:143px;opacity:.3}.hero-planet{width:117px;height:117px;border-radius:50%;background:radial-gradient(circle at 31% 25%,#ffffffae,transparent 13%),radial-gradient(circle at 65% 72%,#000617cc,transparent 65%),radial-gradient(circle at 30% 26%,var(--hero-light,#95e7ff),var(--hero-mid,#296ba3) 60%,var(--hero-dark,#121e4e));box-shadow:inset -20px -13px 24px #020a1bd4,0 0 45px var(--hero-glow,#387aba9c);z-index:1}.agent-name{font-size:23px;letter-spacing:.04em;margin:0 0 3px}.agent-role{font-size:12px;color:#92a9cb;margin:0 0 13px}.status-pill{display:inline-flex;align-items:center;gap:7px;font-size:10px;color:#bdd8cc;background:#1b3f3a80;padding:6px 9px;border-radius:8px;border:1px solid #5d8c8077}.status-pill:before{content:\"\";background:var(--pill,#57efc5);width:7px;height:7px;border-radius:50%;box-shadow:0 0 9px var(--pill,#57efc5)}.section{border-top:1px solid #5e759d36;margin-top:24px;padding-top:19px}.section h3{margin:0 0 12px;font-size:10px;letter-spacing:.17em;font-weight:650;color:#87a8d3;text-transform:uppercase}.panel-text{font-size:12px;line-height:1.65;color:#c7d4e9;margin:0}.task-row{display:flex;gap:9px;align-items:flex-start;margin:11px 0;font-size:11px;color:#bcd0ea}.agent-list-item{display:flex;align-items:flex-start;gap:9px;margin:7px 0;width:100%;background:transparent;border:1px solid transparent;border-radius:7px;text-align:left;padding:8px 6px;color:#bcd0ea;font-size:11px;cursor:pointer}.agent-list-item:hover{background:#1936597a;border-color:#4274a16b}.task-dot{width:7px;height:7px;flex:0 0 auto;border-radius:50%;background:#5cbfd3;margin-top:5px;box-shadow:0 0 8px #47d7eb88}.subtle{color:#819cbd;font-size:11px}.panel-button{width:100%;margin-top:25px;padding:12px 14px;text-align:center;background:linear-gradient(110deg,#214771,#163451);border:1px solid #6ebdf27a;border-radius:10px;cursor:pointer;color:#dff6ff;font-size:12px}.panel-button:hover{background:#245a8b}.notice{font-size:10px;line-height:1.55;color:#9cafd0;margin-top:23px;padding:12px;background:#071f3299;border:1px dashed #4b779568;border-radius:9px}.empty{padding-top:27px;color:#cbdcf5}.empty h2{font-size:20px;font-weight:500}.empty p{font-size:12px;line-height:1.65;color:#91aace}.legend{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:16px}.legend span{font-size:10px;background:#1a2a409e;border:1px solid #3c5c7b55;border-radius:6px;padding:5px 8px;color:#9eb6d8}.backbutton{background:none;border:0;color:#85cdf8;font-size:11px;letter-spacing:.04em;padding:0;cursor:pointer}.backbutton:hover{text-decoration:underline}@keyframes sunPulse{from{filter:brightness(.9)}to{filter:brightness(1.15)}}@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}}@media(max-width:1130px){.main{grid-template-columns:58px minmax(0,1fr) 275px}.brand{min-width:200px}.topbar{padding:0 17px}.tabs .tab{padding:10px}.rightpanel{padding:20px 15px}.universe{padding:115px 28px 110px}.scene-heading{left:25px;right:20px}}@media(max-width:870px){.topbar{height:66px}.brand{min-width:auto}.brand small,.tabs{display:none}.main{grid-template-columns:51px minmax(0,1fr);min-height:calc(100vh - 66px)}.rail{padding:14px 0}.rightpanel{grid-column:2;grid-row:2;border-top:1px solid var(--border);border-left:none;min-height:240px}.scene{height:650px;min-height:650px}.agent-hero{display:none}.scene-bottom{bottom:18px}.demo{font-size:9px}.scene-heading h1{font-size:22px}.universe{gap:13px;padding:130px 20px 110px}.system-tile{min-height:175px}}@media(max-width:580px){.topbar{gap:7px;padding:0 13px}.brand strong{font-size:12px}.brand-logo{width:29px;height:29px;font-size:19px}.top-link{padding:7px;font-size:10px}.demo{max-width:132px;white-space:normal;text-align:center}.universe{grid-template-columns:1fr;padding:128px 16px 120px;gap:11px;overflow:auto;align-content:start}.system-tile{min-height:142px}.scene-heading{top:20px;left:19px;right:12px}.scene-heading p{font-size:10px}.scene-actions{flex-direction:column}.scene{height:710px;min-height:710px}.scene-bottom{left:9px;right:9px}.metric{padding:11px 8px}.metric small{font-size:8px}.metric strong{font-size:18px}.solar-note{display:none}.planet-label{display:none}.sun-label{font-size:9px;padding:7px 9px}}\n#cosmos-3d{position:absolute;z-index:2;inset:0;width:100%;height:100%;cursor:grab;touch-action:pan-y}#cosmos-3d:active{cursor:grabbing}.webgl .orbit-layer{opacity:0}.webgl .sun-core,.webgl .planet-sphere,.webgl .planet-ring{opacity:0;pointer-events:none}.webgl .planet-slot{z-index:6;transform:translate(-50%,-34%)}.webgl .sun{z-index:6}.webgl .sun-core{opacity:0}.webgl .planet-slot:hover .planet-label,.webgl .planet-slot.selected .planet-label{border-color:#c4d9ff;color:white;background:#122b4dee;box-shadow:0 0 18px #428cf966}.webgl .solar-background:after{content:\"\";position:absolute;z-index:1;left:50%;top:50%;width:25%;height:26%;transform:translate(-50%,-50%);border-radius:50%;pointer-events:none;background:radial-gradient(circle,#ffae273b,transparent 70%);filter:blur(25px)}.scene-actions{flex-wrap:wrap;justify-content:end}.scene-actions #mode-3d{min-width:70px;font-size:10px;color:#9feaf2;border-color:#54b7ca5e}.webgl .planet-slot .planet-label{margin-top:15px}@media(max-width:600px){.scene-actions #mode-3d{min-width:54px}}\n\n/* V0.4: movimento astronomico progressivo, acessivel e puramente demonstrativo. */\n@keyframes obStarDrift{0%,100%{transform:scale(1.015) translate3d(0,0,0)}50%{transform:scale(1.035) translate3d(-4px,3px,0)}}\n@keyframes obOrbitFlow{to{stroke-dashoffset:-480}}\n@keyframes obSignalPulse{0%,100%{opacity:.45;box-shadow:0 0 6px currentColor}50%{opacity:1;box-shadow:0 0 19px currentColor}}\n@keyframes obActiveAura{0%,100%{opacity:.18;transform:scale(.91)}50%{opacity:.48;transform:scale(1.07)}}\n@keyframes obOrbitShimmer{0%,100%{opacity:.35}50%{opacity:.79}}\n#starfield{animation:obStarDrift 48s ease-in-out infinite;transform-origin:center}\n.system-tile .sys-orbits{overflow:visible}.system-tile .sys-orbits .orbit-stream{fill:none;stroke-width:2;stroke-linecap:round;stroke-dasharray:11 469;stroke-dashoffset:0;opacity:.55;animation:obOrbitFlow 70s linear infinite}\n.system-tile .sys-orbits circle{filter:drop-shadow(0 0 5px currentColor)}\n.system-tile .system-activity{position:absolute;z-index:3;top:16px;right:18px;padding:5px 8px;font-size:9px;letter-spacing:.06em;border:1px solid rgba(106,171,222,.3);border-radius:8px;background:rgba(5,15,34,.85);color:#acc8e7}\n.system-tile[data-activity=\"active\"]{border-color:rgba(88,230,201,.53)}\n.system-tile[data-activity=\"active\"] .orbit-stream{animation-duration:12s;opacity:.85}\n.system-tile[data-activity=\"attention\"]{border-color:rgba(255,196,110,.65)}\n.system-tile[data-activity=\"attention\"] .orbit-stream{animation-duration:8s;opacity:1}\n.system-tile[data-activity=\"error\"]{border-color:rgba(255,117,128,.6)}\n.system-tile[data-activity=\"error\"] .orbit-stream{animation-duration:22s;opacity:.9}\n.system-tile[data-activity]:not([data-activity=\"idle\"]):before{content:\"\";position:absolute;z-index:1;left:21%;top:17%;width:60%;height:56%;border-radius:50%;pointer-events:none;background:radial-gradient(circle,rgba(83,199,248,.20),transparent 70%);animation:obActiveAura 3.2s ease-in-out infinite}\n.system-tile[data-activity=\"attention\"]:before{background:radial-gradient(circle,rgba(255,188,91,.24),transparent 70%)}\n.system-tile[data-activity=\"error\"]:before{background:radial-gradient(circle,rgba(250,95,120,.24),transparent 70%)}\n.system-tile[data-activity=\"active\"] .system-activity{color:#82f4d1}\n.system-tile[data-activity=\"attention\"] .system-activity{color:#ffd18f}\n.system-tile[data-activity=\"error\"] .system-activity{color:#ffaab1}\n.visual-switch{color:#aedbea;border-color:rgba(94,172,207,.38);white-space:nowrap}\n.visual-switch:hover{border-color:#80dce0}\n.planet-slot .planet-label{transition:border-color .3s,box-shadow .3s}\n.planet-slot[data-activity=\"active\"] .planet-label{color:#e7fff8;border-color:#4bdeae;animation:obOrbitShimmer 2.4s ease-in-out infinite}\n.planet-slot[data-activity=\"attention\"] .planet-label{color:#fff0d2;border-color:#f1b36f;animation:obOrbitShimmer 1.6s ease-in-out infinite}\n.planet-slot[data-activity=\"error\"] .planet-label{color:#ffe1e5;border-color:#e98b9f}\n.planet-slot[data-activity=\"active\"] .planet-status{color:#64f0ca;animation:obSignalPulse 2.3s ease-in-out infinite}\n.planet-slot[data-activity=\"attention\"] .planet-status{color:#ffd182;animation:obSignalPulse 1.7s ease-in-out infinite}\n.planet-slot[data-activity=\"error\"] .planet-status{color:#ff9aab}\n.planet-activity{position:absolute;z-index:7;left:calc(50% + 33px);top:-10px;background:rgba(8,24,42,.95);border:1px solid rgba(100,218,215,.5);border-radius:999px;font-size:9px;line-height:1.3;white-space:nowrap;padding:4px 7px;color:#b8f9f4;pointer-events:none}\n.planet-slot[data-activity=\"attention\"] .planet-activity{border-color:#eac17d;color:#ffe1ac}\n@media(max-width:1130px){.visual-switch{font-size:10px;padding:8px}}\n@media(max-width:870px){.visual-switch{max-width:120px;overflow:hidden;text-overflow:ellipsis}.system-tile .system-activity{top:9px;right:9px}}\n@media(max-width:580px){.visual-switch{font-size:9px;max-width:105px}.system-tile .system-activity{font-size:8px}.planet-activity{display:none}}\n@media(prefers-reduced-motion:reduce){#starfield,.system-tile .sys-orbits .orbit-stream,.system-tile:before,.planet-slot .planet-label,.planet-slot .planet-status{animation:none!important}}\n\n/* V0.4.2: lua realmente consultada. Não identifica agente ou resultado. */\n.real-mission-lua.hidden{display:none}\n.real-mission-lua{position:absolute;z-index:18;left:70%;top:62%;transform:translate(-50%,-50%);border:1px solid #87dcf6;border-radius:22px;background:linear-gradient(145deg,#10375bcf,#06182be6);box-shadow:0 0 27px #4dc2f67a;padding:11px 14px;display:flex;align-items:center;gap:10px;cursor:pointer;color:#effaff;font-size:11px;max-width:220px;text-align:left}\n.real-mission-lua .lua-globo{width:30px;height:30px;flex:none;border-radius:50%;background:radial-gradient(circle at 29% 27%,#fff,#83d5f0 44%,#123d68 90%);box-shadow:0 0 21px #8adbf5aa}\n.real-mission-lua .lua-desc{display:grid;gap:3px;line-height:1.4}\n.real-mission-lua small{font-size:10px;color:#b7d9eb}\n.real-mission-lua:focus-visible{outline:2px solid white}\n@media(max-width:720px){.real-mission-lua{left:65%;top:68%;max-width:150px;font-size:10px;padding:7px}.real-mission-lua .lua-globo{width:23px;height:23px}}\n\n/* V0.5 — grafo de operação. Nós ilustrativos jamais se confundem com dados de origem. */\n.graph{position:absolute;inset:0;overflow:hidden}\n.graph.hidden{display:none}\n.graph-tools{position:absolute;z-index:7;top:128px;left:30px;right:30px;display:flex;align-items:center;flex-wrap:wrap;gap:12px;padding:11px 13px;background:#0b1d35e8;border:1px solid #3b5d8099;border-radius:13px;backdrop-filter:blur(16px)}\n.graph-tools label{display:flex;gap:8px;align-items:center;font-size:11px;color:#c2d8ee}\n.graph-tools select,.graph-tools input{border:1px solid #4c6b90;border-radius:8px;background:#0d223b;color:#e4f3ff;padding:8px;max-width:220px;font:inherit;font-size:12px}\n.graph-tools input{width:180px}\n.graph-map{position:absolute;z-index:1;top:190px;left:20px;right:20px;bottom:145px;border:1px solid #264a6b66;border-radius:18px;overflow:hidden;background:radial-gradient(ellipse at 28% 46%,#27639029,transparent 40%),radial-gradient(ellipse at 76% 44%,#235d5a21,transparent 42%),#06132378}\n.graph-map:before{content:\"\";position:absolute;inset:0;pointer-events:none;opacity:.23;background-image:linear-gradient(#5583ad32 1px,transparent 1px),linear-gradient(90deg,#5583ad32 1px,transparent 1px);background-size:40px 40px}\n.graph-surface{position:absolute;inset:0;transform-origin:center;transition:transform .2s ease}\n.graph-edges{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}\n.graph-edges line{stroke-width:2;stroke:#6688b790;vector-effect:non-scaling-stroke}\n.graph-edges line[data-kind=\"verified\"]{stroke:#55efcc;stroke-width:3}\n.graph-edges line[data-kind=\"manual\"]{stroke:#f6c575;stroke-dasharray:6 8}\n.graph-edges line.dimmed{opacity:.25}\n.graph-node{position:absolute;z-index:2;transform:translate(-50%,-50%);width:clamp(102px,11vw,152px);min-height:64px;padding:10px 9px;background:#102845f0;border:1px solid #678aaf;color:#f1f7ff;box-shadow:0 10px 30px #040e1b99,0 0 16px #3e7caa33;border-radius:14px;cursor:pointer;text-align:center;display:grid;align-content:center;gap:4px;line-height:1.25;overflow-wrap:anywhere}\n.graph-node strong{font-size:12px;line-height:1.3}\n.graph-node small{font-size:9px;letter-spacing:.08em;color:#9bb3cb}\n.graph-node[data-kind=\"demo\"]{border-style:dashed;border-color:#72869e9c;background:#12243bc7}\n.graph-node[data-kind=\"demo-hub\"]{background:#1b2940ee;border-color:#9eaaaf}\n.graph-node[data-kind=\"verified\"]{border-color:#5bdfc1;background:#113e44e8;box-shadow:0 0 25px #32b8a438}\n.graph-node[data-kind=\"manual\"]{border-color:#e5b768;border-style:dashed;background:#373022d9}\n.graph-node.selected,.graph-node:hover{outline:2px solid #d0f7ff;outline-offset:3px}\n.graph-node.dimmed{opacity:.45}\n.graph-empty{position:absolute;z-index:3;left:50%;top:50%;transform:translate(-50%,-50%);text-align:center;max-width:360px;color:#d0e2f4;background:#0b1f36ed;border:1px solid #5f7f9d;padding:22px;border-radius:14px;line-height:1.7;font-size:12px}\n.graph-legend{position:absolute;z-index:4;bottom:156px;left:32px;right:32px;display:flex;flex-wrap:wrap;gap:14px;font-size:10px;color:#a6bed9;pointer-events:none}\n.graph-legend span:before{content:\"\";display:inline-block;width:10px;height:10px;border:1px solid #72869e;background:#12243b;border-radius:50%;margin-right:6px}\n.graph-legend .real:before{background:#55efcc;border-color:#55efcc}\n.graph-legend .manual:before{background:#f6c575;border-color:#f6c575}\n@media(max-width:870px){.graph-tools{top:110px;left:16px;right:16px}.graph-map{top:188px;left:8px;right:8px}.graph-node{width:115px;min-height:61px;padding:8px 5px}.graph-node strong{font-size:10px}.graph-node small{font-size:8px}.graph-legend{left:16px;right:16px}}\n@media(max-width:580px){.graph-tools{top:102px;gap:7px;padding:8px}.graph-tools input{width:120px}.graph-tools label{font-size:10px}.graph-tools select,.graph-tools input{padding:6px;font-size:10px}.graph-map{top:198px;bottom:128px}.graph-node{width:92px;min-height:52px;padding:6px 3px}.graph-node strong{font-size:9px}.graph-node small{font-size:7px}.graph-legend{bottom:139px;gap:8px;font-size:9px}}\n@media(prefers-reduced-motion:reduce){.graph-surface{transition:none}}\n\n.graph-tools button{font:inherit;font-size:11px;color:#dcf9ff;background:#154561;border:1px solid #67bddb;border-radius:8px;padding:8px 10px;cursor:pointer}\n.graph-tools button:hover{background:#215d7b}\n@media(max-width:580px){.graph-tools button{padding:6px;font-size:10px}}";
const MARKUP = "<canvas id=\"starfield\" aria-hidden=\"true\"></canvas>\n<div class=\"app\">\n  <header class=\"topbar\"><div class=\"brand\"><div class=\"brand-logo\" aria-hidden=\"true\">◉</div><div><strong>OBSERVATÓRIO</strong><small>UNIVERSO DE AGENTES</small></div></div><nav class=\"tabs\" aria-label=\"Navegação principal\"><button class=\"tab active\" id=\"top-universe\">UNIVERSO</button><button class=\"tab\" id=\"top-project\">SISTEMA SOLAR</button><button class=\"tab\" id=\"top-graph\" type=\"button\">GRAFO</button></nav><div class=\"top-right\"><button class=\"top-link visual-switch\" id=\"visual-demo\" type=\"button\" title=\"Alternar entre cenários visuais simulados\" aria-label=\"Cenário visual de demonstração: calmo\">SIMULAR: CALMO</button><span class=\"demo\" id=\"source-banner\">◌ PROTÓTIPO · DADOS ILUSTRATIVOS</span><button class=\"top-link\" id=\"info-button\" title=\"Sobre o protótipo\">ⓘ Sobre</button></div></header>\n  <div class=\"main\"><aside class=\"rail\" aria-label=\"Navegação lateral\"><button class=\"railbutton active\" id=\"rail-universe\" aria-label=\"Universo\" title=\"Universo\">✦</button><button class=\"railbutton\" id=\"rail-system\" aria-label=\"Sistema solar\" title=\"Sistema solar\">◎</button><button class=\"railbutton\" id=\"rail-graph\" aria-label=\"Grafo operacional\" title=\"Grafo operacional\">⌘</button><div class=\"rail-bottom\">CONCEITO V.01</div></aside>\n    <main class=\"scene-column\"><div class=\"scene-heading\"><div><span class=\"eyebrow\" id=\"breadcrumb\">NÍVEL 01 / UNIVERSO CENTRAL</span><h1 id=\"scene-title\">Sua galáxia de operações</h1><p id=\"scene-description\">Cada sistema solar representa um projeto. Entre em um deles para explorar seus agentes e tarefas.</p></div><div class=\"scene-actions\"><button class=\"smallbutton\" id=\"mode-3d\" type=\"button\" aria-pressed=\"false\" title=\"Alternar modo 3D ou 2D\">3D</button><button class=\"smallbutton\" id=\"zoom-out\" title=\"Reduzir zoom\" aria-label=\"Reduzir zoom\">−</button><button class=\"smallbutton\" id=\"zoom-reset\" title=\"Restaurar zoom\" aria-label=\"Restaurar zoom\">⌖</button><button class=\"smallbutton\" id=\"zoom-in\" title=\"Ampliar zoom\" aria-label=\"Ampliar zoom\">+</button></div></div>\n    <div class=\"scene\" id=\"scene\"><div class=\"universe\" id=\"universe\" role=\"region\" aria-label=\"Projetos disponíveis\"></div><div class=\"graph hidden\" id=\"graph\" role=\"region\" aria-label=\"Grafo operacional multiprojeto\">\n  <div class=\"graph-tools\"><label>Exibir <select id=\"graph-scope\" aria-label=\"Filtrar nós por origem\"><option value=\"all\">Todos</option><option value=\"verified\">Consulta real</option><option value=\"demo\">Exemplos</option></select></label><label>Buscar <input id=\"graph-search\" type=\"search\" placeholder=\"Projeto ou missão\" autocomplete=\"off\" aria-label=\"Buscar nós no grafo\"></label><button type=\"button\" id=\"graph-open-read\" title=\"Consultar uma conversa real do OpenHands\">☾ Consultar missão</button></div>\n  <div class=\"graph-map\" id=\"graph-map\" aria-label=\"Nós e conexões entre projetos e execuções\"><div class=\"graph-surface\" id=\"graph-surface\"></div></div>\n  <div class=\"graph-legend\"><span class=\"real\">Origem confirmada</span><span class=\"manual\">Associação manual (não atestada)</span><span>Somente demonstração</span></div>\n</div><div class=\"solar hidden\" id=\"solar\" role=\"region\" aria-label=\"Sistema solar de agentes\"><div class=\"solar-background\" id=\"solar-stage\"><svg class=\"orbit-layer\" id=\"orbits\" aria-hidden=\"true\"></svg><button class=\"sun\" id=\"sun\" title=\"Visão geral do sistema\"><span class=\"sun-core\"></span><span class=\"sun-label\" id=\"sun-label\">NÚCLEO<small>COORDENAÇÃO</small></span></button><div id=\"planets\"></div><button type=\"button\" class=\"real-mission-lua hidden\" id=\"real-lua\" aria-label=\"Abrir dados verificados da missão\"><span class=\"lua-globo\" aria-hidden=\"true\"></span><span class=\"lua-desc\"><strong>MISSÃO REAL</strong><small id=\"real-lua-state\">Estado consultado</small></span></button></div></div><div class=\"scene-bottom\"><div class=\"solar-note hidden\" id=\"solar-note\">● Planetas = agentes propostos &nbsp; ● Luas/tarefas = representação conceitual</div><footer class=\"metrics\" id=\"metrics\"><div class=\"metric\"><small>PROJETOS</small><strong>04</strong><span>Ambientes conceituais</span></div><div class=\"metric\"><small>ESTRUTURA</small><strong>Multiuniverso</strong><span>Um sistema por projeto</span></div><div class=\"metric\"><small>CONEXÃO REAL</small><strong>Não ativa</strong><span>Interface demonstrativa</span></div></footer></div></div></main>\n    <aside class=\"rightpanel\" id=\"rightpanel\" aria-live=\"polite\"><div class=\"panel-top\"><span class=\"panel-kicker\">PAINEL DE INSPEÇÃO</span><span class=\"panel-icon\">◎</span></div><div id=\"panel-content\"></div></aside>\n  </div>\n</div>";

const REAL_STYLE = `
.ob-real{position:absolute;z-index:14;top:114px;right:18px;width:min(310px,calc(100% - 36px));background:#08172eee;color:#e3f2ff;border:1px solid #568eab;border-radius:12px;font-size:12px}
.ob-real summary{padding:12px;cursor:pointer;font-weight:bold;color:#a9eeff}
.ob-real .form{padding:0 12px 12px;display:grid;gap:8px}
.ob-real label{display:grid;gap:4px}
.ob-real input{width:100%;min-width:0;background:#10223b;color:white;border:1px solid #537ca3;padding:8px;border-radius:6px}
.ob-real button{padding:8px;border:1px solid #7bd5ef;background:#174564;color:white;border-radius:6px;cursor:pointer}
.ob-real output{display:grid;gap:5px;overflow-wrap:anywhere}
.ob-real output p{margin:0;line-height:1.4}
.graph-active .ob-real:not([open]){display:none}
.graph-active .ob-real[open]{top:210px;right:18px;max-height:calc(100% - 230px);overflow:auto}
.ob-real .moon{display:inline-block;width:15px;height:15px;border-radius:50%;background:radial-gradient(circle at 30% 30%,white,#77d5f3,#23506c);box-shadow:0 0 12px #8edafa}
`;
function mountRealRead(stage,host,onVerified) {
  const scene=stage.querySelector('.scene-column');
  if(!scene)return ()=>{};
  const sheet=document.createElement('style');sheet.textContent=REAL_STYLE;stage.append(sheet);
  const detail=document.createElement('details');detail.className='ob-real';
  detail.innerHTML=`<summary>☾ CONSULTA DE MISSÃO REAL</summary><div class="form">
    <label>ID da conversa OpenHands<input class="id" placeholder="UUID" autocomplete="off"></label>
    <label>Projeto associado pelo operador<input class="project" value="OARANHA/observatorio-agents-openhands" autocomplete="off"></label>
    <button type="button">Consultar estado no OpenHands</button><output aria-live="polite"></output></div>`;
  scene.append(detail);
  const get=s=>detail.querySelector(s), button=get('button'), output=get('output');
  const say=(label,value)=>{const p=document.createElement('p');p.textContent=label+value;output.append(p);};
  let active=true;
  button.addEventListener('click',async()=>{
    const id=get('.id').value.trim().toLowerCase();
    const project=get('.project').value.trim();
    output.replaceChildren();
    if(!/^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(id)){say('Erro: ','UUID inválido');return;}
    if(!/^[A-Za-z0-9._-]+\/[A-Za-z0-9._-]+$/.test(project)){say('Erro: ','projeto inválido');return;}
    if(!host?.agentServer?.request){say('Indisponível: ','API de leitura do Canvas ausente');return;}
    button.disabled=true;say('Consulta: ','em andamento');
    try {
      const item=await host.agentServer.request({method:'GET',path:'/api/conversations/'+id});
      if(!active)return;
      output.replaceChildren();
      if(!item||item.id!==id||typeof item.execution_status!=='string'){say('Erro: ','contrato não confirmado');return;}
      const moon=document.createElement('span');moon.className='moon';moon.setAttribute('aria-label','Lua: execução real verificada');output.append(moon);
      say('Conversa: ',id);
      say('Estado recebido: ',item.execution_status);
      say('Projeto declarado: ',project);
      say('Origem: ','OpenHands Agent Server');
      if(typeof item.updated_at==='string')say('Atualizado no servidor: ',item.updated_at);
      say('Observado em (hora do navegador): ',new Date().toISOString());
      say('Associação de projeto: ','manual, não atestada pela API');
      onVerified({conversationId:id,status:item.execution_status,project,updatedAt:typeof item.updated_at==='string'?item.updated_at:null,observedAt:new Date().toISOString()});
      detail.open=false; // Não encobrir o universo após consulta; reabrível pelo operador.
    } catch (_error) {
      if(active){output.replaceChildren();say('Consulta: ','indisponível/não autorizada; estado desconhecido');}
    } finally {if(active)button.disabled=false;}
  });
  return ()=>{active=false;detail.remove();sheet.remove();};
}


function mountObservatorio({container,host}) {
  const wrapper=document.createElement('section');
  wrapper.className='ob-wrap';
  wrapper.setAttribute('aria-label','Observatório de Agentes — Universo e Grafo');
  const shadow=wrapper.attachShadow({mode:'open'});
  const style=document.createElement('style');
  style.textContent=STYLE;
  shadow.append(style);
  const stage=document.createElement('div');
  stage.className='ob-wrap';
  stage.innerHTML=MARKUP;
  shadow.append(stage);
  container.append(wrapper);
  let destroyed=false,rafId=0;
  const disposeRead=mountRealRead(stage,host,observation=>applyVerifiedMission(observation));
  const resizeCallbacks=[];
  const resize=()=>{if(destroyed)return;for(const cb of resizeCallbacks)cb();};
  const observer=typeof ResizeObserver==='function'?new ResizeObserver(resize):null;
  if(observer)observer.observe(wrapper);
  else window.addEventListener('resize',resize);
  // Código visual herdado da V0.2, agora isolado no mount.
'use strict';
const defs={
 vigiafast:{name:'VIGIAFAST',subtitle:'Inteligência reputacional',core:'VIGIA CORE',color:'#57c9fa',sun:['#fff2bb','#ffbf61','#b65f23'],agents:[
  {name:'SENTINELA',role:'Descoberta de menções',color:'#47d3ed',spectrum:['#a3faff','#2588b4','#0b3251'],orbit:1,angle:-2.6,description:'Descoberta planejada de menções públicas permitidas, observando limites de cada rede social.',tasks:['Verificar fontes públicas autorizadas','Registrar origem e contexto'],state:'Simulação: disponível'},
  {name:'ECHO',role:'Contexto e conversas',color:'#7298ff',spectrum:['#c9baff','#6961ca','#26315b'],orbit:2,angle:-2.3,description:'Agrupamento conceitual de conteúdos, comentários e conversas.',tasks:['Relacionar discussões','Manter referências de origem'],state:'Simulação: executando'},
  {name:'ATLAS',role:'Análise contextual',color:'#ba80ff',spectrum:['#efd5ff','#925be3','#321c62'],orbit:2,angle:-.23,description:'Interpretação contextual em português brasileiro, com revisão humana para casos sensíveis.',tasks:['Analisar menções','Identificar ambiguidades'],state:'Simulação: disponível'},
  {name:'ARES',role:'Sinais e risco',color:'#ff956c',spectrum:['#ffd0a6','#d65333','#742324'],orbit:3,angle:-.7,description:'Triagem de possíveis riscos e anomalias. Não substitui julgamento humano.',tasks:['Priorizar sinais de atenção'],state:'Simulação: atenção'},
  {name:'LEX',role:'Compliance e governança',color:'#c1ccde',spectrum:['#ffffff','#8b98b9','#35415b'],orbit:3,angle:2.2,description:'Verificações de conformidade e encaminhamento à revisão humana.',tasks:['Solicitar revisão quando necessário'],state:'Simulação: aguardando revisão'},
  {name:'ARQUIVUS',role:'Evidências e arquivos',color:'#59c4d9',spectrum:['#d8fdff','#4a93b0','#1a4866'],orbit:4,angle:2.6,description:'Preservação de evidências com origem, horários e integridade verificável.',tasks:['Organizar itens evidenciais'],state:'Simulação: disponível'},
  {name:'AURORA',role:'Alertas operacionais',color:'#6deca9',spectrum:['#d8ffe5','#55b69a','#145a68'],orbit:4,angle:-1.1,description:'Comunicação de alertas às equipes autorizadas.',tasks:['Encaminhar alertas revisados'],state:'Simulação: disponível'},
  {name:'ÓRBITA',role:'Relatórios',color:'#87b9ff',spectrum:['#eaf4ff','#6095c7','#203c67'],orbit:4,angle:.55,description:'Síntese de histórico, ocorrências e métricas por cliente.',tasks:['Consolidar relatórios de demonstração'],state:'Simulação: disponível'}
 ]},
 wandora:{name:'WANDORA',subtitle:'Orquestração e colaboração',core:'WANDORA CORE',color:'#ae91ff',sun:['#fff1dd','#f7b67f','#aa67af'],agents:[
 {name:'FELIX',role:'Assistente digital',color:'#9af59e',spectrum:['#e6ffd8','#79c577','#1a5751'],orbit:1,angle:-2.3,description:'Representação visual conceitual de um agente de atendimento.',tasks:['Fluxo demonstrativo de atendimento'],state:'Simulação: disponível'},
 {name:'WU',role:'Operações',color:'#8bc5ff',spectrum:['#e7f2ff','#649ed9','#254e8a'],orbit:2,angle:0,description:'Representação visual conceitual de apoio operacional.',tasks:['Rotinas demonstrativas'],state:'Simulação: executando'},
 {name:'AURORA',role:'Comunicação',color:'#df9aff',spectrum:['#ffe7fb','#a86acb','#5c2a72'],orbit:3,angle:2.25,description:'Representação visual conceitual de comunicação.',tasks:['Acompanhamento demonstrativo'],state:'Simulação: disponível'}
 ]},
 elus:{name:'ELUS',subtitle:'Relacionamento e operações comerciais',core:'ELUS CORE',color:'#69caff',sun:['#fff1dd','#9dcaff','#486bba'],agents:[
 {name:'ATENDIMENTO',role:'Função proposta',color:'#7dc8ff',spectrum:['#e7f8ff','#699fda','#244882'],orbit:1,angle:-2.2,description:'Possível módulo futuro de apoio ao atendimento do CRM.',tasks:['Exemplo de fila de contato'],state:'Conceito: não implantado'},
 {name:'RELACIONAMENTO',role:'Função proposta',color:'#7de0d3',spectrum:['#dcfff9','#6abeb5','#1d6564'],orbit:2,angle:.23,description:'Possível visão de relacionamento com clientes.',tasks:['Exemplo de acompanhamento'],state:'Conceito: não implantado'},
 {name:'RELATÓRIOS',role:'Função proposta',color:'#bfa7ff',spectrum:['#f4ddff','#a68ed3','#45306a'],orbit:3,angle:2.2,description:'Possível síntese de indicadores operacionais.',tasks:['Exemplo de resumo comercial'],state:'Conceito: não implantado'}
 ]},
 openhands:{name:'OPENHANDS LAB',subtitle:'Desenvolvimento e experimentos',core:'MESH LAB',color:'#ffbe78',sun:['#fff6d9','#fec872','#bd632e'],agents:[
 {name:'CODER',role:'Desenvolvimento',color:'#73d9eb',spectrum:['#d4fdff','#59b8d8','#225071'],orbit:1,angle:-2.5,description:'Posição visual proposta para tarefas de engenharia OpenHands.',tasks:['Exemplo: analisar alterações'],state:'Simulação: disponível'},
 {name:'QA',role:'Testes',color:'#b99bff',spectrum:['#efddff','#9983cb','#3a2a68'],orbit:2,angle:-.15,description:'Posição visual proposta para testes e verificações.',tasks:['Exemplo: testar hipótese'],state:'Simulação: disponível'},
 {name:'DOCUMENTAÇÃO',role:'Memória técnica',color:'#8ceab7',spectrum:['#e5fff0','#74c5a5','#205b52'],orbit:3,angle:2.3,description:'Posição visual proposta para trilhas de documentação.',tasks:['Exemplo: preparar relatório'],state:'Simulação: disponível'}
 ]}
};
const $=id=>shadow.getElementById(id);const systems=Object.keys(defs);let verifiedMission=null;let current=null,selected=null,zoom=1,last=0,view='universe';let reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;let slots=[];let graphScope='all',graphQuery='',graphZoom=1,graphSelected=null;
// Estados visuais somente demonstrativos. Nao inferir atividade real destas amostras.
const visualScenarios=['idle','active','attention','error'];
const visualLabels={idle:'CALMO',active:'ATIVIDADE',attention:'ATENÇÃO',error:'FALHA'};
let visualScenario='idle';
function demoAgentVisual(key,index){
  if(visualScenario==='idle')return {status:'idle',tasks:0};
  if(visualScenario==='active')return {status:index<2?'active':'idle',tasks:index===0?2:index===1?1:0};
  if(visualScenario==='attention')return {status:index===0?'attention':index===1?'active':'idle',tasks:index<2?1:0};
  return {status:index===0?'error':'idle',tasks:0};
}
function demoSystemVisual(key){
  const result=defs[key].agents.map((a,i)=>demoAgentVisual(key,i));
  return {status:result.some(x=>x.status==='error')?'error':result.some(x=>x.status==='attention')?'attention':result.some(x=>x.status==='active')?'active':'idle',tasks:result.reduce((n,x)=>n+x.tasks,0)};
}
function demoStateLabel(state){
  return {idle:'CALMO',active:'ATIVO',attention:'ATENÇÃO',error:'FALHA'}[state]||'CALMO';
}
function safe(v){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function orbitalSVG(color){let circles='';for(let i=0;i<3;i++){const a=46+i*25,b=a*.48;circles+=`<ellipse cx="224" cy="77" rx="${a}" ry="${b}" transform="rotate(-17 224 77)" fill="none" stroke="${color}" stroke-width="1" opacity="${.58-i*.11}"/>${i===2?`<ellipse class="orbit-stream" cx="224" cy="77" rx="${a}" ry="${b}" transform="rotate(-17 224 77)" stroke="${color}"/>`:``}`;}return `<svg class="sys-orbits" viewBox="0 0 430 190" preserveAspectRatio="xMidYMid slice">${circles}<circle cx="224" cy="77" r="22" fill="${color}" opacity=".15"/><circle cx="224" cy="77" r="14" fill="${color}"/><circle cx="224" cy="77" r="8" fill="#fff3d9" opacity=".4"/><circle cx="265" cy="57" r="7" fill="${color}"/><circle cx="164" cy="108" r="5" fill="${color}"/><circle cx="302" cy="39" r="4" fill="${color}" opacity=".6"/></svg>`}

/* Fonte real só após GET autenticado. O projeto foi informado pelo operador, não provado pelo servidor. */
function realMissionActivity(status){
  return status==='running'?'active':status==='waiting_for_confirmation'?'attention':status==='error'?'error':'idle';
}
function applyVerifiedMission(observation){
  if(!observation||!/^[a-f0-9-]{36}$/.test(observation.conversationId))return;
  verifiedMission=Object.freeze({...observation});
  $('source-banner').textContent='4 SISTEMAS DEMO · 1 MISSÃO OPENHANDS CONSULTADA';
  if(!defs.observado){
    defs.observado={name:'OBSERVATÓRIO',subtitle:'Projeto associado manualmente',core:'EXECUÇÃO REAL',color:'#77dbff',sun:['#fff6de','#ffe1a1','#b15c2e'],agents:[]};
    systems.push('observado');
  }
  openVerifiedSystem();
}
function openVerifiedSystem(){
  if(!verifiedMission)return renderUniverse();
  stage.classList.remove('graph-active');$('graph').classList.add('hidden');$('mode-3d').hidden=false;
  current='observado';view='solar';selected=null;slots=[];
  $('universe').classList.add('hidden');$('solar').classList.remove('hidden');$('solar-note').classList.remove('hidden');
  $('breadcrumb').textContent='NÍVEL 02 / OBSERVATÓRIO · CONSULTA AUTENTICADA';
  $('scene-title').textContent='OBSERVATÓRIO · Missão consultada';
  $('scene-description').textContent='Uma execução real consultada no OpenHands. O projeto foi informado manualmente e não foi autenticado como vínculo.';
  $('sun-label').innerHTML='MISSÃO<small>SEM AGENTE ATRIBUÍDO</small>';
  $('planets').replaceChildren();
  const moon=$('real-lua');
  moon.classList.remove('hidden');
  $('real-lua-state').textContent=verifiedMission.status+' · '+verifiedMission.conversationId.slice(0,8);
  $('solar-note').textContent='☾ Lua = conversa OpenHands consultada; nenhum agente individual identificado. Outros sistemas permanecem demonstrativos.';
  $('metrics').innerHTML='<div class="metric"><small>EXECUÇÕES CONSULTADAS</small><strong>01</strong><span>Fonte: OpenHands</span></div><div class="metric"><small>AGENTES COMPROVADOS</small><strong>00</strong><span>Nenhum agente registrado nesta prova</span></div><div class="metric"><small>VÍNCULO AO PROJETO</small><strong>Manual</strong><span>Sem validação no servidor</span></div>';
  drawSolar();setNav();renderPanel();
}
function renderVerifiedPanel(){
  const p=$('panel-content');
  if(!verifiedMission){p.textContent='Sem missão consultada.';return;}
  const v=verifiedMission;
  p.innerHTML=`<div class="empty">
    <div class="panel-kicker">EXECUÇÃO OPENHANDS · CONSULTA REAL</div>
    <div class="agent-hero" style="display:flex"><div class="hero-planet" style="--hero-light:#e8fcff;--hero-mid:#86d5ed;--hero-dark:#124b72;--hero-glow:#71dbffa8"></div></div>
    <h2>Lua de execução verificada</h2>
    <div class="section"><h3>STATUS CONSULTADO</h3><p class="panel-text">${safe(v.status)}</p></div>
    <div class="section"><h3>IDENTIFICADOR DA CONVERSA</h3><p class="panel-text">${safe(v.conversationId)}</p></div>
    <div class="section"><h3>PROJETO INFORMADO PELO OPERADOR</h3><p class="panel-text">${safe(v.project)}</p></div>
    <div class="section"><h3>ORIGEM E HORÁRIOS</h3><p class="panel-text">OpenHands Agent Server · GET /api/conversations/{id}</p><p class="panel-text">Servidor: ${safe(v.updatedAt||'Não fornecido')}</p><p class="panel-text">Observado no navegador: ${safe(v.observedAt)}</p></div>
    <div class="notice">A API confirmou a conversa e seu estado. Não confirma resultado, sucesso, vínculo ao projeto nem identidade de um agente. Os demais planetas são demonstrações.</div>
  </div>`;
}


/* V0.5: grafo com proveniência: demonstração e leitura verificada nunca se misturam. */
function graphModel(){
  const nodes=[
    {id:'demo-root',name:'Projetos ilustrativos',tag:'APENAS DEMO',kind:'demo-hub',x:27,y:48,description:'Agrupador dos quatro exemplos visuais. Não representa inventário de operações reais.'}
  ];
  const places=[[14,19],[43,18],[13,79],[43,79]];
  const edges=[];
  Object.keys(defs).filter(k=>k!=='observado').forEach((key,i)=>{
    const item=defs[key];
    nodes.push({id:'demo-'+key,name:item.name,tag:'DEMONSTRAÇÃO',kind:'demo',x:places[i][0],y:places[i][1],description:'Projeto ilustrativo. Agentes, missões e atividades não comprovados.'});
    edges.push({from:'demo-root',to:'demo-'+key,kind:'demo'});
  });
  if(verifiedMission){
    nodes.push({id:'real-origin',name:'OpenHands',tag:'FONTE AUTENTICADA',kind:'verified',x:69,y:24,description:'Origem: GET de conversa pela sessão autenticada do Canvas.'});
    nodes.push({id:'real-mission',name:'Missão '+verifiedMission.conversationId.slice(0,8),tag:'ESTADO: '+verifiedMission.status,kind:'verified',x:83,y:51,description:'Conversa consultada pontualmente, não sucesso de tarefa ou agente comprovado.'});
    nodes.push({id:'manual-project',name:verifiedMission.project.split('/').pop().slice(0,22),tag:'PROJETO INFORMADO',kind:'manual',x:69,y:81,description:'Associação informada pelo operador; o servidor não confirmou o vínculo.'});
    edges.push({from:'real-origin',to:'real-mission',kind:'verified'});
    edges.push({from:'real-mission',to:'manual-project',kind:'manual'});
  }
  return {nodes,edges};
}
function renderGraphPanel(){
  const p=$('panel-content');
  const node=graphModel().nodes.find(n=>n.id===graphSelected);
  if(!node){
    p.innerHTML='<div class="empty"><h2>Mapa do trabalho</h2><p>Selecione um ponto no grafo para conhecer sua origem e suas conexões.</p><div class="section"><h3>COMO LER</h3><p class="panel-text">Verde: consulta real do OpenHands.</p><p class="panel-text">Amarelo tracejado: associação informada manualmente, sem comprovação da API.</p><p class="panel-text">Cinza tracejado: projetos de demonstração.</p></div><div class="notice">O grafo ainda não descobre agentes ou projetos automaticamente. Primeiro consulte uma conversa real em ☾ CONSULTA DE MISSÃO REAL.</div></div>';
    return;
  }
  let extra='';
  if(node.id==='real-mission'){
    const v=verifiedMission;
    extra='<div class="section"><h3>FONTE DA EXECUÇÃO</h3><p class="panel-text">'+safe(v.conversationId)+'</p><p class="panel-text">Estado: '+safe(v.status)+'</p><p class="panel-text">Observado: '+safe(v.observedAt)+'</p><p class="panel-text">Servidor: '+safe(v.updatedAt||'Não informado')+'</p></div>';
  } else if(node.id==='manual-project'){
    extra='<div class="section"><h3>DECLARAÇÃO MANUAL</h3><p class="panel-text">'+safe(verifiedMission.project)+'</p><p class="panel-text">Não foi validada pelo OpenHands.</p></div>';
  }
  p.innerHTML='<div class="empty"><div class="panel-kicker">NÓ DO GRAFO · '+safe(node.tag)+'</div><h2>'+safe(node.name)+'</h2><p>'+safe(node.description)+'</p>'+extra+'<div class="notice">As linhas mostram somente relações explicitamente classificadas. Uma conversa concluída não garante sucesso da tarefa.</div></div>';
}
function renderGraph(){
  const data=graphModel();
  const nodes=data.nodes.filter(n=>(graphScope==='all'||(graphScope==='demo'?n.kind.startsWith('demo'):!n.kind.startsWith('demo')))&&(!graphQuery||(n.name+' '+n.tag).toLocaleLowerCase('pt-BR').includes(graphQuery)));
  const ids=new Set(nodes.map(n=>n.id));
  const edges=data.edges.filter(e=>ids.has(e.from)&&ids.has(e.to));
  const byId=new Map(nodes.map(n=>[n.id,n]));
  const selected=ids.has(graphSelected)?graphSelected:null;
  const lines=edges.map(e=>{
    const a=byId.get(e.from),b=byId.get(e.to);
    return '<line x1="'+a.x*10+'" y1="'+a.y*6+'" x2="'+b.x*10+'" y2="'+b.y*6+'" data-kind="'+e.kind+'" class="'+(selected&&e.from!==selected&&e.to!==selected?'dimmed':'')+'"></line>';
  }).join('');
  const controls=nodes.map(n=>{
    const selectedClass=selected===n.id?' selected':selected?' dimmed':'';
    return '<button type="button" class="graph-node'+selectedClass+'" data-node="'+safe(n.id)+'" data-kind="'+safe(n.kind)+'" style="left:'+n.x+'%;top:'+n.y+'%" aria-pressed="'+String(selected===n.id)+'" title="'+safe(n.description)+'"><small>'+safe(n.tag)+'</small><strong>'+safe(n.name)+'</strong></button>';
  }).join('');
  $('graph-surface').style.transform='scale('+graphZoom+')';
  $('graph-surface').innerHTML='<svg class="graph-edges" viewBox="0 0 1000 600" preserveAspectRatio="none" aria-hidden="true">'+lines+'</svg>'+controls+(nodes.length?'':'<div class="graph-empty">Nenhum item para este filtro. Para exibir dados reais, consulte uma missão do OpenHands ou limpe a busca.</div>');
  $('graph-surface').querySelectorAll('[data-node]').forEach(button=>{
    button.onclick=()=>{graphSelected=button.dataset.node;renderGraph();renderGraphPanel();};
  });
  if(selected===null&&graphSelected!==null)graphSelected=null;
  renderGraphPanel();
}
function openGraph(){
  view='graph';current=null;selected=null;stage.classList.add('graph-active');
  $('universe').classList.add('hidden');$('solar').classList.add('hidden');
  $('graph').classList.remove('hidden');$('mode-3d').hidden=true;
  $('real-lua').classList.add('hidden');$('solar-note').classList.add('hidden');
  $('breadcrumb').textContent='NÍVEL 02 / MAPA OPERACIONAL';
  $('scene-title').textContent='Grafo · conexões com origem';
  $('scene-description').textContent='Explore projetos ilustrativos e conversas consultadas. Cada linha indica o nível de comprovação.';
  $('metrics').innerHTML='<div class="metric"><small>CONSULTAS OPENHANDS</small><strong>'+(verifiedMission?'01':'00')+'</strong><span>Uma leitura pontual por UUID</span></div><div class="metric"><small>PROJETOS EXEMPLO</small><strong>04</strong><span>Identificados como demonstração</span></div><div class="metric"><small>RELAÇÕES CONFIRMADAS</small><strong>'+(verifiedMission?'01':'00')+'</strong><span>Fonte → conversa; projeto é manual</span></div>';
  renderGraph();setNav();
}

function renderUniverse(){view='universe';stage.classList.remove('graph-active');$('graph').classList.add('hidden');$('mode-3d').hidden=false;current=null;selected=null;$('real-lua').classList.add('hidden');$('universe').classList.remove('hidden');$('solar').classList.add('hidden');$('solar-note').classList.add('hidden');$('breadcrumb').textContent='NÍVEL 01 / UNIVERSO CENTRAL';$('scene-title').textContent='Sua galáxia de operações';$('scene-description').textContent='Sistemas demonstrativos e missões consultadas são identificados separadamente.';$('universe').innerHTML=systems.map(k=>{let s=defs[k];return `<button type="button" class="system-tile" data-sys="${safe(k)}" aria-label="Explorar ${safe(s.name)}" data-activity="${k==='observado'?realMissionActivity(verifiedMission.status):demoSystemVisual(k).status}">${orbitalSVG(s.color)}<span class="system-activity">${k==='observado'?'OPENHANDS REAL · '+safe(verifiedMission.status):'SIMULAÇÃO: '+demoStateLabel(demoSystemVisual(k).status)+(demoSystemVisual(k).tasks?' · '+demoSystemVisual(k).tasks+' TAREFAS':'')}</span><span class="system-name">${safe(s.name)}</span><span class="system-sub">${safe(s.subtitle)}</span><span class="sys-open">EXPLORAR ↗</span></button>`}).join('');$('universe').querySelectorAll('button').forEach(b=>b.onclick=()=>openSystem(b.dataset.sys));$('metrics').innerHTML=`<div class="metric"><small>SISTEMAS</small><strong>${systems.length}</strong><span>${verifiedMission?'4 demos + 1 missão consultada':'4 projetos ilustrativos'}</span></div><div class="metric"><small>VISUALIZAÇÃO</small><strong>Multiuniverso</strong><span>Uma galáxia de projetos</span></div><div class="metric"><small>FONTE DOS DADOS</small><strong>${verifiedMission?'Mista':'Exemplo'}</strong><span>${verifiedMission?'Demos + OpenHands consultado':'Sem consulta OpenHands'}</span></div>`;setNav();renderPanel()}
function setNav(){$('top-universe').classList.toggle('active',view==='universe');$('top-project').classList.toggle('active',view==='solar');$('top-graph').classList.toggle('active',view==='graph');$('rail-universe').classList.toggle('active',view==='universe');$('rail-system').classList.toggle('active',view==='solar');$('rail-graph').classList.toggle('active',view==='graph')}
function openSystem(key){if(key==='observado')return openVerifiedSystem();stage.classList.remove('graph-active');$('graph').classList.add('hidden');$('mode-3d').hidden=false;$('real-lua').classList.add('hidden');$('solar-note').textContent='● Planetas = agentes propostos · ● Luas/tarefas = representação conceitual';current=key||'vigiafast';view='solar';selected=null;let s=defs[current];$('universe').classList.add('hidden');$('solar').classList.remove('hidden');$('solar-note').classList.remove('hidden');$('breadcrumb').textContent='NÍVEL 02 / '+s.name;$('scene-title').textContent=s.name+' · Sistema solar';$('scene-description').textContent='Planetas representam papéis de agentes. Clique em um planeta para explorar sua função conceitual.';$('sun-label').innerHTML=safe(s.core)+'<small>NÚCLEO CONCEITUAL</small>';$('metrics').innerHTML=`<div class="metric"><small>PLANETAS</small><strong>${s.agents.length}</strong><span>Funções ilustrativas</span></div><div class="metric"><small>PROJETO</small><strong>${safe(s.name)}</strong><span>${safe(s.subtitle)}</span></div><div class="metric"><small>INTEGRAÇÃO</small><strong>Demo</strong><span>Sem telemetria real</span></div>`;slots=[];$('planets').innerHTML=s.agents.map((a,i)=>{let color=a.color;let stateColor=a.state.includes('atenção')?'#ffc275':a.state.includes('revisão')?'#ffce8b':a.state.includes('não implantado')?'#839bbd':'#68e4c5';let visual=demoAgentVisual(current,i);return `<button class="planet-slot" type="button" data-activity="${visual.status}" data-idx="${i}" aria-label="Abrir agente ${safe(a.name)}" style="--size:${[53,59,62,55][a.orbit-1]}px;--light:${a.spectrum[0]};--mid:${a.spectrum[1]};--dark:${a.spectrum[2]};--glow:${color}9c;--ring:${color};--status-color:${stateColor}"><span class="planet-sphere"></span>${i%3!==1?'<span class="planet-ring"></span>':''}<span class="planet-label"><span class="planet-status"></span>${safe(a.name)}</span>${visual.tasks?`<span class="planet-activity">${visual.tasks} ${visual.tasks===1?'LUA':'LUAS'} · DEMO</span>`:''}</button>`}).join('');$('planets').querySelectorAll('button').forEach(b=>{b.onclick=()=>{selected=Number(b.dataset.idx);renderPanel();highlight()};slots.push(b)});drawSolar();setNav();renderPanel()}
function highlight(){slots.forEach((s,i)=>s.classList.toggle('selected',i===selected))}
function drawSolar(){if(view!=='solar')return;if(enabled3d){engine3d.draw(performance.now());return;}const el=$('solar');const w=el.clientWidth,h=el.clientHeight;const cx=w*.5,cy=h*.53;const unit=Math.min(1.0,w/1040,h/750)*zoom;const axes=[0,122,207,289,365].map(n=>n*unit);const angle=-17*Math.PI/180;let orbits='';for(let i=1;i<=4;i++){orbits+=`<ellipse cx="${cx}" cy="${cy}" rx="${axes[i]}" ry="${axes[i]*.61}" transform="rotate(-17 ${cx} ${cy})"/>`};$('orbits').setAttribute('width',w);$('orbits').setAttribute('height',h);$('orbits').setAttribute('viewBox',`0 0 ${w} ${h}`);$('orbits').innerHTML=orbits;$('sun').style.left=`${cx}px`;$('sun').style.top=`${cy}px`;if(!current)return;defs[current].agents.forEach((a,i)=>{let phase=a.angle+(reduced?0:Math.min(last/1000,86400)*.014/(.7+a.orbit*.7));let xr=Math.cos(phase)*axes[a.orbit],yr=Math.sin(phase)*axes[a.orbit]*.61;const x=xr*Math.cos(angle)-yr*Math.sin(angle),y=xr*Math.sin(angle)+yr*Math.cos(angle);slots[i].style.left=(cx+x)+'px';slots[i].style.top=(cy+y)+'px';let scale=Math.max(.72,Math.min(1,unit));slots[i].style.scale=scale;});}
function renderPanel(){const p=$('panel-content');if(view==='universe'){p.innerHTML=`<div class="empty"><div class="agent-hero" style="display:flex"><div class="hero-planet" style="--hero-light:#eac9ff;--hero-mid:#485fbc;--hero-dark:#13244b;--hero-glow:#567acf77"></div></div><h2>Uma visão, vários projetos.</h2><p>Um universo central para navegar por sistemas independentes. Dentro de cada sistema, cada planeta representa uma função de agente.</p><div class="section"><h3>PRINCÍPIOS</h3><div class="task-row"><span class="task-dot"></span><span>Visão geral sem misturar clientes ou permissões</span></div><div class="task-row"><span class="task-dot"></span><span>Agentes e tarefas apenas quando existirem na fonte real</span></div><div class="task-row"><span class="task-dot"></span><span>Revisão humana em decisões sensíveis</span></div></div><button type="button" class="panel-button" id="goto-graph">Explorar conexões →</button><div class="notice">${verifiedMission?'Quatro sistemas permanecem demonstrativos. O cartão Observatório é uma conversa real consultada pelo OpenHands; o projeto foi informado manualmente.':'Este é um protótipo visual estático e navegável. Projetos, agentes, estados e tarefas são demonstrativos — nenhum sistema está conectado.'}</div></div>`;$('goto-graph').onclick=openGraph;return}if(current==='observado'){renderVerifiedPanel();return}const s=defs[current];if(selected===null){p.innerHTML=`<div class="empty"><div class="agent-hero" style="display:flex"><div class="hero-planet" style="--hero-light:${s.sun[0]};--hero-mid:${s.sun[1]};--hero-dark:${s.sun[2]};--hero-glow:${s.color}88"></div></div><h2>${safe(s.core)}</h2><p>${safe(s.subtitle)}. Este centro é uma metáfora visual de coordenação, não uma afirmação de que existe um orquestrador implantado.</p><div class="section"><h3>PLANETAS DESTE SISTEMA</h3>${s.agents.map(a=>`<button type="button" class="agent-list-item" data-agent="${s.agents.indexOf(a)}"><span class="task-dot" style="background:${a.color}"></span><span><b>${safe(a.name)}</b> · ${safe(a.role)}</span></button>`).join('')}</div><div class="notice">Clique em um planeta ou selecione o agente nesta lista. Sem conexão a APIs reais.</div></div>`;p.querySelectorAll(".agent-list-item").forEach(b=>b.onclick=()=>{selected=Number(b.dataset.agent);renderPanel();highlight()});return}let a=s.agents[selected];let visual=demoAgentVisual(current,selected);let pill=visual.status==='error'?'#ff9aab':visual.status==='attention'?'#ffcd88':'#57efc5';let stateLabel=visualScenario==='idle'?a.state:`Simulação: ${demoStateLabel(visual.status).toLowerCase()}${visual.tasks?' · '+visual.tasks+' tarefa(s)':''}`;p.innerHTML=`<div class="agent-hero"><div class="hero-planet" style="--hero-light:${a.spectrum[0]};--hero-mid:${a.spectrum[1]};--hero-dark:${a.spectrum[2]};--hero-glow:${a.color}bb"></div></div><div class="panel-kicker">PLANETA ${String(selected+1).padStart(2,'0')} · PAPEL PROPOSTO</div><h2 class="agent-name">${safe(a.name)}</h2><p class="agent-role">${safe(a.role)}</p><span class="status-pill" style="--pill:${pill}">${safe(stateLabel)}</span><section class="section"><h3>SOBRE ESTE AGENTE</h3><p class="panel-text">${safe(a.description)}</p></section><section class="section"><h3>TAREFAS EXEMPLIFICATIVAS</h3>${a.tasks.map(t=>`<div class="task-row"><span class="task-dot"></span><span>${safe(t)}</span></div>`).join('')}</section><section class="section"><h3>STATUS REAL</h3><p class="panel-text">Não conectado a fonte de telemetria. Progresso, custo e tempo de execução não são exibidos sem dados verificáveis.</p></section><button class="panel-button" id="deselect" type="button">Voltar à visão do sistema</button><div class="notice">Todos os estados são simulados. Nenhuma ferramenta de IA é iniciada por esta interface.</div>`;$('deselect').onclick=()=>{selected=null;highlight();renderPanel()}}
// Observatório V0.2 — renderizador WebGL2 próprio e sem dependências externas.
// Camada de demonstração. Não contém credenciais, endpoints ou dados reais.
function make3D(){
  const canvas=document.createElement('canvas');
  canvas.id='cosmos-3d';canvas.setAttribute('aria-hidden','true');
  $('solar-stage').prepend(canvas);
  let gl;
  try {gl=canvas.getContext('webgl2',{antialias:true,alpha:true,powerPreference:'low-power',depth:true});}catch(_){gl=null}
  if(!gl) {canvas.remove();return {enabled:false,draw(){},project(){return null}};}
  const VS=`#version 300 es
    precision highp float;
    in vec3 aPosition;in vec3 aNormal;
    uniform mat4 uVP;uniform mat4 uModel;
    out vec3 vNormal;out vec3 vWorld;out vec3 vLocal;
    void main(){vec4 w=uModel*vec4(aPosition,1.0);vWorld=w.xyz;vNormal=normalize(mat3(uModel)*aNormal);vLocal=aPosition;gl_Position=uVP*w;}
  `;
  const FS=`#version 300 es
    precision highp float;
    in vec3 vNormal;in vec3 vWorld;in vec3 vLocal;
    uniform vec3 uLight;uniform vec3 uDark;uniform vec3 uCamera;uniform float uTime;
    uniform float uSeed;uniform float uSun;uniform float uSelected;uniform float uActivity;
    out vec4 outColor;
    float hash(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
    float noise(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);
      return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x),mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
                 mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z);}
    float fbm(vec3 p){float x=0.0,a=.5;for(int i=0;i<4;i++){x+=a*noise(p);p=p*2.11+13.7;a*=.5;}return x;}
    void main(){
      vec3 N=normalize(vNormal);vec3 V=normalize(uCamera-vWorld);
      vec3 p=normalize(vLocal);
      float az=uTime*.04+uSeed*2.3;
      p=vec3(cos(az)*p.x-sin(az)*p.z,p.y,cos(az)*p.z+sin(az)*p.x);
      float f=fbm(p*(4.8+uSeed*1.2)+vec3(uSeed*2.0));
      float band=sin(p.y*24.0+f*7.0+uSeed*6.0)*.5+.5;
      float terrain=smoothstep(.35,.67, f*.87+band*.2);
      vec3 c=mix(uDark,uLight,terrain*.83+.12);
      c=mix(c,mix(uDark,uLight,.42),smoothstep(.45,.76,fbm(p*13.0+uSeed))* .32);
      if(uSun>.5){
        float sunwave=fbm(p*7.0+vec3(uTime*.035));
        c=mix(vec3(1.0,.28,.035),vec3(1.0,.92,.43),smoothstep(.24,.74,sunwave));
        c+=.18*pow(band,7.0);
        outColor=vec4(c,1.0);return;
      }
      vec3 L=normalize(-vWorld+vec3(1.8,1.4,1.4));
      float shade=dot(N,L);
      float diff=max(.0,shade)*.82+.17;
      float rim=pow(1.0-max(dot(N,V),0.0),3.3);
      float spec=pow(max(dot(reflect(-L,N),V),0.0),19.0)*.22;
      c*=diff;
      c+=uLight*rim*(.43+uSelected*.18+uActivity*(.10+.20*(.5+.5*sin(uTime*3.0+uSeed))));
      c+=spec;
      outColor=vec4(c,1.0);
    }`;
  const LVs=`#version 300 es
    precision highp float;in vec3 aPosition;uniform mat4 uVP;uniform vec3 uOffset;
    void main(){gl_Position=uVP*vec4(aPosition+uOffset,1.0);}`;
  const LFs=`#version 300 es
    precision highp float;uniform vec4 uColor;out vec4 outColor;
    void main(){outColor=uColor;}`;
  function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s}
  function program(v,f){const p=gl.createProgram();gl.attachShader(p,shader(gl.VERTEX_SHADER,v));gl.attachShader(p,shader(gl.FRAGMENT_SHADER,f));gl.linkProgram(p);if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(p));return p}
  let surface,lines;
  try{surface=program(VS,FS);lines=program(LVs,LFs)}catch(e){console.warn('WebGL indisponível:',e.message);canvas.remove();return {enabled:false,draw(){},project(){return null}}}
  const sphere=[];const lat=24,lon=40;
  for(let y=0;y<lat;y++)for(let x=0;x<lon;x++){
    function vert(t,p){const theta=t*Math.PI,phi=p*Math.PI*2;return [Math.sin(theta)*Math.cos(phi),Math.cos(theta),Math.sin(theta)*Math.sin(phi)]}
    const a=vert(y/lat,x/lon),b=vert((y+1)/lat,x/lon),c=vert(y/lat,(x+1)/lon),d=vert((y+1)/lat,(x+1)/lon);
    for(const v of [a,b,c,c,b,d])sphere.push(...v,...v);
  }
  const sbuf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,sbuf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(sphere),gl.STATIC_DRAW);
  const attribPos=gl.getAttribLocation(surface,'aPosition'),attribNormal=gl.getAttribLocation(surface,'aNormal');
  const un={};for(const name of ['uVP','uModel','uLight','uDark','uCamera','uTime','uSeed','uSun','uSelected','uActivity'])un[name]=gl.getUniformLocation(surface,name);
  const lun={};for(const name of ['uVP','uOffset','uColor'])lun[name]=gl.getUniformLocation(lines,name);
  const lbuf=gl.createBuffer();
  const orbits=[];for(let i=1;i<=4;i++){let list=[];for(let j=0;j<=160;j++){const a=j/160*Math.PI*2;list.push((1.42+i*.91)*Math.cos(a),0,(1.42+i*.91)*Math.sin(a))}orbits.push(new Float32Array(list));}
  let vp,eye=[0,10,11],positions=[],angle=0.24,elev=.88,lastDraw=0,dragging=false,startX=0,startY=0;
  const m4={
    mul(a,b){const out=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)out[c*4+r]+=a[k*4+r]*b[c*4+k];return out},
    persp(aspect){const f=1/Math.tan(47*Math.PI/360),n=.1,fa=80;return new Float32Array([f/aspect,0,0,0,0,f,0,0,0,0,(fa+n)/(n-fa),-1,0,0,2*fa*n/(n-fa),0])},
    look(eye){const norm=p=>{const l=Math.hypot(...p)||1;return p.map(x=>x/l)},cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((v,x,i)=>v+x*b[i],0);
      const z=norm(eye),x=norm(cross([0,1,0],z)),y=cross(z,x);
      return new Float32Array([x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-dot(x,eye),-dot(y,eye),-dot(z,eye),1]);},
    model(p,r){return new Float32Array([r,0,0,0,0,r,0,0,0,0,r,0,...p,1])}
  };
  function worldPos(agent,t){const a=agent.angle+(reduced?0:t*.045/(.6+agent.orbit*.52)),r=1.42+agent.orbit*.91;return [Math.cos(a)*r,0,Math.sin(a)*r]}
  function hex(s){let v=parseInt(s.replace('#','').slice(0,6),16);return [(v>>16&255)/255,(v>>8&255)/255,(v&255)/255]}
  function proj(pos){if(!vp)return null;const v=[...pos,1],clip=[];for(let row=0;row<4;row++){clip[row]=0;for(let k=0;k<4;k++)clip[row]+=vp[k*4+row]*v[k];}
    if(clip[3]<=.01)return null;const w=canvas.clientWidth,h=canvas.clientHeight;return {x:(clip[0]/clip[3]*.5+.5)*w,y:(.5-clip[1]/clip[3]*.5)*h,visible:Math.abs(clip[0]/clip[3])<1.1&&Math.abs(clip[1]/clip[3])<1.1};}
  function draw(now){if(view!=='solar'||!current)return;const w=canvas.clientWidth,h=canvas.clientHeight;if(w<50||h<50)return;
    const t=now/1000;if(reduced&&lastDraw&&now-lastDraw<700)return;if(!reduced&&lastDraw&&now-lastDraw<30)return;lastDraw=now;
    const dpr=Math.min(window.devicePixelRatio||1,1.5);const dw=Math.round(w*dpr),dh=Math.round(h*dpr);
    if(canvas.width!==dw||canvas.height!==dh){canvas.width=dw;canvas.height=dh;gl.viewport(0,0,dw,dh)}
    const mobile=w<650;const dist=(mobile?20.5:12.7)/zoom;
    eye=[Math.sin(angle)*Math.cos(elev)*dist,Math.sin(elev)*dist,Math.cos(angle)*Math.cos(elev)*dist];
    vp=m4.mul(m4.persp(w/h),m4.look(eye));
    gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
    gl.useProgram(lines);gl.uniformMatrix4fv(lun.uVP,false,vp);gl.uniform3fv(lun.uOffset,[0,0,0]);
    const ap=gl.getAttribLocation(lines,'aPosition');gl.bindBuffer(gl.ARRAY_BUFFER,lbuf);gl.enableVertexAttribArray(ap);gl.vertexAttribPointer(ap,3,gl.FLOAT,false,0,0);
    for(let i=0;i<4;i++){gl.bufferData(gl.ARRAY_BUFFER,orbits[i],gl.DYNAMIC_DRAW);gl.uniform4fv(lun.uColor,[.38,.56,.79,.12+i*.03]);gl.drawArrays(gl.LINE_STRIP,0,orbits[i].length/3)}
    gl.useProgram(surface);gl.uniformMatrix4fv(un.uVP,false,vp);gl.uniform3fv(un.uCamera,eye);gl.uniform1f(un.uTime,t);
    gl.bindBuffer(gl.ARRAY_BUFFER,sbuf);gl.enableVertexAttribArray(attribPos);gl.vertexAttribPointer(attribPos,3,gl.FLOAT,false,24,0);gl.enableVertexAttribArray(attribNormal);gl.vertexAttribPointer(attribNormal,3,gl.FLOAT,false,24,12);
    function renderPlanet(pos,r,color,dark,seed,sun,selected,activity=0){gl.uniformMatrix4fv(un.uModel,false,m4.model(pos,r));gl.uniform3fv(un.uLight,hex(color));gl.uniform3fv(un.uDark,hex(dark));gl.uniform1f(un.uSeed,seed);gl.uniform1f(un.uSun,sun?1:0);gl.uniform1f(un.uSelected,selected?1:0);gl.uniform1f(un.uActivity,activity);gl.drawArrays(gl.TRIANGLES,0,sphere.length/6)}
    const s=defs[current];
    renderPlanet([0,0,0],.77,'#fff2bb','#ff902d',.9,true,false);
    positions=s.agents.map((a,i)=>worldPos(a,t));
    s.agents.forEach((a,i)=>{
      const visual=demoAgentVisual(current,i);
      const intensity=visual.status==='active'?1:visual.status==='attention'?1.35:visual.status==='error'?.65:0;
      renderPlanet(positions[i],[0,.35,.38,.43,.48][a.orbit],a.spectrum[0],a.spectrum[2],i*.63+.17,false,selected===i,intensity);
      if(!reduced){for(let moon=0;moon<Math.min(visual.tasks,2);moon++){
        const phi=t*(.85+moon*.19)+i*1.7+moon*Math.PI;
        const p=positions[i];
        renderPlanet([p[0]+Math.cos(phi)*.55,p[1]+Math.sin(phi*1.4)*.19,p[2]+Math.sin(phi)*.55],.065,visual.status==='attention'?'#ffdf9d':'#a9fdf0','#1a5a70',.33+moon*.2,false,false,.5);
      }}
    });
    const sun=proj([0,0,0]);if(sun){$('sun').style.left=sun.x+'px';$('sun').style.top=sun.y+'px'}
    slots.forEach((slot,i)=>{let p=proj(positions[i]);slot.hidden=!p?.visible;if(p){slot.style.left=p.x+'px';slot.style.top=p.y+'px';slot.style.scale=Math.max(.7,Math.min(1.2,(mobile?20.5:12.7)/dist));}});
  }
  canvas.addEventListener('pointerdown',e=>{if(e.button!==0)return;dragging=true;startX=e.clientX;startY=e.clientY;canvas.setPointerCapture(e.pointerId)});
  canvas.addEventListener('pointermove',e=>{if(!dragging)return;angle+=(e.clientX-startX)*.004;elev=Math.max(.32,Math.min(1.43,elev+(e.clientY-startY)*.003));startX=e.clientX;startY=e.clientY;draw(performance.now())});
  canvas.addEventListener('pointerup',()=>dragging=false);canvas.addEventListener('pointercancel',()=>dragging=false);
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();enabled3d=false;$('solar').classList.remove('webgl');canvas.style.display='none';drawSolar()},{once:true});
  return {enabled:true,draw,project:proj,canvas};
}
let engine3d=null,enabled3d=false;
function apply3d(enabled){
  if(!engine3d)engine3d=make3D();
  enabled3d=!!(enabled&&engine3d.enabled);
  $('solar').classList.toggle('webgl',enabled3d);
  if(engine3d.canvas)engine3d.canvas.style.display=enabled3d?'block':'none';
  $('mode-3d').textContent=enabled3d?'3D ATIVO':'2D / ATIVAR 3D';
  $('mode-3d').setAttribute('aria-pressed',String(enabled3d));
  if(view==='solar'){if(enabled3d)engine3d.draw(performance.now());else drawSolar();}
}

function initStars(){const c=$('starfield'),ctx=c.getContext('2d');const render=()=>{let dpr=Math.min(2,window.devicePixelRatio||1),w=wrapper.clientWidth,h=wrapper.clientHeight;c.width=Math.floor(w*dpr);c.height=Math.floor(h*dpr);c.style.width=w+'px';c.style.height=h+'px';ctx.scale(dpr,dpr);ctx.clearRect(0,0,w,h);let seed=71373;function rand(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296};let stars=Math.min(370,Math.floor(w*h/2600));for(let i=0;i<stars;i++){let x=rand()*w,y=rand()*h,r=rand()*1.2+.2,a=rand()*.5+.1;ctx.beginPath();ctx.fillStyle=`rgba(${190+Math.floor(rand()*65)},${198+Math.floor(rand()*57)},255,${a})`;ctx.arc(x,y,r,0,Math.PI*2);ctx.fill()}};render();resizeCallbacks.push(render)}
function navSystem(){openSystem(current||'vigiafast')}
function setVisualScenario(next){visualScenario=next;$('visual-demo').textContent='SIMULAR: '+visualLabels[next];$('visual-demo').setAttribute('aria-label','Cenário visual de demonstração: '+visualLabels[next]);if(view==='solar'){let system=current,previous=selected;openSystem(system);if(previous!==null&&previous<defs[system].agents.length){selected=previous;highlight();renderPanel()}}else if(view==='graph'){renderGraph();}else renderUniverse();}
$('visual-demo').onclick=()=>setVisualScenario(visualScenarios[(visualScenarios.indexOf(visualScenario)+1)%visualScenarios.length]);$('top-universe').onclick=renderUniverse;$('rail-universe').onclick=renderUniverse;$('top-project').onclick=navSystem;$('rail-system').onclick=navSystem;$('top-graph').onclick=openGraph;$('rail-graph').onclick=openGraph;$('graph-scope').onchange=e=>{graphScope=e.target.value;graphSelected=null;renderGraph();};$('graph-search').oninput=e=>{graphQuery=e.target.value.trim().toLocaleLowerCase('pt-BR');graphSelected=null;renderGraph();};$('graph-open-read').onclick=()=>{const form=stage.querySelector('details.ob-real');if(form){form.open=true;form.querySelector('input')?.focus();}};
$('mode-3d').onclick=()=>apply3d(!enabled3d);$('zoom-in').onclick=()=>{if(view==='graph'){graphZoom=Math.min(1.7,graphZoom+.15);renderGraph();}else{zoom=Math.min(1.38,zoom+.13);drawSolar();}};$('zoom-out').onclick=()=>{if(view==='graph'){graphZoom=Math.max(.8,graphZoom-.15);renderGraph();}else{zoom=Math.max(.65,zoom-.13);drawSolar();}};$('zoom-reset').onclick=()=>{if(view==='graph'){graphZoom=1;renderGraph();}else{zoom=1;drawSolar();}};$('real-lua').onclick=renderVerifiedPanel;$('sun').onclick=()=>{selected=null;highlight();renderPanel()};$('info-button').onclick=()=>alert('Observatório multiprojeto: Universo e Grafo. Quatro projetos ilustrativos permanecem DEMO. Conversas consultadas no OpenHands aparecem como dados reais, com projeto informado manualmente. Sem monitoramento automático, persistência ou prova de associação.');
$('scene').addEventListener('wheel',e=>{if(view==='solar'&&Math.abs(e.deltaY)>0){e.preventDefault();zoom=Math.max(.65,Math.min(1.38,zoom-e.deltaY*.0008));drawSolar()}},{passive:false});
resizeCallbacks.push(drawSolar);initStars();renderUniverse();apply3d(true);
function tick(now){if(destroyed)return;last=now;if(view==='solar'&&!reduced)drawSolar();rafId=requestAnimationFrame(tick)}rafId=requestAnimationFrame(tick);
  return () => {
    destroyed=true;
    disposeRead();
    cancelAnimationFrame(rafId);
    observer?.disconnect();
    if(!observer)window.removeEventListener('resize',resize);
    try {const gl=engine3d?.canvas?.getContext('webgl2');gl?.getExtension('WEBGL_lose_context')?.loseContext();}catch(_){}
    wrapper.remove();
  };
}
export function activate(host) {
  return host.registerPage('observatorio', ({container}) => mountObservatorio({container,host}));
}
