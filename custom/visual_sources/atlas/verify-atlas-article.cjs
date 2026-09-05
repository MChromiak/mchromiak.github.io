const fs = require("node:fs/promises");
const path = require("node:path");
const { chromium } = require("playwright");

const url = process.argv[2];
const outputDirectory = path.resolve(process.argv[3] || "/tmp/atlas-article-browser-check");

if (!url) {
  throw new Error("Usage: node verify-atlas-article.cjs <article-url> [output-directory]");
}

async function inspectPage(page, label, expected) {
  await page.goto(url, { waitUntil: "networkidle" });
  const image = page.locator("picture img").first();
  await image.waitFor({ state: "visible" });
  await image.scrollIntoViewIfNeeded();
  await image.evaluate(async (element) => element.decode());

  const result = await image.evaluate((element) => {
    const bounds = element.getBoundingClientRect();
    return {
      complete: element.complete,
      currentSrc: element.currentSrc,
      naturalWidth: element.naturalWidth,
      naturalHeight: element.naturalHeight,
      renderedWidth: Math.round(bounds.width),
      renderedHeight: Math.round(bounds.height),
      horizontalOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    };
  });

  if (
    !result.complete ||
    result.naturalWidth !== expected.width ||
    result.naturalHeight !== expected.height ||
    !result.currentSrc.endsWith(expected.path)
  ) {
    throw new Error(`${label}: animated WebP did not load at its expected dimensions`);
  }
  if (result.horizontalOverflow > 1) {
    throw new Error(`${label}: page overflows horizontally by ${result.horizontalOverflow}px`);
  }

  return result;
}

async function main() {
  await fs.mkdir(outputDirectory, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });

  try {
    const desktopContext = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const desktop = await desktopContext.newPage();
    const desktopResult = await inspectPage(desktop, "desktop", {
      width: 1200,
      height: 675,
      path: "/img/atlas-request-flow.webp",
    });
    await desktop.locator("picture img").first().scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(outputDirectory, "desktop-start.png") });
    await desktop.waitForTimeout(2500);
    await desktop.screenshot({ path: path.join(outputDirectory, "desktop-later.png") });
    await desktopContext.close();

    const mobileContext = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const mobile = await mobileContext.newPage();
    const mobileResult = await inspectPage(mobile, "mobile", {
      width: 720,
      height: 1100,
      path: "/img/atlas-request-flow-mobile.webp",
    });
    await mobile.locator("picture img").first().scrollIntoViewIfNeeded();
    await mobile.screenshot({ path: path.join(outputDirectory, "mobile.png") });
    await mobileContext.close();

    const reducedContext = await browser.newContext({
      viewport: { width: 1440, height: 1000 },
      reducedMotion: "reduce",
    });
    const reduced = await reducedContext.newPage();
    await reduced.goto(url, { waitUntil: "networkidle" });
    const reducedImage = reduced.locator("picture img").first();
    await reducedImage.waitFor({ state: "visible" });
    await reducedImage.scrollIntoViewIfNeeded();
    await reducedImage.evaluate(async (element) => element.decode());
    const reducedSource = await reducedImage.evaluate((element) => element.currentSrc);
    if (!reducedSource.endsWith("/img/atlas-conceptual-flow.svg")) {
      throw new Error(`reduced motion: expected the static SVG, received ${reducedSource}`);
    }
    await reducedImage.scrollIntoViewIfNeeded();
    await reduced.screenshot({ path: path.join(outputDirectory, "reduced-motion.png") });
    await reducedContext.close();

    process.stdout.write(
      `${JSON.stringify({ desktop: desktopResult, mobile: mobileResult, reducedSource }, null, 2)}\n`,
    );
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
