async function graphIdentityForObservation(context,conversationId,project){
  const uuid=/^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/;
  if(typeof context!=='string'||typeof conversationId!=='string'||!uuid.test(context)||!uuid.test(conversationId)||typeof project!=='string'||! /^[A-Za-z0-9._-]+\/[A-Za-z0-9._-]+$/.test(project))throw Error('Contexto de leitura inválido');
  const digest=async(kind,parts)=>{
    const bytes=new TextEncoder().encode(JSON.stringify([kind,context,...parts]));
    const hash=await crypto.subtle.digest('SHA-256',bytes);
    return Array.from(new Uint8Array(hash),n=>n.toString(16).padStart(2,'0')).join('');
  };
  const realm=await digest('view-scope',[]);
  const id=async(kind,parts)=>'obs:'+kind+':'+realm+':'+await digest(kind,parts);
  return Object.freeze({scope:'local-view-not-tenant',context:realm,
    source:await id('consulted-source',[]),
    mission:await id('consulted-conversation',[conversationId]),
    project:await id('manual-project',[conversationId,project])});
}
function validGraphIdentity(value){
  return value&&value.scope==='local-view-not-tenant'&&typeof value.context==='string'&&/^[0-9a-f]{64}$/.test(value.context)&&
    [['source','consulted-source'],['mission','consulted-conversation'],['project','manual-project']].every(([key,kind])=>
      typeof value[key]==='string'&&new RegExp('^obs:'+kind+':'+value.context+':[0-9a-f]{64}$').test(value[key]));
}

export {graphIdentityForObservation,validGraphIdentity};

