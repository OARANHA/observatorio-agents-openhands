import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const html=readFileSync(new URL('../source/observatorio-v02.html',import.meta.url),'utf8');
const ext=readFileSync(new URL('../extension.js',import.meta.url),'utf8');
const template=readFileSync(new URL('../scripts/extension-template.txt',import.meta.url),'utf8');

test('real states are labeled without equating finished to success',()=>{
 for(const s of [html,ext]){
  assert.match(s,/function realMissionStateLabel\(status\)/);
  for(const value of ['AGUARDANDO APROVAÇÃO','EM EXECUÇÃO','ENCERRADA (SUCESSO NÃO ATESTADO)','ERRO INFORMADO']){
   assert.ok(s.includes(value),value);
  }
  assert.match(s,/tag:realMissionStateLabel\(verifiedMission\.status\)/);
  assert.match(s,/safe\(realMissionStateLabel\(v\.status\)\)/);
  assert.match(s,/safe\(v\.title\|\|'Não informado pela API'\)/);
 }
});
test('title comes from validated point GET and is not hardcoded',()=>{
 for(const s of [ext,template]){
  assert.match(s,/title:verified\.title,project/);
  assert.match(s,/host\.agentServer\.request\(\{method:'GET',path:'\/api\/conversations\/'\+id\}\)/);
 }
 assert.doesNotMatch(html,/OBS-CONTROLE-001\|OK/);
});
