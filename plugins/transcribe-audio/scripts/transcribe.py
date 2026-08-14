#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "google-generativeai",
# ]
# ///
"""
transcribe.py — chunked Gemini-powered audio/video transcription.

Read SKILL.md (sibling directory) for full docs and design rationale.

Usage:
    GEMINI_API_KEY=AIzaSy... uv run transcribe.py \\
      --input  /path/to/recording.m4a \\
      --output-dir /path/to/transcripts \\
      --languages "Nepali, English" \\
      --target-script roman
"""

from __future__ import annotations

import argparse
import math
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from contextlib import contextmanager

import google.generativeai as genai

# ─── Models (best → fallback) ─────────────────────────────────────────────
PRIMARY_MODEL = "gemini-3-flash-preview"
FALLBACK_MODELS = [
    "gemini-3.1-flash-lite-preview",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]

AUDIO_VIDEO_EXTS = {".m4a", ".mp3", ".wav", ".ogg", ".opus", ".flac",
                    ".mp4", ".mov", ".mkv", ".webm", ".aac"}

# Unicode ranges for non-Roman scripts that "Roman" target should reject.
# Each tuple: (script_name, start, end).
NON_ROMAN_RANGES = [
    ("Devanagari",     0x0900, 0x097F),
    ("Bengali",        0x0980, 0x09FF),
    ("Gurmukhi",       0x0A00, 0x0A7F),
    ("Gujarati",       0x0A80, 0x0AFF),
    ("Tamil",          0x0B80, 0x0BFF),
    ("Telugu",         0x0C00, 0x0C7F),
    ("Kannada",        0x0C80, 0x0CFF),
    ("Malayalam",      0x0D00, 0x0D7F),
    ("Sinhala",        0x0D80, 0x0DFF),
    ("Thai",           0x0E00, 0x0E7F),
    ("Arabic",         0x0600, 0x06FF),
    ("Hebrew",         0x0590, 0x05FF),
    ("Cyrillic",       0x0400, 0x04FF),
    ("Greek",          0x0370, 0x03FF),
    ("CJK",            0x4E00, 0x9FFF),
    ("Hiragana",       0x3040, 0x309F),
    ("Katakana",       0x30A0, 0x30FF),
    ("Hangul",         0xAC00, 0xD7AF),
]


# ─── Prompt building ──────────────────────────────────────────────────────
def build_prompt(languages: str, target_script: str, custom_prompt: str | None) -> str:
    if custom_prompt:
        return custom_prompt

    if target_script.lower() == "roman":
        script_block = f"""\
SCRIPT REQUIREMENT — THIS IS THE MOST IMPORTANT RULE:
- You MUST write ALL non-English words using ROMAN LETTERS (a-z) ONLY.
- ZERO non-Roman characters. No Devanagari (देवनागरी), no Cyrillic, no Arabic, no CJK — none.
- Spoken {languages} is transcribed PHONETICALLY in English letters.
- CORRECT examples: "tapai kaha januhunchha?" "ramro cha" "ke bhayo" "namaste" "dhanyabad"
- WRONG (FORBIDDEN): native script characters of any kind."""
    elif target_script.lower() == "native":
        script_block = f"""\
SCRIPT REQUIREMENT:
- Write each language in its NATIVE script as it is normally written.
- {languages}: use the conventional written form for each."""
    else:
        # Custom script name — pass through with a generic instruction
        script_block = f"""\
SCRIPT REQUIREMENT:
- Write the transcript using the {target_script} script.
- Do not mix in other scripts."""

    return f"""\
Transcribe this audio recording. The speakers may switch between {languages}.

{script_block}

CRITICAL — SPEAKER IDENTIFICATION:
- Identify each unique speaker consistently throughout the entire transcript.
- Once you assign Speaker A, B, C, etc. to a voice, maintain that assignment.
- Do NOT mix up speakers or change assignments mid-transcript.
- If you hear the same person speak again, use the SAME label.
- Use real names if you clearly hear them being called.

OTHER RULES:
1. Transcribe VERBATIM — every word as spoken. No summarizing, paraphrasing, or skipping.
2. English words stay in English as spoken (when English is one of the languages).
3. Label speakers: Speaker A: / Speaker B: / Speaker C: (use real names if you hear them).
4. NO timestamps — transcribe lines without [mm:ss] markers.
5. Keep filler words (um, hmm, haina, aba, ani, tara, okay, etc.).
6. If audio is unclear, write [unclear]. Do NOT guess or hallucinate.
7. Output ONLY the transcript lines. No commentary, no headers, no explanations.

Begin transcription now:"""


# ─── Script validation ────────────────────────────────────────────────────
def script_violations(text: str, target_script: str) -> tuple[str, int] | None:
    """Return (script_name, count) if target_script is 'roman' and non-Roman chars found."""
    if target_script.lower() != "roman":
        return None
    for name, start, end in NON_ROMAN_RANGES:
        count = sum(1 for c in text if start <= ord(c) <= end)
        if count > 0:
            return (name, count)
    return None


