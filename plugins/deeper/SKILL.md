---
name: deeper
description: Rewrite the user's ask into a deeper one before doing it, the way a top professional in that field would frame it. Use when the user types /deeper, or says "go deeper", "deeper not bigger", "sharpen this prompt", "what would an expert do here", or "rewrite my prompt". Not for quick fixes or lookups.
trigger: /deeper
argument-hint: [the ask, or nothing to use the previous message]
---

# deeper

Goal: a deeper version of the ask, not a bigger one. Same scope, sharper method.

Input = the text after /deeper, else the user's previous message. Read the project's CLAUDE.md and any memory notes first so the answer fits their real context (stack, client, budget, constraints).

## Answer these four, briefly (2-4 lines each)

1. **What a top professional would do here that the user isn't asking for.** Name the role (e.g. "a senior payments engineer", "a tax auditor"). The one or two moves that separate expert work from adequate work. Not a list of everything.
2. **The rawest material they'd start from.** Primary sources instead of summaries: the actual logs, the raw data or DB rows, the spec or statute text, the library's source code, the client's own words in the transcript. Say exactly where it is (path, URL, command).
3. **The specific methods and tools they'd use.** Named techniques and named tools or commands, not "analyze carefully".
4. **What would show the result is right, beyond the assistant or the user saying so.** An outside check: a test, a reconciliation against the bank statement, a second model's review, a real user, the official validator, a measurable before/after.

## Then

5. **Rewrite the prompt** to ask for exactly that, in the user's voice, as one copyable block. Keep it the same size or smaller than a normal ask; depth comes from precision, not length.
6. Ask one line: run it now, or plan it first? Building something → hand the rewritten prompt to your planning skill if you have one (or plan mode). Stress-testing a plan or decision → an interview-style skill such as `grill-me` if installed. Small → just run it.

## Rules
- Plain words, no filler. The whole output fits on one screen.
- Don't invent facts about the user's situation; if something is unknown, say what to check.
- If the ask is already sharp, say so in one line and run it.
