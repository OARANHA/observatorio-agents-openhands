import test from 'node:test';
import assert from 'node:assert/strict';
// Deliberately synthetic: no host/HTTP/credential access.
function allow(e) {
 return e?.installedVersionMatched===true &&
        e?.hostRouteProven===true &&
        e?.serverResourceAclProven===true &&
        e?.projectScopeProven===true &&
        e?.revocationProven===true &&
        e?.operatorApproved===true;
}
const valid={installedVersionMatched:true,hostRouteProven:true,serverResourceAclProven:true,projectScopeProven:true,revocationProven:true,operatorApproved:true};
test('upstream authentication never proves installed Canvas capability',()=>{
 assert.equal(allow({sessionKeyValid:true,upstreamSearchRoute:true}),false);
});
test('metadata and pagination cannot bypass server project ACL',()=>{
 assert.equal(allow({...valid,serverResourceAclProven:false,selected_repository:'project-A',page_id:'synthetic-cursor'}),false);
});
test('each independent proof must be present',()=>{
 for(const key of Object.keys(valid)) assert.equal(allow({...valid,[key]:false}),false,key);
});
test('synthetic full evidence only passes illustrative model, not real authorization',()=>{
 assert.equal(allow(valid),true);
});
