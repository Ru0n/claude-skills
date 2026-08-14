# claude-skills

A collection of standalone [Claude Code](https://claude.com/claude-code) skills, each independently installable:

- **`gemma-4-31b-prompting`** — Expert reference for prompting, configuring, and deploying Google Gemma 4 31B via the Gemini API: thinkingConfig, safety settings, chat template, tool calling, token-collapse mitigation, code-switching, and migration notes from Gemini 3 Flash. Synthesized from official docs, model cards, and a 56-source deep-research pass — fully cited.
- **`iphone-mirroring`** — Drive an iPhone from a Mac through the iPhone Mirroring app: launch it, check lock state, screenshot the mirrored screen, and map coordinates for taps. Built from hands-on, dated verification against real macOS behavior, not just API docs.
- **`explain`** — Layered explanations for a smart non-specialist: a plain-language pitch, one mental-model analogy, then real technical detail with file paths and function names. Optionally renders a standalone HTML diagram.
- **`higgsfield-generate`** — Prompt-engineering and CLI/MCP workflow guide for Higgsfield AI image/video generation: model catalog, marketing modes, media inputs, troubleshooting.
- **`transcribe-audio`** — Turns audio/video files into clean verbatim Markdown transcripts using the Gemini API. Handles long recordings via chunking, model-cascade fallback, API-key rotation, and code-switched/transliterated speech (e.g. Nepali written in Roman script).
- **`carousel-genius`** — Designs and ships multi-slide carousels (Instagram, LinkedIn, TikTok, X) using one of 5 reverse-engineered creator layouts (credited to their original creators). Works with any brand you specify, or clean neutral defaults if you don't.
- **`testing`** — Iron-clad pre-production testing gauntlet: dual independent adversarial code review, a real non-prod test environment, a Chrome DevTools functional + UI sweep, a fix-and-retest loop, and a final zero-context adversarial agent — only claims "good to go" when every gate has evidence, not a guess.

Each is a separate plugin — install only the ones you want.

## Install

### Option A — Plugin marketplace (recommended)

```
/plugin marketplace add Ru0n/claude-skills
/plugin install gemma-4-31b-prompting@claude-skills
/plugin install iphone-mirroring@claude-skills
/plugin install explain@claude-skills
/plugin install higgsfield-generate@claude-skills
/plugin install transcribe-audio@claude-skills
/plugin install carousel-genius@claude-skills
/plugin install testing@claude-skills
```

Restart Claude Code (or run `/reload-plugins` if prompted) after installing.

### Option B — manual

```bash
git clone https://github.com/Ru0n/claude-skills.git
cp -r claude-skills/plugins/<skill-name> ~/.claude/skills/<skill-name>
```

Restart Claude Code. The leftover `.claude-plugin/plugin.json` in each folder is harmless metadata under manual install.

## Requirements per skill

- `gemma-4-31b-prompting`, `explain` — no external dependencies, pure reference/methodology skills.
- `iphone-mirroring` — macOS with the iPhone Mirroring app; some steps need Accessibility permissions granted to your terminal/Claude Code.
- `higgsfield-generate` — a Higgsfield account/API access.
- `transcribe-audio` — `ffmpeg`/`ffprobe` on PATH, `uv` for running the bundled script, and a free Gemini API key (`GEMINI_API_KEY`, get one at https://aistudio.google.com/apikey).
- `carousel-genius` — Node.js (`npm install` in the skill folder — pulls in `playwright` and `pdfkit`) and Python 3 with `pyyaml`/`jinja2` for the build script.
- `testing` — Chrome DevTools MCP (or fall back to a Playwright-based skill) for Gate 3; two independent subagents/review tools for Gate 1.

## License

MIT — see [LICENSE](LICENSE).
