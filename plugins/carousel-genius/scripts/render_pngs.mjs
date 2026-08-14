#!/usr/bin/env node
/**
 * Render carousel HTML files to PNGs.
 *
 * Usage:
 *   node render_pngs.mjs <slide_dir> [--pdf] [--width 1080] [--height 1350]
 *
 * Reads slide-NN.html files from <slide_dir>, screenshots each at the
 * given dimensions, writes slide-NN.png alongside.
 *
 * --pdf flag: also stitches PNGs into a single PDF (LinkedIn-doc compatible).
 */

import { chromium } from 'playwright';
import { readdirSync, existsSync, createWriteStream } from 'fs';
import { resolve, join, basename } from 'path';
import { pathToFileURL } from 'url';

const args = process.argv.slice(2);
const dir = resolve(args[0] || '.');
const wantPdf = args.includes('--pdf');
const widthIdx = args.indexOf('--width');
const heightIdx = args.indexOf('--height');
const onlyIdx = args.indexOf('--only');
const width = widthIdx > -1 ? parseInt(args[widthIdx + 1], 10) : 1080;
const height = heightIdx > -1 ? parseInt(args[heightIdx + 1], 10) : 1440;
const onlySlide = onlyIdx > -1 ? parseInt(args[onlyIdx + 1], 10) : null;

if (!existsSync(dir)) {
  console.error(`Directory not found: ${dir}`);
  process.exit(1);
}

let htmlFiles = readdirSync(dir)
  .filter((f) => /^slide-\d+\.html$/.test(f))
  .sort();

if (onlySlide !== null) {
  const padded = String(onlySlide).padStart(2, '0');
  htmlFiles = htmlFiles.filter((f) => f === `slide-${padded}.html`);
  if (htmlFiles.length === 0) {
    console.error(`No slide ${padded} found in ${dir}`);
    process.exit(1);
  }
  console.log(`(--only ${onlySlide}: rendering single slide for visual verification)`);
}

if (htmlFiles.length === 0) {
  console.error(`No slide-NN.html files in ${dir}`);
  process.exit(1);
}

console.log(`Rendering ${htmlFiles.length} slides at ${width}×${height}...`);

const browser = await chromium.launch({
  headless: true,
  timeout: 60000,
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none'],
});

const context = await browser.newContext({
  viewport: { width, height },
  deviceScaleFactor: 2,
});

const pngPaths = [];

try {
  for (const file of htmlFiles) {
    const htmlPath = join(dir, file);
    const pngPath = htmlPath.replace(/\.html$/, '.png');
    const page = await context.newPage();
    await page.goto(pathToFileURL(htmlPath).href, {
      waitUntil: 'networkidle',
      timeout: 30000,
    });
    await page.waitForTimeout(500); // let fonts settle

    // Auto-detect canvas size from <body> width/height (templates set this)
    const bodySize = await page.evaluate(() => {
      const cs = getComputedStyle(document.body);
      return {
        w: parseInt(cs.width, 10) || 0,
        h: parseInt(cs.height, 10) || 0,
      };
    });
    const clipW = bodySize.w || width;
    const clipH = bodySize.h || height;
    if (clipH !== height) {
      await page.setViewportSize({ width: clipW, height: clipH });
      await page.waitForTimeout(100);
    }

    await page.screenshot({
      path: pngPath,
      clip: { x: 0, y: 0, width: clipW, height: clipH },
      type: 'png',
    });
    await page.close();
    console.log(`  ${basename(pngPath)}  (${clipW}×${clipH})`);
    pngPaths.push(pngPath);
  }
} finally {
  await browser.close();
}

if (wantPdf) {
  let PDFDocument;
  try {
    ({ default: PDFDocument } = await import('pdfkit'));
  } catch {
    console.error('pdfkit not installed. Run: npm install pdfkit');
    process.exit(1);
  }
  const slug = basename(dir);
  const pdfPath = join(dir, `${slug}.pdf`);
  const doc = new PDFDocument({ size: [width, height], margin: 0, autoFirstPage: false });
  doc.pipe(createWriteStream(pdfPath));
  for (const png of pngPaths) {
    doc.addPage({ size: [width, height], margin: 0 });
    doc.image(png, 0, 0, { width, height });
  }
  doc.end();
  console.log(`PDF: ${pdfPath}`);
}

console.log('Done.');
