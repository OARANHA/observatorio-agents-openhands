// Frozen PR7 pure function; inputs synthetic. No DOM, Canvas or network.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import vm from 'node:vm';
import test from 'node:test';
const code=readFileSync(new URL('./fixtures/pr7_graph_model.js',import.meta.url),'utf8');
const provenance=JSON.parse(readFileSync(new URL('./fixtures/pr7_graph_model_provenance.json',import.meta.url)));
const defs=Object.fromEntries(['one','two','three','four'].map(k=>[k,{name:'Synthetic '+k}]));
function model(mission=null,items=defs){
  const context=vm.createContext({defs:structuredClone(items),verifiedMission:mission&&structuredClone(mission)});
  return JSON.parse(vm.runInContext(code+';JSON.stringify(graphModel())',context,{timeout:1000}));
}
const mission={conversationId:'00000000-0000-4000-8000-000000000001',status:'finished',project:'synthetic/repo'};
test('frozen extraction integrity',()=>{
  assert.equal(createHash('sha256').update(code).digest('hex'),provenance.extracted_sha256);
  assert.equal(provenance.source_commit,'48f898d99a8979ef2c794513131506b028772666');
  assert.equal(provenance.synthetic_fixture_inputs,true);
});
test('without observation only demonstrations exist',()=>{
  const m=model();assert.equal(m.nodes.length,5);assert.equal(m.edges.length,4);
  assert.ok(m.nodes.every(n=>n.kind.startsWith('demo')));
  assert.ok(m.edges.every(e=>e.kind==='demo'));
});
test('source edge and manual association preserve distinct provenance',()=>{
  const m=model(mission);assert.equal(m.nodes.length,8);
  assert.deepEqual(m.edges.filter(e=>e.kind!=='demo'),[
    {from:'real-origin',to:'real-mission',kind:'verified'},
    {from:'real-mission',to:'manual-project',kind:'manual'}]);
  assert.equal(m.nodes.find(n=>n.id==='manual-project').kind,'manual');
});
test('finished conversation creates no agent or success assertion',()=>{
  const m=model(mission);assert.equal(m.nodes.find(n=>n.id==='real-mission').tag,'ESTADO: finished');
  assert.ok(m.nodes.every(n=>!Object.hasOwn(n,'agentId')&&!Object.hasOwn(n,'success')));
});
test('repeated projection stable; all edges resolve inside view',()=>{
  const m=model(mission);assert.deepEqual(model(mission),m);
  const ids=new Set(m.nodes.map(n=>n.id));assert.equal(ids.size,m.nodes.length);
  assert.ok(m.edges.every(e=>ids.has(e.from)&&ids.has(e.to)));
  assert.equal(model(null,{...defs,observado:{name:'Synthetic observed'}}).nodes.length,5);
});
test('characterizes unresolved cross-project collision without claiming isolation',()=>{
  const other={...mission,conversationId:'00000000-0000-4000-8000-000000000002',project:'other/repo'};
  const first=model(mission),second=model(other);
  assert.equal(first.nodes.find(n=>n.id==='manual-project').name,second.nodes.find(n=>n.id==='manual-project').name);
  assert.deepEqual(first.nodes.map(n=>n.id),second.nodes.map(n=>n.id));
  // This passing characterization preserves an OPEN GAP, not an RBAC guarantee.
});
