# carousel-genius — quick start

A Claude Code skill that ships multi-slide carousels using one of 5 reverse-engineered creator layouts.

## What's in the box

```
carousel-genius/
├── SKILL.md                       # Skill body (auto-loaded by Claude)
├── README.md                      # This file
├── references/
│   ├── layouts.md                 # All 5 layouts in detail
│   ├── hooks.md                   # 12 hook archetypes + slide patterns + voice tics
│   ├── components.md              # Copy-paste HTML/CSS for chrome, pills, terminal, etc.
│   └── render-pipeline.md         # Playwright notes + zombie troubleshooting
├── templates/
│   ├── 01-rahul-display.html      # Tactical listicle (Druk/Bebas all-caps)
│   ├── 02-marketing-harry.html    # Educational meta (1080×1440, gradient accent)
│   ├── 03-sago-editorial.html     # Editorial poster (paper + charcoal + red)
│   ├── 04-terminal-mono.html      # News commentary / data (mono labels, magenta)
│   ├── 05-photo-narrative.html    # Case study atmospheric (AI photo + alt designed)
│   └── 06-bare-hook.html          # Single-statement hook / manifesto decks
├── scripts/
│   ├── build_carousel.py          # YAML brief → N slide HTMLs
│   └── render_pngs.mjs            # Playwright HTML → PNG (and optional PDF)
└── examples/
    ├── example-brief.yaml         # 9 AI agents (terminal layout)
    ├── example-rahul.yaml         # 5 Claude skills (rahul layout)
    ├── example-sago.yaml          # Agency model is over (sago)
    ├── example-harry.yaml         # ART of viral carousels (marketing-harry)
    └── example-photo.yaml         # 14-day → 38-min case study (photo-narrative)
```

## Run it

```bash
# 1. Install Python deps (one-time)
pip3 install pyyaml jinja2

# 2. Build slides from a YAML brief
python3 ~/.claude/skills/carousel-genius/scripts/build_carousel.py \
  ~/.claude/skills/carousel-genius/examples/example-brief.yaml \
  --out ./out

# 3. Render to PNGs (in any project dir with playwright installed)
node ~/.claude/skills/carousel-genius/scripts/render_pngs.mjs \
  ./out/9-agents-creative

# 4. (Optional) Add --pdf for LinkedIn doc
node ~/.claude/skills/carousel-genius/scripts/render_pngs.mjs \
  ./out/9-agents-creative --pdf
```

## How Claude uses it

When you ask Claude to "make a carousel about X" / "build a swipe deck on Y":

1. Claude auto-loads this skill (description matches "carousel" / "swipe deck" / "slides for")
2. Asks only the missing inputs (story, platform if not obvious)
3. Picks a layout based on story type (uses the picker heuristics in SKILL.md)
4. Writes a YAML brief
5. Runs `build_carousel.py` to generate HTML
6. Runs `render_pngs.mjs` to generate PNGs
7. Suggests `/caption <topic>` to delegate caption-writing to the `viral-captions` plugin

## The 5 layouts at a glance

| # | When | Visual signature |
|---|---|---|
| 1 | Tactical listicle / steps | All-caps display + step numerals + terminal blocks |
| 2 | Educational meta / how-to | Gradient accent word + anatomy stamps + mock IG proof |
| 3 | Personal-brand opinion | Paper + charcoal + red, editorial subhead, hand-drawn doodles |
| 4 | News / data / financial | JetBrains Mono labels + data tables + bottom-edge purple glow |
| 5 | Case study / atmospheric | AI-generated photo with negative space + alternating designed slides |

## What's missing / known issues

- **Bebas Neue / Anton fallback only** — Druk Wide and Tungsten are paid; templates use the free Google Font alternates. For premium look, swap in self-hosted Druk via `@font-face` in the template.
- **AI photo step is manual** — Layout 5's hero photo prompt is in `references/image-generation.md`; generate the photo separately (Higgsfield, Nano Banana, or your tool of choice), then reference the path in the YAML brief.
- **Per-layout color/font overrides aren't wired through the YAML brief yet** — `brand.name`, `brand.handle`, and `brand.logo_svg` work; a full color/font re-theme means editing the `:root` CSS variables in the template file directly. See "Brand tokens" in `SKILL.md`.
- **Playwright may hang on Mac** — see `references/render-pipeline.md` for zombie-process troubleshooting + manual fallback (open HTML in Chrome, screenshot manually).

## Inspirations & source research

This skill was built by reverse-engineering 41 source slides across three real creators — @therahulyadav, @marketingharry, @thesagocreator — plus two original data/photo layouts developed for this system. The templates and `references/*.md` files already encode those patterns, so you shouldn't need outside material to use it.

If you're maintaining your own research folder of source slides/creator analyses, point Claude at it the same way when you want pixel-parity with a specific creator's post.
