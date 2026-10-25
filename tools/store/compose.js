// Captioned Play screenshots: node tools/store/compose.js  (reads store/screenshots/raw, writes store/screenshots)
const { chromium } = require('playwright'), path = require('path');
const root = path.resolve(__dirname, '../..');
const SHOTS = [
  ['1-saplings', 'Every nest wants one owl', 'A calm logic puzzle you play with one finger', 'linear(#ff6a4d,#e04a3a)', '#151838'],
  ['2-hollow-grove', 'Owls never touch', 'Not even corner to corner', 'linear(#6fb7d8,#3d7fb8)', '#ff6a4d'],
  ['3-moonfall-pines', 'Follow the numbers', 'They count the owls in each row and column', 'linear(#3c3e86,#151838)', '#ff6a4d'],
  ['4-old-oak', '65 levels, 4 woods', 'From the Saplings to the mighty Old Oak', 'linear(#5f8f4e,#3e6a33)', '#151838'],
  ['5-daily-streak', 'A new tree every night', 'Keep your Daily Roost streak going', 'linear(#f4b942,#e08f2c)', '#151838'],
  ['6-menu', 'Pure logic, no guessing', 'Every puzzle has one solution. Hints explain why.', 'linear(#c95a9a,#7c3d8f)', '#151838'],
];
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [f, t, s, bg, sh] of SHOTS) {
    const u = new URL('file://' + path.join(__dirname, 'compose.html'));
    Object.entries({ t, s, sh, bg: bg.replace('linear(', 'linear-gradient(180deg,'), img: 'file://' + path.join(root, 'store/screenshots/raw', f + '.png') }).forEach(([k, v]) => u.searchParams.set(k, v));
    await p.goto(u.href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(root, 'store/screenshots', f + '.png') });
  }
  await b.close();
})();
