// Public, synthetic fixtures only. Real DOM; no Canvas session or provider.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync} from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.OBS_PLAYWRIGHT_MODULE||'playwright');
const extension=readFileSync(new URL('../../extension.js',import.meta.url),'utf8');
const origin='http://127.0.0.1:3999';
const html=`<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="icon" href="data:,"></head><body style="margin:0;background:#050a16"><main id="fixture"></main><script type="module">
import {activate} from '/extension.js';
window.fixtureReads=[];window.fixtureObservation={id:'00000000-0000-4000-8000-000000000001',execution_status:'finished',updated_at:'2026-10-11T00:00:00Z'};
const host={registerPage(_id,mount){window.fixtureMount=()=>mount({container:document.getElementById('fixture')});window.fixtureDispose=window.fixtureMount();return ()=>{};},agentServer:{async request(request){window.fixtureReads.push(request);if(window.fixturePending)await new Promise(resolve=>window.fixtureFinishRead=resolve);if(window.fixtureError)throw Error('synthetic denied');return window.fixtureObservation;}}};
if(window.fixtureFault==='crypto')Object.defineProperty(Crypto.prototype,'randomUUID',{configurable:true,value(){throw Error('synthetic nonce failure');}});
if(window.fixtureFault==='resize')window.ResizeObserver=class{constructor(){throw Error('synthetic resize failure');}};
if(window.fixtureFault==='digest'){
  const nativeDigest=crypto.subtle.digest.bind(crypto.subtle);
  Object.defineProperty(SubtleCrypto.prototype,'digest',{configurable:true,value:function(...args){
    if(!window.fixtureDigestHeld){
      window.fixtureDigestHeld=true;
      return new Promise(resolve=>{window.fixtureReleaseDigest=()=>resolve(nativeDigest(...args));});
    }
    return nativeDigest(...args);
  }});
}
if(window.fixtureFault==='shadow-gpu')window.ResizeObserver=class{
  constructor(){
    const canvas=document.createElement('canvas');canvas.dataset.syntheticGpu='1';
    document.querySelector('section.ob-wrap')?.shadowRoot?.querySelector('#solar-stage')?.append(canvas);
    canvas.getContext('webgl2');
    throw Error('synthetic shadow GPU mount failure');
  }
};
try{activate(host);}catch(error){window.fixtureMountFailure=String(error);}window.fixtureReady=true;</script></body></html>`;
const artifacts='test-artifacts/graph';mkdirSync(artifacts,{recursive:true});
let browser;
test.before(async()=>{browser=await chromium.launch({headless:true,chromiumSandbox:true});});
test.after(async()=>{await browser?.close();});
async function fixture({mobile=false,reduced=false,fault=null,viewport=null}={}){
 const context=await browser.newContext({viewport:viewport||(mobile?{width:390,height:844}:{width:1440,height:1000}),reducedMotion:reduced?'reduce':'no-preference',serviceWorkers:'block'});
 const unexpected=[];
 await context.route('**/*',async route=>{
   const url=route.request().url();
   if(url===origin+'/')return route.fulfill({contentType:'text/html',body:html});
   if(url===origin+'/extension.js')return route.fulfill({contentType:'text/javascript',body:extension});
   unexpected.push(url);return route.abort();
 });
 const page=await context.newPage();page.setDefaultTimeout(5000);
 await page.addInitScript(()=>{
   const get=HTMLCanvasElement.prototype.getContext;
   window.fixtureGpuAcquisitions=0;window.fixtureGpuLosses=0;
   HTMLCanvasElement.prototype.getContext=function(type,...args){
     if(type==='webgl2'&&this.dataset.syntheticGpu==='1'){
       window.fixtureGpuAcquisitions++;
       return {getExtension(name){return name==='WEBGL_lose_context'?{loseContext(){window.fixtureGpuLosses++;}}:null;}};
     }
     return type==='webgl2'?null:get.call(this,type,...args);
   };
   const request=window.requestAnimationFrame.bind(window),cancel=window.cancelAnimationFrame.bind(window);
   window.fixtureFrames=new Set();window.requestAnimationFrame=fn=>{let id=request(time=>{window.fixtureFrames.delete(id);fn(time);});window.fixtureFrames.add(id);return id;};
   window.cancelAnimationFrame=id=>{window.fixtureFrames.delete(id);cancel(id);};
   const Observer=window.ResizeObserver;window.fixtureObservers=new Set();
   window.ResizeObserver=class extends Observer{observe(...args){window.fixtureObservers.add(this);return super.observe(...args);}disconnect(){window.fixtureObservers.delete(this);return super.disconnect();}};
 });
 if(fault)await page.addInitScript(value=>{window.fixtureFault=value;},fault);
 await page.goto(origin+'/');await page.waitForFunction(()=>window.fixtureReady);
 return {page,context,unexpected};
}
async function close(f){assert.deepEqual(f.unexpected,[],'unexpected external request');await f.context.close();}
async function consult(page){await page.locator('details.ob-real summary').click();await page.locator('input.id').fill('00000000-0000-4000-8000-000000000001');await page.locator('button').filter({hasText:'Consultar estado no OpenHands'}).click();await page.locator('#source-banner').filter({hasText:'1 CONVERSA'}).waitFor();}
test('open, keyboard select/deselect, focus survives DOM replacement',async()=>{
 const f=await fixture();try{const p=f.page;await p.locator('#top-graph').click();const node=p.locator('.graph-node').first();await node.focus();await p.keyboard.press('Enter');assert.equal(await p.locator('.graph-node[aria-pressed=true]').count(),1);assert.equal(await p.evaluate(()=>document.querySelector('.ob-wrap').shadowRoot.activeElement?.dataset.node),await p.locator('.graph-node[aria-pressed=true]').getAttribute('data-node'));await p.keyboard.press('Enter');assert.equal(await p.locator('.graph-node[aria-pressed=true]').count(),0);await p.keyboard.press('Escape');assert.equal(await p.locator('.graph-node[aria-pressed=true]').count(),0);await p.screenshot({path:artifacts+'/graph-desktop.png',fullPage:true});}finally{await close(f);}
});
test('project navigation, demo source, search and empty filter keep search focus',async()=>{
 const f=await fixture();try{const p=f.page;await p.locator('.system-tile').first().click();assert.ok((await p.locator('#scene-title').innerText()).includes('Sistema solar'));await p.locator('#top-universe').click();assert.equal(await p.locator('.system-tile').count(),4);await p.locator('#top-graph').click();assert.equal(await p.locator('.graph-node').count(),5);await p.locator('#graph-search').fill('NOT_FOUND_SYNTHETIC');await p.locator('.graph-empty').waitFor();assert.equal(await p.evaluate(()=>document.querySelector('.ob-wrap').shadowRoot.activeElement?.id),'graph-search');await p.locator('#graph-search').fill('');await p.locator('#graph-scope').selectOption('verified');assert.equal(await p.locator('.graph-node').count(),0);}finally{await close(f);}
});
test('synthetic consulted source remains distinct from manual and errors create no new observation',async()=>{
 const f=await fixture();try{const p=f.page;await consult(p);await p.locator('#top-graph').click();await p.locator('#graph-scope').selectOption('verified');assert.equal(await p.locator('.graph-node').count(),3);assert.equal(await p.locator('.graph-node[data-kind=manual]').count(),1);assert.equal(await p.locator('.graph-edges path.graph-arc[data-kind=verified]').count(),1);assert.equal(await p.locator('.graph-edges path.graph-arc[data-kind=manual]').count(),1);assert.deepEqual(await p.evaluate(()=>window.fixtureReads),[{method:'GET',path:'/api/conversations/00000000-0000-4000-8000-000000000001'}]);}finally{await close(f);}
 const bad=await fixture();try{await bad.page.evaluate(()=>window.fixtureError=true);await bad.page.locator('details.ob-real summary').click();await bad.page.locator('input.id').fill('00000000-0000-4000-8000-000000000001');await bad.page.getByText('Consultar estado no OpenHands',{exact:true}).click();await bad.page.locator('output').filter({hasText:'desconhecido'}).waitFor();await bad.page.locator('#top-graph').click();assert.equal(await bad.page.locator('.graph-node[data-kind=verified]').count(),0);}finally{await close(bad);}
});
test('mobile/reduced-motion, zoom and keyboard pan are bounded and resettable',async()=>{
 const f=await fixture({mobile:true,reduced:true});try{const p=f.page;await p.locator('#rail-graph').click();assert.ok(await p.locator('#graph-search').isVisible());const intro=await p.locator('.scene-heading').boundingBox(),tools=await p.locator('.graph-tools').boundingBox(),map=await p.locator('#graph-map').boundingBox();assert.ok(tools.y>=intro.y+intro.height+8,'mobile controls must not overlap heading');assert.ok(map.y>=tools.y+tools.height+8,'mobile map must not overlap controls');await p.locator('#zoom-in').click();assert.notEqual(await p.locator('#graph-surface').evaluate(e=>getComputedStyle(e).transform),'matrix(1, 0, 0, 1, 0, 0)');await p.locator('#graph-map').focus();await p.keyboard.press('ArrowRight');assert.ok((await p.locator('#graph-surface').getAttribute('style')).includes('translate('));await p.locator('#zoom-reset').click();assert.deepEqual(await p.locator('#graph-surface').evaluate(e=>{const m=new DOMMatrixReadOnly(getComputedStyle(e).transform);return [m.a,m.d,m.e,m.f];}),[1,1,0,0]);assert.equal(await p.locator('#graph-surface').evaluate(e=>getComputedStyle(e).transitionDuration),'0s');const box=await p.locator('#graph-map').boundingBox();assert.ok(box.width>200&&box.height>100);await p.locator('#graph-map').focus();for(let i=0;i<20;i++)await p.keyboard.press('ArrowRight');assert.equal(await p.locator('#graph-surface').evaluate(e=>new DOMMatrixReadOnly(getComputedStyle(e).transform).e),140);await p.locator('#zoom-reset').click();await p.mouse.move(box.x+8,box.y+8);await p.mouse.down();await p.mouse.move(box.x+48,box.y+8);await p.mouse.up();assert.equal(await p.locator('#graph-surface').evaluate(e=>new DOMMatrixReadOnly(getComputedStyle(e).transform).e),40);await p.locator('#zoom-reset').click();assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await p.screenshot({path:artifacts+'/graph-mobile.png',fullPage:true});}finally{await close(f);}
});
test('content is escaped and graph text has contrast on declared solid background',async()=>{
 const f=await fixture();try{await f.page.locator('#top-graph').click();const colors=await f.page.locator('.graph-node small').first().evaluate(e=>({fg:getComputedStyle(e).color,bg:getComputedStyle(e.parentElement).backgroundColor}));const luminance=s=>{const c=s.match(/[\d.]+/g).slice(0,3).map(Number).map(n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;});return .2126*c[0]+.7152*c[1]+.0722*c[2];};assert.ok((luminance(colors.fg)+.05)/(luminance(colors.bg)+.05)>=4.5);assert.equal(await f.page.locator('#graph-map').getAttribute('aria-label'),'Nós e conexões entre projetos demonstrativos e conversas consultadas');assert.equal(await f.page.locator('html').getAttribute('lang'),'pt-BR');await f.page.locator('#top-universe').click();await f.page.evaluate(()=>fixtureObservation.execution_status='<img src=\"https://unexpected.invalid\">');await consult(f.page);await f.page.locator('#top-graph').click();assert.equal(await f.page.locator('#graph img').count(),0);await f.page.locator('.graph-node[data-kind=verified]').last().click();assert.equal(await f.page.locator('#panel-content img').count(),0);}finally{await close(f);}
});
test('teardown releases RAF/observer and remount does not duplicate reads',async()=>{
 const f=await fixture();try{await f.page.evaluate(()=>window.fixtureDispose());assert.equal(await f.page.locator('section.ob-wrap').count(),0);assert.deepEqual(await f.page.evaluate(()=>[fixtureFrames.size,fixtureObservers.size]),[0,0]);await f.page.evaluate(()=>window.fixtureDispose=window.fixtureMount());await consult(f.page);assert.equal(await f.page.evaluate(()=>fixtureReads.length),1);}finally{await close(f);}
});
test('mobile provenance labels and legend are legible at 390px',async()=>{
 const f=await fixture({mobile:true,reduced:true});
 try{
  const p=f.page;await p.locator('#rail-graph').click();
  const sizes=await p.locator('.graph-node small').evaluateAll(els=>els.map(el=>parseFloat(getComputedStyle(el).fontSize)));
  assert.ok(sizes.length>=5&&sizes.every(n=>n>=10),'mobile provenance labels must be at least 10px');
  const demo=await p.locator('.graph-node[data-kind="demo"] small').evaluateAll(els=>els.map(el=>({text:el.textContent.trim(),height:el.getBoundingClientRect().height,lineHeight:parseFloat(getComputedStyle(el).lineHeight)})));
  assert.equal(demo.length,4);
  assert.ok(demo.every(x=>x.text==='DEMO'&&x.height<=x.lineHeight+1),'mobile DEMO labels must fit on a single line');
  assert.ok(await p.locator('.graph-legend').isVisible());
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 }finally{await close(f);}
});
test('pending synthetic GET cannot repopulate UI after teardown',async()=>{
 const f=await fixture();
 try{
  const p=f.page;await p.evaluate(()=>window.fixturePending=true);
  await p.locator('details.ob-real summary').click();
  await p.locator('input.id').fill('00000000-0000-4000-8000-000000000001');
  await p.getByText('Consultar estado no OpenHands',{exact:true}).click();
  await p.waitForFunction(()=>typeof window.fixtureFinishRead==='function');
  await p.evaluate(()=>window.fixtureDispose());
  await p.evaluate(()=>window.fixtureFinishRead());
  await p.waitForTimeout(30);
  assert.equal(await p.locator('section.ob-wrap').count(),0);
  assert.deepEqual(await p.evaluate(()=>[fixtureFrames.size,fixtureObservers.size]),[0,0]);
  assert.equal(await p.evaluate(()=>fixtureReads.length),1);
 }finally{await close(f);}
});
test('mobile simulation control has complete compact text and accessible scenario',async()=>{
 const f=await fixture({mobile:true,reduced:true});
 try{
  const p=f.page,button=p.locator('#visual-demo');
  await p.locator('#rail-graph').click();
  assert.equal(await p.locator('.scenario-compact').isVisible(),true);
  assert.equal((await button.innerText()).trim(),'DEMO: CALMO');
  assert.equal(await button.getAttribute('aria-label'),'Cenário visual de demonstração: calmo');
  const initial=await button.evaluate(el=>({scroll:el.scrollWidth,client:el.clientWidth}));
  assert.ok(initial.scroll<=initial.client+1,'the simulation label may not be clipped in mobile');
  await button.click();
  assert.equal((await button.innerText()).trim(),'DEMO: ATIVIDADE');
  assert.equal(await button.getAttribute('aria-label'),'Cenário visual de demonstração: ATIVIDADE');
  const box=await button.boundingBox();
  assert.ok(box&&box.x>=0&&box.x+box.width<=390,'the simulation control must fit the mobile viewport');
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 }finally{await close(f);}
});
test('denied second GET removes stale observation and manual association',async()=>{
 const f=await fixture();try{
  const p=f.page;await consult(p);await p.locator('#top-graph').click();
  await p.locator('#graph-scope').selectOption('verified');
  assert.equal(await p.locator('.graph-node[data-kind=verified]').count(),2);
  await p.locator('#graph-open-read').click();
  await p.evaluate(()=>window.fixtureError=true);
  await p.locator('details.ob-real input.id').fill('00000000-0000-4000-8000-000000000001');
  await p.getByText('Consultar estado no OpenHands',{exact:true}).click();
  await p.locator('details.ob-real output').filter({hasText:'estado desconhecido'}).waitFor();
  assert.equal(await p.locator('.graph-node[data-kind=verified]').count(),0);
  assert.equal(await p.locator('.graph-node[data-kind=manual]').count(),0);
  assert.equal(await p.locator('#source-banner').innerText(),'◌ PROTÓTIPO · DADOS ILUSTRATIVOS');
  assert.equal(await p.evaluate(()=>fixtureReads.length),2);
 }finally{await close(f);}
});
test('idle conversation never appears as verified execution',async()=>{
 const f=await fixture();try{
  const p=f.page;await p.evaluate(()=>window.fixtureObservation.execution_status='idle');
  await consult(p);
  assert.equal(await p.locator('.ob-real .moon').getAttribute('aria-label'),'Lua: conversa consultada');
  assert.ok((await p.locator('#scene-title').innerText()).includes('Conversa consultada'));
  assert.ok((await p.locator('#panel-content').innerText()).includes('Lua · conversa consultada'));
  assert.equal(await p.locator('#real-lua').getAttribute('aria-label'),'Abrir estado recebido da conversa');
 }finally{await close(f);}
});
test('hung host GET hits local deadline; late completion does not update evidence',async()=>{
 const f=await fixture();try{
  const p=f.page;await p.clock.install();await p.evaluate(()=>window.fixturePending=true);
  await p.locator('details.ob-real summary').click();
  await p.locator('details.ob-real input.id').fill('00000000-0000-4000-8000-000000000001');
  await p.getByText('Consultar estado no OpenHands',{exact:true}).click();
  await p.waitForFunction(()=>typeof window.fixtureFinishRead==='function');
  await p.clock.fastForward(10010);
  await p.locator('details.ob-real output').filter({hasText:'prazo local excedido'}).waitFor();
  assert.equal(await p.getByText('Consultar estado no OpenHands',{exact:true}).isEnabled(),true);
  await p.evaluate(()=>window.fixtureFinishRead());
  assert.ok((await p.locator('details.ob-real output').innerText()).includes('resposta tardia ignorada'));
  assert.equal(await p.locator('.ob-real .moon').count(),0);
  assert.equal(await p.locator('#source-banner').innerText(),'◌ PROTÓTIPO · DADOS ILUSTRATIVOS');
  assert.equal(await p.evaluate(()=>fixtureReads.length),1);
 }finally{await close(f);}
});
test('failed WebCrypto nonce prevents mount and leaves no wrapper',async()=>{
 const f=await fixture({fault:'crypto'});try{
  const p=f.page;
  assert.match(await p.evaluate(()=>window.fixtureMountFailure||''),/synthetic nonce failure/);
  assert.equal(await p.locator('section.ob-wrap').count(),0);
  assert.deepEqual(await p.evaluate(()=>[fixtureFrames.size,fixtureObservers.size]),[0,0]);
 }finally{await close(f);}
});
test('failed resize setup after append rolls back partial mount',async()=>{
 const f=await fixture({fault:'resize'});try{
  const p=f.page;
  assert.match(await p.evaluate(()=>window.fixtureMountFailure||''),/synthetic resize failure/);
  assert.equal(await p.locator('section.ob-wrap').count(),0);
  assert.deepEqual(await p.evaluate(()=>[fixtureFrames.size,fixtureObservers.size]),[0,0]);
 }finally{await close(f);}
});
test('mobile map retains native pan-y and pinch-zoom with bounded keyboard pan',async()=>{
 const f=await fixture({mobile:true,reduced:true});try{
  const p=f.page;await p.locator('#rail-graph').click();
  const value=await p.locator('#graph-map').evaluate(el=>getComputedStyle(el).touchAction);
  assert.ok(value.includes('pan-y')&&value.includes('pinch-zoom'),value);
  assert.equal(value.includes('none'),false);
  await p.locator('#graph-map').focus();await p.keyboard.press('ArrowRight');
  assert.equal(await p.locator('#graph-surface').evaluate(el=>new DOMMatrixReadOnly(getComputedStyle(el).transform).e),20);
 }finally{await close(f);}
});
test('graph instructional copy does not claim verified execution',async()=>{
 const f=await fixture();try{
  const p=f.page;await p.locator('#top-graph').click();
  assert.equal((await p.locator('#graph-open-read').innerText()).trim(),'☾ Consultar conversa');
  assert.equal(await p.locator('#graph-search').getAttribute('placeholder'),'Projeto ou conversa');
  const panel=await p.locator('#panel-content').innerText();
  assert.ok(panel.includes('estado de conversa consultado no OpenHands'));
  assert.ok(panel.includes('CONSULTA DE CONVERSA'));
  assert.doesNotMatch(panel,/CONSULTA DE MISSÃO REAL|execução verificada|consulta real do OpenHands/i);
 }finally{await close(f);}
});
test('digest stays hung after GET but entire read times out and late identity is ignored',async()=>{
 const f=await fixture({fault:'digest'});try{
  const p=f.page;await p.clock.install();
  await p.locator('details.ob-real summary').click();
  await p.locator('details.ob-real input.id').fill('00000000-0000-4000-8000-000000000001');
  await p.getByText('Consultar estado no OpenHands',{exact:true}).click();
  await p.waitForFunction(()=>typeof window.fixtureReleaseDigest==='function');
  assert.equal(await p.getByText('Consultar estado no OpenHands',{exact:true}).isEnabled(),false);
  await p.clock.fastForward(10010);
  await p.locator('details.ob-real output').filter({hasText:'prazo local excedido'}).waitFor();
  assert.equal(await p.getByText('Consultar estado no OpenHands',{exact:true}).isEnabled(),true);
  await p.evaluate(()=>window.fixtureReleaseDigest());
  await p.waitForTimeout(50);
  assert.equal(await p.locator('#source-banner').innerText(),'◌ PROTÓTIPO · DADOS ILUSTRATIVOS');
  assert.equal(await p.locator('details.ob-real .moon').count(),0);
  assert.equal(await p.evaluate(()=>fixtureReads.length),1);
 }finally{await close(f);}
});
test('rollback releases a synthetic GPU context inside shadow root',async()=>{
 const f=await fixture({fault:'shadow-gpu'});try{
  const p=f.page;
  assert.match(await p.evaluate(()=>window.fixtureMountFailure||''),/synthetic shadow GPU mount failure/);
  assert.ok(await p.evaluate(()=>window.fixtureGpuAcquisitions>=2));
  assert.equal(await p.evaluate(()=>window.fixtureGpuLosses),1);
  assert.equal(await p.locator('section.ob-wrap').count(),0);
  assert.deepEqual(await p.evaluate(()=>[fixtureFrames.size,fixtureObservers.size]),[0,0]);
 }finally{await close(f);}
});
test('manifest and universe metrics describe a consulted conversation, not executed mission',async()=>{
 const manifest=JSON.parse(readFileSync(new URL('../../canvas-extension.json',import.meta.url),'utf8'));
 assert.match(manifest.contributes.pages[0].description,/conversas OpenHands consultadas/);
 assert.doesNotMatch(manifest.contributes.pages[0].description,/execu(?:ç|c)ão OpenHands consultada/i);
 const f=await fixture();try{
  const p=f.page;await consult(p);
  await p.locator('#top-universe').click();
  const info=await p.locator('#metrics').innerText();
  assert.match(info,/1 conversa consultada/i);
  assert.doesNotMatch(info,/missão consultada/i);
  await p.locator('#top-graph').click();
  await p.locator('#graph-scope').selectOption('verified');
  await p.locator('#graph-search').fill('nao-encontra-nada');
  const empty=await p.locator('.graph-empty').innerText();
  assert.match(empty,/estado de uma conversa/);
  assert.doesNotMatch(empty,/consulte uma missão/i);
 }finally{await close(f);}
});
test('stellar graph has accessible typed constellations and curved classified links',async()=>{
 const f=await fixture();try{
  const p=f.page;await p.locator('#top-graph').click();
  assert.equal(await p.locator('#graph-map').getAttribute('data-visual'),'stellar');
  assert.equal(await p.locator('.graph-map-index').getAttribute('aria-hidden'),'true');
  assert.equal(await p.locator('.graph-node .graph-beacon').count(),5);
  assert.equal(await p.locator('.graph-node[data-kind=demo]').count(),4);
  assert.equal(await p.locator('.graph-node[data-kind=verified]').count(),0);
  assert.equal(await p.locator('.graph-edges path.graph-arc[data-kind=demo]').count(),4);
  const curves=await p.locator('.graph-edges path.graph-arc').evaluateAll(paths=>paths.map(el=>el.getAttribute('d')));
  assert.ok(curves.every(path=>path.startsWith('M ')&&path.includes(' Q ')));
  assert.equal(await p.locator('.graph-edges').getAttribute('aria-hidden'),'true');
  assert.match(await p.locator('#scene-title').innerText(),/Grafo estelar/);
 }finally{await close(f);}
});
test('stellar graph keeps verified and manual provenance distinct when a test conversation is consulted',async()=>{
 const f=await fixture();try{
  const p=f.page;await consult(p);await p.locator('#top-graph').click();
  assert.equal(await p.locator('.graph-edges path.graph-arc[data-kind=verified]').count(),1);
  assert.equal(await p.locator('.graph-edges path.graph-arc[data-kind=manual]').count(),1);
  assert.equal(await p.locator('.graph-edges path.graph-arc[data-kind=demo]').count(),4);
  assert.equal(await p.locator('.graph-node[data-kind=verified]').count(),2);
  assert.equal(await p.locator('.graph-node[data-kind=manual]').count(),1);
  const labels=await p.locator('.graph-node[data-kind=demo] small').allInnerTexts();
  assert.deepEqual(labels,['DEMO','DEMO','DEMO','DEMO']);
 }finally{await close(f);}
});
test('stellar reduced-motion disables ambient animation and preserves keyboard control on mobile',async()=>{
 const f=await fixture({mobile:true,reduced:true});try{
  const p=f.page;await p.locator('#rail-graph').click();
  const visual=await p.locator('.graph-node[data-kind=demo] .graph-beacon').first().evaluate(el=>({
   animation:getComputedStyle(el).animationName,tag:getComputedStyle(el.closest('.graph-node')).backgroundColor
  }));
  assert.equal(visual.animation,'none');
  assert.ok(visual.tag.startsWith('rgb('));
  const map=p.locator('#graph-map');
  const style=await map.evaluate(el=>getComputedStyle(el).touchAction);
  assert.ok(style.includes('pan-y')&&style.includes('pinch-zoom'));
  await map.focus();await p.keyboard.press('ArrowRight');
  assert.equal(await p.locator('#graph-surface').evaluate(el=>new DOMMatrixReadOnly(getComputedStyle(el).transform).e),20);
 }finally{await close(f);}
});
test('consulted constellation nodes do not collide from 320px through desktop widths',async()=>{
 const f=await fixture({viewport:{width:900,height:700},reduced:true});try{
  const p=f.page;await consult(p);await p.locator('#top-graph').click();
  for(const size of [{width:900,height:700},{width:390,height:844},{width:360,height:844},{width:350,height:844},{width:340,height:844},{width:320,height:844},{width:390,height:844}]){
   await p.setViewportSize(size);
   await p.waitForTimeout(320); // Wait for stellar node position transition.
   const nodes=await p.locator('.graph-node').evaluateAll(items=>items.map(n=>{
    const r=n.getBoundingClientRect();
    return {label:n.textContent.trim().replace(/\s+/g,' '),x:r.x,y:r.y,right:r.right,bottom:r.bottom};
   }));
   assert.equal(nodes.length,8,'4 DEMO + hub + consulted source/conversation/manual nodes');
   const overlaps=[];
   for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){
    const a=nodes[i],b=nodes[j];
    const dx=Math.min(a.right,b.right)-Math.max(a.x,b.x);
    const dy=Math.min(a.bottom,b.bottom)-Math.max(a.y,b.y);
    if(dx>0.5&&dy>0.5)overlaps.push({a:a.label,b:b.label,width:+dx.toFixed(2),height:+dy.toFixed(2)});
   }
   assert.deepEqual(overlaps,[],'node overlap at '+size.width+'x'+size.height);
   // Em 320–350 px, os cartões devem permanecer inteiros dentro do mapa ampliado.
   if(size.width<=350){
    assert.equal(await p.locator('#graph-map').getAttribute('data-layout'),'narrow-consulted');
    const map=await p.locator('#graph-map').boundingBox();
    assert.ok(map.height>=539,'narrow map must grow instead of shrinking labels');
    const outside=nodes.filter(n=>n.x<map.x-1||n.right>map.x+map.width+1||n.y<map.y-1||n.bottom>map.y+map.height+1);
    assert.deepEqual(outside,[],'no clipped nodes at '+size.width+'x'+size.height);
   }else{
    assert.equal(await p.locator('#graph-map').getAttribute('data-layout'),'default');
   }
  }
 }finally{await close(f);}
});
test('graph resize within same layout preserves node DOM and keyboard focus',async()=>{
 const f=await fixture({mobile:true,reduced:true});try{
  const p=f.page;await p.locator('#rail-graph').click();
  const node=p.locator('.graph-node').first();
  const id=await node.getAttribute('data-node');
  await node.focus();
  await node.evaluate(el=>{el.dataset.resizeSentinel='retained';});
  for(const size of [{width:390,height:800},{width:400,height:800},{width:390,height:844}]){
   await p.setViewportSize(size);
   await p.waitForTimeout(50);
   assert.equal(await p.locator('.graph-node').first().getAttribute('data-resize-sentinel'),'retained',
    'resize without layout transition must not destroy node DOM');
   assert.equal(await p.evaluate(()=>document.querySelector('.ob-wrap').shadowRoot.activeElement?.dataset.node),id,
    'resize without layout transition must retain keyboard focus');
   assert.equal(await p.locator('#graph-map').getAttribute('data-layout'),'default');
  }
 }finally{await close(f);}
});

