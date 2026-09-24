// Visual review aid, not an aesthetic score. Reads optional shot metadata from the film.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawn,spawnSync} from 'node:child_process';
import {args,launch,openFilm} from './lib/browser.mjs';
const a=args(process.argv.slice(2)),film=a._[0];
if(!film){console.error('usage: node review.mjs <film.html> [--out directory] [--engine firefox] [--mp4 render.mp4 [--from s] [--floor %] [--hold s]]');process.exit(1);}

// Runs of a render where the picture stays as it was. Frames are box-averaged to 270 px grey, which
// descreens the halftone: a pinned screen reads as static and a tone change as a change. A pixel
// counts as changed above 4/255. A run lasts while every frame differs from the run's FIRST frame
// on under `floor` percent of pixels, so a fade too slow to show frame to frame still ends it.
// Held pictures are not failures; the shot's action says whether one is intended. A slow camera
// creep changes every pixel and passes this.
async function stillness(mp4,from,floor,hold){
  const {FFMPEG}=await import('./lib/ffmpeg.mjs');
  const info=spawnSync(FFMPEG,['-hide_banner','-i',mp4],{encoding:'utf8'}).stderr;
  const fps=Number(info.match(/(\d+(?:\.\d+)?) fps/)?.[1]);
  if(!(fps>0))throw Error(`Cannot read a frame rate from ${mp4}`);
  const S=270,px=S*S,changed=[],runs=[];
  const diff=(x,y)=>{let c=0;for(let i=0;i<px;i++)if(Math.abs(x[i]-y[i])>4)c++;return c/px;};
  // Frame n shows t = from + n/fps, as render.mjs seeks. A run spans frames k0..last.
  let n=0,prev=null,anchor=null,k0=0,drift=0,identical=0;
  const close=last=>{if((last-k0)/fps>=hold)runs.push({start:Number((from+k0/fps).toFixed(3)),end:Number((from+last/fps).toFixed(3)),
    seconds:Number(((last-k0)/fps).toFixed(3)),maxChangePct:Number((drift*100).toFixed(3)),identicalSteps:identical});};
  const p=spawn(FFMPEG,['-v','error','-i',mp4,'-vf',`scale=${S}:${S}:flags=area,format=gray`,'-f','rawvideo','-']);
  let err='',pending=Buffer.alloc(0);p.stderr.on('data',d=>err+=d);
  const closed=new Promise(res=>p.on('close',res));
  for await(const chunk of p.stdout){
    pending=Buffer.concat([pending,chunk]);
    for(;pending.length>=px;pending=pending.subarray(px),n++){
      const f=Buffer.from(pending.subarray(0,px));
      if(prev){
        changed.push(diff(f,prev));
        const d=diff(f,anchor);
        if(d<floor/100){drift=Math.max(drift,d);if(changed.at(-1)===0)identical++;}
        else{close(n-1);anchor=f;k0=n;drift=0;identical=0;}
      } else anchor=f;
      prev=f;
    }
  }
  if(await closed)throw Error(`ffmpeg could not decode ${mp4}: ${err.trim()}`);
  close(n-1);
  // changed[k] compares frame k+1 with frame k.
  return {fps,frames:n,from,floorPct:floor,holdSeconds:hold,changed,runs};
}
const out=path.resolve(a.out||`../out/${path.basename(path.dirname(path.resolve(film)))}-review`);
const browser=await launch(a.engine||'firefox');
let duration,shots,notes=[],times;
try {
  const opened=await openFilm(browser,film);duration=opened.duration;
  shots=await opened.page.evaluate(()=>window.__riso.shots||[]);
  if(opened.errors.length)throw Error(opened.errors.join('\n'));
  if(!(duration>0&&Number.isFinite(duration)))throw Error('Invalid duration');
  if(!shots.length){notes.push('No shot metadata: evenly spaced samples cannot establish pacing or action quality.');times=Array.from({length:12},(_,i)=>i*Math.max(0,duration-1/30)/11);}
  else {
    times=[];
    for(let i=0;i<shots.length;i++) {
      const s=shots[i];
      if(!s.id||![s.start,s.end].every(Number.isFinite)||s.start<0||s.end>duration||s.end<=s.start)
        throw Error(`Invalid shot ${i}: id, start and end required within the film duration`);
      const readAt=s.readAt??(s.start+s.end)/2;
      if(!Number.isFinite(readAt)||readAt<s.start||readAt>=s.end)throw Error(`Invalid readAt: ${s.id}`);
      times.push(s.start,readAt,Math.max(s.start,s.end-1/30));
      s.seconds=Number((s.end-s.start).toFixed(3));
      if(!s.action)notes.push(`${s.id}: name what changes within the shot, or why it holds.`);
      if(i>=2&&shots[i-2].start>0&&s.transition&&!['cut','none'].includes(s.transition)
        &&s.transition===shots[i-1].transition&&s.transition===shots[i-2].transition)
        notes.push(`${s.id}: third consecutive '${s.transition}' handoff; inspect whether repetition is intentional.`);
    }
  }
} finally {await browser.close();}
times=[...new Set(times.map(t=>Number(t.toFixed(3))))].sort((x,y)=>x-y);
let still=null;
if(a.mp4){
  const mp4=path.resolve(a.mp4),from=Number(a.from||0);
  if(fs.statSync(mp4).mtimeMs<fs.statSync(path.resolve(film)).mtimeMs)notes.push(`${path.basename(mp4)} is older than the film source; the stillness report describes the earlier render.`);
  const {changed,...s}=await stillness(mp4,from,Number(a.floor??0.1),Number(a.hold??0.5));still=s;
  const endT=from+(s.frames-1)/s.fps;
  if(endT>duration+1/s.fps)notes.push(`${path.basename(mp4)} runs to ${endT.toFixed(2)} s, past the film's ${duration} s: wrong file, or a range render needs --from.`);
  const med=xs=>{const v=[...xs].sort((x,y)=>x-y);return v.length?Number((v[v.length>>1]*100).toFixed(3)):null;};
  s.medianChangePct=med(changed);
  for(const sh of shots)sh.changePct=med(changed.filter((_,k)=>{const t=from+(k+1)/s.fps;return t>sh.start&&t<sh.end;}));
  for(const r of s.runs){
    r.shots=shots.filter(sh=>sh.start<r.end&&sh.end>r.start).map(sh=>sh.id);
    const held=r.shots.map(id=>{const sh=shots.find(x=>x.id===id);return sh.action?`${id} (${sh.action})`:id;}).join(', ');
    notes.push(`${r.start}-${r.end} s holds still for ${r.seconds} s (at most ${r.maxChangePct}% of pixels differ from its first frame${r.identicalSteps?`; ${r.identicalSteps} identical steps`:''})${held?` in ${held}`:''}: confirm at playback speed that the hold is intended.`);
  }
  console.log(`Stillness: ${s.frames} frames at ${s.fps} fps, median ${s.medianChangePct}% of pixels changed per frame, ${s.runs.length} run(s) under ${s.floorPct}% for ${s.holdSeconds} s or longer.`);
}
fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'review.json'),JSON.stringify({duration,shots,notes,times,stillness:still,judgment:'Human/model visual review required; metadata and deterministic pixels do not certify art.'},null,2));
if(shots.length)console.table(shots.map(({id,seconds,action,transition,changePct})=>({id,seconds,action,transition,...(still&&{changePct})})));
notes.forEach(n=>console.log(`Review: ${n}`));
const shoot=fileURLToPath(new URL('./shoot.mjs',import.meta.url));
const r=spawnSync(process.execPath,[shoot,path.resolve(film),'--times',times.join(','),'--engine',a.engine||'firefox','--out',out,'--sheet','--cols','3','--cell','340'],{stdio:'inherit'});
if(r.error)throw r.error;
process.exit(r.status??1);
