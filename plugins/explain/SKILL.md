---
name: explain
description: Use when the user says "/explain", "explain it to me", "explain this", "break it down", "break this down", "walk me through", "make me understand", "help me understand", "ELI5 but technical", "explain like a junior dev", "I don't get this", "what's actually happening here", "demystify", "make it click", or asks for a visual/diagram explanation of how code or a system works. Produces a layered explanation (plain-language pitch → ONE mental-model analogy → real technical details with file paths and function names) for a smart non-specialist — NOT a literal 5-year-old. Renders a standalone HTML artifact with diagrams when the user says "visualize", "show me", "diagram", "make it visual", or "render it". Trigger aggressively whenever the user is asking to understand a concept, not just look something up — undertriggering means falling back to either too-childish ELI5 or too-jargon-heavy walls of text, both of which the user has explicitly pushed back on.
---

# Explain

Layered explanation for a smart non-specialist. The audience is someone who knows programming but not this specific stack/concept/codebase — not a literal 5-year-old.

## Why this skill exists

Without this skill, "explain X" requests collapse into one of two failure modes:

1. **Too childish** — toy boxes, lockers, "imagine you have…". The user has pushed back on this multiple times. From their memory: *"ELI5 first then technical tables"* — the analogy is a *stepping stone*, not the destination.
2. **Too jargon-heavy** — a wall of stack-trace-level detail with no on-ramp. The user knows *some* technical things but not everything, and the response should bridge from where they are, not show off.

This skill defines the on-ramp: **pitch → analogy → technical bit → exit.**

## When to invoke

Trigger on any of these (or near-equivalents):

- `/explain`
- "explain it / this to me", "break it down", "break this down"
- "walk me through X", "make me understand X", "help me understand X"
- "I don't get X", "I'm confused about X", "what's actually happening with X"
- "demystify", "make it click"
- "explain like a junior dev", "explain like I don't know this stack"
- Visual cues: "visualize", "show me", "diagram", "make it visual", "render it", "draw it"

**Do NOT invoke** for:

- Simple lookups ("what's the syntax for X" — just answer it)
- Code reviews (use code-review skill)
- Debugging help where the user wants you to FIX, not explain (use systematic-debugging skill)

## Output modes

The skill has two output modes. Pick automatically based on cues in the request.

### Mode A — Chat (default)

The standard case. Use this 90% of the time.

Structure (always exactly these four parts, in this order):

```
### The pitch
<1–2 sentences in plain language. State what it is and what it does. No jargon yet.
This is the "if you only read one line, this is what you walk away with" answer.>

### Mental model
<ONE analogy that maps to the technical thing. Pick a real-world system the user
likely already understands (a postal sorting office, a kitchen pass, an airport
security line). Be specific — name the parts of the analogy that correspond to
real parts of the concept. Avoid generic "imagine a box" framing.>

| Analogy | Real thing |
|---|---|
| The mail clerk | The router |
| The sorting bin | The middleware stack |
| The address label | The URL |

### The technical bit
<The actual mechanics, named with real terms. File paths with line numbers. Function
names. Module names. Just enough to act on. Skip background theory unless it's the
load-bearing thing.>

- `path/to/file.py:42` — what's there, why it matters
- `function_name()` — what it does
- Sequence: A → B → C (or numbered steps if linear)

### What to do with this
<1–3 lines: the next action this understanding enables. "If you want to add a new
middleware, edit X." "If this is breaking, check Y first." Anchors the explanation
to action.>
```

**Length budget for chat mode:** roughly 150–400 words total. If you're writing more than 400, you're padding — cut the analogy or the technical detail, not both.

### Mode B — HTML visual

Use when the request contains visual cues ("visualize", "show me", "diagram", "make it visual", "render it"). Or when the concept is genuinely graph-shaped (state machine, request flow, hierarchy, timeline) and a diagram beats prose.

Write a standalone HTML file to `/tmp/explain-<topic-slug>-<date>.html`. Open it with `open <path>` after writing.

**HTML requirements:**

