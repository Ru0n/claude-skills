---
name: quick
description: Use when the user says "/quick", "/quick N" (e.g. "/quick 3"), "quick version", "just the points", "tldr", "bullet it", or "cut the essay". Compresses the answer — or the previous wall of text — into the N most important points and nothing else. Default 3 points if no number is given.
trigger: /quick
---

# quick

Give the N most important points, nothing else.

- N is the number the user passed (`/quick 5` → 5 points). No number → 3.
- Rank most important first. Each point is one line, leading with the takeaway word.
- No preamble, no intro sentence, no "here are the points", no closing line. Nothing before point 1, nothing after point N.
- If the user is compressing a previous long answer, pull the load-bearing points straight from it - don't re-derive or re-research.
- Plain words, no jargon. No em dashes, no emoji, no exclamation marks.
- Numbered list only.
