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
activate(host);window.fixtureReady=true;</script></body></html>`;
const artifacts='test-artifacts/graph';mkdirSync(artifacts,{recursive:true});
let browser;
test.before(async()=>{browser=await chromium.launch({headless:true,chromiumSandbox:true});});
test.after(async()=>{await browser?.close();});
async function fixture({mobile=false,reduced=false}={}){
 const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},reducedMotion:reduced?'reduce':'no-preference',serviceWorkers:'block'});
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
   HTMLCanvasElement.prototype.getContext=function(type,...args){return type==='webgl2'?null:get.call(this,type,...args);};
   const request=window.requestAnimationFrame.bind(window),cancel=window.cancelAnimationFrame.bind(window);
   window.fixtureFrames=new Set();window.requestAnimationFrame=fn=>{let id=request(time=>{window.fixtureFrames.delete(id);fn(time);});window.fixtureFrames.add(id);return id;};
   window.cancelAnimationFrame=id=>{window.fixtureFrames.delete(id);cancel(id);};
   const Observer=window.ResizeObserver;window.fixtureObservers=new Set();
   window.ResizeObserver=class extends Observer{observe(...args){window.fixtureObservers.add(this);return super.observe(...args);}disconnect(){window.fixtureObservers.delete(this);return super.disconnect();}};
 });
 await page.goto(origin+'/');await page.waitForFunction(()=>window.fixtureReady);
 return {page,context,unexpected};
}
async function close(f){assert.deepEqual(f.unexpected,[],'unexpected external request');await f.context.close();}
async function consult(page){await page.locator('details.ob-real summary').click();await page.locator('input.id').fill('00000000-0000-4000-8000-000000000001');await page.locator('button').filter({hasText:'Consultar estado no OpenHands'}).click();await page.locator('#source-banner').filter({hasText:'1 MISSÃO'}).waitFor();}
test('open, keyboard select/deselect, focus survives DOM replacement',async()=>{
 const f=await fixture();try{const p=f.page;await p.locator('#top-graph').click();const node=p.locator('.graph-node').first();await node.focus();await p.keyboard.press('Enter');assert.equal(await p.locator('.graph-node[aria-pressed=true]').count(),1);assert.equal(await p.evaluate(()=>document.querySelector('.ob-wrap').shadowRoot.activeElement?.dataset.node),await p.locator('.graph-node[aria-pressed=true]').getAttribute('data-node'));await p.keyboard.press('Enter');assert.equal(await p.locator('.graph-node[aria-pressed=true]').count(),0);await p.keyboard.press('Escape');assert.equal(await p.locator('.graph-node[aria-pressed=true]').count(),0);await p.screenshot({path:artifacts+'/graph-desktop.png',fullPage:true});}finally{await close(f);}
});
test('project navigation, demo source, search and empty filter keep search focus',async()=>{
 const f=await fixture();try{const p=f.page;await p.locator('.system-tile').first().click();assert.ok((await p.locator('#scene-title').innerText()).includes('Sistema solar'));await p.locator('#top-universe').click();assert.equal(await p.locator('.system-tile').count(),4);await p.locator('#top-graph').click();assert.equal(await p.locator('.graph-node').count(),5);await p.locator('#graph-search').fill('NOT_FOUND_SYNTHETIC');await p.locator('.graph-empty').waitFor();assert.equal(await p.evaluate(()=>document.querySelector('.ob-wrap').shadowRoot.activeElement?.id),'graph-search');await p.locator('#graph-search').fill('');await p.locator('#graph-scope').selectOption('verified');assert.equal(await p.locator('.graph-node').count(),0);}finally{await close(f);}
});
test('synthetic consulted source remains distinct from manual and errors create no new observation',async()=>{
 const f=await fixture();try{const p=f.page;await consult(p);await p.locator('#top-graph').click();await p.locator('#graph-scope').selectOption('verified');assert.equal(await p.locator('.graph-node').count(),3);assert.equal(await p.locator('.graph-node[data-kind=manual]').count(),1);assert.equal(await p.locator('.graph-edges line[data-kind=verified]').count(),1);assert.equal(await p.locator('.graph-edges line[data-kind=manual]').count(),1);assert.deepEqual(await p.evaluate(()=>window.fixtureReads),[{method:'GET',path:'/api/conversations/00000000-0000-4000-8000-000000000001'}]);}finally{await close(f);}
 const bad=await fixture();try{await bad.page.evaluate(()=>window.fixtureError=true);await bad.page.locator('details.ob-real summary').click();await bad.page.locator('input.id').fill('00000000-0000-4000-8000-000000000001');await bad.page.getByText('Consultar estado no OpenHands',{exact:true}).click();await bad.page.locator('output').filter({hasText:'desconhecido'}).waitFor();await bad.page.locator('#top-graph').click();assert.equal(await bad.page.locator('.graph-node[data-kind=verified]').count(),0);}finally{await close(bad);}
});
test('mobile/reduced-motion, zoom and keyboard pan are bounded and resettable',async()=>{
 const f=await fixture({mobile:true,reduced:true});try{const p=f.page;await p.locator('#rail-graph').click();assert.ok(await p.locator('#graph-search').isVisible());const intro=await p.locator('.scene-heading').boundingBox(),tools=await p.locator('.graph-tools').boundingBox(),map=await p.locator('#graph-map').boundingBox();assert.ok(tools.y>=intro.y+intro.height+8,'mobile controls must not overlap heading');assert.ok(map.y>=tools.y+tools.height+8,'mobile map must not overlap controls');await p.locator('#zoom-in').click();assert.notEqual(await p.locator('#graph-surface').evaluate(e=>getComputedStyle(e).transform),'matrix(1, 0, 0, 1, 0, 0)');await p.locator('#graph-map').focus();await p.keyboard.press('ArrowRight');assert.ok((await p.locator('#graph-surface').getAttribute('style')).includes('translate('));await p.locator('#zoom-reset').click();assert.deepEqual(await p.locator('#graph-surface').evaluate(e=>{const m=new DOMMatrixReadOnly(getComputedStyle(e).transform);return [m.a,m.d,m.e,m.f];}),[1,1,0,0]);assert.equal(await p.locator('#graph-surface').evaluate(e=>getComputedStyle(e).transitionDuration),'0s');const box=await p.locator('#graph-map').boundingBox();assert.ok(box.width>200&&box.height>100);await p.locator('#graph-map').focus();for(let i=0;i<20;i++)await p.keyboard.press('ArrowRight');assert.equal(await p.locator('#graph-surface').evaluate(e=>new DOMMatrixReadOnly(getComputedStyle(e).transform).e),140);await p.locator('#zoom-reset').click();await p.mouse.move(box.x+8,box.y+8);await p.mouse.down();await p.mouse.move(box.x+48,box.y+8);await p.mouse.up();assert.equal(await p.locator('#graph-surface').evaluate(e=>new DOMMatrixReadOnly(getComputedStyle(e).transform).e),40);await p.locator('#zoom-reset').click();assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await p.screenshot({path:artifacts+'/graph-mobile.png',fullPage:true});}finally{await close(f);}
});
test('content is escaped and graph text has contrast on declared solid background',async()=>{
 const f=await fixture();try{await f.page.locator('#top-graph').click();const colors=await f.page.locator('.graph-node small').first().evaluate(e=>({fg:getComputedStyle(e).color,bg:getComputedStyle(e.parentElement).backgroundColor}));const luminance=s=>{const c=s.match(/[\d.]+/g).slice(0,3).map(Number).map(n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;});return .2126*c[0]+.7152*c[1]+.0722*c[2];};assert.ok((luminance(colors.fg)+.05)/(luminance(colors.bg)+.05)>=4.5);assert.equal(await f.page.locator('#graph-map').getAttribute('aria-label'),'Nós e conexões entre projetos e execuções');assert.equal(await f.page.locator('html').getAttribute('lang'),'pt-BR');await f.page.locator('#top-universe').click();await f.page.evaluate(()=>fixtureObservation.execution_status='<img src=\"https://unexpected.invalid\">');await consult(f.page);await f.page.locator('#top-graph').click();assert.equal(await f.page.locator('#graph img').count(),0);await f.page.locator('.graph-node[data-kind=verified]').last().click();assert.equal(await f.page.locator('#panel-content img').count(),0);}finally{await close(f);}
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
