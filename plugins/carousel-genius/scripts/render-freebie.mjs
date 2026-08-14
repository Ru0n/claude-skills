#!/usr/bin/env node
/**
 * Render a single standalone HTML page (e.g. a freebie/report) to PDF.
 *
 * Usage:
 *   node render-freebie.mjs <input.html> [output.pdf]
 *
 * If output.pdf is omitted, writes alongside the input file with a .pdf extension.
 */
import { chromium } from 'playwright';
import { resolve } from 'path';
import { pathToFileURL } from 'url';

const [inputArg, outputArg] = process.argv.slice(2);
if (!inputArg) {
  console.error('Usage: node render-freebie.mjs <input.html> [output.pdf]');
  process.exit(1);
}

const html = resolve(inputArg);
const pdf = resolve(outputArg || inputArg.replace(/\.html?$/i, '.pdf'));

const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
const ctx = await browser.newContext();
const page = await ctx.newPage();
await page.goto(pathToFileURL(html).href, { waitUntil: 'networkidle', timeout: 60000 });
await page.waitForTimeout(800);
await page.pdf({
  path: pdf,
  format: 'Letter',
  printBackground: true,
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
  preferCSSPageSize: true,
});
await browser.close();
console.log('PDF:', pdf);
