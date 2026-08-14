# Component library — copy-paste-ready HTML/CSS

All components assume Public Sans + JetBrains Mono + Bebas Neue loaded via Google Fonts CDN. Sizes calibrated for 1080×1350 canvas. Adapt rem-style if scaling.

---

## Persistent chrome (every slide, every layout)

```html
<!-- Top-left: logo -->
<div class="chrome chrome-tl">
  <svg width="80" height="60" viewBox="0 0 64 48" fill="white">
    <!-- logo path here, or use {{LOGO_SVG}} -->
  </svg>
</div>

<!-- Top-right: section + counter -->
<div class="chrome chrome-tr">
  <span class="kicker-mono">{{SECTION}} · {{N}} / {{TOTAL}}</span>
</div>

<!-- Bottom-left: handle -->
<div class="chrome chrome-bl">
  <span class="dot"></span>
  <span class="kicker-mono">@{{HANDLE}}</span>
</div>

<!-- Bottom-right: swipe cue (interior slides) or save cue (final) -->
<div class="chrome chrome-br">
  <span class="kicker-mono">{{SWIPE_CUE}}</span>
</div>
```

```css
.chrome { position: absolute; }
.chrome-tl { top: 40px; left: 80px; }
.chrome-tr { top: 56px; right: 80px; }
.chrome-bl { bottom: 56px; left: 80px; display: flex; align-items: center; gap: 10px; }
.chrome-br { bottom: 56px; right: 80px; }

.kicker-mono {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  font-size: 14px;
  letter-spacing: 0.20em;
  text-transform: uppercase;
  color: var(--accent);
}

.dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--accent);
}

.chrome-bl .kicker-mono { color: rgba(255,255,255,0.85); letter-spacing: 0.20em; }
.chrome-br .kicker-mono { color: var(--accent); }
```

**Escalating swipe cue sequence (interior slides):**
- Slide 2: `KEEP GOING →`
- Slide 3: `NEXT →`
- Slide 4: `ALMOST →`
- Slide 5: `ONE MORE →`
- Slide 6: `LAST ONE →`
- Slide N (final): `SAVE THIS ↓` (replace arrow with bookmark glyph)

---

## Pill payoff (one per interior slide)

```html
<div class="pill">{{TWEETABLE_TAKEAWAY}}</div>
```

```css
.pill {
  display: inline-block;
  padding: 14px 26px;
  border-radius: 12px;
  background: rgba(215, 119, 244, 0.10);
  border: 1px solid rgba(215, 119, 244, 0.30);
  color: var(--magenta);
  font-family: 'Public Sans', sans-serif;
  font-weight: 500;
  font-size: 26px;
  letter-spacing: -0.01em;
}
```

**Pill formulas:**
- Two-beat punchy: "Same output. Fraction of the time."
- Comparator: "Agencies: 6 weeks. This stack: one weekend."
- Reframe: "Co-builder, not a chatbot."
- Specific outcome: "$11k saved per client onboarding."

---

## Terminal block (Layouts 1, 4)

```html
<div class="terminal">
  <div class="t-line t-cmd">$ {{COMMAND}}</div>
  <div class="t-line t-progress">{{PROGRESS_OUTPUT}}</div>
  <div class="t-line t-success">✓ {{SUCCESS_MESSAGE}}</div>
</div>
```

```css
.terminal {
  background: #0F0F1A;
  border: 1px solid rgba(44, 38, 85, 0.30);
  border-radius: 12px;
  padding: 28px 32px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px;
  line-height: 1.6;
}
.t-cmd { color: white; }
.t-progress { color: #7A7C7C; }
.t-success { color: #00D67D; }
```

---

## Two-tone headline

