#!/usr/bin/env python3
"""Export SEO blog hero images at 1280×702 and patch live posts that were missing heroes."""

from __future__ import annotations

import importlib.util
import re
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BASE_URL = "https://richviewcapitalmic.com"

from blog_image_utils import BATCH3_PENDING_IMAGE_MAP, BATCH4_IMAGE_MAP, export_all_mapped


def load_batch3():
    spec = importlib.util.spec_from_file_location(
        "publish_batch3_blogs", REPO / "scripts/publish_batch3_blogs.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def patch_post_hero(slug: str, hero_alt: str) -> bool:
    path = REPO / f"blog/{slug}/index.html"
    if not path.is_file():
        return False
    img_path = f"/images/blog/{slug}.jpg"
    if not (REPO / f"images/blog/{slug}.jpg").is_file():
        return False

    text = path.read_text(encoding="utf-8")
    image_url = f"{BASE_URL}{img_path}"

    text = re.sub(
        r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="{image_url}">',
        text,
    )
    text = re.sub(
        r'<meta name="twitter:image" content="[^"]*">',
        f'<meta name="twitter:image" content="{image_url}">',
        text,
    )
    text = re.sub(
        r'"image": "https://richviewcapitalmic\.com/images/logo\.png"',
        f'"image": "{image_url}"',
        text,
    )

    hero_block = (
        '\n                <figure class="post-hero-figure post-hero-figure--object-contain" '
        'aria-label="Article hero image">\n'
        f'                    <img src="{img_path}" width="1280" height="702" '
        f'alt="{escape(hero_alt, quote=True)}" loading="eager" decoding="async">\n'
        "                </figure>"
    )

    if "post-hero-figure" not in text:
        text = re.sub(
            r'(<h1 class="post-title">.*?</h1>)',
            r"\1" + hero_block,
            text,
            count=1,
            flags=re.DOTALL,
        )

    path.write_text(text, encoding="utf-8")
    return True


def patch_card_images(slug: str) -> None:
    img_path = f"/images/blog/{slug}.jpg"
    if not (REPO / f"images/blog/{slug}.jpg").is_file():
        return
    for rel in ("blog/index.html", "index.html"):
        path = REPO / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            rf'(<a href="/blog/{re.escape(slug)}/"[^>]*><img )src="/images/logo\.png"',
            rf'\1src="{img_path}"',
            text,
        )
        text = re.sub(
            rf'(href="/blog/{re.escape(slug)}/" class="blog-card-thumb[^"]*"[^>]*>\s*<img )src="/images/logo\.png"',
            rf'\1src="{img_path}"',
            text,
        )
        path.write_text(text, encoding="utf-8")


BATCH3_HERO_ALTS = {
    "vendor-take-back-mortgage-ontario": (
        "Vendor take-back mortgage in Ontario — sold sign and home, Richview Capital VTB guide"
    ),
    "mortgage-on-inherited-property-ontario": (
        "Mortgage on inherited property in Ontario — estate and probate financing, Richview Capital"
    ),
}


def main() -> int:
    exported = export_all_mapped([BATCH4_IMAGE_MAP, BATCH3_PENDING_IMAGE_MAP])
    if not exported:
        print("No hero images exported.", file=sys.stderr)
        return 1

    batch3 = load_batch3()
    pending_slugs = [s for s in BATCH3_PENDING_IMAGE_MAP if s in exported]
    for slug in pending_slugs:
        cfg = next(c for c in batch3.BLOGS if c["slug"] == slug)
        if patch_post_hero(slug, cfg["hero_alt"]):
            patch_card_images(slug)
            print(f"Patched live post /blog/{slug}/ with new hero")

    print(f"Done — {len(exported)} hero image(s) at 1280×702.")
    missing_b4 = set(BATCH4_IMAGE_MAP) - set(exported)
    if missing_b4:
        print("Batch 4 still missing hero source:", ", ".join(sorted(missing_b4)))
    missing_b3 = {k for k, v in BATCH3_PENDING_IMAGE_MAP.items() if not v.is_file()}
    if missing_b3:
        print("Batch 3 still missing hero source:", ", ".join(sorted(missing_b3)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
