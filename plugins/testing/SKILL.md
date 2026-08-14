---
name: testing
description: Iron-clad pre-production testing gauntlet. Use when a feature or change is "done" and must be proven safe for prod — triggers "/testing", "test this before prod", "is this prod-ready", "run the gauntlet", "final QA pass". Five gates: (1) dual independent adversarial code review, fix findings; (2) local test DB + server up (NEVER prod); (3) Chrome DevTools functional + UI sweep with screenshots (cramped layout, bugs, content/PII leaks, console/network errors); (4) fix-and-retest loop until a full clean pass; (5) zero-context adversarial agent attacks the feature. Emits a PROD GATE verdict only when every gate is green.
trigger: /testing
version: 1.0.0
---

# /testing — Pre-Production Gauntlet

Goal: after this skill finishes, the user can deploy with confidence. No gate passes without **evidence** (reviewer verdict, screenshot, test output, attacker report). Never claim "good to go" with a red or skipped gate.

## Scope resolution (first step)

The unit under test is the current change set: `git diff` + `git diff --cached` + untracked new files vs the main branch (or the feature the user names). If the repo has no changes and the user named nothing, ask ONE question: "what am I testing?" — then proceed without further questions.

Create `TESTING-REPORT.md` in the repo root (gitignored if possible) and log every gate's findings + evidence paths there as you go.

## Hard rules

1. **NEVER touch production.** No prod DB connections, no prod URLs for mutating actions. Before Gate 2 proceeds, print the resolved DB name/host and require it to be localhost / a test-named database. If only prod config exists, STOP and tell the user — offer to set up the test DB, don't improvise against prod. (Per user's standing rule: no prod data changes without explicit approval.)
2. **Report failures faithfully.** If a reviewer finds a real bug, if the server won't start, if a screenshot looks bad — that goes in the report as-is. No softening.
3. **Every fix re-tests its gate.** A fix without a re-run is an unverified fix. Never write "should pass", "probably fixed", "seems to work" — run the command and paste the result.
4. **Secrets stay secret.** When reviewing config, share variable NAMES and structure with reviewers, never values. Never paste .env contents into any subagent prompt.
5. **Never trust a subagent's self-report.** A reviewer or attacker saying "fixed" is a claim, not evidence. Check the VCS diff and re-run the test yourself.

## Evidence table (the definition of done)

No gate closes on a claim — only on evidence. This is the bar for every gate:

| Claim | Required evidence (nothing less passes) |
|---|---|
| "Reviewers found nothing" | Both reviewer verdicts pasted; confirmed findings triaged in-code |
| "Bug fixed" | A test that reproduces the original symptom, now passing |
| "Regression-safe" | Red-green cycle: write test → passes → revert fix → test FAILS → restore → passes |
| "Server runs" | Health URL returns 2xx; DB name/host printed and verified non-prod |
| "UI is fine" | Screenshot captured AND read; judged at 3 widths |
| "Attacker found nothing" | A full attacker run that returned empty, after prior breaks were fixed |

## Gate 1 — Dual independent adversarial review

