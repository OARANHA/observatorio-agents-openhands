import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../scripts/extension-template.txt',import.meta.url),'utf8');
const built=readFileSync(new URL('../extension.js',import.meta.url),'utf8');

test('batch requires operator click and reuses the established individual GET',()=>{
 for(const s of [source,built]){
  assert.match(s,/consultAll\.addEventListener\('click',async\(\)=>/);
  assert.match(s,/const ids=parseExplicitConversationIds\(input\.value\)/);
  assert.match(s,/const ok=await consultOne\(\)/);
  assert.match(s,/if\(!ok\)/);
  assert.match(s,/batchRunning=true/);
  assert.match(s,/consultAll\.disabled=true/);
  assert.equal((s.match(/host\.agentServer\.request\(/g)||[]).length,1);
 }
});
test('batch is sequential, bounded and has no background discovery',()=>{
 const first=source.indexOf("consultAll.addEventListener('click'");
 const last=source.indexOf("  return ()=>{",first);
 const block=source.slice(first,last);
 assert.ok(first>0 && last>first);
 assert.doesNotMatch(block,/setInterval|fetch\(|search_conversations|list_conversations/);
 assert.match(block,/for\(const id of ids\)/);
 assert.match(block,/if\(!active\)break/);
 assert.match(source,/ids\.length>20/);
});
