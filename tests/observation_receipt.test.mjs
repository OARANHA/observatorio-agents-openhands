// Contract tests load the function from the real extension template, without HTTP/Canvas.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const template=readFileSync(new URL('../scripts/extension-template.txt',import.meta.url),'utf8');
const begin=template.indexOf('function formatObservationReceipt(');
const end=template.indexOf('function mountRealRead(',begin);
assert.ok(begin>=0&&end>begin,'receipt helper must exist in the official template');
const receipt=vm.runInNewContext(template.slice(begin,end)+';formatObservationReceipt');
const id='00000000-0000-4000-8000-000000000001';
test('receipt includes source and explicit manual/unverified semantics but no private extras',()=>{
 const result=receipt(id,'org/projeto',{status:'finished',updatedAt:'2026-10-12T10:00:00Z',token:'PRIVATE'},'2026-10-12T10:01:00Z');
 assert.match(result,/OpenHands Agent Server/);
 assert.match(result,/Projeto declarado manualmente/);
 assert.match(result,/não comprovados/);
 assert.doesNotMatch(result,/PRIVATE/);
});
test('invalid identifiers, project, status and observation time fail closed',()=>{
 for(const args of [
 ['invalid','org/projeto',{status:'finished'},'2026-10-12T10:01:00Z'],
 [id,'invalid',{status:'finished'},'2026-10-12T10:01:00Z'],
 [id,'org/projeto',{status:'finished\n'},'2026-10-12T10:01:00Z'],
 [id,'org/projeto',{status:'finished'},'yesterday']
 ])assert.equal(receipt(...args),null);
});
test('missing server timestamp is not fabricated',()=>{
 assert.match(receipt(id,'org/projeto',{status:'running',updatedAt:null},'2026-10-12T10:01:00Z'),/Atualizado no servidor: não informado/);
});
