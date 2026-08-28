#!/usr/bin/env python3
"""Standardize all blog hero JPGs at 1280×702 (cover) and patch index card classes."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

from blog_image_utils import (
    BATCH3_PENDING_IMAGE_MAP,
    BATCH4_IMAGE_MAP,
    BLOG_CARD_IMAGE_CLASS,
    BLOG_CARD_THUMB_CLASS,
    HERO_H,
    HERO_W,
    export_hero,
    resize_hero_cover,
)

# Legacy on-disk filenames that differ from /images/blog/{slug}.jpg
LEGACY_HERO_FILES: dict[str, str] = {
    "private-construction-loan-ontario": "private-construction-loan-ontario-hero.jpg",
}


def load_batch3():
    spec = importlib.util.spec_from_file_location(
        "publish_batch3_blogs", REPO / "scripts/publish_batch3_blogs.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def source_map() -> dict[str, Path]:
    batch3 = load_batch3()
    mapping: dict[str, Path] = {}
    for cfg in batch3.BLOGS:
        src = cfg.get("image_src")
        if src and Path(src).is_file():
            mapping[cfg["slug"]] = Path(src)
    mapping.update(BATCH3_PENDING_IMAGE_MAP)
    mapping.update(BATCH4_IMAGE_MAP)
    return mapping


def live_slugs() -> list[str]:
    return sorted(p.name for p in (REPO / "blog").iterdir() if p.is_dir())


def hero_dst(slug: str) -> Path:
    return REPO / f"images/blog/{slug}.jpg"


def fallback_src(slug: str) -> Path | None:
    blog_dir = REPO / "images/blog"
    legacy = LEGACY_HERO_FILES.get(slug)
    if legacy:
        p = blog_dir / legacy
        if p.is_file():
            return p
    canonical = hero_dst(slug)
    if canonical.is_file():
        return canonical
    return None


def export_all_heroes() -> list[str]:
    exported: list[str] = []
    sources = source_map()
    for slug in live_slugs():
        dst = hero_dst(slug)
        src = sources.get(slug) or fallback_src(slug)
        if not src or not src.is_file():
            print(f"Skip {slug}: no hero source", file=sys.stderr)
            continue
        if src.resolve() == dst.resolve():
            resize_hero_cover(src, dst)
        else:
            export_hero(slug, src)
        exported.append(slug)
        print(f"  {slug}.jpg ({HERO_W}×{HERO_H})")
    return exported


def patch_card_classes() -> None:
    for rel in ("blog/index.html", "index.html"):
        path = REPO / rel
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r"blog-card-image blog-card-image--(?:object-contain|object-left|hero-fit)",
            f"blog-card-image {BLOG_CARD_IMAGE_CLASS}",
            text,
        )
        text = re.sub(
            r'(<div class="blog-card-image">)(\s*<a href="/blog/)',
            rf'<div class="blog-card-image {BLOG_CARD_IMAGE_CLASS}">\2',
            text,
        )
        text = re.sub(
            r"blog-card-thumb blog-card-thumb--(?:object-contain|object-left|hero-fit)",
            f"blog-card-thumb {BLOG_CARD_THUMB_CLASS}",
            text,
        )
        text = re.sub(
            r'(<a href="/blog/[^"]+/") class="blog-card-thumb"(?! )',
            rf'\1 class="blog-card-thumb {BLOG_CARD_THUMB_CLASS}"',
            text,
        )
        text = text.replace(
            "/images/blog/private-construction-loan-ontario-hero.jpg",
            "/images/blog/private-construction-loan-ontario.jpg",
        )
        text = re.sub(
            r'(<img src="/images/blog/[^"]+\.jpg"[^>]*?) width="[^"]*" height="[^"]*"',
            rf'\1 width="{HERO_W}" height="{HERO_H}"',
            text,
        )
        path.write_text(text, encoding="utf-8")
        print(f"Patched {rel}")


def main() -> int:
    print("Exporting heroes…")
    exported = export_all_heroes()
    patch_card_classes()
    print(f"Done — {len(exported)} blog hero(s) at {HERO_W}×{HERO_H}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
