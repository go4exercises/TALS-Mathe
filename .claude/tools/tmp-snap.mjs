import { chromium } from 'playwright';
const b = await chromium.launch();
for (const [thema,suffix] of [['light','h'],['dark','d']]) {
  const p = await b.newPage({ viewport:{width:1280,height:2200} });
  await p.goto('http://localhost:8921/leitprogramme/potenzen.html', { waitUntil:'networkidle' });
  await p.evaluate(t => document.documentElement.setAttribute('data-theme', t), thema);
  await p.waitForTimeout(700);
  await p.screenshot({ path: `${process.env.SP}/tok-${process.env.PHASE}-${suffix}.png` });
  await p.close();
}
await b.close();
