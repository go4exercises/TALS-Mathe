import { chromium } from 'playwright';
const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+process.cwd()+'/clips/g1-3-zweiklammersatz.html');
await p.addStyleTag({content:'body{background:#fff}'});
await p.evaluate(()=>document.body.classList.add('render'));
await p.waitForTimeout(300);
await p.evaluate(s=>window.__seek(s), 44.8);
await p.waitForTimeout(120);
const r=await p.evaluate(()=>[...document.querySelectorAll('.l')]
  .filter(e=>parseFloat(getComputedStyle(e).opacity)>0.5)
  .map(e=>{const b=e.getBoundingClientRect();
    return {k:e.className, t:Math.round(b.top), b:Math.round(b.bottom), h:Math.round(b.height),
            txt:(e.textContent||'').trim().slice(0,40)};}));
r.forEach(x=>console.log(`  ${String(x.t).padStart(4)}–${String(x.b).padStart(4)} (h${String(x.h).padStart(3)}) [${x.k}] ${x.txt}`));
await b.close();
