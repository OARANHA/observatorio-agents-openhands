function graphModel(){
  const nodes=[
    {id:'demo-root',name:'Projetos ilustrativos',tag:'APENAS DEMO',kind:'demo-hub',x:27,y:48,description:'Agrupador dos quatro exemplos visuais. Não representa inventário de operações reais.'}
  ];
  const places=[[14,19],[43,18],[13,79],[43,79]];
  const edges=[];
  Object.keys(defs).filter(k=>k!=='observado').forEach((key,i)=>{
    const item=defs[key];
    nodes.push({id:'demo-'+key,name:item.name,tag:'DEMONSTRAÇÃO',kind:'demo',x:places[i][0],y:places[i][1],description:'Projeto ilustrativo. Agentes, missões e atividades não comprovados.'});
    edges.push({from:'demo-root',to:'demo-'+key,kind:'demo'});
  });
  if(verifiedMission){
    nodes.push({id:'real-origin',name:'OpenHands',tag:'FONTE AUTENTICADA',kind:'verified',x:69,y:24,description:'Origem: GET de conversa pela sessão autenticada do Canvas.'});
    nodes.push({id:'real-mission',name:'Missão '+verifiedMission.conversationId.slice(0,8),tag:'ESTADO: '+verifiedMission.status,kind:'verified',x:83,y:51,description:'Conversa consultada pontualmente, não sucesso de tarefa ou agente comprovado.'});
    nodes.push({id:'manual-project',name:verifiedMission.project.split('/').pop().slice(0,22),tag:'PROJETO INFORMADO',kind:'manual',x:69,y:81,description:'Associação informada pelo operador; o servidor não confirmou o vínculo.'});
    edges.push({from:'real-origin',to:'real-mission',kind:'verified'});
    edges.push({from:'real-mission',to:'manual-project',kind:'manual'});
  }
  return {nodes,edges};
}
