# Viral font combinations

Source: @marketingharry "Ultimate Carousel Guide in 2026" (post 1, slide 7) + this skill's shipped defaults.

The rule: pick **2 fonts only** — one Headline (display) + one Body (text). Don't mix more.

---

## The 6 viral combos for 2026

| # | Headline | Body | Vibe |
|---|---|---|---|
| 1 | **Thunder** | **Euclid Square** | Tactical, aggressive, listicle energy |
| 2 | **Creato Display** | **Plus Jakarta Sans** | Modern editorial, premium, clean |
| 3 | **Bethany Elingston** | **Neulis Neue** | Elegant serif, magazine, thought-leadership |
| 4 | **Titillium Web** | **Unigeo64** | Tech, geometric, futuristic |
| 5 | **Calm Love** | **Constantia** | Soft serif, lifestyle, personal-brand |
| 6 | **Brunson Rough** | **Darker Grotesque** | Editorial, bold, confident |

## Shipped defaults (for this skill)

The skill ships with these as defaults because they're free Google Fonts:

| Role | Font | Use |
|---|---|---|
| Headline (display) | **Bebas Neue** (free) — substitute for Thunder/Brunson | All-caps, condensed, headline-dominant |
| Headline (alt) | **Anton** (free) — substitute for Thunder | Marketing Harry layout |
| Body | **Public Sans** (free) — substitute for Plus Jakarta Sans | Default body font |
| Mono | **JetBrains Mono** (free) | Code, terminal, kicker labels |
| Editorial | **Playfair Display** (free) — substitute for Bethany Elingston | Sago layout subheads |

## How to swap fonts in a brief

In the YAML brief:

```yaml
brand:
  display_font: "Bebas Neue"   # or any Google Font name
  body_font: "Public Sans"
  mono_font: "JetBrains Mono"
```

Templates load fonts via Google Fonts CDN. To use one of the paid combos (Thunder, Creato Display, etc.):

1. Buy/license the woff2 file
2. Drop it in `~/.claude/skills/carousel-genius/assets/fonts/`
3. Add `@font-face` declaration to the template's `<style>` block
4. Reference via the `display_font` field

## Why "2 fonts only" matters

Mixing 3+ fonts is the single most common signature of an AI-generated carousel. The eye reads "this was made fast and cheap" before it reads the headline. One display font + one body font = one decision = one rhythm.

If you absolutely need a third "voice," use **JetBrains Mono** for code/labels/kickers — it doesn't compete because it serves a different role (data, not narrative).

## Pairing rules

- **Display = condensed bold all-caps** + body = neutral sans → tactical / listicle / news (Layouts 1, 4)
- **Display = elegant serif** + body = grotesque sans → editorial / opinion (Layout 3)
- **Display = geometric sans** + body = humanist sans → tech / surreal (Layout 2)
- **Display = display sans** + body = same family different weight → minimal / brand-locked (Layout 5)

## Font weight rule

- Display: 600-900 only. Anything lighter dies on IG's compression.
- Body: 400-500. Heavier reads as desperate.
- Italic only on the accent word.
- Letter-spacing always negative on display (-0.02em to -0.04em). Always slightly positive on labels/kickers (+0.20em).
