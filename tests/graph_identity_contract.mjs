import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {webcrypto} from 'node:crypto';
import vm from 'node:vm';
const src=readFileSync(new URL('../source/observatorio-v02.html',import.meta.url),'utf8');
const stateLabelStart=src.indexOf('function realMissionStateLabel(status){');
assert.ok(stateLabelStart>=0,'real mission status formatter missing');
const stateLabel=src.slice(stateLabelStart,src.indexOf('function clearConsultedObservation(){',stateLabelStart));
const start=src.indexOf('async function graphIdentityForObservation(');
const identity=start<0?'':src.slice(start,src.indexOf('function validGraphIdentity(',start));
const validation=start<0?'':src.slice(src.indexOf('function validGraphIdentity('),src.indexOf('function graphModel(narrowConsulted=false){'));
const modelCode=src.slice(src.indexOf('function graphModel(narrowConsulted=false){'),src.indexOf('function renderGraphPanel(){'));
const ctx=vm.createContext({crypto:webcrypto,TextEncoder,defs:Object.fromEntries(['one','two','three','four'].map(k=>[k,{name:k}])),verifiedMission:null});
vm.runInContext(stateLabel+identity+validation+modelCode,ctx);
const context='00000000-0000-4000-8000-000000000010',cid='00000000-0000-4000-8000-000000000001';
async function ids(contextValue=context,conversation=cid,project='synthetic/repo'){
 assert.equal(vm.runInContext('typeof graphIdentityForObservation',ctx),'function','identity contract missing');
 ctx.args=[contextValue,conversation,project];return JSON.parse(JSON.stringify(await vm.runInContext('graphIdentityForObservation(...args)',ctx)));
}
function model(graphIdentity,narrow=false){ctx.verifiedMission={conversationId:cid,status:'finished',project:'synthetic/repo',graphIdentity};return JSON.parse(vm.runInContext('JSON.stringify(graphModel('+String(Boolean(narrow))+'))',ctx));}
const real=m=>m.nodes.filter(n=>!n.kind.startsWith('demo'));
 test('same context and input produce deterministic ids',async()=>assert.deepEqual(await ids(),await ids()));
 test('different conversations cannot reuse conversation or manual identities',async()=>{const a=await ids(),b=await ids(context,'00000000-0000-4000-8000-000000000002');assert.notEqual(a.mission,b.mission);assert.notEqual(a.project,b.project);assert.equal(a.source,b.source);});
 test('local view context isolates projections without tenant claim',async()=>{const a=await ids(),b=await ids('00000000-0000-4000-8000-000000000011');assert.ok(['source','mission','project'].every(k=>a[k]!==b[k]));assert.equal(a.scope,'local-view-not-tenant');});
 test('manual project switch changes only manual relation identity',async()=>{const a=await ids(),b=await ids(context,cid,'other/repo');assert.equal(a.source,b.source);assert.equal(a.mission,b.mission);assert.notEqual(a.project,b.project);});
 test('ids contain no raw conversation or repository label',async()=>{for(const value of Object.values(await ids())){assert.ok(!value.includes(cid));assert.ok(!value.includes('synthetic/repo'));}});
 test('missing context omits consulted nodes instead of inventing provenance',()=>assert.equal(real(model(undefined)).length,0));
 test('malformed or cross-kind references cannot create consulted edges',async()=>{const a=await ids(),b=await ids('00000000-0000-4000-8000-000000000011');for(const bad of [{...a,mission:b.mission},{...a,source:a.project},{...a,mission:a.source},{...a,scope:'authenticated-tenant'}]){const m=model(bad);assert.equal(real(m).length,0);assert.ok(m.edges.every(e=>e.kind==='demo'));}});
 test('invalid identity input rejected and valid edges resolve distinctly',async()=>{for(const args of [['',cid,'synthetic/repo'],[context,'invalid','synthetic/repo'],[context,cid,'invalid']])await assert.rejects(()=>ids(...args));const m=model(await ids());assert.equal(real(m).length,3);assert.equal(new Set(m.nodes.map(n=>n.id)).size,m.nodes.length);const n=new Set(m.nodes.map(n=>n.id));assert.ok(m.edges.every(e=>n.has(e.from)&&n.has(e.to)));assert.equal(real(m).find(n=>n.role==='project').kind,'manual');});
test('responsive layout parameter never bypasses the identity guard',async()=>{const good=await ids();for(const invalid of [undefined,{...good,scope:'authenticated-tenant'}]){const narrow=model(invalid,true);assert.equal(real(narrow).length,0);assert.ok(narrow.edges.every(e=>e.kind==='demo'));assert.equal(narrow.narrowConsulted,false);}const wide=model(good,false),narrow=model(good,true);assert.equal(real(wide).length,3);assert.equal(real(narrow).length,3);assert.equal(narrow.narrowConsulted,true);assert.deepEqual(new Set(wide.nodes.map(x=>x.id)),new Set(narrow.nodes.map(x=>x.id)));assert.deepEqual(wide.edges,narrow.edges);});
