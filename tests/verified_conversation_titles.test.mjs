import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

for (const name of ['scripts/extension-template.txt','extension.js']) {
 const code=readFileSync(new URL('../'+name,import.meta.url),'utf8');
 test(name+' preserves API-only optional title and provenance',()=>{
  assert.match(code,/typeof item\.title==='string'/);
  assert.match(code,/item\.title\.length<=160/);
  assert.match(code,/return \{status, updatedAt, title\}/);
  assert.match(code,/if\(verified\.title\)say\('Título recebido: ',verified\.title\)/);
  assert.match(code,/title:verified\.title/);
  assert.match(code,/task\.title\?task\.title/);
  assert.match(code,/Título informado pela API:/);
  assert.match(code,/Associação ao projeto: não verificada/);
  assert.equal((code.match(/host\.agentServer\.request\(/g)||[]).length,1);
 });
}