- Self-contained — inline CSS, no external libs except optionally Mermaid via CDN if a diagram needs it
- Dark mode by default (matches typical dev-tool conventions for the user's environment)
- Same four-section structure as chat mode, but rendered with visual layout:
  - **The pitch** — big hero text, centered, max 2 sentences
  - **Mental model** — side-by-side or table layout pairing analogy ↔ real thing, with subtle dividers
  - **The technical bit** — code blocks (monospace), file:line refs as clickable-looking anchors, optional Mermaid diagram for flows / state machines / dependency graphs
  - **What to do with this** — call-to-action card at the bottom
- Type: system-ui or Inter for body, JetBrains Mono / SF Mono for code
- Color: prefer one accent color from context (if the project has an established brand color, use it — e.g. `#c026d3`; otherwise default to a calm blue #4f46e5)
- After writing, also drop a 2-3 line chat summary so the user gets the highlight without opening the file

**When to add a Mermaid diagram** (use the Mermaid CDN: `https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js`):

- Request flow: `sequenceDiagram` or `flowchart LR`
- State machine: `stateDiagram-v2`
- Hierarchy / dependencies: `flowchart TB`
- Decision tree: `flowchart TD`
- Timeline of events: `gantt` or numbered `flowchart LR`

Don't force a diagram for a flat concept (e.g., "what does this filter function do" — that's prose).

## Persona — smart non-specialist

The audience for every explanation produced by this skill:

- **Knows:** programming fundamentals, basic CLI, what an API is, what a database is, what HTML/CSS/JS do at a high level
- **Doesn't know:** the specific framework, library, or pattern you're explaining; the codebase you're in
- **Wants:** to act on this information after reading. Not to pass an exam, not to write a thesis.

Calibration rules:

- **Use real names.** `BuyerLeadViewSet`, not "the thing that handles requests".
- **Define jargon once, inline.** First mention: `the QuerySet (Django's lazy DB query builder)`. After that, just `QuerySet`.
- **One good analogy beats five.** Pick the best mapping and commit. Don't pile on metaphors.
- **Cite paths and line numbers** when explaining real code in the user's project. Drives the "I can go look at it myself" instinct.
- **Skip "concepts you'll learn"** preambles and "I hope this clarifies!" outros. Just answer.

## Anti-patterns

Don't do these. They each correspond to a specific failure mode the user has called out:

- **Toy-box analogies** ("imagine you have a box of toys…") — too childish. The user is a working dev.
- **Three different analogies in one explanation** — pick ONE that maps cleanly. Stacking analogies confuses more than it clarifies.
- **Wall of unbroken jargon** — at least sketch the mental model before naming components.
- **Padding sections** like "Background", "History", "Conclusion" — they aren't pulling weight. Cut them.
- **"I hope this helps!" / "Hope that makes sense!"** — fluff. End on the "what to do with this" line, not pleasantries.
- **Missing the technical bit** — if the explanation is *only* the analogy, you've failed the brief. The user needs to act on real code.
- **Emojis or hype** unless the user used them first. Default tone: friendly but exact, like a senior dev pair-walking a teammate through their first day.

## Examples

### Example 1 — Chat mode

**User:** "explain what a Django middleware is"

**Output:**

```
### The pitch
A Django middleware is a piece of code that runs on every request and every response
— think of it as a customs checkpoint between the outside world and your view code.

### Mental model
Imagine an airport with a single corridor between arrivals and the city. Every
passenger (request) walks through the same line of checkpoints — passport check,
customs, baggage scan — before reaching the city (your view). On the way out
(response), they pass through a different sequence (duty-free, gate scan) before
leaving.

| Airport | Django |
|---|---|
| Passenger | HTTP request |
| Checkpoint | A middleware class |
| The city | Your view function |
| Exit corridor | The response path back through the same middlewares in reverse |

### The technical bit
- Configured at `src/settings.py` → `MIDDLEWARE` list (order matters; runs top-to-bottom on request, bottom-to-top on response)
- Each middleware is a class with `__call__(self, request)` — calls `self.get_response(request)` to pass control to the next layer
- Built-ins you already have: `SecurityMiddleware` (HTTPS headers), `AuthenticationMiddleware` (attaches `request.user`), `CsrfViewMiddleware` (token check)
- Custom example: `core/middleware/audit.py` if you wanted to log every authed request

### What to do with this
If you want to add a "block X for unauthed users" rule, write a middleware — don't
put the check in every view. If a request seems to be modified before your view sees
it, the answer is in the MIDDLEWARE list, in order.
```

### Example 2 — HTML mode triggered

**User:** "visualize the lead-pool selector logic for me"

**Output (in chat):**

```
Wrote /tmp/explain-lead-pool-selector-2026-05-23.html — opened it in your browser.

Quick highlight: the selector intersects three filters (role-scope, location-scope,
visible_sellers), and the bug last week was treating location_scope as an OVERRIDE
instead of an intersection. The diagram in the HTML shows where the 813-leads
inflation came from.
```

**The HTML file** contains the four-section layout with a Mermaid `flowchart LR` showing the three filters as composable gates feeding into the final QuerySet, plus the analogy table and file:line refs.

## Notes

- **No CLAUDE.md changes needed.** The user picked "skill, not always-on rule" — keep this on-demand. Existing memory notes like *"ELI5 first then technical tables"* still apply as defaults during normal work; this skill is the explicit deep-dive mode.
- **No CSS/JS bundling.** HTML mode writes one self-contained file. If a diagram is needed, use Mermaid via CDN (no install). Don't introduce build tooling.
- **No emoji output** even in HTML mode unless the user asked for emoji/playful tone — keep it clean.
