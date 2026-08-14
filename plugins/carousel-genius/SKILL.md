---
name: carousel-genius
description: Design and ship multi-slide carousels (Instagram, LinkedIn, TikTok, X) using one of 5 reverse-engineered creator layouts (Rahul Yadav, Marketing Harry, Sago, terminal/monospace, photo-narrative). Use whenever the user asks to create a carousel, IG post deck, LinkedIn doc, slide series, swipe deck, or multi-slide social content. Also trigger on phrases like "make a carousel", "design slides for X", "build a swipe deck", "turn this into slides", "post this as a deck", or any request to produce 3+ social slides as a set. Distinct from single-artifact brand-styling skills (use your own if you have one) — this skill orchestrates story → layout pick → templates → rendered PNG slides → captions delegated to a captions plugin if you have one. Works with any brand, or with clean neutral defaults if you don't specify one.
created_by: external
pinned: false
version: 0.1.0
---

# Carousel Genius

Production system for shipping carousel decks that look like the top AI-niche creators, not generic AI templates. Built from reverse-engineering 41 source slides across 3 real creators (@therahulyadav, @marketingharry, @thesagocreator), plus two original data/photo layouts developed for this system. Works for any brand — apply your own brand skill if you have one, or use the clean neutral defaults if you don't.

## When to use

Trigger this skill when the request involves making 3+ slides as a set:
- "Make a carousel about X"
- "Build a LinkedIn doc on Y"
- "Turn this story into a swipe deck"
- "Design 7 slides about Z"
- "Post this as an IG carousel"

For single-image branded artifacts (one social post, a freebie cover, a website hero), use your own brand-styling skill instead if you have one (e.g. a `<your-brand>-brand` skill). For caption-only requests after the deck is designed, delegate to a captions plugin if you have one (e.g. `viral-captions` via `/caption <topic>`).

## Real-data sourcing (do this BEFORE writing copy)

**Never fabricate revenue, usage, or outcome numbers.** Carousels live or die on specificity, and specificity that turns out to be invented kills trust on contact.

**Before drafting any slide copy, pull real numbers from your own source of truth** — whatever notes file, CRM export, deal tracker, or research library you already keep. If this workspace has a verified-metrics doc or a research folder, read it first and prefer those numbers over anything you'd otherwise have to guess at.

**Rule:** if a number is verified, use it verbatim. If you need a number that isn't measured yet, mark it explicitly — "projected," "estimated," "based on [named source]." Never round up an estimate into a hard claim.

**Example of the discipline:** a stat-grid slide reading "−59% time / −67% tokens / 14 skills/mo" should be labeled "projected from [named source]. Measurement starts this week" rather than presented as a confirmed result — that's the difference between a claim that survives scrutiny and one that doesn't.

## The 4-step workflow

```
1. INTAKE  →  2. PICK LAYOUT  →  3. BUILD HTML  →  4. RENDER + CAPTIONS
```

### Step 1 — Intake (always do this first)

Ask only what's missing. Don't run a 10-question intake when the story is obvious. The fields:

| Field | Required? | Default if missing |
|---|---|---|
| **Story / topic** | yes | — |
| **Platform** | yes | IG (1080×1350) |
| **Slide count** | no | 7 (IG) / 9 (LinkedIn) / 5 (TikTok) |
| **Layout variant** | no | Recommend one based on story type (see § Layout Picker) |
| **Brand** | no | Clean neutral defaults baked into the templates; apply your own brand skill first if you have one, or override via the `brand:` YAML block |
| **Voice override** | no | Pull from `~/.claude/plugins/viral-captions/knowledge/USER_VOICE.md` if exists, else neutral |
| **CTA type** | no | Question close (default), DM trigger, manifesto, soft offer |

If story or platform is missing, ask once. Anything else — make a reasonable default and proceed. Show the user the picked layout + headline pattern, get a thumbs-up, then build.

### Step 2a — Pick a content format (orthogonal to layout)

The 5 content formats — what KIND of carousel this is. Pick one before picking visual layout:

