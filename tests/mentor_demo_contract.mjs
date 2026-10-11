import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const load=()=>import('../tools/mentor-demo/model.mjs');
const first='00000000-0000-4000-8000-000000000010';
const second='00000000-0000-4000-8000-000000000011';
test('review is required and no result authorizes operation',async()=>{
 const {createMentorDemoSession}=await load();const s=await createMentorDemoSession({context:first});
 await assert.rejects(()=>s.recommend(true),/mentor_demo_denied/);
 const v=await createMentorDemoSession({context:first});const c=v.review(['status','event']);
 assert.equal(c.classification,'demo');assert.equal(c.source,'synthetic_fixture');assert.equal(c.operational_go,false);
 assert.equal('project' in c,false);assert.equal('notes' in c,false);
 const r=await v.recommend(true);assert.equal(r.classification,'demo');assert.equal(r.operational_go,false);
 assert.equal(r.authorizes_agent,false);assert.equal('shared_context' in r,false);
});
test('context can be explicitly minimized and cannot include private or unknown fields',async()=>{
 const {createMentorDemoSession}=await load();const s=await createMentorDemoSession({context:first});
 const c=s.review([]);assert.deepEqual(Object.keys(c).sort(),['classification','operational_go','source']);
 for(const selection of [['notes'],['prompt'],['status','status'],'status']){
  const v=await createMentorDemoSession({context:first});assert.throws(()=>v.review(selection),/mentor_demo_denied/);
 }
});
test('approval must be literal and is never agent permission',async()=>{
 const {createMentorDemoSession}=await load();
 for(const value of [false,undefined,1,'yes']){
  const s=await createMentorDemoSession({context:first});s.review(['status']);
  await assert.rejects(()=>s.recommend(value),/mentor_demo_denied/);
 }
});
test('close during asynchronous recommendation prevents stale result',async()=>{
 const {createMentorDemoSession}=await load();const s=await createMentorDemoSession({context:first,delay:30});s.review(['status']);
 const pending=s.recommend(true);s.close();await assert.rejects(()=>pending,/mentor_demo_closed/);
 assert.equal(s.state,'closed');assert.throws(()=>s.review(['status']),/mentor_demo_denied/);
});
test('second request during pending work cancels both with no fallback',async()=>{
 const {createMentorDemoSession}=await load();const s=await createMentorDemoSession({context:first,delay:30});s.review(['status']);
 const a=s.recommend(true);await assert.rejects(()=>s.recommend(true),/mentor_demo_denied/);
 await assert.rejects(()=>a,/mentor_demo_closed/);
});
test('compound ids segregate local context and projects without tenant claims',async()=>{
 const {createMentorDemoSession}=await load();const a=await createMentorDemoSession({context:first,project:'synthetic/alpha'});
 const b=await createMentorDemoSession({context:second,project:'synthetic/alpha'});
 const c=await createMentorDemoSession({context:first,project:'synthetic/beta'});
 assert.notEqual(a.identity.mission,b.identity.mission);assert.notEqual(a.identity.project,c.identity.project);
 assert.equal(a.identity.scope,'local-view-not-tenant');assert.equal(a.observation.classification,'demo');
});
test('unknown configuration cannot admit live data or arbitrary delays',async()=>{
 const {createMentorDemoSession}=await load();
 for(const p of [{token:'SYNTHETIC'}, {project:'customer/private'}, {delay:251},{delay:true},{context:'live-context'}]){
  await assert.rejects(()=>createMentorDemoSession({context:first,...p}),/mentor_demo_denied/);
 }
});
test('frozen fixture cannot be replaced by source mutation',async()=>{
 const {createMentorDemoSession}=await load();const s=await createMentorDemoSession({context:first});
 assert.throws(()=>{s.observation.status='running';});assert.throws(()=>{s.identity.scope='authenticated_tenant';});
 const c=s.review(['project']);c.project='changed';assert.equal(s.context.project,'synthetic/alpha');
});
test('identity reuse is byte-for-byte frozen with public provenance',()=>{
 const body=readFileSync(new URL('../tools/mentor-demo/identity.mjs',import.meta.url),'utf8');
 const p=JSON.parse(readFileSync(new URL('../tools/mentor-demo/identity-provenance.json',import.meta.url),'utf8'));
 assert.equal(createHash('sha256').update(body).digest('hex'),p.sha256);
 assert.equal(p.source_head,'811d5fa4c48aa9eb2cf618174b7d645039a590ac');assert.equal(p.classification,'public_source_copy_not_deploy');
});
