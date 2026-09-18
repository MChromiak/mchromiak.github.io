const fs = require("node:fs/promises");
const path = require("node:path");
const { chromium } = require("playwright");

const url = process.argv[2];
const outputDirectory = path.resolve(process.argv[3] || "/tmp/jev-article-browser-check");

if (!url) {
  throw new Error("Usage: node verify-article.cjs <article-url> [output-directory]");
}

async function inspectImages(page) {
  const images = page.locator("article img");
  const count = await images.count();
  const results = [];

  for (let index = 0; index < count; index += 1) {
    const image = images.nth(index);
    await image.scrollIntoViewIfNeeded();
    try {
      await image.evaluate(async (element) => element.decode());
    } catch (error) {
      const state = await image.evaluate((element) => ({
        src: element.currentSrc || element.src,
        complete: element.complete,
        naturalWidth: element.naturalWidth,
        naturalHeight: element.naturalHeight,
      }));
      throw new Error(`Image ${index} could not decode: ${JSON.stringify(state)}; ${error.message}`);
    }
    results.push(
      await image.evaluate((element) => ({
        src: element.currentSrc,
        complete: element.complete,
        naturalWidth: element.naturalWidth,
        naturalHeight: element.naturalHeight,
      })),
    );
  }

  const broken = results.filter(
    (item) => !item.complete || item.naturalWidth === 0 || item.naturalHeight === 0,
  );
  if (broken.length > 0) {
    throw new Error(`Broken article images: ${JSON.stringify(broken)}`);
  }
  return results;
}

async function inspectViewport(browser, label, viewport, reducedMotion, expectedPaths) {
  const context = await browser.newContext({ viewport, reducedMotion });
  const page = await context.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  const images = await inspectImages(page);
  const diagramSources = await page.locator("article picture img").evaluateAll((elements) =>
    elements.map((element) => new URL(element.currentSrc).pathname),
  );

  expectedPaths.forEach((expected, index) => {
    if (!diagramSources[index]?.endsWith(expected)) {
      throw new Error(`${label}: expected ${expected}, received ${diagramSources[index]}`);
    }
  });

  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  if (overflow > 1) {
    throw new Error(`${label}: page overflows horizontally by ${overflow}px`);
  }

  await page.locator("article picture").first().scrollIntoViewIfNeeded();
  await page.screenshot({ path: path.join(outputDirectory, `${label}.png`), fullPage: false });
  await context.close();
  return { label, diagramSources, imageCount: images.length, overflow };
}

async function verifyMotion(browser) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  const diagram = page.locator("article picture img").first();
  await diagram.scrollIntoViewIfNeeded();
  await diagram.evaluate(async (element) => element.decode());
  const first = await diagram.screenshot();
  await page.waitForTimeout(1800);
  const second = await diagram.screenshot();
  await context.close();
  if (first.equals(second)) {
    throw new Error("Desktop WebP did not visibly advance between captures");
  }
  return true;
}

async function main() {
  await fs.mkdir(outputDirectory, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });

  try {
    const desktop = await inspectViewport(
      browser,
      "desktop",
      { width: 1440, height: 1000 },
      "no-preference",
      ["/articles/2026/Sep/17/img/jev-parallel-flow.webp", "/articles/2026/Sep/17/img/jev-enterprise-routing.webp"],
    );
    const mobile = await inspectViewport(
      browser,
      "mobile",
      { width: 390, height: 844 },
      "no-preference",
      ["/img/jev-parallel-flow-mobile.svg", "/img/jev-enterprise-routing-mobile.svg"],
    );
    const reduced = await inspectViewport(
      browser,
      "reduced-motion",
      { width: 1440, height: 1000 },
      "reduce",
      ["/articles/2026/Sep/17/img/jev-parallel-flow-static.png", "/articles/2026/Sep/17/img/jev-enterprise-routing-static.png"],
    );
    await verifyMotion(browser);
    process.stdout.write(`${JSON.stringify({ desktop, mobile, reduced, motion: true }, null, 2)}\n`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