```html
<!-- Terminal-mono / Sago style: italic accent word -->
<h1 class="headline">
  Stop using ChatGPT in Adobe.
  <em class="accent">Use Claude.</em>
</h1>

<!-- Rahul style: ALL-CAPS color swap, NOT italic -->
<h1 class="headline-rahul">
  WEB DESIGNERS CHARGE $5K.
  <span class="red">YOU'RE WORTH MORE.</span>
</h1>

<!-- Marketing Harry: gradient accent word -->
<h1 class="headline-harry">
  The ART of <span class="gradient">Viral</span> Carousels
</h1>
```

```css
/* Terminal-mono italic + glow */
.headline { font-family: 'Public Sans', sans-serif; font-weight: 600; font-size: 130px; line-height: 1.05; letter-spacing: -0.04em; color: white; }
.headline em.accent {
  font-style: italic;
  color: #D777F4;
  font-weight: 600;
  text-shadow: 0 0 32px rgba(215, 119, 244, 0.35);
}

/* Rahul ALL-CAPS */
.headline-rahul { font-family: 'Bebas Neue', sans-serif; font-weight: 400; font-size: 148px; line-height: 0.95; letter-spacing: -0.02em; color: white; text-transform: uppercase; }
.headline-rahul .red { color: #E40A14; }

/* Harry gradient */
.headline-harry { font-family: 'Anton', sans-serif; font-weight: 400; font-size: 130px; line-height: 0.95; letter-spacing: -0.02em; color: white; text-transform: uppercase; }
.headline-harry .gradient {
  background: linear-gradient(90deg, #FF1B6B 0%, #FF8A00 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

---

## Step block (Layouts 1, 4)

```html
<div class="step-block">
  <div class="step-num">{{N}}</div>
  <div class="step-content">
    <div class="step-kicker">STEP {{N}}</div>
    <h2 class="step-headline">{{IMPERATIVE_VERB}}</h2>
    <p class="step-desc">{{ONE_LINE_DESCRIPTION}}</p>
  </div>
