// Real Chromium DOM against public fixtures only; all other requests denied.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync} from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.OBS_PLAYWRIGHT_MODULE||'playwright');
const source=readFileSync(new URL('../../tools/mentor-demo/index.html',import.meta.url),'utf8');
const origin='http://127.0.0.1:3998';
const artifacts='test-artifacts/mentor';mkdirSync(artifacts,{recursive:true});
let browser;
test.before(async()=>{browser=await chromium.launch({headless:true,chromiumSandbox:true});});
test.after(async()=>{await browser?.close();});
async function fixture({mobile=false,mode='ready',delay=0}={}){
 const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1280,height:1000},reducedMotion:'reduce',serviceWorkers:'block'});
 const unexpected=[];
 const options=JSON.stringify({mode,delay,context:'00000000-0000-4000-8000-000000000010'});
 const html=source.replace("mountMentorDemo(document.getElementById('mentor'));",`window.fixtureMount=(opts=${options})=>mountMentorDemo(document.getElementById('mentor'),opts);window.fixtureDispose=window.fixtureMount();window.fixtureReady=true;`);
 await context.route('**/*',async route=>{if(route.request().url()===origin+'/')return route.fulfill({contentType:'text/html',body:html});unexpected.push(route.request().url());return route.abort();});
 const page=await context.newPage();page.setDefaultTimeout(5000);
 await page.addInitScript(()=>{
  window.syntheticNetworkAttempts=0;const deny=()=>{window.syntheticNetworkAttempts++;throw Error('synthetic network denied');};
  window.fetch=deny;window.XMLHttpRequest=class{constructor(){deny();}};window.WebSocket=class{constructor(){deny();}};
  navigator.sendBeacon=deny;window.Worker=class{constructor(){deny();}};
 });
 await page.goto(origin+'/');await page.waitForFunction(()=>window.fixtureReady);
 if(mode==='ready')await page.getByRole('button',{name:'Chamar Mentor (DEMO)',exact:true}).waitFor({state:'visible'});
 return {page,context,unexpected,async close(){assert.deepEqual(unexpected,[]);assert.equal(await page.evaluate(()=>window.syntheticNetworkAttempts),0);await context.close();}};
}
async function readyOpen(page){const b=page.getByRole('button',{name:'Chamar Mentor (DEMO)',exact:true});await page.waitForFunction(()=>!document.querySelector('section').shadowRoot.querySelector('[data-open]').disabled);await b.click();}
function shadow(page,selector){return page.locator(selector);}
test('review shows exact minimized context, resets consent on changes, no permission or egress',async()=>{
 const f=await fixture();try{
  await readyOpen(f.page);const p=f.page;const preview=shadow(p,'[data-context]');
  let payload=JSON.parse(await preview.textContent());assert.equal(payload.classification,'demo');assert.equal(payload.project,undefined);assert.equal(payload.status,'paused');
  assert.equal(await p.getByRole('button',{name:'Gerar orientação fictícia'}).isEnabled(),false);
  await p.getByLabel('Projeto declarado fictício',{exact:true}).check();await p.getByLabel('Revisei este contexto fictício',{exact:true}).check();
  await p.getByLabel('Estado fictício',{exact:true}).uncheck();assert.equal(await p.getByLabel('Revisei este contexto fictício',{exact:true}).isChecked(),false);
  payload=JSON.parse(await preview.textContent());assert.equal(payload.status,undefined);assert.equal(payload.project,'synthetic/alpha');assert.equal(payload.operational_go,false);
  await p.getByLabel('Revisei este contexto fictício',{exact:true}).check();await p.getByRole('button',{name:'Gerar orientação fictícia'}).click();
  await p.getByText('Orientação fictícia: manter NO-GO',{exact:false}).waitFor();
  assert.equal(await p.getByRole('button',{name:'Chamar Mentor (DEMO)',exact:true}).isEnabled(),false);
  assert.equal(await p.evaluate(()=>document.querySelector('section').shadowRoot.activeElement?.hasAttribute('data-result')),true);
  await p.screenshot({path:artifacts+'/desktop.png',fullPage:true});
 }finally{await f.close();}
});
test('keyboard modal focus and Escape terminate simulation without instruction',async()=>{
 const f=await fixture();try{
  const p=f.page;await readyOpen(p);
  assert.equal(await p.evaluate(()=>document.querySelector('section').shadowRoot.activeElement?.dataset.field),'status');
  await p.keyboard.press('Shift+Tab');
  assert.equal(await p.evaluate(()=>document.querySelector('section').shadowRoot.activeElement?.hasAttribute('data-cancel')),true);
  for(let i=0;i<10;i++){await p.keyboard.press('Tab');assert.equal(await p.evaluate(()=>document.querySelector('section').shadowRoot.querySelector('dialog').contains(document.querySelector('section').shadowRoot.activeElement)),true);}
  await p.keyboard.press('Escape');assert.equal(await p.locator('dialog').evaluate(d=>d.open),false);
  assert.match(await p.locator('[data-result]').textContent(),/cancelada/);
  assert.equal(await p.getByRole('button',{name:'Chamar Mentor (DEMO)',exact:true}).isEnabled(),false);
 }finally{await f.close();}
});
test('empty and error states cannot request recommendation',async()=>{
 for(const mode of ['empty','error']){const f=await fixture({mode});try{
  assert.equal(await f.page.getByRole('button',{name:'Chamar Mentor (DEMO)',exact:true}).isEnabled(),false);
  assert.match(await f.page.locator('[data-state]').textContent(),mode==='empty'?/Sem conversa/:/Erro fictício/);
 }finally{await f.close();}}
});
test('pending teardown and remount ignore stale asynchronous completion',async()=>{
 const f=await fixture({delay:250});try{
  const p=f.page;await readyOpen(p);await p.getByLabel('Revisei este contexto fictício',{exact:true}).check();await p.getByRole('button',{name:'Gerar orientação fictícia'}).click();
  await p.evaluate(()=>{window.fixtureDispose();window.fixtureDispose();window.fixtureDispose=window.fixtureMount({mode:'empty'});});
  await p.waitForTimeout(300);assert.equal(await p.locator('main > section').count(),1);assert.match(await p.locator('[data-result]').textContent(),/Nenhuma orientação/);
  assert.equal(await p.getByRole('button',{name:'Chamar Mentor (DEMO)',exact:true}).isEnabled(),false);
 }finally{await f.close();}
});
test('mobile dialog fits viewport and controls have touch targets and visible focus',async()=>{
 const f=await fixture({mobile:true});try{
  const p=f.page;await readyOpen(p);
  const box=await p.locator('dialog').boundingBox();assert.ok(box.x>=0&&box.x+box.width<=391);assert.ok(box.height<=844);
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true);
  const target=await p.getByRole('button',{name:'Cancelar',exact:true}).boundingBox();assert.ok(target.height>=44);
  await p.keyboard.press('Tab');await p.keyboard.press('Shift+Tab');
  const outline=await p.locator('[data-field="status"]').evaluate(e=>getComputedStyle(e).outlineWidth);assert.equal(outline,'3px');
  await p.screenshot({path:artifacts+'/mobile-context.png',fullPage:true});
 }finally{await f.close();}
});
