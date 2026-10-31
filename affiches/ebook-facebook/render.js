// Exporte l'affiche en PNG pour les 3 formats Facebook/Instagram : node render.js
const { chromium } = require("playwright");
const path = require("path");

const FORMATS = { feed: [1080, 1350], carre: [1080, 1080], story: [1080, 1920] };

(async () => {
  const browser = await chromium.launch();
  for (const [nom, [width, height]] of Object.entries(FORMATS)) {
    const page = await browser.newPage({ viewport: { width, height } });
    await page.goto("file://" + path.join(__dirname, "affiche.html") + "?format=" + nom);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(__dirname, "renders", `affiche-${nom}.png`) });
    await page.close();
  }
  await browser.close();
})();