# ─── Audio splitting ──────────────────────────────────────────────────────
def split_audio(input_path: Path, chunks_dir: Path, chunk_minutes: int) -> list[Path]:
    chunks_dir.mkdir(parents=True, exist_ok=True)
    chunk_secs = chunk_minutes * 60

    duration = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(input_path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip())

    n_chunks = max(1, math.ceil(duration / chunk_secs))
    ext = input_path.suffix.lower()

    chunks = []
    for i in range(n_chunks):
        start = i * chunk_secs
        end = min(start + chunk_secs, duration)
        out_path = chunks_dir / f"chunk_{i+1:02d}{ext}"
        if not out_path.exists():
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(input_path),
                 "-ss", str(start), "-t", str(chunk_secs),
                 "-c", "copy", str(out_path)],
                capture_output=True, check=True,
            )
            print(f"    chunk_{i+1:02d}{ext}  ({start/60:.0f}m–{end/60:.0f}m)", flush=True)
        else:
            print(f"    [skip] chunk_{i+1:02d}{ext} already split", flush=True)
        chunks.append(out_path)
    return chunks


# ─── Timeout handler ──────────────────────────────────────────────────────
class TimeoutException(Exception):
    pass

@contextmanager
def timeout_handler(seconds: int, label: str = "operation"):
    """Context manager with explicit timeout. Raises TimeoutException if exceeded."""
    def timeout_signal(signum, frame):
        raise TimeoutException(f"{label} exceeded {seconds}s timeout")

    old_handler = signal.signal(signal.SIGALRM, timeout_signal)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


# ─── Gemini upload + transcribe ───────────────────────────────────────────
def upload_and_wait(chunk_path: Path, api_key: str):
    genai.configure(api_key=api_key)
    audio_file = genai.upload_file(str(chunk_path))
    for _ in range(40):
        if audio_file.state.name == "ACTIVE":
            return audio_file
        if audio_file.state.name == "FAILED":
            raise RuntimeError(f"Upload failed: {chunk_path.name}")
        time.sleep(3)
        audio_file = genai.get_file(audio_file.name)
    raise RuntimeError(f"Upload timeout: {chunk_path.name}")


def transcribe_chunk(
    chunk_path: Path,
    chunk_idx: int,
    total: int,
    api_keys: list[str],
    prompt: str,
    target_script: str,
) -> str:
    models = [PRIMARY_MODEL] + FALLBACK_MODELS
    last_err: Exception | None = None

    for model_id in models:
        for key_idx, api_key in enumerate(api_keys):
            try:
                audio_file = upload_and_wait(chunk_path, api_key)
                genai.configure(api_key=api_key)
                print(f"    [{chunk_idx}/{total}] {model_id} (key {key_idx+1}) ...", flush=True)
                model = genai.GenerativeModel(model_id)

                # Wrap generate_content with explicit 90-second timeout
                try:
                    with timeout_handler(90, f"{model_id}/key{key_idx+1}"):
                        response = model.generate_content(
                            [audio_file, prompt],
                            generation_config=genai.types.GenerationConfig(temperature=0.0),
                            request_options={"timeout": 80},
                        )
                    text = response.text
                except TimeoutException as te:
                    last_err = te
                    print(f"    TIMEOUT on {model_id}/key{key_idx+1}, rotating key", flush=True)
                    time.sleep(3)
                    continue  # next key

                try:
                    genai.delete_file(audio_file.name)
                except Exception:
                    pass

                violation = script_violations(text, target_script)
                if violation:
                    name, count = violation
                    print(f"    [{model_id}] REJECTED — {count} {name} chars, trying next model", flush=True)
                    break  # next model

                return text

            except TimeoutException as e:
                last_err = e
                # Already handled above, continue to next key
                continue
            except Exception as e:
                last_err = e
                msg = str(e)
                if any(s in msg for s in ("429", "503", "quota", "RESOURCE_EXHAUSTED")):
                    print(f"    rate-limited on {model_id}/key{key_idx+1}, rotating key", flush=True)
                    time.sleep(5)
                    continue  # next key
                print(f"    [{model_id}] error: {msg[:120]}", flush=True)
                break  # next model

    raise RuntimeError(f"All models/keys exhausted. Last error: {last_err}")


