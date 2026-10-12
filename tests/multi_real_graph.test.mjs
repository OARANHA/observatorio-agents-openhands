import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const html=readFileSync(new URL('../source/observatorio-v02.html',import.meta.url),'utf8');
const template=readFileSync(new URL('../scripts/extension-template.txt',import.meta.url),'utf8');
const ext=readFileSync(new URL('../extension.js',import.meta.url),'utf8');

test('graph holds only explicitly verified observations and bounds visible missions',()=>{
 for(const s of [html,ext]){
  assert.match(s,/verifiedMissions=\[verifiedMission,\.\.\.verifiedMissions\.filter/);
  assert.match(s,/\.slice\(0,20\)/);
  assert.match(s,/verifiedMissions\.filter\(v=>validGraphIdentity\(v\.graphIdentity\)\)\.slice\(0,5\)/);
  assert.match(s,/recent\.forEach\(\(v,i\)=>/);
  assert.match(s,/conversationId:v\.conversationId/);
  assert.match(s,/if\(i===0\)nodes\.push\(\{id:ids\.source/);
  assert.match(s,/edges\.push\(\{from:ids\.mission,to:ids\.project,kind:'manual'\}\)/);
  assert.match(s,/function forgetConsultedObservation\(id\)/);
 }
});
test('each new authorized read invalidates only its UUID and graph list never floats atop graph',()=>{
 for(const s of [template,ext]){
  assert.match(s,/onReset\(id\)/);
  assert.match(s,/\.graph-active \.ob-task-list\{position:relative!important/);
 }
 assert.match(ext,/id=>forgetConsultedObservation\(id\)/);
});

test('reorganization retains manual dragging controls',()=>{
 assert.match(html,/function reorganizeGraph\(\)/);
 assert.match(html,/graphNodePositions\.clear\(\)/);
 assert.match(html,/graph-organize/);
 assert.match(ext,/reorganizeGraph/);
});
