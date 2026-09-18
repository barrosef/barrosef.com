#!/usr/bin/env python3
"""Renders one social card (1200×630) per article, in each language.

Output: static/og/<translationKey>.<lang>.png — picked up automatically by
layouts/_partials/head.html when the file exists (a page can still set
`image:` in its front matter to override). Same ground, rule and type as
static/og-default.png; the site's own woff2 fonts are converted on the fly.

Usage: python3 scripts/gen_og_images.py            # every post
       python3 scripts/gen_og_images.py --check    # exit 1 if a post has no card (CI; stdlib only)
Rendering needs Pillow + fontTools; a title change means re-running this and
committing the new PNG (the check only sees a missing card, not a stale one).
"""
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "static" / "og"
SECTIONS = {"en": ROOT / "content/en/writing", "pt-br": ROOT / "content/pt-br/artigos"}
KICKER = {"en": "barrosef.com / writing", "pt-br": "barrosef.com / artigos"}
BYLINE = {"en": "Ed Barros · Software & Solutions Architect", "pt-br": "Ed Barros · Arquiteto de Software e Soluções"}

W, H = 1200, 630
BG, INK, ACCENT = (11, 22, 34), (220, 230, 242), (91, 143, 214)
MARGIN = 96
TEXT_W = W - 2 * MARGIN

FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
KEY_VALUE = re.compile(r'^(\w+):\s*"?(.*?)"?\s*$')


def fonts():
    """The site's woff2 files as TTFs Pillow can load, in a temp dir."""
    from fontTools.ttLib import TTFont
    tmp = Path(tempfile.mkdtemp(prefix="og-fonts-"))
    out = {}
    for name in ("ibmplexsans-400", "ibmplexmono-400"):
        t = TTFont(ROOT / "static/fonts" / f"{name}.woff2")
        t.flavor = None
        t.save(tmp / f"{name}.ttf")
        out[name] = tmp / f"{name}.ttf"
    return out


def front_matter(path):
    m = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
    if not m:
        sys.exit(f"ERROR: {path}: missing front matter")
    fields = {}
    for line in m.group(1).splitlines():
        kv = KEY_VALUE.match(line)
        if kv:
            fields[kv.group(1)] = kv.group(2)
    return fields


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_title(draw, text, ttf):
    """Largest size (64 → 44) whose wrapped title fits in four lines."""
    from PIL import ImageFont
    for size in (64, 58, 52, 48, 44):
        font = ImageFont.truetype(str(ttf), size)
        lines = wrap(draw, text, font, TEXT_W)
        if len(lines) <= 4:
            return font, lines, size
    return font, lines[:4], size


def render(title, lang, ttfs, dest):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    mono = ImageFont.truetype(str(ttfs["ibmplexmono-400"]), 26)
    d.text((MARGIN, 78), KICKER[lang], font=mono, fill=ACCENT)
    d.rectangle([MARGIN, 150, MARGIN + 96, 157], fill=ACCENT)
    font, lines, size = fit_title(d, title, ttfs["ibmplexsans-400"])
    y = 190
    for ln in lines:
        d.text((MARGIN, y), ln, font=font, fill=INK)
        y += int(size * 1.22)
    d.text((MARGIN, H - 78 - 26), BYLINE[lang], font=mono, fill=ACCENT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, optimize=True)


def main(check=False):
    ttfs = None if check else fonts()
    stale = []
    for lang, folder in SECTIONS.items():
        for md in sorted(folder.glob("*.md")):
            if md.name == "_index.md":
                continue
            fm = front_matter(md)
            if fm.get("draft", "false") == "true" or "translationKey" not in fm:
                continue
            dest = OUT / f"{fm['translationKey']}.{lang}.png"
            if check:
                if not dest.exists():
                    stale.append(dest.relative_to(ROOT))
                continue
            render(fm["title"], lang, ttfs, dest)
            print("wrote", dest.relative_to(ROOT))
    if check and stale:
        print("posts without a social card — run scripts/gen_og_images.py:\n  " + "\n  ".join(map(str, stale)))
        sys.exit(1)


if __name__ == "__main__":
    main(check="--check" in sys.argv)
