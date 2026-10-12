// Offline contract tests: no Canvas, HTTP, credentials, or real conversation data.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

const extension=readFileSync(new URL('../extension.js',import.meta.url),'utf8');
const functionSource=extension.match(/function validateConversationObservation\(item, expectedId\) \{[\s\S]*?\n\}/)?.[0];
assert.ok(functionSource,'built extension must include the validation contract');
const validate=runInNewContext(functionSource+'\nvalidateConversationObservation');

const uuid='00000000-0000-4000-8000-000000000001';
const valid={id:uuid,execution_status:'finished',updated_at:'2026-10-11T00:00:00Z'};
test('accepts matched conversation, returns minimal safe metadata',()=>{
 assert.deepEqual(JSON.parse(JSON.stringify(validate({...valid,secret:'PRIVATE'},uuid))),{status:'finished',updatedAt:'2026-10-11T00:00:00Z'});
});
test('rejects mismatched ID, missing status, empty status and control characters',()=>{
 for(const data of [{...valid,id:'another'},{id:uuid},{...valid,execution_status:''},{...valid,execution_status:'\nfinished'},{...valid,execution_status:1},{...valid,execution_status:'x'.repeat(129)}]){
  assert.equal(validate(data,uuid),null);
 }
});
test('invalid calendar days and out-of-range clock or timezone are not server timestamps',()=>{
 for(const updated_at of ['2026-02-30T00:00:00Z','2025-02-29T00:00:00Z','2026-13-01T00:00:00Z','2026-10-11T25:00:00Z','2026-10-11T00:60:00Z','2026-10-11T00:00:00+25:00']){
  assert.equal(validate({...valid,updated_at},uuid).updatedAt,null,updated_at);
 }
 assert.equal(validate({...valid,updated_at:'2024-02-29T12:30:00Z'},uuid).updatedAt,'2024-02-29T12:30:00Z');
});
test('malformed, missing and untrusted timestamps are not displayed as server time',()=>{
 for(const updated_at of ['yesterday','2026-99-99T00:00:00Z','2026-10-11','2026-10-11T00:00:00',1,null]){
  assert.equal(validate({...valid,updated_at},uuid).updatedAt,null);
 }
 assert.equal(validate({id:uuid,execution_status:'running'},uuid).updatedAt,null);
});
