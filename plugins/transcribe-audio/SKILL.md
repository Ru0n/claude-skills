---
name: transcribe-audio
description: Transcribe audio or video recordings (meetings, calls, interviews, lectures, voice notes) into clean verbatim text using the Gemini API. Handles long files via chunking, code-switched speech (e.g. Nepali+English), and language→script transliteration (e.g. Devanagari→Roman). Use whenever the user wants a transcript of an audio/video file — even when they don't say the word "transcribe" (phrases like "what does this recording say", "convert this call to text", "give me the transcript", "summarize this meeting" all qualify; for summarize-style requests, transcribe first then summarize).
created_by: external
pinned: false
version: 0.1.0
---

# transcribe-audio

Turns audio/video files into Markdown transcripts using Gemini. Built for code-switched, multi-language, and long-form recordings where vanilla speech-to-text breaks down.

## When to use this

- User points at an audio file (`.m4a`, `.mp3`, `.wav`, `.ogg`, `.opus`) or video file (`.mp4`, `.mov`, `.mkv`, `.webm`) and wants its content as text.
- Recordings longer than ~30 minutes — chunked processing is more resilient than one giant request.
- Code-switched speech (Nepali↔English, Hindi↔English, Spanish↔English etc.).
- The user wants **transliteration** rather than translation — Nepali/Hindi spoken in Devanagari script written out in Roman letters.
- The user wants a verbatim transcript, not a summary. (If they want a summary, transcribe first, then summarize from the transcript — never let Gemini summarize directly, hallucination risk is high.)

If the audio is in just one language and short (<10 min), this skill is still fine but overkill.

## Quick start

The bundled script `scripts/transcribe.py` does the whole pipeline. Invoke with `uv run`, resolved relative to this skill's own base directory (given to you when the skill was invoked) rather than a fixed path, so dependencies install automatically:

```bash
uv run "<this skill's base directory>/scripts/transcribe.py" \
  --input "/path/to/recording.m4a" \
  --output-dir "/path/to/transcripts" \
  --target-script roman \
  --languages "Nepali, English"
```

For multiple files in one run, pass `--input` multiple times. For a folder, pass `--input-dir /path/to/folder`. Each file gets its own subfolder under `--output-dir`.

## How it works (and why)

1. **Chunk the audio with ffmpeg stream-copy.** Default 15-minute chunks. Stream-copy is lossless, takes ~1 sec per file, and gives every chunk an independent retry boundary. If any chunk fails or returns garbage, you redo just that chunk — not the whole 90-minute meeting.
2. **Upload chunk to Gemini Files API.** Audio is processed at ~32 tokens/sec, so 15 min ≈ 28k tokens — fits easily into any model.
3. **Transcribe with a model cascade.** Tries `gemini-3.1-pro-preview` (best quality, tightest free quota) and falls back through `gemini-2.5-pro` → `gemini-3-flash-preview` → `gemini-3.1-flash-lite-preview` → 2.5 Flash variants → 2.0 Flash. Each model has its own free-tier quota pool, so cascading is more effective than retrying the same model.
4. **Rotate API keys on rate-limit.** Each Google account = one independent free-tier pool. Reading from `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3` … env vars.
5. **Reject + retry on script violations.** Some Gemini models (notably `gemini-2.5-pro`) ignore "use Roman script" instructions for Nepali/Hindi and emit Devanagari. The script auto-detects target-script violations and rotates to the next model. This is why the cascade matters — a single model is unreliable for transliteration tasks.
6. **Resume on re-run.** If `chunk_03.md` already exists, the script skips it. Killing the process and restarting picks up where it left off — no wasted API calls.
7. **Merge into `FULL_TRANSCRIPT.md`.** Combines all chunk files with timestamp headers per chunk.

## Setup (one-time per machine)

Gemini API keys live in env vars. Free keys at https://aistudio.google.com/apikey — sign in with each Google account you have to get a separate free quota pool.

