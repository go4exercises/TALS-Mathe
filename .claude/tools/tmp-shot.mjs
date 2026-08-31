import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({ viewport:{width:1280,height:1400} });
await p.goto('http://localhost:8908/leitprogramme/potenzen.html', { waitUntil:'networkidle' });
await p.waitForTimeout(700);
await p.screenshot({ path: process.env.SP + '/' + process.env.NAME + '.png', fullPage:false });
await b.close();
