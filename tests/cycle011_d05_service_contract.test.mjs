// Offline structural fixture derived from reviewed ConversationService._search_conversations.
// NOT an execution of upstream Python and NOT an authorization implementation.
import test from 'node:test';
import assert from 'node:assert/strict';
function searchCatalog(records,{status=null,limit=2,pageId=null}={}){
 const rows=records.filter(x=>status===null||x.status===status)
  .sort((a,b)=>b.createdAt-a.createdAt);
 let start=0;
 if(pageId){const i=rows.findIndex(x=>x.id===pageId);if(i>=0)start=i;}
 const items=rows.slice(start,start+limit);
 const nextPageId=rows[start+limit]?.id??null;
 return {items,nextPageId};
}
const records=[
 {id:'A',project:'alpha',status:'idle',createdAt:3},
 {id:'B',project:'beta',status:'running',createdAt:2},
 {id:'C',project:'alpha',status:'idle',createdAt:1}
];
test('structural catalog fixture sorts and pages without project input',()=>{
 const first=searchCatalog(records,{limit:2});
 assert.deepEqual(first.items.map(x=>x.id),['A','B']);
 assert.equal(first.nextPageId,'C');
 assert.deepEqual(searchCatalog(records,{pageId:first.nextPageId,limit:2}).items.map(x=>x.id),['C']);
});
test('status filtering does not imply authorization: cross-project fixture records coexist',()=>{
 const page=searchCatalog(records,{limit:3});
 assert.deepEqual(new Set(page.items.map(x=>x.project)),new Set(['alpha','beta']));
 const idle=searchCatalog(records,{status:'idle',limit:3});
 assert.deepEqual(idle.items.map(x=>x.id),['A','C']);
});
test('project labels are ignored by reviewed signature fixture',()=>{
 const page=searchCatalog(records,{project:'alpha',limit:3});
 assert.equal(page.items.some(x=>x.project==='beta'),true);
});