```bash
export GEMINI_API_KEY=AIzaSy...
export GEMINI_API_KEY_2=AIzaSy...   # optional, for rotation
export GEMINI_API_KEY_3=AIzaSy...
```

Add to `~/.zshrc` to persist across sessions. The script also checks `GOOGLE_API_KEY` as an alias.

## Common invocation patterns

**Single meeting, Nepali+English → Roman:**
```bash
uv run scripts/transcribe.py \
  --input "~/Downloads/meeting.m4a" \
  --output-dir "~/Downloads/transcripts"
```

**Two recordings on Desktop, separate output folders:**
```bash
uv run scripts/transcribe.py \
  --input "~/Desktop/recording1.m4a" \
  --input "~/Desktop/recording2.m4a" \
  --output-dir "~/Desktop/transcripts"
```

**Whole folder of recordings:**
```bash
uv run scripts/transcribe.py --input-dir "~/Recordings" --output-dir "~/Recordings/transcripts"
```

**Different language pair (Hindi+English):**
```bash
uv run scripts/transcribe.py \
  --input "~/podcast.mp3" \
  --output-dir "~/transcripts" \
  --languages "Hindi, English" \
  --target-script roman
```

**Spanish meeting, native script:**
```bash
uv run scripts/transcribe.py \
  --input "~/junta.m4a" \
  --output-dir "~/transcripts" \
  --languages "Spanish" \
  --target-script native
```

**Smaller chunks for noisy / fast-paced audio:**
```bash
uv run scripts/transcribe.py --input "~/talk.m4a" --output-dir "~/out" --chunk-minutes 10
```

## Output format

Each input file gets:

```
output-dir/
└── <input-filename-stem>/
    ├── chunks/                   # raw audio chunks (kept for debugging)
    │   ├── chunk_01.m4a
    │   ├── chunk_02.m4a
    │   └── ...
    ├── chunk_01.md               # per-chunk transcript
    ├── chunk_02.md
    ├── ...
    └── FULL_TRANSCRIPT.md        # merged transcript
```

Each transcript line looks like:
```
[Speaker A] [00:30] tapai kaha januhunchha? we have a meeting at 5pm.
[Speaker B] [00:34] thik cha, ma 4:30 ma ready hunchhu.
```

If a chunk had unintelligible audio, you'll see `[unclear]` markers — Gemini correctly flags this rather than hallucinating, which is the whole point of the strict prompt.

## Long-running transcriptions

A 90-min recording at ~5–10 min per chunk takes 45–90 minutes of wall time. Run the script in the background and check on it periodically — don't poll faster than every 5 minutes since each chunk is a single API call.

```bash
uv run scripts/transcribe.py --input "~/long.m4a" --output-dir "~/out" &
```

Watch progress with:
```bash
ls -la ~/out/long/*.md         # which chunks are done
ps aux | grep transcribe.py    # is it still running
```

Re-run the same command to resume after a kill or crash.

## Customizing the prompt

If the user has unusual requirements (e.g. "skip the small talk", "label speakers by name when you hear them, not A/B"), edit the prompt template by passing `--prompt-file /path/to/prompt.txt`. Otherwise stick to the built-in prompt — it's been hardened against the common failure modes (Devanagari leaking through, summarization, hallucinated content during silence).

## Failure modes & what to do

- **All chunks come back `[unclear]`.** Audio is genuinely too quiet/muffled for Gemini. Try `ffmpeg -i in.m4a -af "loudnorm=I=-16:TP=-1.5:LRA=11" out.m4a` to normalize then re-run.
- **Script keeps producing the wrong script even after cascade.** Means every model in the cascade defaults to native script for that language. Edit `scripts/transcribe.py` `validate_script()` to be more lenient, or accept native-script output and post-process with a transliteration library.
- **All keys rate-limited.** Wait an hour, or get more keys (free tier daily quotas reset at midnight Pacific time).
- **Chunk takes >15 min and never returns.** Likely a network hang on the upload. Kill and restart — resume will skip done chunks.
