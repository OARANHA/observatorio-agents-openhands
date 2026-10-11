// Generates only tools/mentor-demo/index.html; never the installed extension.
import {readFileSync,writeFileSync} from 'node:fs';
const root=new URL('../',import.meta.url);
const read=path=>readFileSync(new URL(path,root),'utf8');
const identity=read('tools/mentor-demo/identity.mjs').replace('export {graphIdentityForObservation,validGraphIdentity};','');
const model=read('tools/mentor-demo/model.mjs').replace("import {graphIdentityForObservation} from './identity.mjs';",'').replace('export async function createMentorDemoSession','async function createMentorDemoSession');
const ui=read('tools/mentor-demo/ui.mjs').replace("import {createMentorDemoSession} from './model.mjs';",'').replace('export function mountMentorDemo','function mountMentorDemo');
const html=`<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; form-action 'none'; base-uri 'none'">
<title>Observatório — Mentor DEMO offline</title><style>body{margin:0;background:#070e1d;padding:16px}main{max-width:1040px;margin:auto}</style></head>
<body><main id="mentor"></main><script type="module">${identity}\n${model}\n${ui}\nmountMentorDemo(document.getElementById('mentor'));</script></body></html>\n`;
const target=new URL('tools/mentor-demo/index.html',root);
if(process.argv.includes('--check')){if(readFileSync(target,'utf8')!==html)throw Error('mentor_demo_generation_drift');}
else writeFileSync(target,html);