</div>
```

```css
.step-block { display: flex; gap: 40px; align-items: flex-start; }
.step-num {
  font-family: 'Public Sans', sans-serif;
  font-weight: 700;
  font-size: 96px;
  line-height: 0.95;
  color: var(--accent);
  letter-spacing: -0.04em;
}
.step-kicker {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  letter-spacing: 0.20em;
  color: var(--accent);
  text-transform: uppercase;
  margin-bottom: 12px;
}
.step-headline { font-size: 64px; font-weight: 600; line-height: 1.0; letter-spacing: -0.04em; color: white; margin-bottom: 16px; }
.step-desc { font-size: 28px; color: #7A7C7C; line-height: 1.4; }
```

---

## Anatomy stamp card (Layout 2 — Marketing Harry)

```html
<div class="stamp-card">
  <div class="stamp-label">{{LABEL_UPPERCASE}}</div>
  <div class="stamp-figure">{{NUMBER_OR_LETTER}}</div>
  <p class="stamp-body">{{BODY_TEXT}}</p>
</div>
```

```css
.stamp-card {
  background: white;
  border: 1px solid #E5E5E5;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.stamp-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #5C5C5C;
  margin-bottom: 24px;
}
.stamp-figure {
  font-family: 'Anton', sans-serif;
  font-size: 180px;
  line-height: 1;
  color: #0B0C0C;
}
.stamp-body { font-family: 'Inter', sans-serif; font-size: 22px; line-height: 1.5; color: #0B0C0C; margin-top: 20px; }
```

---

## Mock IG post block (Layout 2 — proof element)

```html
<div class="mock-ig">
  <div class="mig-header">
    <div class="mig-avatar"></div>
    <div class="mig-meta">
      <div class="mig-handle">@{{HANDLE}}</div>
      <div class="mig-time">{{TIME_STAMP}}</div>
    </div>
  </div>
  <div class="mig-image"></div>
  <div class="mig-actions">♡ {{LIKES}} · 💬 {{COMMENTS}} · ↗</div>
  <div class="mig-caption"><b>@{{HANDLE}}</b> {{CAPTION_PREVIEW}}</div>
</div>
```

```css
.mock-ig {
  width: 360px;
  background: white;
  border: 1px solid #E5E5E5;
  border-radius: 12px;
  overflow: hidden;
}
.mig-header { display: flex; padding: 12px; gap: 10px; align-items: center; }
.mig-avatar { width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #FF1B6B, #FF8A00); }
.mig-handle { font-weight: 600; font-size: 14px; }
.mig-time { font-size: 11px; color: #999; }
.mig-image { width: 100%; aspect-ratio: 1/1; background: linear-gradient(135deg, #1A1A1A, #5C1C8A); }
.mig-actions { padding: 10px 12px; font-size: 13px; }
.mig-caption { padding: 0 12px 12px; font-size: 13px; line-height: 1.4; }
```

---

## Doodle pack (Layout 3 — Sago)

Hand-drawn SVGs at `assets/doodles/`. Stroke 3-4px, slightly imperfect.

```html
<svg class="doodle doodle-arrow" width="80" height="40" viewBox="0 0 80 40">
  <path d="M5 20 Q40 5, 70 20 M55 10 L70 20 L55 30" stroke="#1A1A1A" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

<svg class="doodle doodle-asterisk" width="40" height="40" viewBox="0 0 40 40">
  <line x1="20" y1="5" x2="20" y2="35" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round"/>
  <line x1="5" y1="20" x2="35" y2="20" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round"/>
  <line x1="9" y1="9" x2="31" y2="31" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round"/>
  <line x1="31" y1="9" x2="9" y2="31" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round"/>
</svg>

<svg class="doodle doodle-underline" width="200" height="20" viewBox="0 0 200 20">
  <path d="M5 12 Q60 18, 195 8" stroke="#E63946" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>
```

---

## Comparison cards (Layout 4 — Terminal-mono)

```html
<div class="compare-row">
  <div class="compare-card compare-bad">
    <div class="compare-icon">✗</div>
    <h3 class="compare-title">{{BAD_OPTION}}</h3>
    <p class="compare-body">{{WHY_IT_FAILS}}</p>
  </div>
  <div class="compare-card compare-good">
    <div class="compare-icon">✓</div>
    <h3 class="compare-title">{{GOOD_OPTION}}</h3>
    <p class="compare-body">{{WHY_IT_WINS}}</p>
  </div>
</div>
```

```css
.compare-row { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.compare-card { padding: 40px; border-radius: 24px; }
.compare-bad { background: rgba(255, 70, 84, 0.05); border: 1px solid rgba(255, 70, 84, 0.30); }
.compare-good { background: rgba(215, 119, 244, 0.08); border: 1px solid rgba(215, 119, 244, 0.40); }
.compare-icon { font-size: 48px; margin-bottom: 20px; }
.compare-bad .compare-icon { color: #FF4654; }
.compare-good .compare-icon { color: #D777F4; }
.compare-title { font-size: 32px; font-weight: 600; color: white; margin-bottom: 12px; }
.compare-body { font-size: 22px; color: #7A7C7C; line-height: 1.5; }
```

---

## Photo overlay (Layout 5 — Photo-narrative)

```html
<div class="photo-slide">
  <img class="photo-bg" src="{{PHOTO_PATH}}" alt="">
  <div class="photo-gradient"></div>
  <div class="photo-headline">
    {{HEADLINE_LINE_1}} <em class="accent">{{ACCENT_WORD}}</em> {{HEADLINE_LINE_2}}
  </div>
  <div class="photo-caption">{{CAPTION_UPPERCASE}}</div>
</div>
```

```css
.photo-slide { position: relative; width: 1080px; height: 1350px; overflow: hidden; }
.photo-bg { width: 100%; height: 100%; object-fit: cover; }
.photo-gradient {
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.3) 40%, transparent 60%);
}
.photo-headline {
  position: absolute;
  bottom: 240px; left: 80px; right: 80px;
  font-family: 'Public Sans', sans-serif;
  font-weight: 500;
  font-size: 96px;
  line-height: 1.05;
  letter-spacing: -0.04em;
  color: white;
  text-shadow: 0 4px 24px rgba(0,0,0,0.6);
}
.photo-headline em.accent {
  font-style: italic;
  color: #D777F4;
  text-shadow: 0 0 32px rgba(215, 119, 244, 0.5);
}
.photo-caption {
  position: absolute;
  top: 56px; right: 80px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  letter-spacing: 0.20em;
  text-transform: uppercase;
  color: white;
  text-shadow: 0 2px 8px rgba(0,0,0,0.6);
}
```

**Soul V2 prompt for hero photos:**
```
{subject description}, intentional negative space on left side, subject positioned right-third of frame, dark moody lighting, cinematic, shot on Hasselblad, 4:5 vertical
```

---

## Pull-quote (Layout 4 — centered big quote)

```html
<div class="pullquote">
  Markdown is just where I say
  <span class="accent">'hey Claude please use X agent'</span>
  and then pray.
</div>
<div class="pullquote-attribution">Hacker News · OpenCode thread</div>
```

```css
.pullquote {
  border-left: 6px solid #5C1C8A;   /* deep purple */
  padding: 8px 0 8px 56px;
  font-family: 'Public Sans', sans-serif;
  font-weight: 500;
  font-size: 64px;
  line-height: 1.18;
  letter-spacing: -0.025em;
  color: white;
  max-width: 900px;
}
.pullquote .accent {
  background: linear-gradient(135deg, #D777F4 0%, #D142FC 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}
.pullquote-attribution {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  letter-spacing: 0.20em;
  text-transform: uppercase;
  color: #7A7C7C;
  margin-top: 36px;
  padding-left: 56px;
}
```

**Use for:** HN complaints, customer quotes, manifesto lines. One per deck — overused, it loses punch.

---

## Code compare (Layout 4 — bad/good two-column code blocks)

```html
<div class="code-compare">
  <div class="code-block bad">
    <div class="code-header"><span class="code-dot"></span>CLAUDE.md</div>
    <div class="code-body">
      <div class="code-strike"># Routing</div>
      <div class="code-strike">Always use leads-agent</div>
      <div class="code-strike">for /leads/* files.</div>
    </div>
  </div>
  <div class="code-block good">
    <div class="code-header"><span class="code-dot"></span>agents-routing.yaml</div>
    <div class="code-body">
      <span class="yaml-comment"># enforced at session start</span>
      <span class="yaml-key">routes:</span>
      &nbsp;&nbsp;<span class="yaml-key">"leads/*":</span> <span class="yaml-val">leads-agent</span>
    </div>
  </div>
</div>
```

```css
.code-compare { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.code-block { border-radius: 16px; overflow: hidden; font-family: 'JetBrains Mono', monospace; }
.code-block.bad { background: #1A1A1A; border: 1px solid rgba(255,255,255,0.10); }
.code-block.good {
  background: linear-gradient(135deg, #15101F 0%, #1F0E2E 100%);
  border: 1px solid #D777F4;
  box-shadow: 0 0 32px rgba(215, 119, 244, 0.20);
}
.code-header {
  padding: 12px 18px;
  font-size: 13px;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  display: flex; align-items: center; gap: 10px;
}
.code-block.bad .code-header { color: rgba(255,255,255,0.55); }
.code-block.good .code-header { color: #D777F4; }
.code-dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; opacity: 0.6; }
.code-body { padding: 24px 22px; font-size: 16px; line-height: 1.7; }
.code-block.bad .code-body { color: rgba(255,255,255,0.50); }
.code-block.good .code-body { color: white; }

/* YAML syntax tinting inside .good */
.yaml-key { color: #D777F4; }
.yaml-val { color: #A894F7; }
.yaml-comment { color: rgba(255,255,255,0.35); font-style: italic; }
.code-strike { text-decoration: line-through; opacity: 0.55; }
```

**Use for:** before/after configs, wrong-vs-right code, markdown-vs-YAML, prompt-vs-spec.

---

## Stat grid (Layout 4 — 3 hero stat cards horizontal)

```html
<div class="stat-grid">
  <div class="stat-card">
    <div class="stat-label">REPEAT TASK TIME</div>
    <div class="stat-delta"><s>22 min</s> → 9 min</div>
    <div class="stat-hero">−59%</div>
    <div class="stat-arrow down">↓ time per task</div>
  </div>
  <!-- ...2 more cards... -->
</div>
```

```css
.stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.stat-card {
  border-radius: 24px;
  padding: 32px 24px;
  border: 1px solid rgba(215, 119, 244, 0.30);
  background: linear-gradient(135deg, rgba(215,119,244,0.06) 0%, rgba(92,28,138,0.12) 100%);
  display: flex; flex-direction: column; gap: 10px;
  min-height: 280px;
}
.stat-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px; letter-spacing: 0.18em;
  text-transform: uppercase; color: #D777F4;
}
.stat-delta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px; color: rgba(255,255,255,0.45);
}
.stat-delta s { text-decoration: line-through; }
.stat-hero {
  font-family: 'Public Sans', sans-serif;
  font-weight: 700; font-size: 96px;
  line-height: 0.95; letter-spacing: -0.05em;
  background: linear-gradient(135deg, #D777F4 0%, #D142FC 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-top: auto;
}
.stat-arrow { font-family: 'JetBrains Mono', monospace; font-size: 28px; color: #D777F4; }
.stat-arrow.down { color: #00D67D; }   /* green for "improvement = down" */
```

**Use for:** dashboard-style "what changed" / projected gains / outcome metrics. Mark "projected" if not measured.

---

## Icon row (Layout 4 — 3 brand glyphs side-by-side with arrows)

```html
<div class="icon-row">
  <div class="icon-cell">
    <div class="icon-glyph real-svg terminal">{{terminal_svg}}</div>
    <div class="icon-label">LAPTOP / LOCAL</div>
  </div>
  <div class="icon-arrow">→</div>
  <div class="icon-cell">
    <div class="icon-glyph real-svg docker">{{docker_svg}}</div>
    <div class="icon-label">DOCKER</div>
  </div>
  <div class="icon-arrow">→</div>
  <div class="icon-cell">
    <div class="icon-glyph real-svg modal">{{modal_svg}}</div>
    <div class="icon-label">MODAL</div>
  </div>
</div>
```

```css
.icon-row {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  gap: 24px; align-items: center;
}
.icon-cell { display: flex; flex-direction: column; align-items: center; gap: 16px; }
.icon-glyph {
  width: 140px; height: 140px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(215,119,244,0.10) 0%, rgba(92,28,138,0.20) 100%);
  border: 1px solid rgba(215, 119, 244, 0.35);
  display: flex; align-items: center; justify-content: center;
}
.icon-glyph.real-svg { background: white; padding: 22px; }
.icon-glyph.real-svg svg { width: 100%; height: 100%; fill: #0B0C0C; }
.icon-glyph.real-svg.docker svg { fill: #2496ED; }
.icon-glyph.real-svg.modal svg { fill: #06FF92; }
.icon-glyph.real-svg.terminal svg { fill: #D777F4; }
.icon-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px; letter-spacing: 0.18em;
  text-transform: uppercase; color: #7A7C7C;
  text-align: center;
}
.icon-arrow { font-family: 'JetBrains Mono', monospace; font-size: 32px; color: #D777F4; opacity: 0.6; }
```

**Use for:** "X → Y → Z" architecture flows, tech stack reveal, before/middle/after journey. Pair with `logo_icon:` in YAML for auto-SVG resolution.

---

## Harness cards (Layout 4 — 3-tool comparison grid)

```html
<div class="harness-grid">
  <div class="harness-card tier-good">
    <div class="harness-logo-row">
      <div class="harness-logo-mark real-svg">{{hermes_svg}}</div>
      <div class="harness-name">Hermes</div>
    </div>
    <div class="harness-positioning">Self-improving. Auto-writes a skill file after every non-trivial task. Compounds.</div>
    <div class="harness-stat">95.6K STARS · 6 BACKENDS</div>
  </div>
  <!-- ...2 more cards with tier-flag, tier-default... -->
</div>
```

```css
.harness-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.harness-card {
  border-radius: 20px;
  padding: 28px 22px;
  border: 1px solid rgba(215, 119, 244, 0.30);
  display: flex; flex-direction: column; gap: 14px;
  min-height: 280px;
}
.harness-card.tier-good {
  background: linear-gradient(135deg, rgba(215,119,244,0.12) 0%, rgba(92,28,138,0.20) 100%);
  border-color: #D777F4;
}
.harness-card.tier-flag {
  background: rgba(255, 184, 60, 0.06);
  border-color: rgba(255, 184, 60, 0.40);
}
.harness-logo-row { display: flex; align-items: center; gap: 12px; }
.harness-logo-mark {
  width: 64px; height: 64px; border-radius: 14px;
  background: linear-gradient(135deg, #D777F4 0%, #5C1C8A 100%);
  display: flex; align-items: center; justify-content: center;
  color: white; font-weight: 700; font-family: 'JetBrains Mono', monospace; font-size: 26px;
}
.harness-logo-mark.real-svg { background: white; padding: 10px; }
.harness-logo-mark.real-svg svg { width: 100%; height: 100%; fill: #0B0C0C; }
.harness-logo-mark.real-svg.multicolor { background: #FFF1EE; padding: 4px; }
.harness-logo-mark.real-svg.multicolor svg { fill: unset; }
.harness-name { font-family: 'Public Sans', sans-serif; font-weight: 700; font-size: 30px; color: white; }
.harness-positioning {
  font-family: 'Public Sans', sans-serif;
  font-weight: 500; font-size: 18px;
  line-height: 1.4; color: rgba(255,255,255,0.70);
  flex: 1;
}
.harness-stat {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px; letter-spacing: 0.12em;
  text-transform: uppercase; color: #D777F4;
  padding-top: 10px; border-top: 1px solid rgba(215, 119, 244, 0.25);
}
```

**Use for:** comparing 3 tools / pricing tiers / approach options. Tier highlights one as winner (`good`), one as cautionary (`flag`), one neutral (`default`).

---

## Term-side (Layout 4 — terminal left + framework right)

```html
<div class="term-side-row">
  <div class="terminal">
    <div class="t-cmd">$ ls ~/.claude/</div>
    <div class="t-progress">agents-routing.yaml</div>
    <div class="t-progress">hooks/stop-skill.sh</div>
    <div class="t-success">✓ harness · ready</div>
  </div>
  <div class="framework-list">
    <div class="fw-row">
      <div class="fw-num-card">01</div>
      <div class="fw-content">
        <div class="fw-title">agents-routing.yaml</div>
        <div class="fw-body">Hook reads at session start. Sub-agents fire deterministically.</div>
      </div>
    </div>
    <!-- ...more rows... -->
  </div>
</div>
```

```css
.term-side-row {
  display: grid;
  grid-template-columns: 1fr 0.85fr;
  gap: 36px; align-items: center;
}
.term-side-row .terminal { font-size: 18px; padding: 24px 28px; }
.term-side-row .framework-list { gap: 24px; }
.term-side-row .fw-num-card { width: 60px; height: 60px; font-size: 24px; border-radius: 12px; }
.term-side-row .fw-title { font-size: 26px; }
.term-side-row .fw-body { font-size: 16px; }
```

**Use for:** showing a real command + the files / steps it touches. Terminal carries the proof; framework explains.

---

## Mockup card (Layout 4 — white profile receipt)

```html
<div class="mockup-row">
  <div class="mockup-card">
    <div class="mc-header">
      <div class="mc-avatar">A</div>
      <div>
        <div class="mc-handle">your_handle</div>
        <div class="mc-meta">7.3K followers · AI implementation</div>
      </div>
    </div>
    <div class="mc-stats">
      <div><div class="mc-stat-num">3</div><div class="mc-stat-label">Posts</div></div>
      <div><div class="mc-stat-num">7.3K</div><div class="mc-stat-label">Followers</div></div>
      <div><div class="mc-stat-num">412</div><div class="mc-stat-label">Following</div></div>
    </div>
    <div class="mc-bio">I help founders ship AI products. Studio name · City.</div>
  </div>
  <div class="mockup-annotation">
    <span>Built in <span class="accent">14 days.</span> Live on yoursite.com.</span>
  </div>
</div>
```

```css
.mockup-row { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: center; }
.mockup-card {
  background: white;
  border-radius: 24px;
  padding: 24px 28px;
  color: #0B0C0C;
  box-shadow: 0 12px 48px rgba(0,0,0,0.5);
  font-family: 'Public Sans', sans-serif;
}
.mc-header { display: flex; align-items: center; gap: 14px; padding-bottom: 16px; border-bottom: 1px solid #E5E5E5; margin-bottom: 16px; }
.mc-avatar {
  width: 56px; height: 56px; border-radius: 50%;
  background: linear-gradient(135deg, #D777F4, #5C1C8A);
  display: flex; align-items: center; justify-content: center;
  color: white; font-weight: 700; font-size: 22px;
}
.mc-handle { font-weight: 700; font-size: 20px; }
.mc-meta { font-size: 13px; color: #999; }
.mc-stats { display: flex; gap: 24px; font-family: 'JetBrains Mono', monospace; font-size: 18px; padding: 12px 0; }
.mc-stat-num { font-weight: 700; }
.mc-stat-label { font-size: 12px; color: #5C5C5C; text-transform: uppercase; letter-spacing: 0.05em; }
.mc-bio { font-size: 16px; line-height: 1.4; }
.mockup-annotation {
  display: flex; flex-direction: column; gap: 12px;
  font-family: 'Public Sans', sans-serif;
  font-weight: 500; font-size: 28px; line-height: 1.3;
  color: rgba(255,255,255,0.85);
}
.mockup-annotation .accent {
  background: linear-gradient(135deg, #D777F4 0%, #D142FC 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}
```

**Use for:** track-record proof / receipt slide. Pair with a specific outcome in the annotation.

---

## Ghost numeral (slide-level decoration)

```html
<svg class="ghost-numeral-svg" viewBox="0 0 1080 1440" preserveAspectRatio="none">
  <text x="1100" y="1450" text-anchor="end"
        font-family="Public Sans" font-weight="700" font-size="900"
        fill="none" stroke="rgba(215,119,244,0.35)" stroke-width="3"
        letter-spacing="-50">5</text>
</svg>
```

```css
.ghost-numeral-svg {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  z-index: 2; pointer-events: none;
}
body.theme-light .ghost-numeral-svg text { stroke: rgba(92, 28, 138, 0.35); }
```

**Use for:** "3 things" / "5 patterns" slides where the number IS the slide-level identifier. Always outlined (no fill) so it reads as graphic element, not content. Bottom-right anchor.

---

## Diagonal stripe (slide-level decoration)

```html
<div class="diagonal-stripe"></div>
```

```css
.diagonal-stripe {
  position: absolute; z-index: 1;
  top: 50%; left: -10%;
  width: 130%; height: 80px;
  background: linear-gradient(90deg, transparent 0%, #D777F4 30%, #5C1C8A 70%, transparent 100%);
  opacity: 0.20;
  transform: rotate(-8deg);
  pointer-events: none;
}
```

**Use for:** visual rhythm-break on text-heavy slides. Pairs with `pullquote` or single-line headline slides where the canvas otherwise feels flat.