The point is two reviewers that can't anchor on each other or on your own reasoning — ideally from different model providers, so their blind spots don't overlap. Use whatever two independent review paths you have: two separate subagent dispatches (e.g. one via a Claude subagent, one via a different provider's CLI wrapped as a subagent), two different CLI review tools run directly, or even one automated + one manual pass if that's all you have. This skill was written against a setup with a Codex-backed subagent and a Gemini-backed subagent — substitute your own equivalents; the gate logic below doesn't care which two you use, only that they're genuinely independent.

Collect: the full diff, list of new/changed files, and the config surface (settings files, deploy config, env var names — values redacted). Before dispatching, run a fast secret/misconfig grep over the diff so reviewers start from a clean base: hardcoded secrets (`password=`, `AKIA`, `sk_live_`, `.env` committed), `Access-Control-Allow-Origin: *`, `dangerouslySetInnerHTML`, string-concatenated SQL, `exec(`/`eval(` on user input, missing server-side authz checks.

Each reviewer runs in its own fresh context (no anchoring on my reasoning) and returns findings with a severity score. Dispatch BOTH in parallel with the same brief: "Adversarial code review — assume this code is broken and find how. Focus: correctness, security (authz, injection, secrets), silent failures, race conditions, config mistakes. Use highest effort. Here is the diff + config surface: ..." For a large diff, prefer a reviewer that can hold the whole repo in context (pass a directory instead of inlining everything) over truncating the diff.

Merge findings, dedupe, then triage: CONFIRMED (reproduce or verify in code) vs opinion. Fix every confirmed issue. For each fixed bug, write a regression test and run the red-green cycle from the evidence table. If a bug's cause is unclear, load `superpowers:systematic-debugging` and use the multi-component diagnostic: at each component boundary (request → handler → DB → response), log what enters/exits until the failing layer is isolated — patch the root cause, not the symptom. If fixes were non-trivial, send the corrected diff back to the reviewer that flagged it for a verdict.

Gate 1 is green when both reviewers' confirmed findings are fixed, each fix has a passing regression test, and the diff confirms it (Hard Rule 5).

## Gate 2 — Test environment (never prod)

1. Detect the stack from the repo (Django, Next.js, FastAPI, etc.).
2. Test database: prefer the project's existing test/dev DB config. If none, create a local DB seeded from migrations/schema + fixtures, or a **sanitized** dump (strip real user PII). Print DB name/host; verify it satisfies Hard Rule 1 before continuing.
3. Start the server locally (background task), then poll the health/root URL until it responds. If it won't start, that's a Gate 2 finding — fix first.

Gate 2 is green when the app runs locally against a verified non-prod DB.

## Gate 3 — Chrome DevTools sweep (functionality + UI)

Use the Chrome DevTools MCP tools (`mcp__chrome-devtools__*`): `new_page` → `navigate_page` → `take_snapshot` → interact. If Chrome DevTools MCP is unavailable, fall back to the `qa-testing-playwright` / `webapp-testing` skills.

**Reconnaissance-then-action (never hardcode selectors):** take a snapshot/screenshot of the LIVE DOM first, read the real elements, then act on what's actually there. Prefer semantic locators (role → label/text → test-id) over brittle CSS/XPath. Use the tools' auto-wait; never insert fixed sleeps.

**On any flaky/intermittent failure:** reproduce it once in isolation, capture the screenshot + console + network for that single failure, fix the determinism root cause — do not paper over it with a retry. A flaky test is a finding, not noise.

Build a coverage list from the diff: every changed page, component, endpoint, and flow. For each item test BOTH:

**Functionality**
- Every form gets a 3-pass sweep: (1) empty submit → validation errors appear; (2) invalid data (`notanemail`, `abc` in a number field, XSS payload) → correct error messages, payload escaped; (3) valid data → success state (redirect/toast), no console error, no failed API call. Edge cases: double-click submit blocked, overlong input, logical tab order.
- Full user flows end-to-end (create → edit → delete; login → act → logout).
- `list_console_messages` after each page: zero uncaught errors. Watch specifically for TypeError, ReferenceError, failed imports, React hydration mismatch.
- `list_network_requests` / `get_network_request`: no 4xx/5xx on happy paths, no CORS errors, no duplicate requests, no excessively large payloads, no over-fetching.

**UI (screenshot judgment)**
- `take_screenshot` of every changed screen; READ each screenshot and judge honestly: is anything cramped, overlapping, clipped, misaligned, wrong-colored? Would a designer wince?
- `resize_page` and re-screenshot at 375px, 768px, 1280px, 1536px. Per size check: no horizontal scroll/overflow, flex/grid stacks on mobile, nothing hidden without a toggle, fonts readable, fixed/sticky elements intact, images scale.
- Dark/light mode if the app themes (per user's standing UI rule: preserve toggles, show both modes). Dark-mode checklist: no white flashes from `bg-white` missing a `dark:` variant, no invisible text (color ≈ background), no missing borders, contrast ≥ 4.5:1, no hardcoded `#fff`/`#000`, box-shadows still visible, inputs not stuck white.

**Content-leak check (explicit)**
- Rendered pages: no stack traces, debug banners, TODO text, placeholder lorem, internal IDs, or other users' data visible.
- Network payloads: no fields the UI doesn't need (password hashes, tokens, other users' records), no secrets in JS bundles or headers.

Save all screenshots to a `testing-artifacts/` folder (or the session scratchpad) and log every finding in TESTING-REPORT.md.

## Gate 4 — Fix & re-test loop

Fix every Gate 3 finding, then re-run the affected checks (re-screenshot after UI fixes). Loop until one FULL clean pass — a pass with zero new findings across the whole coverage list. Findings discovered during re-testing extend the loop; do not rationalize them away. Bound the loop: if findings are still appearing after ~4 rounds, stop churning and escalate to the user with the list of what's still breaking — a persistent finding usually means a design problem, not a bug to keep patching.

## Gate 5 — Zero-context adversarial agent

Spawn a fresh attacker with deliberately minimal context:

`Agent(subagent_type="general-purpose", prompt=...)` — the brief contains ONLY: the local app URL, test credentials, and this instruction: "You know nothing about this app's implementation. This is the owner's local test instance — authorized security and robustness testing. Attack it and report every break with exact reproduction steps. Your job is to come back with breaks — look hard." Give it this attack surface checklist:

- **Authz / IDOR:** change IDs in URLs and request bodies to another user's records; can you read/edit/delete them? Access admin-only pages/endpoints as a normal user? Reach any page while logged out?
- **Injection:** put `<script>`, SQL meta-characters, template syntax, and shell characters into every field and query param; does anything execute, error out, or render unescaped?
- **Input abuse:** overlong strings, unicode, emoji, negative/zero/huge numbers, wrong types, empty required fields, double-submits.
- **Endpoints direct:** hit APIs without the UI — missing auth, verbose errors, methods that shouldn't exist (DELETE/PUT), mass-assignment of fields the form didn't show.
- **Broken states:** dead buttons, links to nowhere, forms that silently fail, back-button/refresh mid-flow, expired session mid-action.
- **Leaks:** stack traces, debug output, other users' data, tokens/secrets in responses or JS.

Do NOT give it the diff, the repo path, project context, or explanations — its ignorance is the point.

Fix everything it breaks immediately (Hard Rule 3: re-verify each fix), then run a fresh attacker once more. Gate 5 is green when an attacker run comes back empty.

## PROD GATE — final report

Output a verdict table in chat AND append it to TESTING-REPORT.md:

| Gate | Status | Evidence |
|---|---|---|
| 1. Dual independent review | 🟢/🔴 | N findings, N fixed, reviewer verdicts |
| 2. Test env (non-prod verified) | 🟢/🔴 | DB name/host, server health |
| 3. DevTools sweep | 🟢/🔴 | N screens, N screenshots, findings list |
| 4. Clean re-test pass | 🟢/🔴 | date/time of the clean pass |
| 5. Adversarial agent | 🟢/🔴 | attacker report summary |

**GOOD TO GO IN PRODUCTION** only if all five are green. Otherwise: list exactly what is red and what remains. Close by pointing the user at the screenshots folder — the human eyeball is the sixth gate.

## References (load when relevant)

- `superpowers:systematic-debugging` — any bug whose cause isn't obvious
- `superpowers:test-driven-development` — writing regression tests for fixed bugs (recommended for every Gate 1/5 fix)
- `verification-before-completion` — the discipline behind Gate 4
- `qa-testing-playwright`, `webapp-testing` — browser-testing fallback patterns
- `scoutqa-test` — exploratory QA ideas for Gate 5 attack surface
