import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const source=readFileSync(new URL('../scripts/extension-template.txt',import.meta.url),'utf8');
const begin=source.indexOf('function upsertObservedTask(');
const end=source.indexOf('function mountRealRead(',begin);
assert.ok(begin>=0&&end>begin);
const upsert=vm.runInNewContext(source.slice(begin,end)+';upsertObservedTask');
const make=(num,project='org/repo',status='running')=>({
 id:'00000000-0000-4000-8000-'+String(num).padStart(12,'0'),
 project,status,observedAt:'2026-10-12T18:00:00Z'
});
test('multiple explicitly obtained tasks are listed, newest first',()=>{
 const a=upsert([],make(1));const b=upsert(a,make(2));
 assert.equal(b.length,2);assert.equal(b[0].id,make(2).id);assert.equal(b[1].id,make(1).id);
});
test('same conversation updates state, never invents extra agents',()=>{
 const a=upsert([make(1)],make(1,'org/repo','finished'));
 assert.equal(a.length,1);assert.equal(a[0].status,'finished');
});
test('invalid input fails closed and stops at 20 entries',()=>{
 const bad={...make(1),status:'finished\nprivate'};
 assert.equal(upsert([make(2)],bad).length,1);
 let tasks=[];for(let n=1;n<=25;n++)tasks=upsert(tasks,make(n));
 assert.equal(tasks.length,20);assert.equal(tasks[0].id,make(25).id);
});
test('source is explicit-only, no background request or persistent storage added',()=>{
 const panel=source.slice(source.indexOf('function mountRealRead('),source.indexOf('function mountObservatorio('));
 assert.ok(panel.includes('upsertObservedTask('));
 assert.ok(panel.includes('observedTasks=[];panel.remove()'));
 assert.ok(!panel.includes('localStorage')&&!panel.includes('setInterval'));
});
