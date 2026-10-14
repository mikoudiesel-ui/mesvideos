// Rastérise des pages HTML (logos SVG, planches) en PNG avec le Chromium de Playwright.
//   NODE_PATH=$(npm root -g) node tools/render.cjs jobs.json
// jobs.json : [{ "file": "/chemin/page.html" ou "html": "<html>…", "out": "/chemin/x.png",
//               "width": 1080, "height": 1350, "scale": 2, "transparent": false }]
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.width, height: j.height }, deviceScaleFactor: j.scale || 1 });
    if (j.html) await page.setContent(j.html, { waitUntil: 'load' });
    else await page.goto('file://' + j.file, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: j.out, omitBackground: !!j.transparent });
    await page.close();
  }
  await browser.close();
})();
