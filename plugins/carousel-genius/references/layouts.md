# Layout reference — the 5 variants in detail

Each variant has a fixed typographic stack, color discipline, and chrome rules. Don't blend.

---

## Layout 1 — Rahul (heavy display)

**Source:** @therahulyadav, posts DXHFAh6k6x7 / DXb1q_5EzFa / DWyffywkyVH.

**Visual signature:** AI-generated portrait of the creator on cover, giant condensed-bold all-caps headline, one word swapped to red. Tactical step-by-step body. Loud, magazine-cover energy.

**Canvas:** 1080 × 1350.

**Color tokens (locked):**
- `bg`: `#0B1733` deep navy (master) or `#0B0C0C` warm black
- `accent-primary`: `#E40A14` cover red (for cover headline word swap)
- `accent-secondary`: `#EE1D52` magenta-red (for body emphasis)
- `text`: white
- `muted`: `#7A7C7C`
- `chrome`: white at 60% opacity

**Typography stack:**
- Display (cover + section heads): **Druk Wide Bold** (paid) or **Bebas Neue 400** (free Google Font, fallback). All-caps, letter-spacing -0.02em, line-height 0.95. Hero size 130-148px.
- Body: **Tungsten Bold** (paid) or **Public Sans 600** (free fallback). 26-32px.
- Step numerals: **Public Sans 700** at 88-96px in `accent-primary`.
- Code/terminal: **JetBrains Mono 500** 22-28px.
- Kicker: **JetBrains Mono 500** tracked +0.20em, 14-18px in `accent-secondary` ALL-CAPS.

**Two-tone headline rule:** ALL-CAPS color-swap. One word in pure `accent-primary` red, NOT italic. Visual contrast comes from the color jump alone.
- Example: `"WEB DESIGNERS CHARGE $5K. <span class='red'>YOU'RE WORTH MORE.</span>"`

**Persistent chrome (4 corners):**
- Top-left: white wordmark logo, 80×60
- Top-right: `[KICKER] · NN/TT` in JetBrains Mono 14px tracked +0.20em, magenta-red
- Bottom-left: `● @{{handle}}` JetBrains Mono 14px tracked +0.20em
- Bottom-right: escalating swipe cue (`KEEP GOING →` etc), JetBrains Mono 14px

**Body components:**
- **Step blocks:** giant numeral (88-96px red) on left + imperative verb headline (52-72px white) on right + 1-line description in muted
- **Terminal block:** 3-line JetBrains Mono on `#0F0F1A` bg, 1px border `#2C2655` at 30%, rx=12. Lines = command (white) → progress (muted) → success (green `#00D67D`)
- **Pill payoff:** rounded-12 pill, bg `rgba(238,29,82,0.10)`, 1px border `rgba(238,29,82,0.30)`, text `#EE1D52`, Public Sans 500 at 24-28px

**Hero/cover:**
- Optional AI portrait of subject on right 40% of canvas, with intentional negative space on left for text
- If no portrait: heavy red→navy radial gradient in upper third, headline anchored bottom-third
- Headline: 130-148px, one word in red, max 3 lines

**End slide rhymes with cover:** same portrait/gradient treatment, headline replaced by question or DM trigger.

---

## Layout 2 — Marketing Harry (meta)

**Source:** @marketingharry, post DWLSbsUjP0x ("The ART of Viral Carousels").

**Visual signature:** Surreal AI hero image with one keyword in pink-orange gradient. Anatomy-stamp cards on white interior backgrounds. Mock IG post screenshots as proof. Evolving acronym footer.

**Canvas:** 1080 × 1440 (3:4 — the alt size).

**Safe zones:** 180px top, 180px bottom, 50px left, 120px right.

**Color tokens:**
- `bg-cover`: black `#000000`
- `bg-interior`: white `#FAFAFA`
- `accent-gradient`: `linear-gradient(90deg, #FF1B6B 0%, #FF8A00 100%)` (pink → orange)
- `text-on-dark`: white
- `text-on-light`: `#0B0C0C`
- `muted`: `#5C5C5C`
- `card-border`: `#E5E5E5`

**Typography:**
- Display: **Anton 400** (free Google Font), all-caps, 110-130px
- Body: **Inter 500** or **Public Sans 500**, 22-28px
- Card label: **JetBrains Mono 600** tracked +0.15em, 12-14px, ALL-CAPS

**Two-tone headline rule:** ONE keyword gets the pink-orange gradient via `background-clip: text`. Rest of headline in solid color (white on dark, navy on light).

