// Fixed synthetic fixtures. No SDK, network, account or operational authorization.
import {graphIdentityForObservation} from './identity.mjs';
const fields=['project','status','event'];
const cid='00000000-0000-4000-8000-000000000001';
class MentorDemoSession {
 constructor(identity,project,delay){
  Object.defineProperty(this,'identity',{value:identity,enumerable:true});
  Object.defineProperty(this,'observation',{value:Object.freeze({classification:'demo',source:'synthetic_fixture',
   conversation_id:cid,project,status:'paused',event:'needs_review'}),enumerable:true});
  this.state='ready';this._context=null;this._generation=0;this._delay=delay;
 }
 get context(){return this._context?structuredClone(this._context):null;}
 _deny(){this.close();throw Error('mentor_demo_denied');}
 review(selection){
  if(!['ready','reviewed'].includes(this.state)||!Array.isArray(selection)||selection.length>3||
   new Set(selection).size!==selection.length||selection.some(k=>!fields.includes(k)))this._deny();
  this._context=Object.freeze({classification:'demo',source:'synthetic_fixture',operational_go:false,
   ...Object.fromEntries(selection.map(k=>[k,this.observation[k]]))});
  this.state='reviewed';return this.context;
 }
 async recommend(approval){
  if(this.state!=='reviewed'||approval!==true)this._deny();
  this.state='pending';const generation=++this._generation;
  await new Promise(resolve=>setTimeout(resolve,this._delay));
  if(this.state==='closed'||generation!==this._generation)throw Error('mentor_demo_closed');
  this.state='complete';return Object.freeze({classification:'demo',operational_go:false,authorizes_agent:false,
   recommendation:'Orientação fictícia: manter NO-GO, revisar a fonte, os limites e a confirmação humana. Nenhum agente recebeu instruções.'});
 }
 close(){this.state='closed';this._generation++;this._context=null;}
}
export async function createMentorDemoSession(options){
 try{
  if(!options||Object.getPrototypeOf(options)!==Object.prototype||Object.keys(options).some(k=>!['context','project','delay'].includes(k)))throw Error();
  const {context,project='synthetic/alpha',delay=0}=options;
  if(!['synthetic/alpha','synthetic/beta'].includes(project)||typeof delay!=='number'||!Number.isInteger(delay)||delay<0||delay>250)throw Error();
  const identity=await graphIdentityForObservation(context,cid,project);
  return new MentorDemoSession(identity,project,delay);
 }catch{throw Error('mentor_demo_denied');}
}