# ─── Process one input file ───────────────────────────────────────────────
def process_file(
    input_path: Path,
    output_base: Path,
    api_keys: list[str],
    chunk_minutes: int,
    prompt: str,
    target_script: str,
):
    out_dir = output_base / input_path.stem
    chunks_dir = out_dir / "chunks"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*56}\n  {input_path.name}\n{'='*56}", flush=True)

    print("\n[1/3] Splitting ...", flush=True)
    chunks = split_audio(input_path, chunks_dir, chunk_minutes)
    print(f"  → {len(chunks)} chunk(s)", flush=True)

    print("\n[2/3] Transcribing ...", flush=True)
    all_text: list[str] = []
    for idx, chunk in enumerate(chunks, 1):
        md_path = out_dir / f"chunk_{idx:02d}.md"
        if md_path.exists():
            print(f"    [skip] chunk_{idx:02d}.md already exists", flush=True)
            all_text.append(md_path.read_text(encoding="utf-8"))
            continue
        try:
            text = transcribe_chunk(chunk, idx, len(chunks), api_keys, prompt, target_script)
            md_path.write_text(text, encoding="utf-8")
            print(f"    saved chunk_{idx:02d}.md ({len(text):,} chars)", flush=True)
            all_text.append(text)
            time.sleep(2)
        except Exception as e:
            print(f"    ERROR chunk {idx}: {e}", flush=True)
            placeholder = f"\n[TRANSCRIPTION FAILED — CHUNK {idx}: {e}]\n"
            md_path.write_text(placeholder, encoding="utf-8")
            all_text.append(placeholder)

    print("\n[3/3] Merging ...", flush=True)
    merged_path = out_dir / "FULL_TRANSCRIPT.md"
    lines = [
        f"# {input_path.stem} — Transcript",
        f"_Source: `{input_path}`_  ",
        f"_Primary model: `{PRIMARY_MODEL}` · Chunk size: {chunk_minutes} min · Target script: {target_script}_\n",
    ]
    for idx, text in enumerate(all_text, 1):
        s, e = (idx - 1) * chunk_minutes, idx * chunk_minutes
        lines += [
            f"\n{'─' * 56}",
            f"## Chunk {idx:02d}  [{s}m – {e}m]",
            f"{'─' * 56}\n",
            text,
        ]
    merged_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  → {merged_path} ({merged_path.stat().st_size:,} bytes)", flush=True)


# ─── Main ─────────────────────────────────────────────────────────────────
def collect_api_keys() -> list[str]:
    keys: list[str] = []
    base_vars = ["GEMINI_API_KEY", "GOOGLE_API_KEY"]
    numbered = [f"GEMINI_API_KEY_{i}" for i in range(2, 11)]
    for var in base_vars + numbered:
        v = os.environ.get(var, "").strip()
        if v and v not in keys:
            keys.append(v)
    return keys


def gather_inputs(args) -> list[Path]:
    found: list[Path] = []
    for p in (args.input or []):
        path = Path(p).expanduser()
        if not path.exists():
            print(f"WARN: input not found: {path}", flush=True)
            continue
        found.append(path)
    if args.input_dir:
        d = Path(args.input_dir).expanduser()
        if not d.is_dir():
            print(f"WARN: --input-dir not a directory: {d}", flush=True)
        else:
            for p in sorted(d.iterdir()):
                if p.suffix.lower() in AUDIO_VIDEO_EXTS:
                    found.append(p)
    return found


def main():
    parser = argparse.ArgumentParser(description="Chunked Gemini audio/video transcription")
    parser.add_argument("--input", action="append",
                        help="Input audio/video file (repeatable)")
    parser.add_argument("--input-dir",
                        help="Directory of audio/video files (all supported extensions transcribed)")
    parser.add_argument("--output-dir", required=True,
                        help="Where to put per-file transcript folders")
    parser.add_argument("--languages", default="English",
                        help='Comma-separated language list, e.g. "Nepali, English"')
    parser.add_argument("--target-script", default="roman",
                        help="'roman' (transliterate non-Latin → Roman), 'native', or a script name")
    parser.add_argument("--chunk-minutes", type=int, default=15,
                        help="Audio chunk length in minutes (default 15)")
    parser.add_argument("--prompt-file",
                        help="Path to a custom prompt text file (overrides built-in template)")
    args = parser.parse_args()

    inputs = gather_inputs(args)
    if not inputs:
        print("ERROR: no input files found. Pass --input <file> and/or --input-dir <dir>.")
        sys.exit(1)

    api_keys = collect_api_keys()
    if not api_keys:
        print("ERROR: no Gemini API key in environment.")
        print("  Get a free key at https://aistudio.google.com/apikey")
        print("  Then: export GEMINI_API_KEY=AIzaSy...")
        print("  Optional rotation: also set GEMINI_API_KEY_2, GEMINI_API_KEY_3, ...")
        sys.exit(1)

    custom_prompt = None
    if args.prompt_file:
        custom_prompt = Path(args.prompt_file).expanduser().read_text(encoding="utf-8")
    prompt = build_prompt(args.languages, args.target_script, custom_prompt)

    output_base = Path(args.output_dir).expanduser()
    output_base.mkdir(parents=True, exist_ok=True)

    print(f"Inputs: {len(inputs)} file(s) | Keys: {len(api_keys)} | "
          f"Languages: {args.languages} | Script: {args.target_script}", flush=True)

    for f in inputs:
        process_file(f, output_base, api_keys, args.chunk_minutes, prompt, args.target_script)

    print(f"\nDone. Transcripts at: {output_base}", flush=True)


if __name__ == "__main__":
    main()
