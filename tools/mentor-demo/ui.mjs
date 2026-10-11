// Standalone Shadow DOM demo. Never activated by the Canvas extension.
import {createMentorDemoSession} from './model.mjs';
export function mountMentorDemo(container,options={}){
 const {mode='ready',delay=0,project='synthetic/alpha',context=crypto.randomUUID()}=options;
 if(Object.keys(options).some(k=>!['mode','delay','project','context'].includes(k))||!['ready','empty','error'].includes(mode))throw Error('mentor_demo_denied');
 const host=document.createElement('section');container.append(host);
 const root=host.attachShadow({mode:'open'});let disposed=false,session=null;
 root.innerHTML=`<style>
 :host{display:block;color:#eaf0ff;font:16px/1.5 system-ui,sans-serif;background:#111827;padding:clamp(16px,4vw,36px);border-radius:16px}
 *{box-sizing:border-box}h1{font-size:clamp(1.5rem,4vw,2.2rem);margin:0 0 12px}h2{font-size:1.15rem}p{margin:10px 0}.badge{color:#c4b5fd;font-weight:700}
 .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:16px}.card{background:#1f2937;border:1px solid #64748b;border-radius:12px;padding:16px}
 button{font:inherit;background:#c4b5fd;color:#111827;border:2px solid transparent;border-radius:8px;padding:10px 16px;min-height:44px;cursor:pointer}
 button:disabled{background:#475569;color:#e2e8f0;cursor:default}button.secondary{background:#334155;color:#fff;border-color:#94a3b8}
 :focus-visible{outline:3px solid #facc15;outline-offset:3px}label{display:flex;align-items:center;gap:10px;margin:12px 0;min-height:44px}input{width:20px;height:20px;accent-color:#c4b5fd}
 pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.6 ui-monospace,monospace;background:#111827;color:#eaf0ff;padding:12px;border-radius:8px}
 dialog{color:#eaf0ff;background:#1f2937;border:2px solid #a78bfa;border-radius:12px;max-width:560px;width:calc(100% - 24px);max-height:90vh;overflow:auto;padding:20px}dialog::backdrop{background:#000b}
 .actions{display:flex;flex-wrap:wrap;gap:12px}.small{font-size:.875rem;color:#cbd5e1;overflow-wrap:anywhere}.result{border-left:4px solid #facc15;padding-left:12px}
 @media(prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
 </style>
 <header><p class="badge">OBSERVATÓRIO · DEMO HORIZONTAL</p><h1>Chamar Mentor</h1>
 <p>Simulação offline. Nenhuma presença real do ChatGPT, mensagem ao OpenHands ou autorização de agente.</p></header>
 <div class="grid"><section class="card" aria-labelledby="conversation"><h2 id="conversation">Conversa fictícia</h2>
 <p data-state role="status" aria-live="polite">Preparando fixture…</p><p data-project></p>
 <p class="small">Origem: fixture sintética. Projeto declarado. Identidade composta da visão local; sem RBAC ou autenticação de projeto.</p></section>
 <section class="card" aria-labelledby="events"><h2 id="events">Evento e evidência</h2><p data-event></p>
 <p class="small">DEMO-001 · needs_review · Fonte declarada, sem prova operacional.</p></section></div>
 <p data-scope class="small"></p><p><button data-open disabled>Chamar Mentor (DEMO)</button></p>
 <section aria-labelledby="recommendation"><h2 id="recommendation">Orientação</h2><p data-result class="result" role="status" aria-live="polite">Nenhuma orientação gerada.</p></section>
 <dialog aria-labelledby="review-heading"><h2 id="review-heading">Revisar contexto fictício</h2>
 <p>Veja exatamente o contexto da simulação. Exclua campos antes de gerar uma recomendação local.</p>
 <label><input data-field="status" type="checkbox" checked> Estado fictício</label>
 <label><input data-field="event" type="checkbox" checked> Tipo de evento fictício</label>
 <label><input data-field="project" type="checkbox"> Projeto declarado fictício</label>
 <p class="small">Notas, prompts, credenciais e dados privados não são aceitos nem compartilhados. Não há envio externo.</p>
 <pre data-context aria-label="Contexto exato da simulação"></pre>
 <label><input data-consent type="checkbox"> Revisei este contexto fictício</label>
 <p data-pending role="status" aria-live="polite"></p>
 <div class="actions"><button data-generate disabled>Gerar orientação fictícia</button><button class="secondary" data-cancel>Cancelar</button></div></dialog>`;
 const el=selector=>root.querySelector(selector),dialog=el('dialog'),open=el('[data-open]');
 const fields=[...root.querySelectorAll('[data-field]')],consent=el('[data-consent]'),generate=el('[data-generate]');
 const update=()=>{
  if(disposed||!session)return;
  try{el('[data-context]').textContent=JSON.stringify(session.review(fields.filter(x=>x.checked).map(x=>x.dataset.field)),null,2);consent.checked=false;generate.disabled=true;}
  catch{el('[data-pending]').textContent='Simulação encerrada.';generate.disabled=true;}
 };
 open.addEventListener('click',()=>{if(disposed||!session)return;update();dialog.showModal();fields[0].focus();});
 fields.forEach(field=>field.addEventListener('change',update));
 consent.addEventListener('change',()=>{generate.disabled=!consent.checked||session?.state!=='reviewed';});
 const cancel=()=>{session?.close();open.disabled=true;dialog.close();el('[data-result]').textContent='Simulação cancelada. Nenhuma instrução foi enviada.';el('[data-result]').tabIndex=-1;el('[data-result]').focus();};
 el('[data-cancel]').addEventListener('click',cancel);
 dialog.addEventListener('cancel',()=>{cancel();});
 // Chromium can leave a Shadow DOM dialog at a Tab boundary. Keep focus on
 // enabled controls explicitly; Escape still uses the native cancel event.
 dialog.addEventListener('keydown',event=>{
  if(event.key!=='Tab')return;
  const controls=[...dialog.querySelectorAll('input,button')].filter(x=>!x.disabled&&!x.hidden);
  if(!controls.length)return;
  event.preventDefault();const current=controls.indexOf(root.activeElement);
  const next=current<0?(event.shiftKey?controls.length-1:0):
   (current+(event.shiftKey?-1:1)+controls.length)%controls.length;
  controls[next].focus();
 });
 generate.addEventListener('click',async()=>{
  if(disposed||!session)return;
  generate.disabled=true;consent.disabled=true;fields.forEach(x=>x.disabled=true);el('[data-pending]').textContent='Gerando somente uma orientação fictícia…';
  try{
   const result=await session.recommend(consent.checked===true);
   if(disposed||!host.isConnected)return;
   el('[data-result]').textContent=result.recommendation;dialog.close();open.disabled=true;
   el('[data-result]').tabIndex=-1;el('[data-result]').focus();
  }catch{if(!disposed&&host.isConnected){el('[data-pending]').textContent='Simulação encerrada; sem fallback.';generate.disabled=true;}}
 });
 (async()=>{
  if(mode!=='ready'){
   el('[data-state]').textContent=mode==='empty'?'Sem conversa na fixture.':'Erro fictício: fonte indisponível.';
   el('[data-event]').textContent='Sem eventos disponíveis.';return;
  }
  try{
   const created=await createMentorDemoSession({context,project,delay});
   if(disposed){created.close();return;}
   session=created;el('[data-state]').textContent='Estado fictício: paused';el('[data-project]').textContent='Projeto declarado: '+project;
   el('[data-event]').textContent='Evento fictício: needs_review / blocked';
   el('[data-scope]').textContent='Identidade local DEMO: '+session.identity.mission;open.disabled=false;
  }catch{if(!disposed){el('[data-state]').textContent='Erro fictício: configuração recusada.';}}
 })();
 return ()=>{if(disposed)return;disposed=true;session?.close();if(dialog.open)dialog.close();host.remove();};
}
