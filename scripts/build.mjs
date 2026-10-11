import {readFileSync,writeFileSync} from 'node:fs';
const base=new URL('../',import.meta.url);
const src=readFileSync(new URL('source/observatorio-v02.html',base),'utf8');
let css=src.match(/<style>([\s\S]*?)<\/style>/)?.[1]?.trim();
let markup=src.match(/<body>([\s\S]*?)<script>/)?.[1]?.trim();
let js=src.match(/<script>\s*\(\(\) => \{\s*([\s\S]*?)\s*\}\)\(\);\s*<\/script>/)?.[1];
if(!css||!markup||!js)throw Error('Estrutura V0.2 alterada');
css=css.replace(':root{',':host{').replace('html,body{','.ob-wrap{').replace('body:before{content:"";position:fixed;','.ob-wrap:before{content:"";position:absolute;').replace('#starfield{position:fixed;','#starfield{position:absolute;').replace('.app{position:relative;z-index:1;min-height:100vh;','.app{position:relative;z-index:1;min-height:720px;');
css=':host{display:block;min-width:0;width:100%;color-scheme:dark;--paper:#e6efff;--muted:#94a6c4;--gold:#ffd27c;--teal:#57efc5;--border:rgba(140,181,240,.19);--glass:rgba(9,19,41,.78)}\n.ob-wrap{position:relative;isolation:isolate;min-height:720px;width:100%;overflow:hidden}\n'+css;
if(!js.includes('const $=id=>document.getElementById(id)')||!js.includes('requestAnimationFrame(tick)}requestAnimationFrame(tick)'))throw Error('Contrato V0.2 mudou');
js=js.replace('const $=id=>document.getElementById(id)','const $=id=>shadow.getElementById(id)').replace('let dpr=Math.min(2,window.devicePixelRatio||1),w=innerWidth,h=innerHeight;','let dpr=Math.min(2,window.devicePixelRatio||1),w=wrapper.clientWidth,h=wrapper.clientHeight;').replace("window.addEventListener('resize',render)",'resizeCallbacks.push(render)').replace("window.addEventListener('resize',drawSolar);",'resizeCallbacks.push(drawSolar);').replace('requestAnimationFrame(tick)}requestAnimationFrame(tick)','rafId=requestAnimationFrame(tick)}rafId=requestAnimationFrame(tick)').replace('function tick(now){last=now;','function tick(now){if(destroyed)return;last=now;').replace('Protótipo independente do Observatório de Agentes.','Extensão demonstrativa do Observatório de Agentes.');
if(js.includes('fetch(')||js.includes('localStorage')||js.includes('sessionStorage')||js.includes('document.getElementById'))throw Error('API não autorizada');
const tmpl=readFileSync(new URL('scripts/extension-template.txt',base),'utf8');
// Callback replacements preserve literal $&, $` and $' in source code.
writeFileSync(new URL('extension.js',base),tmpl.replace('__STYLE__',()=>JSON.stringify(css)).replace('__MARKUP__',()=>JSON.stringify(markup)).replace('__CODE__',()=>js));