**Persistent chrome:**
- Top-left: handle with avatar circle + `@marketingharry` style
- Top-right: slide counter `NN/TT`
- Bottom-left: evolving acronym footer (one letter highlights per slide — V·I·R·A·L)
- Bottom-right: small swipe cue arrow

**Body components:**
- **Anatomy stamp card:** white card with rx=24, 1px border `#E5E5E5`, drop-shadow `0 4px 16px rgba(0,0,0,0.08)`. Stamp label (uppercase mono) at top-left, large illustrative number/letter, body text below.
- **Mock IG post block:** rendered fake IG post with username + image placeholder + like/comment counts. Used as social proof.
- **Concept diagram:** simple line illustrations with hand-drawn quality, single-color stroke.

**Hero/cover:**
- Surreal AI image (dreamlike, vaporwave, conceptual) covering full canvas
- Black overlay 40% for text legibility
- Headline anchored bottom-third, one word in pink-orange gradient
- Slide 1 has dark bg; slides 2-N alternate light + dark for rhythm

---

## Layout 3 — Sago (editorial poster)

**Source:** @thesagocreator, posts DXrSeLhk9pt / DXJtsX3E4Rt / DW-iwK-k7t-.

**Visual signature:** Charcoal + paper + red. Hand-drawn doodles. Persistent 4-corner chrome. Editorial magazine feel — thinks like a printed zine.

**Canvas:** 1080 × 1350.

**Color tokens:**
- `bg-paper`: `#F4EFE4` (cream paper texture)
- `bg-charcoal`: `#1A1A1A` (deep charcoal)
- `accent-red`: `#E63946` (vermillion red — for headline keywords)
- `text-on-paper`: `#1A1A1A`
- `text-on-charcoal`: `#F4EFE4`
- `doodle-stroke`: `#1A1A1A` on paper, `#F4EFE4` on charcoal

**Typography:**
- Display: **Tungsten Bold** (paid) or **Bebas Neue 400** (free). 110-140px.
- Editorial subhead: **Playfair Display 700 italic** (free). 36-48px.
- Body: **Public Sans 500**. 24-30px line-height 1.5.
- Quote: **Playfair Display 400 italic**. 28-36px.

**Two-tone headline rule:** keyword gets `accent-red` color, often combined with a subtle weight shift (the rest at 600, the keyword at 700). NOT italic on the headline — Sago reserves italic for editorial subheads + quotes only.

**Persistent chrome (the trademark Sago feature):**
- Top-left: small wordmark or handle
- Top-right: page number `01.` `02.` (with period, like a book)
- Bottom-left: section label in caps, tracked
- Bottom-right: tiny doodle (arrow, asterisk, hand-drawn star)

**Body components:**
- **Hand-drawn doodle pack:** SVG arrows, asterisks, underlines, circles. Stroke 3-4px, slightly imperfect. Used to annotate body text. Library at `assets/doodles/`.
- **Quote block:** centered, italic Playfair, with red left-border 4px
- **Alternating spreads:** odd slides on cream paper, even slides on charcoal — creates magazine spread rhythm

**Hero/cover:**
- Portrait of creator (photographic, not AI) with paper texture overlay
- Giant red headline anchored bottom-third
- Subtle grain/paper noise filter on entire slide

---

## Layout 4 — Terminal / monospace layout

**Source:** an original dark-mode data/terminal layout, refined across several iterations (not reverse-engineered from an external creator — built for this system, and free to reskin).

**Visual signature:** Big numerical hero ($40B, 7 agents, 11hrs/week). JetBrains Mono labels everywhere. Data tables with thin magenta dividers. Bottom-edge purple glow strip.

**Canvas:** 1080 × 1350.

