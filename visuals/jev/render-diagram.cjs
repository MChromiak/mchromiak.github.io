const fs = require("node:fs/promises");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("playwright");

const source = path.resolve(process.argv[2]);
const outputDirectory = path.resolve(process.argv[3]);
const frameCount = Number(process.argv[4] || 120);
const durationSeconds = Number(process.argv[5] || 10);
const width = Number(process.argv[6] || 1200);
const height = Number(process.argv[7] || 675);

if (!process.argv[2] || !process.argv[3]) {
  throw new Error(
    "Usage: node render-diagram.cjs <source.html> <frames-directory> [frame-count] [duration] [width] [height]",
  );
}

async function main() {
  await fs.mkdir(outputDirectory, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });

  try {
    await page.goto(`${pathToFileURL(source).href}?frame=0`, { waitUntil: "load" });
    await page.waitForFunction(() => typeof window.renderFrame === "function");
    for (let index = 0; index < frameCount; index += 1) {
      const seconds = (index / frameCount) * durationSeconds;
      await page.evaluate((time) => window.renderFrame(time), seconds);
      await page.screenshot({
        path: path.join(outputDirectory, `frame-${String(index).padStart(4, "0")}.png`),
        animations: "disabled",
      });
    }
  } finally {
    await browser.close();
  }

  process.stdout.write(`Rendered ${frameCount} deterministic frames to ${outputDirectory}\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
