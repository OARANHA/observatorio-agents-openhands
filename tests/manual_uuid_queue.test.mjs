import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const template=readFileSync(new URL('../scripts/extension-template.txt',import.meta.url),'utf8');
const begin=template.indexOf('function parseExplicitConversationIds(');
const end=template.indexOf('function mountRealRead(',begin);
assert.ok(begin>=0&&end>begin,'parser exists in template');
const parse=vm.runInNewContext(template.slice(begin,end)+';parseExplicitConversationIds');
const id1='00000000-0000-4000-8000-000000000001';
const id2='00000000-0000-4000-8000-000000000002';

test('accepts multiple explicitly supplied UUIDs and deduplicates',()=>{
 const ids=parse(id1+'\\n'+id2+', '+id1);
 assert.deepEqual(Array.from(ids),[id1,id2]);
});
test('fails closed for invalid items and oversized input',()=>{
 assert.equal(parse('bad').length,0);
 assert.equal(parse(id1+' not-an-id').length,0);
 assert.equal(parse((id1+' ').repeat(21)).length,0);
 assert.equal(parse('x'.repeat(2049)).length,0);
});
test('does not issue network requests when preparing local selection',()=>{
 const panel=template.slice(template.indexOf('const queue=document.createElement'),template.indexOf('const get=s=>detail.querySelector'));
 assert.match(panel,/parseExplicitConversationIds/);
 assert.doesNotMatch(panel,/agentServer\\.request|fetch\\(|setInterval/);
 assert.match(template,/queue\\.remove\\(\\)/);
});
