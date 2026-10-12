import test from 'node:test';import assert from 'node:assert/strict';
// Synthetic decision model only; no HTTP, SDK loading or credential access.
function permitted(e){return e?.installedVersionVerified===true&&e?.transportPathReviewed===true&&e?.serverResourceAclVerified===true&&e?.projectMembershipVerified===true&&e?.revocationVerified===true&&e?.operatorApproved===true;}
const all={installedVersionVerified:true,transportPathReviewed:true,serverResourceAclVerified:true,projectMembershipVerified:true,revocationVerified:true,operatorApproved:true};
test('public pin and transport key alone cannot authorize a project',()=>{assert.equal(permitted({publicVersionPin:'1.54.0',apiKeyPresent:true}),false)});
test('a metadata project label cannot replace server ACL',()=>{assert.equal(permitted({...all,serverResourceAclVerified:false,selected_repository:'repo'}),false)});
test('every independent gate is required',()=>{for(const k of Object.keys(all))assert.equal(permitted({...all,[k]:false}),false,k)});
test('complete synthetic evidence only illustrates the decision model',()=>{assert.equal(permitted(all),true)});
