import test from 'node:test';
import assert from 'node:assert/strict';
// Synthetic policy model only. No requests, credentials or production authorization.
function canRead(e) {
 return e?.installedVersionKnown===true &&
 e?.serverAuthenticatedIdentity===true &&
 e?.resourceProjectAclVerified===true &&
 e?.membershipCurrentlyValid===true &&
 e?.revocationChecked===true &&
 e?.operatorConsent===true;
}
const proof={installedVersionKnown:true,serverAuthenticatedIdentity:true,resourceProjectAclVerified:true,membershipCurrentlyValid:true,revocationChecked:true,operatorConsent:true};
test('a session key and repository metadata are not project authorization',()=>assert.equal(canRead({sessionKeyPresent:true,selected_repository:'demo'}),false));
test('each proof is independently required',()=>{for(const key of Object.keys(proof))assert.equal(canRead({...proof,[key]:false}),false,key);});
test('revoked association must be denied even with valid server session',()=>assert.equal(canRead({...proof,membershipCurrentlyValid:false,sessionKeyPresent:true}),false));
test('synthetic full evidence is not a permission on a real server',()=>assert.equal(canRead(proof),true));
