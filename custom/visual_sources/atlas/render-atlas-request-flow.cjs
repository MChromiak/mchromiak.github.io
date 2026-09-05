const fs = require("node:fs/promises");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("playwright");

const source = path.resolve(process.argv[2] || path.join(__dirname, "atlas-request-flow.html"));
const outputDirectory = path.resolve(process.argv[3] || "/tmp/atlas-request-flow-frames");
const frameCount = Number(process.argv[4] || 108);
const durationSeconds = Number(process.argv[5] || 9);
const width = Number(process.argv[6] || 1200);
const height = Number(process.argv[7] || 675);

async function main() {
  await fs.mkdir(outputDirectory, { recursive: true });

  const browser = await chromium.launch({
    headless: true,
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });
  const page = await browser.newPage({
    viewport: { width, height },
    deviceScaleFactor: 1,
  });

  await page.goto(`${pathToFileURL(source).href}?frame=0`, { waitUntil: "load" });
  for (let index = 0; index < frameCount; index += 1) {
    const seconds = (index / frameCount) * durationSeconds;
    await page.evaluate((time) => window.renderFrame(time), seconds);
    await page.screenshot({
      path: path.join(outputDirectory, `frame-${String(index).padStart(4, "0")}.png`),
      animations: "disabled",
    });
  }

  await browser.close();
  process.stdout.write(`Rendered ${frameCount} deterministic frames to ${outputDirectory}\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
