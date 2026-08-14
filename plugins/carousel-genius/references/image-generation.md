# Image generation for carousel heroes

When a layout calls for an AI hero photo (Layout 5 photo-narrative, Layout 2 cover, Layout 3 cover, or any slide where you want a generated visual), use one of these pipelines. **Always view the generated image before adding to the deck — don't trust prompt-to-image fidelity blind.**

---

## Pipeline A — Higgsfield (preferred for portraits / cinematic)

Higgsfield supports 30+ models via MCP. Routing:

| Need | Skill / model | Cost |
|---|---|---|
| Subject = creator's face, cinematic | `higgsfield-soul-id` (Soul Cinematic V2) | **Free** on Ultimate |
| Subject = creator's face, simpler | `higgsfield-soul-id` (Soul V2) | **Free** on Ultimate |
| Generic image, branded | `higgsfield-product-photoshoot` (gpt_image_2 modes) | Paid |
| Generic image, raw | `higgsfield-generate` | Soul V2 free, Nano Banana Pro paid |
| Marketing video / ad | `higgsfield-generate` (Marketing Studio) | Paid |

**Default guidance:** stick to **Soul V2 / Soul Cinematic** (free) unless the user explicitly asks for paid models — confirm before spending credits.

### Soul V2 hero photo prompt (Layout 5 standard)

```
{subject description}, intentional negative space on LEFT side of frame
(headline overlay goes there), subject positioned in right-third,
dark moody cinematic lighting, shot on Hasselblad, 4:5 vertical,
photorealistic, high contrast, shallow depth of field
```

Examples:
- "The founder, in a dimly lit modern studio at dawn, intentional negative space..."
- "Designer hands typing at a black mechanical keyboard, screen glow on face, intentional negative space..."

---

## Pipeline B — Nano Banana via opencli (Gemini)

For when Higgsfield is rate-limited or you need a quick free generation.

```bash
# Generate via Gemini's Nano Banana
opencli gemini imagen \
  --prompt "subject right of frame, intentional negative space left, dark moody cinematic" \
  --aspect 4:5 \
  --out ./out/{slug}/assets/hero.jpg

# View it
opencli web read --url file://./out/{slug}/assets/hero.jpg
```

Nano Banana is free via Gemini API. Output quality < Soul V2 for portraits but solid for objects, scenes, abstract concepts.

---

## Pipeline C — Manual Nano Banana Pro (paid, top quality)

If user explicitly asks for top-tier generation:
1. Use `nano-banana-pro` skill
2. Costs credits — confirm with user first
3. Best for: hero photos that NEED to look stock-photography quality

---

## Visual verification (mandatory)

Before referencing the image in a YAML brief:

1. Save image to `out/{slug}/assets/hero.jpg`
2. View it in chat: `Read("/abs/path/to/hero.jpg")`
3. Confirm it has the negative space you asked for
4. If wrong — regenerate with adjusted prompt
5. Only then add `photo_path: "./assets/hero.jpg"` to brief

If the image doesn't have proper negative space, the headline overlay will collide with the subject and the slide reads as cluttered.

---

## Image style consistency rule

From @design.deb's "3 hard rules": **pick a consistent image style across the deck.**

- All photos → realism, OR all photos → editorial (high contrast B&W), OR all photos → surreal
- Don't mix: realism portrait on slide 1 + cartoon illustration on slide 3 = looks slapped together

Lock the style in the brief:

```yaml
image_style: "cinematic-photorealism"   # or "editorial-bw" / "surreal-vaporwave" / "brutalist"
```

Pass this to every Soul V2 / Nano Banana prompt as a suffix.

---

## When to NOT use AI images

- **Layout 4 (terminal)** — should be text + data tables + terminal blocks. Photos clutter the data story.
- **Layout 6 (bare hook)** — by definition no decoration.
- **Slide 2 (transition)** — text-dominant; image distracts from the promise.
- **Final CTA slide** — if you have a real photo of yourself, use that, not AI.

The strongest decks use AI photos sparingly — 2-3 per 10-slide deck max. Over-generation reads as "made by AI." Use real screenshots, real receipts, real product photos when possible.
