// Pure, offline decision model. Does not grant permissions or call the host.
import test from 'node:test';
import assert from 'node:assert/strict';

const decide=(evidence)=>Boolean(
 evidence && evidence.upstreamRouteDocumented===true
 && evidence.installedHostContractProven===true
 && evidence.serverAuthorizationProven===true
 && evidence.projectScopeProven===true
 && evidence.userApprovedDiscovery===true
);

test('upstream /search alone cannot authorize Canvas discovery',()=>{
 assert.equal(decide({upstreamRouteDocumented:true}),false);
});
test('an apparent page or repo label cannot stand in for server authorization',()=>{
 const hypothetical={upstreamRouteDocumented:true,installedHostContractProven:true,serverAuthorizationProven:false,projectScopeProven:true,userApprovedDiscovery:true};
 assert.equal(decide(hypothetical),false);
});
test('absence of explicit operator approval blocks even hypothetically complete evidence',()=>{
 assert.equal(decide({upstreamRouteDocumented:true,installedHostContractProven:true,serverAuthorizationProven:true,projectScopeProven:true}),false);
});
test('only hypothetical full evidence passes decision model, not production permission',()=>{
 assert.equal(decide({upstreamRouteDocumented:true,installedHostContractProven:true,serverAuthorizationProven:true,projectScopeProven:true,userApprovedDiscovery:true}),true);
});
