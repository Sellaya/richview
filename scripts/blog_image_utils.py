#!/usr/bin/env python3
"""Resize branded blog hero art to 1280×702 and map SEO source files to slugs."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

SEO_ROOT = Path("/Users/ali/Downloads/SEO Blogs")
REPO = Path(__file__).resolve().parents[1]
HERO_W = 1280
HERO_H = 702
HERO_BG = (11, 22, 53)  # #0B1635 — matches .post-hero-figure background

# Verified 2026-08-28: each WhatsApp graphic headline matches its article topic.
BATCH4_IMAGE_MAP: dict[str, Path] = {
    "place-declined-mortgage-files-ontario": SEO_ROOT / "WhatsApp Image 2026-08-28 at 11.18.40.jpeg",
    "fast-private-mortgage-closing-ontario": SEO_ROOT / "WhatsApp Image 2026-08-28 at 11.12.10.jpeg",
    "fsra-private-mortgage-rules-ontario-brokers": SEO_ROOT / "WhatsApp Image 2026-08-28 at 11.15.27.jpeg",
    "mic-vs-private-lender-broker-deals-ontario": SEO_ROOT / "WhatsApp Image 2026-08-28 at 11.15.34.jpeg",
    "private-mortgage-commitment-letter-fees-conditions-ontario": SEO_ROOT
    / "WhatsApp Image 2026-08-28 at 11.22.34.jpeg",
    "appraisal-requirements-private-mortgage-ontario": SEO_ROOT / "WhatsApp Image 2026-08-28 at 11.08.48.jpeg",
    "mortgage-arrears-power-of-sale-broker-ontario": SEO_ROOT / "WhatsApp Image 2026-08-28 at 11.20.13.jpeg",
    "direct-private-mortgage-lender-toronto-brokers": SEO_ROOT / "WhatsApp Image 2026-08-28 at 11.10.46.jpeg",
    "private-lending-mortgage-brokers-ontario": SEO_ROOT / "WhatsApp Image 2026-08-28 at 11.21.26.jpeg",
}

# Batch 3 posts still missing dedicated hero files (add to SEO Blogs folder and extend map).
BATCH3_PENDING_IMAGE_MAP: dict[str, Path] = {
    "vendor-take-back-mortgage-ontario": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (7).jpeg",
    "mortgage-on-inherited-property-ontario": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (8).jpeg",
}


def resize_hero_contain(src: Path, dst: Path, width: int = HERO_W, height: int = HERO_H) -> None:
    """Letterbox source image onto exact width×height canvas (full logo + headline visible)."""
    img = Image.open(src).convert("RGB")
    src_w, src_h = img.size
    scale = min(width / src_w, height / src_h)
    new_w = max(1, int(src_w * scale))
    new_h = max(1, int(src_h * scale))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (width, height), HERO_BG)
    canvas.paste(resized, ((width - new_w) // 2, (height - new_h) // 2))
    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst, "JPEG", quality=88, optimize=True)


def export_hero(slug: str, src: Path, repo: Path = REPO) -> Path:
    dst = repo / f"images/blog/{slug}.jpg"
    resize_hero_contain(src, dst)
    return dst


def export_all_mapped(maps: list[dict[str, Path]]) -> list[str]:
    exported: list[str] = []
    for mapping in maps:
        for slug, src in mapping.items():
            if not src.is_file():
                print(f"Skip {slug}: missing source {src.name}")
                continue
            out = export_hero(slug, src)
            exported.append(slug)
            print(f"Exported {out.relative_to(REPO)} ({HERO_W}×{HERO_H}) from {src.name}")
    return exported
