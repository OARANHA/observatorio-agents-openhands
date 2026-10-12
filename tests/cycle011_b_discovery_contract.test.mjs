// CYCLE011-B offline model of a *proposed* list contract. Not a Canvas API implementation.
import test from 'node:test';
import assert from 'node:assert/strict';
const uuid=/^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i;
function evaluateSyntheticPage(response,authorizedRepository){
 if(typeof authorizedRepository!=='string'||!authorizedRepository)return null;
 if(!response||typeof response!=='object'||Array.isArray(response)||!Array.isArray(response.items)||response.items.length>20)return null;
 if(response.next_page_id!==null&&response.next_page_id!==undefined&&(typeof response.next_page_id!=='string'||response.next_page_id.length>256))return null;
 const ids=new Set(),items=[];
 for(const record of response.items){
  if(!record||typeof record!=='object'||Array.isArray(record)||!uuid.test(record.id)||typeof record.execution_status!=='string'||!record.execution_status.trim()||record.execution_status.length>128||/[\x00-\x1f\x7f]/.test(record.execution_status)||record.selected_repository!==authorizedRepository||ids.has(record.id))return null;
  ids.add(record.id);items.push({id:record.id,status:record.execution_status});
 }
 return {items,nextPageId:response.next_page_id??null};
}
const id='00000000-0000-4000-8000-000000000001',repo='acme/authorized';
const item={id,execution_status:'finished',selected_repository:repo,title:'PRIVATE',session_api_key:'SECRET'};
test('fixture minimizes fields and never propagates secret/title',()=>{
 assert.deepEqual(evaluateSyntheticPage({items:[item],next_page_id:null},repo),{items:[{id,status:'finished'}],nextPageId:null});
});
test('fixture denies cross-project and missing explicit scope',()=>{
 assert.equal(evaluateSyntheticPage({items:[item]},'other/repo'),null);
 assert.equal(evaluateSyntheticPage({items:[item]},''),null);
});
test('fixture denies invalid, duplicate, and excessively large pages',()=>{
 assert.equal(evaluateSyntheticPage({items:[item,item]},repo),null);
 assert.equal(evaluateSyntheticPage({items:[{...item,id:'bad'}]},repo),null);
 assert.equal(evaluateSyntheticPage({items:Array(21).fill(item)},repo),null);
 assert.equal(evaluateSyntheticPage({items:[item],next_page_id:42},repo),null);
});
test('V0 response format cannot be accidentally treated as V1',()=>{
 assert.equal(evaluateSyntheticPage({results:[{conversation_id:id}],next_page_id:null},repo),null);
});

test('fixture rejects control characters and excessively long statuses',()=>{
 assert.equal(evaluateSyntheticPage({items:[{...item,execution_status:String.fromCharCode(10)+'done'}]},repo),null);
 assert.equal(evaluateSyntheticPage({items:[{...item,execution_status:'x'.repeat(129)}]},repo),null);
});
test('fixture rejects non-array results and unexpected pagination token shapes',()=>{
 assert.equal(evaluateSyntheticPage({items:{}},repo),null);
 assert.equal(evaluateSyntheticPage({items:[item],next_page_id:'x'.repeat(257)},repo),null);
});