| # | Format | When | Example title |
|---|---|---|---|
| 1 | **Comparison** | Bad vs Good / Old vs New / Wrong vs Right | "Ugly carousel vs Viral carousel" |
| 2 | **Tutorial** | Step-by-step how-to | "Viral Carousel in 2 minutes" |
| 3 | **Native** | Your picture used inside the design | "How I got 37 logo design projects in 30 days" |
| 4 | **Compilation** | Curated list / guide / catalog | "Best carousel tools for 2026" |
| 5 | **Story** | Personal narrative + lesson | "I lost a $40k retainer the week I shipped this" |

**Format → layout mapping (default suggestions):**
- Comparison → Layout 4 (Terminal / monospace) compare cards
- Tutorial → Layout 1 (Rahul) step blocks + terminal
- Native → Layout 5 (Photo-narrative)
- Compilation → Layout 2 (Marketing Harry) anatomy stamps OR Layout 1 (Rahul) listicle
- Story → Layout 3 (Sago) editorial

### Step 2b — Layout picker

The 5 visual variants. Each has a distinct personality. **Always pick exactly one — don't blend.**

| # | Layout | Hero | Body | When to use | Template |
|---|---|---|---|---|---|
| 1 | **Rahul (heavy display)** | AI portrait + giant Druk/Bebas two-tone headline (one word red) | Step numerals + terminal blocks + pill payoff | Tactical "X tools / N steps" listicle | `templates/01-rahul-display.html` |
| 2 | **Marketing Harry (meta)** | Surreal AI hero + single keyword in pink-orange gradient | White-bg anatomy stamp cards + mock IG post proof | Educational "How to do X" | `templates/02-marketing-harry.html` |
| 3 | **Sago (editorial poster)** | Portrait + giant red headline on textured paper bg | Charcoal/paper alternating + hand-drawn doodles | Personal-brand thought-leadership | `templates/03-sago-editorial.html` |
| 4 | **Terminal / monospace** | Big numerical hero + JetBrains Mono labels | Data tables + thin magenta dividers + bottom-edge glow | News commentary, financial story, deal breakdown | `templates/04-terminal-mono.html` |
| 5 | **Photo-narrative** | AI-generated photo with intentional negative space (subject right, dark left for text) | Photo + designed alternating | Case study, atmospheric mood, founder story | `templates/05-photo-narrative.html` |
| 6 | **Bare hook** | Background + headline only, no chrome decoration | Same — bare text on color | Single-statement hook decks, manifesto, "fragment" carousels | `templates/06-bare-hook.html` |

