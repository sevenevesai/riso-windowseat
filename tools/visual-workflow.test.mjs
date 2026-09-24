// End-to-end regressions for late-film coverage, native PNGs, and clean scaffolding.
// Writes isolated disposable fixtures under out/, never existing art.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {launch,openFilm} from './lib/browser.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
fs.mkdirSync(path.resolve(here,'../out'),{recursive:true});
const temp=fs.mkdtempSync(path.resolve(here,'../out/visual-workflow-test-'));
function run(script,args,success=true){
  const r=spawnSync(process.execPath,[path.join(here,script),...args],{cwd:here,encoding:'utf8'});
  assert.equal(r.status===0,success,r.stdout+'\n'+r.stderr);return r.stdout;
}
const late=path.join(temp,'late.html');
fs.writeFileSync(late,`<canvas width="1080" height="1080" style="width:720px;height:720px"></canvas><script>
let n=0;const c=document.querySelector('canvas'),g=c.getContext('2d');
window.__riso={duration:90,ready:true,seek(t){g.fillStyle=t>60?(++n%2?'#0078BF':'#FF6C2F'):'#F2EDE3';g.fillRect(0,0,1080,1080);}};
</script>`);
const negative=run('verify.mjs',[late],false);
assert.match(negative,/t=(72|89\.966667).*not repeatable/);
assert.match(negative,/DIAGNOSIS t=\S+ changes when drawn twice on a fresh page/);
fs.writeFileSync(path.join(temp,'late-verifier.txt'),negative);
// A cache keyed by shot instead of by t keeps whichever frame of the shot was drawn first: it agrees
// with itself on one page, so only the fresh reverse-order page exposes it.
const cached=path.join(temp,'cached.html');
fs.writeFileSync(cached,`<canvas width="1080" height="1080" style="width:720px;height:720px"></canvas><script>
const c=document.querySelector('canvas'),g=c.getContext('2d'),cache={};
window.__riso={duration:30,ready:true,seek(t){const k=t<15?'a':'b';cache[k]??=t;g.fillStyle='#F2EDE3';g.fillRect(0,0,1080,1080);g.fillStyle='#0078BF';g.fillRect(100,100,100+cache[k]*20,300);}};
</script>`);
const order=run('verify.mjs',[cached,'--times','12,18,24'],false);
assert.match(order,/t=24 differs on a fresh page drawn in reverse order/);
assert.match(order,/DIAGNOSIS t=24 changes when t=18 is drawn first/);
fs.writeFileSync(path.join(temp,'cached-verifier.txt'),order);
// A deliverable that reaches the network fails, and the request never leaves the machine.
const online=path.join(temp,'online.html');
fs.writeFileSync(online,`<canvas width="320" height="240"></canvas><script>
new Image().src='https://example.invalid/texture.png';
const g=document.querySelector('canvas').getContext('2d');window.__riso={duration:1,ready:true,seek(){g.fillStyle='#0078BF';g.fillRect(0,0,320,240);}};
</script>`);
const r=spawnSync(process.execPath,[path.join(here,'still.mjs'),online,'--out',path.join(temp,'online.png')],{cwd:here,encoding:'utf8'});
assert.notEqual(r.status,0);assert.match(r.stderr,/network request blocked: https:\/\/example\.invalid\/texture\.png/);
// Stillness: the bar slides for 1 s, holds for 1 s, then slides again.
const held=path.join(temp,'held.html');
fs.writeFileSync(held,`<canvas width="1080" height="1080" style="width:720px;height:720px"></canvas><script>
const g=document.querySelector('canvas').getContext('2d');
window.__riso={duration:3,ready:true,shots:[{id:'slide',start:0,end:1,action:'bar slides'},{id:'rest',start:1,end:2,action:'bar rests'},{id:'go',start:2,end:3,action:'bar slides on'}],
seek(t){const x=t<1?t*300:t<2?300:300+(t-2)*300;g.fillStyle='#F2EDE3';g.fillRect(0,0,1080,1080);g.fillStyle='#0078BF';g.fillRect(100+x,400,200,200);}};
</script>`);
const mp4=path.join(temp,'held.mp4');
run('render.mjs',[held,'--size','360','--out',mp4]);
run('review.mjs',[held,'--mp4',mp4,'--out',path.join(temp,'held-review')]);
const review=JSON.parse(fs.readFileSync(path.join(temp,'held-review','review.json'),'utf8'));
assert.deepEqual(review.stillness.runs.map(({start,end,shots})=>({start,end,shots})),[{start:1,end:2,shots:['rest']}]);
assert.ok(review.shots.find(s=>s.id==='slide').changePct>0);
const native=path.join(temp,'native.html');
fs.writeFileSync(native,`<canvas width="320" height="240" style="width:720px;height:720px"></canvas><script>
const c=document.querySelector('canvas'),g=c.getContext('2d');window.__riso={duration:1,ready:true,seek(){g.fillStyle='#0078BF';g.fillRect(0,0,320,240);}};
</script>`);
const png=path.join(temp,'native.png');run('still.mjs',[native,'--out',png]);
const bytes=fs.readFileSync(png);assert.equal(bytes.readUInt32BE(16),320);assert.equal(bytes.readUInt32BE(20),240);
const browser=await launch('firefox');
try{
  for(const kind of ['film','still']){
    const out=path.join(temp,kind,'index.html');
    run('new-riso.mjs',['--kind',kind,'--duration','70','--out',out]);
    const original=fs.readFileSync(out,'utf8');
    run('new-riso.mjs',['--kind',kind,'--duration','70','--out',out],false);
    assert.equal(fs.readFileSync(out,'utf8'),original);
    // Exercise the extracted craft kit rather than checking a blank renderer alone.
    const art=`scene('test',{inks:['blue','orange'],plates(g,ink,r,sr){const p=cut([[250,260],[790,290],[820,760],[220,720]],sr,{amp:2});print(g,p,ink==='blue'?.6:.3);}});function drawArt(t){paintBaked('test');}`;
    fs.writeFileSync(out,original.replace('function drawArt(t) { }',art));
    const {page,duration,errors}=await openFilm(browser,out);
    assert.equal(duration,kind==='film'?70:1);
    const pixel=await page.evaluate(()=>{window.__riso.seek(0);return Array.from(document.querySelector('canvas').getContext('2d').getImageData(540,540,1,1).data);});
    assert.equal(pixel[3],255);assert.equal(errors.length,0,errors.join('\n'));
    if(kind==='still')assert.equal(await page.locator('nav').isVisible(),false);
    await page.close();
  }
}finally{await browser.close();}
console.log(`PASS: late-film failure diagnosed, order-dependent cache caught and traced, network request blocked, held stretch located, native PNG dimensions, both scaffolds render, overwrite refused.\nEvidence: ${temp}`);
