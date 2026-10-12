import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../scripts/extension-template.txt',import.meta.url),'utf8');
const generated=readFileSync(new URL('../extension.js',import.meta.url),'utf8');
test('recheck is explicit and uses the existing point-read handler',()=>{
 for(const code of [source,generated]){
  assert.match(code,/refresh\.textContent='Reconsultar agora'/);
  assert.match(code,/refresh\.addEventListener\('click'/);
  assert.match(code,/get\('\.id'\)\.value=task\.id/);
  assert.match(code,/get\('\.project'\)\.value=task\.project/);
  assert.match(code,/button\.click\(\)/);
  assert.match(code,/if\(!active\|\|button\.disabled\)return/);
 }
});
test('no implicit list/refresh request added',()=>{
 const start=source.indexOf('const renderTasks=()=>');
 const end=source.indexOf('clear.addEventListener',start);
 assert.ok(start>0&&end>start);
 const panel=source.slice(start,end);
 assert.doesNotMatch(panel,/agentServer\.request|fetch\(|setInterval|setTimeout/);
 assert.match(panel,/list\.append\(item\)/);
});
