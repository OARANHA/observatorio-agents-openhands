// Offline policy model, not the OpenHands authorization implementation.
import test from 'node:test';
import assert from 'node:assert/strict';
function canExposeConversation(e){
 return e?.hostContractVerified===true &&
 e?.sessionAuthenticated===true &&
 e?.serverProjectAuthorization===true &&
 e?.conversationProjectBindingVerified===true &&
 e?.explicitOperatorConsent===true;
}
const base={hostContractVerified:true,sessionAuthenticated:true,serverProjectAuthorization:true,conversationProjectBindingVerified:true,explicitOperatorConsent:true};
test('session authentication alone cannot authorize cross-project observation',()=>{
 assert.equal(canExposeConversation({sessionAuthenticated:true}),false);
});
test('matching repository metadata cannot substitute server authorization',()=>{
 assert.equal(canExposeConversation({...base,serverProjectAuthorization:false,selected_repository:'same/repo'}),false);
});
test('workspace cookie alone is not conversation API authorization',()=>{
 assert.equal(canExposeConversation({workspaceCookiePresent:true}),false);
});
test('each independent proof is required and explicit consent stays distinct',()=>{
 for(const key of Object.keys(base)) assert.equal(canExposeConversation({...base,[key]:false}),false,key);
 assert.equal(canExposeConversation(base),true);
});
