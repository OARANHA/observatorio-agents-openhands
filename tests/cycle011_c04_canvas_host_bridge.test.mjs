import test from 'node:test';
import assert from 'node:assert/strict';
// Synthetic defensive policy, NOT OpenHands implementation or a live permission check.
const UUID=/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
function localPointReadAllowed(request,proof) {
 if(!request || request.method!=='GET'||request.body!==undefined||request.headers!==undefined) return false;
 const m=/^\/api\/conversations\/([^/?#]+)$/.exec(request.path||'');
 return Boolean(m&&UUID.test(m[1])&&proof?.operatorApproved===true&&proof?.resourceAuthorizedByServer===true);
}
const good={method:'GET',path:'/api/conversations/11111111-1111-4111-8111-111111111111'};
const proof={operatorApproved:true,resourceAuthorizedByServer:true};
test('local point GET requires independent server authorization',()=>{assert.equal(localPointReadAllowed(good,{}),false);assert.equal(localPointReadAllowed(good,proof),true)});
test('generic Canvas host write methods are not acceptable to Observatorio',()=>{for(const method of ['POST','PUT','PATCH','DELETE']) assert.equal(localPointReadAllowed({...good,method},proof),false)});
test('list/search/foreign paths and path tricks are denied',()=>{for(const path of ['/api/conversations/search','/api/conversations','//api/conversations/11111111-1111-4111-8111-111111111111','/api/conversations/11111111-1111-4111-8111-111111111111?x=1','/api/conversations/../search']) assert.equal(localPointReadAllowed({...good,path},proof),false,path)});
test('no caller headers or body and no local operator approval',()=>{assert.equal(localPointReadAllowed({...good,headers:{Authorization:'synthetic'}},proof),false);assert.equal(localPointReadAllowed({...good,body:{}},proof),false);assert.equal(localPointReadAllowed(good,{resourceAuthorizedByServer:true}),false)});
