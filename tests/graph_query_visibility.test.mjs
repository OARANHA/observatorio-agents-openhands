import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
for(const path of ['scripts/extension-template.txt','extension.js']){
  test('graph keeps collapsed real conversation query visible: '+path,()=>{
    const s=readFileSync(new URL('../'+path,import.meta.url),'utf8');
    assert.match(s,/\.graph-active \.ob-real:not\(\[open\]\)\{display:block;top:145px;right:18px\}/);
    assert.doesNotMatch(s,/\.graph-active \.ob-real:not\(\[open\]\)\{display:none\}/);
    assert.match(s,/<summary>☾ CONSULTA DE CONVERSA<\/summary>/);
    assert.match(s,/host\.agentServer\.request\(\{method:'GET',path:'\/api\/conversations\/'\+id\}\)/);
  });
}