**Picker heuristics** (when user doesn't specify):
- Story has steps / a numbered list / a workflow → **#1 Rahul**
- Story is a "how" or "anatomy of X" educational → **#2 Marketing Harry**
- Story is opinion / philosophy / personal essay → **#3 Sago**
- Story is news / data / numbers / a deal → **#4 Terminal / monospace**
- Story is a case study / mood / atmospheric → **#5 Photo-narrative**
- Story is a single statement / manifesto / one-line bomb per slide → **#6 Bare hook**

### Step 2c — Pick body types per slide (NEW — orthogonal to layout)

Within Layout 4 (Terminal / monospace — the most-used), every interior slide is built from one **body type**. Vary them across the deck — same body type on consecutive slides reads as a template.

Full anatomy + CSS specs in `references/components.md`. Quick catalog:

| Body type | Visual purpose | When to use | YAML key |
|---|---|---|---|
| **pullquote** | Centered big quote + deep-purple left border + attribution | HN complaint, customer quote, manifesto line | `pullquote:` |
| **code_compare** | Two code blocks side-by-side (bad / good) with YAML syntax tinting + strikethrough | Before/after configs, wrong-vs-right code | `code_compare:` |
| **stat_grid** | 3 hero stat cards horizontal. Each: label / before→after / giant magenta hero number / arrow | Dashboard "what changed", projected gains, outcome metrics | `stat_grid:` |
| **icon_row** | 3 brand glyphs side-by-side with `→` arrows between, label below each | "X → Y → Z" architecture flow, tech stack reveal | `icon_row:` |
| **harness_cards** | 3-column grid: logo mark + name + positioning paragraph + stat footer. Tiers: `good` (magenta glow), `flag` (yellow), `default` | Comparing 3 tools / pricing tiers / approach options | `harness_cards:` |
| **term_side** | Terminal block left + framework list right (2-col grid) | Real command + the files/files-it-touches explanation | `term_side:` |
| **mockup** | White profile card (avatar + handle + stats + bio) + annotation right | Track-record proof, receipt slide | `mockup:` |
| **framework** (+ optional `side_thumbs`) | Numbered list (left) + optional card thumbnails (right) | Multi-step playbook + visual receipt | `framework:` / `side_thumbs:` |
| **data_table** | 2-3 column table, JetBrains Mono, magenta dividers | Specs, comparisons, numerical breakdown | `data_table:` |
| **terminal** | Single 3-line terminal block (`$ cmd` → progress → `✓ success`) | One-command receipt | `terminal:` |
| **num_hero** | Giant 220px mono number + label below | The slide IS one number ($40B, 14× etc.) | `num_hero:` |
| **compare** | Two cards side-by-side (✗ red / ✓ magenta) | Quick before/after option pair | `compare:` |
| **step_block** | One numbered card left + imperative title + 1-line description right | One-step-per-slide tutorials | `step_num:` + `step_imperative:` + `step_desc:` |
| **size_cards** | 3 horizontal spec cards with bad/ok/good tiers | Canvas size pick, plan tiers | `size_cards:` |

**Slide-level decoration props (orthogonal — stack on top of any body type):**

- `ghost_numeral: "5"` — giant outlined SVG numeral floats bottom-right as graphic element. Use on "3 things" / "5 patterns" slides.
- `diagonal_stripe: true` — asymmetric magenta-gradient slash at -8° across canvas. Use as visual rhythm-break on text-heavy slides.

### Step 2d — Pick a theme per slide (NEW — rhythm matters)

Slide-level `theme:` prop on Layout 4 (Terminal / monospace). Mix themes across the deck OR commit to one theme + lean on `ghost_numeral` / `diagonal_stripe` for variety.

| Theme | bg / text | Accent treatment | When to use |
|---|---|---|---|
| **(default — no theme)** | `#0B0C0C` dark + white text + 8-layer SVG purple glow stack | Magenta-to-violet gradient text on accent words | Most slides. The default house style — swap the CSS variables for your own brand colors if you like. |
| **`theme: light`** | `#F4EFE4` cream + deep navy text + soft purple ellipses (no glow) | Brand-purple → magenta gradient text. Dark thumb cards POP on cream. | Cover/CTA, alternating-rhythm decks, anything that needs to feel "premium print" instead of "agency dark mode" |
| **`theme: accent`** | Full magenta-purple radial gradient bg (no glow, no ellipses) | Solid white statement, smaller white pill at bottom | Climax slide ONLY. The thesis. The one-line bomb. Use exactly once per deck. |

**Rhythm rule:** alternate themes across the deck (e.g. harness deck = cream cream cream cream cream cream cream cream **accent** cream — 9 cream + 1 climax) OR full-dark with occasional cream interjection. The all-dark monotone is what reads as "AI carousel template" — at least one rhythm-break per 5 slides.

### Step 2e — Icon resolver (NEW — drop SVG → use `logo_icon: <name>`)

For `harness_cards` and `icon_row` body types, real brand SVGs beat emoji or single-letter monograms every time. The build script auto-resolves:

```yaml
harness_cards:
  - logo_icon: hermes        # → assets/icons/hermes.svg
    name: "Hermes"
  - logo_icon: openclaw
    logo_multicolor: true    # preserve SVG's own colors (e.g. pixel lobster)
    name: "OpenClaw"
  - logo_icon: claude        # → assets/icons/claude.svg
    name: "Claude Code"

icon_row:
  - logo_icon: terminal
    label: "LAPTOP / LOCAL"
  - logo_icon: docker
    svg_class: "docker"      # → fill: #2496ED (Docker blue)
    label: "DOCKER"
  - logo_icon: modal
    svg_class: "modal"       # → fill: #06FF92 (Modal green)
    label: "MODAL"
```

**How it works:** `resolve_icons_in()` in `scripts/build_carousel.py` walks every dict/list in the YAML. Where it finds `logo_icon: <name>`, it reads `assets/icons/<name>.svg` and injects the inline SVG as `logo_svg:`. The template renders `{{card.logo_svg | safe}}` inside the logo mark.

**Brand-color overrides** (defined in template CSS — `templates/04-terminal-mono.html`):
- `svg_class: docker` → fill `#2496ED`
- `svg_class: modal` → fill `#06FF92`
- `svg_class: terminal` → fill magenta (dark) / brand-purple (light)
- Default (no `svg_class`) → fill `#0B0C0C` on dark bg, fill white on light

**Multicolor SVGs** — set `logo_multicolor: true` to skip the fill override. The SVG renders with its own colors on a peach pad (`#FFF1EE`). Used for the OpenClaw pixel lobster.

**Adding new icons:**
1. Drop `assets/icons/<slug>.svg` (keep viewBox, strip width/height)
2. Reference as `logo_icon: <slug>` in YAML
3. Done

**Quick source for brand icons:** `curl -sf https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/<slug>.svg -o assets/icons/<slug>.svg`. Works for `docker`, `anthropic`, `ycombinator`, etc.

Already shipped: `claude.svg`, `anthropic.svg`, `docker.svg`, `ycombinator.svg`, `hermes.svg`, `openclaw.svg` (pixel lobster — multicolor), `modal.svg`, `terminal.svg`.

## Spacing & text-mass rules (the part v1 missed)

The single biggest difference between viral creators and AI-generated decks is **how much canvas the text occupies.**

**Hard rule: text fills 40-60% of canvas, NOT 80%.** The rest is intentional whitespace + brand chrome.

### Title-top, content-center, chrome-edge anchoring

**Stop anchoring headlines at `bottom: 220px`.** That's the v1 mistake.

Instead, every layout uses this 3-zone vertical grid:

```
┌─────────────────────────┐  y=40   ─ chrome top (logo, counter)    [120px]
│  CHROME ZONE            │  y=160
├─────────────────────────┤
│                         │  y=200  ─ TITLE ZONE                    [240px]
│  TITLE / HEADLINE       │
├─────────────────────────┤
│                         │  y=440  ─ CONTENT ZONE                  [780px]
│  body / proof block     │
│  (with breathing room   │
│   between elements)     │
│                         │
├─────────────────────────┤
│                         │  y=1220 ─ chrome bottom (handle, swipe) [220px]
│  CHROME ZONE            │
└─────────────────────────┘  y=1440
```

- **Title zone** = 16-18% of canvas height — short headline, max 2 lines
- **Content zone** = 54-58% — proof block (terminal, table, cards, photo, diagram). Lots of breathing room between elements (60-100px gaps).
- **Chrome zones** combine to ~25% — top (logo + counter) + bottom (handle + swipe + hairline)

### Numbered yellow-card pattern (design.deb signature)

For step / item / framework slides, use small colored cards on the left + content on the right. Cards are 80-100px wide rounded squares with the brand accent color, white number inside.

```
[01]  Pick 2 fonts
       Headline + Body

[02]  Pick 3 colors
       Background + Text + Accent

[03]  Pick a consistent image style
       Ex: Realism
```

- Cards: 88×100px, accent fill, rx=12
- Number: 44-52px, JetBrains Mono 700, contrasting color (black on yellow, white on purple)
- Content right of card: 36-44px headline + 22-26px description
- Vertical spacing between rows: 80-100px

### Breathing room rules

- Between any two visual elements: **minimum 60px**, ideally 80-100px
- Between title and first content element: **120-160px**
- Around any photo or screenshot: **40px padding** so it doesn't kiss the edge
- Empty bottom 20-30% of slide is fine — that's where the chrome lives + lets the swipe cue have room

## Visual verification workflow (MANDATORY — do not skip)

**Never batch-render before verifying slide 1.** Code-level inspection lies about font sizes, gradient contrast, and spacing density. The only trustworthy check is the rendered PNG.

**The loop:**

- [ ] **1. Build YAML brief** — `examples/` for reference
- [ ] **2. Run build** — `python3 scripts/build_carousel.py brief.yaml` → N HTMLs in `out/{slug}/`
- [ ] **3. Render slide 1 ONLY** — `node scripts/render_pngs.mjs out/{slug} --only 1`
- [ ] **4. Read the PNG via the Read tool** — verify visually against the inspo / brand reference
- [ ] **5. If wrong:** edit template/brief, repeat from step 3 (re-render only slide 1)
- [ ] **6. Once slide 1 lands:** render full deck (`node scripts/render_pngs.mjs out/{slug}`)
- [ ] **7. Spot-check slide 2-3 visually** — body type swap is where new bugs hide
- [ ] **8. Squint test the cover** — readable at 25% zoom? If not, headline too small or contrast wrong

Why this matters:
- Font sizes look different rendered vs. in code
- Spacing looks tight in code, fine rendered (or vice versa — gradient text gets crushed)
- Glow stack overlap with photo / pill creates illegibility you can't see in HTML source
- The squint test only works on rendered output

The `render_pngs.mjs` script supports `--only N` to render a single slide.

## Image generation (for hero photos / cover images)

Before rendering Layout 5 (photo-narrative) or any slide needing an AI image, generate it via:

**Option A — Higgsfield (Soul V2 free tier or Ultimate Cinematic):**
- Use `higgsfield-soul-id` skill if you need creator's face
- Use `higgsfield-generate` skill for general images
- Soul V2 = free; GPT Image 2, Cinema Studio = paid (warn user about credits)
- Save output to `out/{slug}/assets/hero.jpg`, reference in brief

**Option B — Nano Banana via opencli (Gemini):**
```bash
opencli gemini imagen --prompt "subject right of frame, intentional negative space left, dark moody, cinematic" --out out/{slug}/assets/hero.jpg
```

**Hero photo prompt template (Layout 5):**
```
{subject description}, intentional negative space on LEFT side (for headline overlay),
subject positioned in right-third of frame, dark moody cinematic lighting,
shot on Hasselblad, 4:5 vertical, photorealistic, high contrast
```

Always view the generated image before adding to the brief — don't trust the prompt-to-image fidelity blind. Use the same visual-verification rule.

### Step 3 — Build HTML

Every deck is N HTML files (one per slide), all rendered at the platform canvas size. Use `scripts/build_carousel.py` with a YAML brief (see `examples/example-brief.yaml`).

**Universal rules — apply to every layout:**

1. **Persistent chrome on every slide** — top-left logo, top-right `[SECTION] · NN/TT`, bottom-left handle (`@your_handle` or whatever the brief sets), bottom-right escalating swipe cue (KEEP GOING → NEXT → ALMOST → ONE MORE → SAVE THIS ↓ on final).
2. **One idea per slide** — single dominant headline carries the slide. No two competing thoughts.
3. **Two-tone headline** — mostly white (or mostly navy on light) + ONE word in the layout's accent color. **COLOR ONLY — never italic, never slanted.** The color jump alone carries the emphasis. Italic on emphasis is the #1 AI-design tell.
4. **Three-color discipline** — pick 3 colors for the deck and stick to them. Cover/outro can use a 4th tier.
5. **Text mass > image mass (~70/30)** — typography dominates. The hero glow/photo is supporting, not the focal point.
6. **Engineered swipe motivation** — every non-final slide ends with directional cue + withheld payoff in the headline.
7. **Named CTA** — final slide says `Comment STACK` or `DM AUDIT` or asks a specific question. Never "DM us to learn more."
8. **Brand face appears 2×** — slide 1 + final slide. Wordmark + handle ribbon. Author-less middle slides are fine, but the deck closes the loop.

**Canvas sizes (UPDATED 2026-05-06 — both @marketingharry and @design.deb confirmed):**
- **Default = 1080 × 1440 (3:4) — THE best.** Maximum vertical real estate, fully native to IG, LinkedIn doc, Threads.
- 1080 × 1350 (4:5) — only use if you're going to boost the post.
- 1080 × 1080 (1:1) — DO NOT POST. Wasted space, looks small in feed.
- 9:16 export for TikTok / Stories: 1080 × 1920 (re-render not re-design)

**Safe zone (cover survives crops):** 180px top + bottom, 50px left, 120px right.

**Distribution hack:** Carousels published with music appear in the **Reels tab** as well as the feed grid — double surface. Always add a track on IG.

### Step 4 — Render + captions

Render with `scripts/render_pngs.mjs` (Playwright Chromium → PNG screenshots). LinkedIn-doc PDF via the same script with `--pdf` flag.

**Captions:** delegate to the `viral-captions` plugin. After deck is rendered, suggest the user run `/caption <story>` to get per-platform captions in their voice.

## Brand tokens — opt-in, with clean neutral defaults

This skill (`carousel-genius`) is responsible for the **multi-slide system** — slide anatomy, hook copy, layout picking, persistent chrome, render pipeline. Visual identity is separate and optional.

**If you have your own brand skill or style guide** (e.g. `<your-brand>/SKILL.md`), read it first and pull its logo, colors, and type before building the brief — don't redeclare tokens here.

**If you don't have one**, the templates ship with clean neutral defaults baked in: Layouts 1/2/3 (Rahul, Marketing Harry, Sago) use each creator's own locked palette by design — that's the point of picking them. Layouts 4/5/6 (Terminal / monospace, Photo-narrative, Bare hook) ship with a dark-bg + magenta/purple accent default that's free to reskin.

**What's actually override-able via the YAML brief today:**

```yaml
brand:
  name: "AcmeCo"        # used for the fallback text wordmark
  handle: "acme"        # rendered as @{{handle}} in the chrome
  logo_svg: "<svg>...</svg>"   # optional inline SVG; overrides the text wordmark
```

If `brand:` is omitted, the skill falls back to a placeholder name/handle (`YOUR BRAND` / `your_handle`) so nothing renders as another user's identity.

**What's NOT wired through the brief yet:** per-layout color/font overrides (`bg`, `primary`, `accent`, `display_font`, `body_font`). Layouts 4/5/6's colors and Layouts 1-6's fonts are set in each template's CSS `:root` block — to reskin them, edit the `:root` custom properties directly in the relevant `templates/*.html` file.

## The 12 hook archetypes (pick one for slide 1)

Don't mix archetypes within a deck. Adapt with named numbers + named villain.

| # | Archetype | Template |
|---|---|---|
| 1 | Contrarian punch | "Everyone is X. They're <em>building the wrong thing</em>." |
| 2 | Specific number + outcome | "We shipped N Y in W weeks. <em>Here's the stack.</em>" |
| 3 | Mistake confession | "I burned $X on Y nobody used. <em>N lessons.</em>" |
| 4 | Curiosity gap | "The X most Y will <em>quietly kill</em> in 2026." |
| 5 | Listicle promise | "N X you'll <em>actually use</em>." |
| 6 | Question hook | "Why does X keep failing <em>inside Y</em>?" |
| 7 | Identity callout | "If you're a [role] in 2026, <em>read this first.</em>" |
| 8 | Status reveal | "How X are quietly replacing Y — <em>in N slides.</em>" |
| 9 | Before/after compression | "From [old metric] to <em>[new metric].</em>" |
| 10 | Enemy-Hero-Teaser | "[Enemy] is dying. [Hero] is <em>eating it.</em>" |
| 11 | Receipt drop | Slack/DM screenshot + carousel of how |
| 12 | Naming-the-thing | "There's a name for X: <em>'[term].'</em>" |

**Hook quality test:** if you can't paste it into Twitter and have it land as a single tweet, it's not a hook yet. Iterate before building.

## Slide-2 patterns (the swipe-survival slide)

60-70% of viewers bail or commit on slide 2. Pick ONE based on hook:

- **Agitate the pain:** "And it's worse than you think. Here's what [Y] actually costs you: [stat]."
- **Reframe the villain:** "The problem isn't [obvious]. It's [unseen lever]."
- **Set the stakes:** "Skip this and [consequence]. By [date], [outcome]."
- **Promise the payoff:** "By slide [N] you'll know [specific thing]."
- **List intro:** "Here are the [N]. Number [X] is the one nobody copies."

## Voice tics (apply to all copy)

- Sentence-fragment punch ("Then it clicked." "Wrong." "Every time.")
- Odd numbered counts (9 beats 10, 7 beats 5)
- Self-aware aside ("(you'll hate slide 4)")
- First-person stakes ("I lost a $40k retainer the week I shipped this.")
- Mid-sentence em-dash reveal — used sparingly
- Specificity ($11,400 beats ~$10k; "Tuesday 9:43am" beats "last week")
- Jargon followed by translation ("MCP servers — basically USB-C for AI tools")
- One contraction per slide minimum (kills the AI cadence)
- Imperative verbs in step headlines (INSTALL / ADD / LOAD / CONNECT)

## The 10-slide carousel anatomy (Marketing Harry + Design.deb confirmed)

Both top creators converge on the same skeleton. Use this for IG; contract to 7 for short attention; extend to 12 for LinkedIn.

| Slide | Phase | Function |
|---|---|---|
| 1 | **HOOK** | Stop the scroll. One of the 42 archetypes. Two-tone headline. |
| 2 | **TRANSITION** | Confirm the hook. Restate the promise. What user will gain / avoid / qualify. |
| 3 | **TEASE 1** | Build interest with an example. |
| 4 | **TEASE 2** | Retain attention with a diagram / visual proof. |
| 5 | **TEASE 3** | First piece of practical info. |
| 6 | **TEASE 4** | Practical info continued. |
| 7 | **TEASE 5** | Practical info continued (optional save-the-post slide). |
| 8 | **CLIMAX 1** | The "Aha" moment. Big reveal, quotable line, lesson. |
| 9 | **CLIMAX 2** | Hammer home the insight with proof / receipt / screenshot. |
| 10 | **ACTION** | Make the next step obvious. Named CTA. |

## Three slide types (slide-level discipline)

Every slide is one of these — never two:

| Type | Body rule | Use on |
|---|---|---|
| **Hook slide** | Headline-dominant, minimal body | 1, 2 |
| **Value slide** | A little text + a lot of visuals (diagram, photo, terminal, table, screenshot) | 3-9 |
| **CTA slide** | Image of you + 1 simple action | 10 |

## Carousel design — the 3 hard rules

From @design.deb (cross-confirmed by all sources):

1. **Pick 2 fonts** — one Headline, one Body. No more. Pair from the viral font combos in `references/font-combos.md`.
2. **Pick 3 colors** — Background + Text + Accent. Lock them. Cover/outro can use a 4th tier.
3. **Pick a consistent image style** — Realism, Editorial, Surreal, Brutalist, Photographic. Don't mix styles within one deck.

## Anti-patterns — what NOT to do (the AI-design tells)

These are the patterns that mark a carousel as generic-AI-template-output. Avoid all of them.

- **Italic on emphasis words** — color swap only. Italic on an accent word is the #1 AI tell. Use `<span class="accent">` with a magenta-to-violet gradient instead.
- **Top-anchored headline + empty bottom 40%** — center the content vertically (`grid-template-rows: auto 1fr auto`) or push proof into the middle zone. Dead air at the bottom looks like a half-finished slide.
- **Same body type on three consecutive slides** — vary. If you're using `framework` on slide 3, switch to `code_compare` or `stat_grid` on slide 4.
- **Personal data in generic carousels** — generalize the metric. Say "your skill library" not "my 197 skills" when the carousel is about a pattern, not a brag. Reserve specific personal numbers for receipt-drop slides.
- **Single accent solid color where a gradient works** — accent words on dark theme should use `linear-gradient(135deg, magenta, hot-purple, lavender)`, not solid `#D777F4`. The gradient is the brand signature.
- **All slides the same theme** — see the rhythm rule above. Dark-dark-dark-dark-dark reads as a template. Drop one cream or one accent climax.
- **Buzzword filler in copy** — never use `leverage`, `pivotal`, `unlock`, `showcase`, or `harness` as a verb. Replace with the concrete verb (`use`, `key`, `open`, `show`, `wire`).
- **Emoji in chrome** — SVG glyphs only. Dot, arrow, asterisk, doodle pack. No 🚀 or 💡.
- **Headline lines that look like 1.05 line-height but render too loose** — Public Sans at 76px needs `line-height: 1.0`, not `1.05`. Verify rendered.
- **YAML / code blocks in regular slide font** — code goes in `code_compare` or `terminal` (JetBrains Mono, dark card, magenta border on the good side).

## Quality checklist (run before render)

**The squint test:** Squint at the cover from arm's length. Can you still read the headline? If not, headline is too small or contrast is wrong. **Every cover must pass this.**

- [ ] **Cover passes the squint test** (readable at 25% zoom)
- [ ] Hook is one of the 42 archetypes with named numbers + named villain
- [ ] Slide 2 confirms the hook (transition slide)
- [ ] Each slide is exactly one of: Hook / Value / CTA (no hybrids)
- [ ] **2 fonts, 3 colors, 1 image style** locked across deck
- [ ] One idea per slide
- [ ] Persistent chrome on every slide (4 corners)
- [ ] Two-tone headline (one accent word per headline)
- [ ] Specific numbers on at least one block per slide
- [ ] One pill payoff per interior slide
- [ ] Escalating swipe cue sequence
- [ ] End slide visually rhymes with cover
- [ ] Named CTA (not "DM us")
- [ ] At least one contraction per slide
- [ ] No emojis in deck (SVG icons only)
- [ ] Brand face/wordmark visible on slides 1 + N
- [ ] Music attached on IG publish (carousels with music = Reels tab distribution)

## File index

- `references/layouts.md` — full breakdown of all 5 layouts (typography stacks, color tokens, component anatomy)
- `references/hooks.md` — **42 archetypes** (12 originals + 30 viral templates from @marketingharry) with real examples + slide-2/mid/end patterns
- `references/components.md` — persistent chrome, pill payoff, terminal block, anatomy stamp, mock-IG-post, doodle pack
- `references/font-combos.md` — 6 viral font pairings (Thunder+Euclid, Creato+Plus Jakarta, Bethany Elingston+Neulis Neue, Titillium+Unigeo64, Calm Love+Constantia, Brunson Rough+Darker Grotesque) + this skill's shipped defaults
- `references/anatomy.md` — the 10-slide carousel anatomy + 3-slide-type discipline + squint test
- `references/render-pipeline.md` — Playwright render notes + zombie-process troubleshooting
- `templates/01-rahul-display.html` through `06-bare-hook.html` — six layout templates (04 has the full body-type catalog + theme variants)
- `scripts/build_carousel.py` — YAML brief → N slide HTMLs. Includes `resolve_icons_in()` icon resolver + `ICONS_DIR` lookup
- `scripts/render_pngs.mjs` — Playwright PNG/PDF renderer (supports `--only N`)
- `assets/icons/` — brand SVG glyphs (claude, anthropic, docker, ycombinator, hermes, openclaw, modal, terminal). Drop new ones here as `<slug>.svg`
- `examples/example-brief.yaml` — minimal sample input
- `examples/example-harness-deck.yaml` — **cleanest reference deck.** Uses ALL new body types (pullquote, code_compare, stat_grid, icon_row, harness_cards, term_side, framework) + theme rhythm (9× light + 1× accent climax) + icon resolver + ghost numeral

## Rendering troubleshooting

If Playwright hangs on Mac (known issue from 2026-05-06):
1. Kill all `playwright-mcp` zombies first: `pkill -f playwright-mcp; pkill -f chromium`
2. Reinstall chromium: `npx playwright install chromium --force`
3. Use `chromium.launch({ headless: 'new', timeout: 60000 })` in render script
4. Fallback: open HTML files in Chrome directly and screenshot manually

## Inspirations on disk (optional)

The templates and reference docs in this skill already encode the reverse-engineered patterns (41 source slides across @therahulyadav, @marketingharry, @thesagocreator), so a fresh read usually isn't needed.

If you keep your own folder of reference/inspiration slides for a creator you're modeling, point Claude at it the same way when the request is "match this creator exactly" — otherwise the templates here capture the system well enough to build from directly.
