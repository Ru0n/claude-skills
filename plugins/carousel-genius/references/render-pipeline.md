# Render pipeline notes

## How the pipeline works

```
brief.yaml  →  build_carousel.py  →  N HTMLs in out/{slug}/  →  render_pngs.mjs  →  N PNGs + optional PDF
```

1. `build_carousel.py` reads YAML brief, picks layout, fills templates, writes N HTML files to `out/{slug}/slide-NN.html`.
2. `render_pngs.mjs` (Playwright) opens each HTML at canvas size, takes screenshot, saves PNG.
3. Optional `--pdf` flag stitches PNGs into a single PDF (LinkedIn-doc compatible).

## Dependencies

```bash
# Python (in skill scripts/ dir, or globally)
pip3 install pyyaml jinja2

# Node (in project dir where you're rendering)
npm init -y
npm install playwright pdfkit
npx playwright install chromium
```

The skill assumes Playwright is installed in the project's working directory (the carousel-genius skill folder ships scripts but doesn't ship `node_modules` — install per-project).

## Canvas sizes

| Platform | Size | Aspect | Use |
|---|---|---|---|
| **Default — best for IG/LinkedIn/Threads** | **1080×1440** | **3:4** | Default master. Both @marketingharry and @design.deb confirmed (2026-05). |
| Boost-only fallback | 1080×1350 | 4:5 | Only if you're going to put paid behind it. |
| Don't post | 1080×1080 | 1:1 | Wasted vertical space, looks small in feed. |
| 9:16 export | 1080×1920 | 9:16 | TikTok/Stories — re-render not re-design |

**Safe zone:** 180px top + bottom, 50px left, 120px right.

The renderer auto-detects canvas size from the `<body>` `width`/`height` CSS, so each layout template can ship at its native size. Layout 2 (Marketing Harry) is 1080×1440 by default; Layouts 1, 3, 4, 5 are 1080×1350 (legacy). To upgrade Layouts 1/3/4/5 to 1080×1440 swap `body { height: 1350px; }` → `1440px;` in the template.

## Known issue: Playwright hang on Mac (2026-05-06)

**Symptom:** Render starts, no PNGs appear, process sits at 0% CPU. Multiple `playwright-mcp` zombies in `ps`.

**Diagnosis steps:**
1. `ps aux | grep -E 'playwright|chromium' | grep -v grep`
2. If zombies present: `pkill -9 -f playwright-mcp; pkill -9 -f chromium`
3. Reinstall chromium with `--force`: `npx playwright install chromium --force`
4. In `render_pngs.mjs`, use:
   ```js
   const browser = await chromium.launch({
     headless: 'new',
     timeout: 60000,
     args: ['--no-sandbox', '--disable-dev-shm-usage']
   });
   ```
5. Add per-page timeout: `await page.goto(url, { timeout: 30000, waitUntil: 'networkidle' });`

**Manual fallback (when render still hangs):**
- Open each HTML file in Chrome directly
- Use Chrome DevTools (Cmd+Shift+P → "Capture full size screenshot")
- Or use `webapp-testing` skill (Playwright with retry logic) to render

**Last-resort fallback:** Use the `chrome-devtools` MCP (`mcp__chrome-devtools__navigate_page` + `mcp__chrome-devtools__take_screenshot`) per-slide. Slow but reliable.

## PDF output for LinkedIn docs

LinkedIn natively supports PDF document posts up to 100MB. Generate from the rendered PNGs:

```js
// In render_pngs.mjs --pdf mode
import PDFDocument from 'pdfkit';
const doc = new PDFDocument({ size: [1080, 1350], margin: 0 });
doc.pipe(fs.createWriteStream(`out/${slug}/${slug}.pdf`));
for (const png of pngFiles) {
  doc.addPage({ size: [1080, 1350], margin: 0 });
  doc.image(png, 0, 0, { width: 1080, height: 1350 });
}
doc.end();
```

## Font loading

All 5 layouts use Google Fonts. Templates include the font CSS link in `<head>`. Playwright respects `waitUntil: 'networkidle'` to ensure fonts load before screenshot.

If fonts fail to load (offline render), fall back to bundling the woff2 files in `assets/fonts/` and using `@font-face` declarations. See `templates/_fonts.css` for the offline-safe variant.

## Per-platform export pattern

Build once at 1080×1350, then re-render at 1080×1920 for TikTok/Stories by:
1. Same HTML, swap CSS variable `--canvas-h: 1920px;`
2. Re-export with Playwright at the new viewport
3. Designed slides reflow because the body grid is set to `grid-template-rows: auto 1fr auto;`

**Don't try to design separately for each size.** One canvas, two exports.
