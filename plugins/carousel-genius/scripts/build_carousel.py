#!/usr/bin/env python3
"""
Build a carousel deck from a YAML brief.

Usage:
    python3 build_carousel.py <brief.yaml> [--out <output_dir>]

The YAML brief defines: layout, brand, slides[]. Each slide gets rendered to
out/<slug>/slide-NN.html. Pair with render_pngs.mjs to convert to PNGs.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml first")

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    sys.exit("pip install jinja2 first")


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
ICONS_DIR = SKILL_DIR / "assets" / "icons"


def load_icon(name: str) -> str:
    """Load brand SVG by name from assets/icons/. Returns inline svg string or empty."""
    path = ICONS_DIR / f"{name}.svg"
    if path.exists():
        return path.read_text()
    return ""


def resolve_icons_in(obj):
    """Walk dict/list and replace 'logo_icon: <name>' with 'logo_svg: <inline-svg>'."""
    if isinstance(obj, dict):
        if "logo_icon" in obj and "logo_svg" not in obj:
            svg = load_icon(obj["logo_icon"])
            if svg:
                obj["logo_svg"] = svg
        return {k: resolve_icons_in(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve_icons_in(x) for x in obj]
    return obj

LAYOUT_MAP = {
    "rahul": "01-rahul-display.html",
    "harry": "02-marketing-harry.html",
    "marketing-harry": "02-marketing-harry.html",
    "sago": "03-sago-editorial.html",
    "terminal": "04-terminal-mono.html",
    "adryze-terminal": "04-terminal-mono.html",  # legacy alias, kept for old briefs
    "photo": "05-photo-narrative.html",
    "adryze-photo": "05-photo-narrative.html",   # legacy alias, kept for old briefs
    "bare": "06-bare-hook.html",
    "bare-hook": "06-bare-hook.html",
}

SWIPE_CUES = ["KEEP GOING →", "NEXT →", "ALMOST →", "ONE MORE →", "LAST ONE →", "ALMOST THERE →"]

# Neutral fallback brand — used only when a brief has no `brand:` block at all.
# Override per-deck via the brief's `brand: {name, handle, logo_svg}`, or apply
# your own brand skill's tokens before calling this script.
DEFAULT_BRAND = {
    "name": "YOUR BRAND",
    "handle": "your_handle",
    "logo_svg": None,
}


def get_swipe_cue(slide_n: int, total: int) -> str:
    """Return escalating swipe cue for slide_n (1-indexed). Final = SAVE THIS."""
    if slide_n == total:
        return "SAVE THIS ↓"
    if slide_n == 1:
        return "KEEP GOING →"
    idx = min(slide_n - 1, len(SWIPE_CUES) - 1)
    return SWIPE_CUES[idx]


def slugify(text: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-")[:40]


def build(brief_path: Path, out_root: Path | None = None) -> Path:
    brief = yaml.safe_load(brief_path.read_text())

    layout_key = brief.get("layout", "terminal")
    template_file = LAYOUT_MAP.get(layout_key)
    if not template_file:
        sys.exit(f"Unknown layout: {layout_key}. Pick one of: {list(LAYOUT_MAP)}")

    brand = {**DEFAULT_BRAND, **(brief.get("brand") or {})}

    title = brief.get("title", "carousel")
    slug = brief.get("slug") or slugify(title)
    out_dir = (out_root or (Path.cwd() / "out")) / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(disabled_extensions=("html",), default=False),
        trim_blocks=True, lstrip_blocks=True,
    )
    template = env.get_template(template_file)

    slides = brief.get("slides", [])
    total = len(slides)

    rendered = []
    for i, slide in enumerate(slides, start=1):
        slide = resolve_icons_in(slide)
        is_cover = i == 1
        is_final = i == total

        body_class = slide.get("body_class")
        if not body_class:
            if is_cover:
                body_class = "cover"
            elif is_final:
                body_class = "final"
            else:
                body_class = "body"

        ctx = {
            "title": title,
            "slide_n": i,
            "slide_total": total,
            "slide_n_padded": f"{i:02d}",
            "slide_total_padded": f"{total:02d}",
            "is_cover": is_cover,
            "is_final": is_final,
            "swipe_cue": get_swipe_cue(i, total),
            "body_class": body_class,
            "brand_name": brand["name"],
            "handle": brand["handle"],
            "logo_svg": brand.get("logo_svg"),
            **slide,
        }

        html = template.render(**ctx)
        out_file = out_dir / f"slide-{i:02d}.html"
        out_file.write_text(html)
        rendered.append(out_file)

    print(f"Rendered {len(rendered)} slides to {out_dir}")
    print(f"Layout: {layout_key} ({template_file})")
    print(f"Next: node {SKILL_DIR}/scripts/render_pngs.mjs {out_dir}")
    return out_dir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", type=Path, help="YAML brief file")
    parser.add_argument("--out", type=Path, default=None, help="Output root (default: ./out)")
    args = parser.parse_args()

    if not args.brief.exists():
        sys.exit(f"Brief not found: {args.brief}")

    build(args.brief, args.out)


if __name__ == "__main__":
    main()