test('stellar graph heading, filters and map never overlap in responsive viewports',async()=>{
 const f=await fixture({viewport:{width:900,height:700},reduced:true});try{
  const p=f.page;await p.locator('#top-graph').click();
  for(const size of [
   {width:1550,height:870},{width:1440,height:900},
   {width:1200,height:850},{width:900,height:700},
   {width:820,height:700},{width:700,height:760},
   {width:600,height:700},{width:581,height:700},
   {width:580,height:844},{width:390,height:844}
  ]){
   await p.setViewportSize(size);
   const layout=await p.evaluate(()=>{
    const shadow=document.querySelector('section.ob-wrap').shadowRoot;
    const rect=selector=>{
     const r=shadow.querySelector(selector).getBoundingClientRect();
     return {top:r.top,bottom:r.bottom,left:r.left,right:r.right};
    };
    return {description:rect('#scene-description'),tools:rect('.graph-tools'),map:rect('#graph-map')};
   });
   assert.ok(layout.tools.top-layout.description.bottom>=7,
    'description overlaps filters at '+size.width+'x'+size.height+': '+JSON.stringify(layout));
   assert.ok(layout.map.top-layout.tools.bottom>=7,
    'filters overlap map at '+size.width+'x'+size.height+': '+JSON.stringify(layout));
  }
 }finally{await close(f);}
});