**Color tokens (default palette — swap by editing the `:root` CSS variables in the template, or apply your own brand skill's tokens):**
- `bg`: `#0B0C0C`
- `purple-deep`: `#5C1C8A`
- `magenta`: `#D777F4`
- `text`: white
- `muted`: `#7A7C7C`
- `success`: `#00D67D`
- `error`: `#FF4654`

**Typography:**
- Display (cover): **Public Sans 600** at 130-148px, letter-spacing -0.04em
- Numerical hero: **JetBrains Mono 700** at 180-220px (the "$40B" energy)
- Section heading: **Public Sans 500** at 52-72px, -0.04em
- Data table cells: **JetBrains Mono 500** at 24-28px
- Kicker: **JetBrains Mono 500** tracked +0.20em, 14-18px magenta ALL-CAPS

**Two-tone headline rule:** one word in `magenta` — color only, no italic (the v1 italic-on-accent rule was reversed; gradient or solid color carries the emphasis). Optional text-shadow glow `0 0 32px rgba(215,119,244,0.35)`.

**Persistent chrome:**
- Top-left: brand wordmark/logo (white, 80×60) — falls back to a plain text wordmark if no `logo_svg` is supplied
- Top-right: `[SECTION] · NN/TT` JetBrains Mono 14px magenta
- Bottom-left: `● @{{handle}}` JetBrains Mono 14px
- Bottom-right: swipe cue
- Bottom-edge: 4px gradient strip `purple-deep → magenta → transparent`

**Body components (the full catalog — pick one per interior slide):**

| Body type | Anatomy | YAML key |
|---|---|---|
| **Data table** | 2-3 cols, thin magenta dividers `rgba(215,119,244,0.30)`, JetBrains Mono cells, alternating row bg `rgba(255,255,255,0.02)` | `data_table:` |
| **Num hero** | Giant 220px JetBrains Mono number + 18px uppercase label below | `num_hero:` + `num_label:` |
| **Comparison cards** | Two cards side-by-side: left ✗ (red 8% bg, red 30% border) / right ✓ (magenta gradient bg, magenta 40% border). rx=24 | `compare.bad:` / `compare.good:` |
| **Step block** | 132×132 purple gradient card (left) + imperative title 56px + 1-line description in muted | `step_num:` + `step_imperative:` + `step_desc:` |
| **Terminal block** | `#0F0F1A` bg, magenta-25% border, rx=16. Lines: white cmd → muted progress → green success | `terminal:` |
| **Framework** | Vertical list of `fw-row` items: 88×88 magenta-gradient num card + 42px title + 24px body. Optional `side_thumbs` shows 200px-tall card thumbnails on the right. | `framework:` (+ optional `side_thumbs:`) |
| **Pull-quote** | 64px Public Sans, 6px deep-purple left border, 56px padding, magenta-gradient accent words, mono attribution below | `pullquote.text_html:` + `pullquote.attribution:` |
| **Code compare** | Two code blocks: `.bad` (gray `#1A1A1A` bg, line-through content) / `.good` (`#15101F` gradient + magenta border + magenta glow). YAML tinting via `.yaml-key` (magenta) / `.yaml-val` (lavender) / `.yaml-comment` (35% white) spans | `code_compare.bad:` / `code_compare.good:` |
| **Stat grid** | 3 hero cards horizontal. Each: 13px magenta uppercase label + strikethrough before→after delta + giant 96px magenta-gradient hero number + 28px arrow row (`.down` flips to green) | `stat_grid:` (array of `{label, before, after, hero, arrow, dir}`) |
| **Icon row** | `1fr auto 1fr auto 1fr` grid: 140px brand-icon pad + 14px mono label + `→` arrows between. Real SVG via `logo_icon:`. Brand-color CSS overrides for docker (`#2496ED`) / modal (`#06FF92`) / terminal (magenta) | `icon_row:` |
| **Harness cards** | 3-col grid: 64px logo mark + 30px name + 18px positioning body + uppercase mono stat footer. Tiers: `tier: good` (magenta glow + magenta border), `tier: flag` (yellow), `tier: default` | `harness_cards:` |
| **Term-side** | 2-col grid (`1fr 0.85fr`): terminal block left + tighter framework list right. Use for "real command + the files it touches" | `term_side.terminal:` + `term_side.framework:` |
| **Mockup** | White profile card (avatar circle + handle + meta + stats row + bio) + annotation text right with arrow | `mockup:` |
| **Size cards** | 3 horizontal spec cards with `tier: bad/ok/good` styling | `size_cards:` |

**Slide-level decoration props (stack on top of any body type):**
- `ghost_numeral: "5"` — giant outlined SVG numeral floats bottom-right (text-stroke `rgba(215,119,244,0.35)`, 900px font-size, no fill)
- `diagonal_stripe: true` — asymmetric magenta-gradient slash at -8° across canvas, 20% opacity

**Theme variants (slide-level `theme:` prop):**

| `theme:` | Background | Glow stack | Accent rendering |
|---|---|---|---|
| (omitted) | `#0B0C0C` dark | 8-layer SVG glow (purple) | Magenta-to-violet gradient text |
| `light` | `#F4EFE4` cream | Hidden — soft purple ellipses only | Brand-purple → magenta gradient text. Dark thumb cards POP on cream. |
| `accent` | Full magenta-purple radial gradient | Hidden | Solid white statement, smaller white pill bottom. Climax slide only. |

**Rhythm rule:** alternate themes across the deck OR commit to one + use `ghost_numeral` / `diagonal_stripe` for variety. Monotone dark = AI-template tell.

**Hero/cover:**
- Heavy purple glow upper half (the SVG glow stack baked into the template — swap colors for your own brand if you like) — or hidden on `theme: light` / `theme: accent`
- Headline vertically centered (`cover-stack` uses `justify-content: center`)
- Optional numerical overlay if story is "the X number"

---

## Layout 5 — Photo-narrative layout

**Source:** an original photo + icon layout, refined across several iterations (not reverse-engineered from an external creator — built for this system, and free to reskin).

**Visual signature:** Soul V2 generated photo with intentional negative space. Photo on one slide, designed slide on next. Atmospheric, founder-story energy. Less typography-loud than Layout 4.

**Canvas:** 1080 × 1350.

**Color tokens:** same as Layout 4 (default palette — swap by editing the template's `:root` CSS variables).

**Typography:**
- Display: **Public Sans 500** at 90-110px (smaller than terminal — photo carries more weight)
- Body: Public Sans 500 at 24-32px
- Caption (over photos): **JetBrains Mono 500** 16-18px tracked +0.10em ALL-CAPS, white on photo with subtle drop-shadow

**Two-tone headline rule:** same as Layout 4 (one word in magenta — color only, no italic — with optional glow).

**Photo prompt requirement:**
Soul V2 prompts for hero photos must include: `"intentional negative space on left side, subject positioned right-third of frame, dark moody lighting, cinematic, shot on Hasselblad"` to leave room for headline overlay.

**Persistent chrome:**
- Top-left: brand logo with drop-shadow `0 2px 6px rgba(0,0,0,0.5)` (legibility on photo)
- Top-right: slide counter
- Bottom-left: handle
- Bottom-right: swipe cue
- All chrome on photo slides: white with subtle drop-shadow

**Slide rhythm pattern:**
- Slide 1: photo with headline overlay
- Slide 2: designed (Layout 4 terminal style — text-dominant)
- Slide 3: photo
- Slide 4: designed
- Slide 5: photo
- Slide 6: designed (proof — receipt/screenshot)
- Slide 7: photo with CTA overlay

**Body components on photo slides:**
- Headline overlay: bottom-third, white with `0 4px 24px rgba(0,0,0,0.6)` text-shadow
- Caption strip: top-right or bottom-left, JetBrains Mono caps
- Subtle bottom-gradient `linear-gradient(to top, rgba(0,0,0,0.6), transparent 30%)` for text legibility

**Body components on designed slides:**
- Same as Layout 4 (Terminal / monospace) but with reduced visual weight — more whitespace, fewer data tables, more pull-quotes

---

## Layout 6 — Bare hook

**Source:** Distilled from manifesto-style decks where every slide is a single one-line statement, no chrome decoration, no proof block, no pill.

**Visual signature:** Background color + one centered headline + the four corner chrome ribbons. Nothing else. Each slide is a fragment.

**Canvas:** 1080 × 1440 (default).

**Color tokens:** any brand can drive it. Shipped default = `#0B0C0C` bg + magenta accent + white text.

**Typography:**
- Display: **Public Sans 600** at 110-148px. Single headline, max 3 lines, line-height 1.0.
- Accent word: magenta gradient (same as Layout 4).
- Optional small kicker: **JetBrains Mono 500** tracked +0.22em, 16-18px above headline.

**Two-tone headline rule:** one accent word per slide, gradient text — same as Layout 4 (Terminal / monospace).

**Persistent chrome:** standard 4-corner (logo TL, counter TR, handle BL, swipe cue BR). Bottom-edge magenta gradient strip optional.

**Body components:** none. The whole point. Each slide is a complete thought on its own.

**When to use:**
- Manifesto carousel (the 10 commandments of X)
- Fragment-style decks where each slide is a quote / thesis / declaration
- Cover or final slides that need to be loud and bare
- Storyboard sequences where the rhythm is "punch · punch · punch · receipt"

**Don't use when:** the slide needs proof, framework, code, or a stat block. That's Layout 4.
