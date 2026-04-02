#!/usr/bin/env python3
"""
Move root *.html pages into folder/index.html so URLs are /borrowers/ with no .html
(static servers serve directory indexes). Root-qualify css/js/images paths.
Run once from repo root: python3 scripts/migrate_to_folder_routes.py
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (source relative to ROOT, destination relative to ROOT)
MOVES: list[tuple[str, str]] = [
    ("richview-about.html", "about/index.html"),
    ("richview-borrowers.html", "borrowers/index.html"),
    ("richview-capital-brokers.html", "brokers/index.html"),
    ("richview-capital-mic.html", "investors/index.html"),
    ("richview-faq.html", "faq/index.html"),
    ("richview-blog.html", "blog/index.html"),
    ("richview-what-is-a-mic.html", "what-is-a-mic/index.html"),
    ("privacy.html", "privacy/index.html"),
    ("terms.html", "terms/index.html"),
    ("disclaimer.html", "disclaimer/index.html"),
    ("thank-you.html", "thank-you/index.html"),
    ("blog-second-mortgages-when-they-help.html", "blog/second-mortgages-when-they-help/index.html"),
    ("blog-construction-financing-ontario.html", "blog/construction-financing-ontario/index.html"),
    ("blog-mics-registered-accounts.html", "blog/mics-registered-accounts/index.html"),
]


def rootize_assets(html: str) -> str:
    pairs = [
        ('href="css/', 'href="/css/'),
        ("href='css/", "href='/css/"),
        ('src="css/', 'src="/css/'),
        ('href="js/', 'href="/js/'),
        ('src="js/', 'src="/js/'),
        ('href="images/', 'href="/images/'),
        ('src="images/', 'src="/images/'),
        ('srcset="images/', 'srcset="/images/'),
        ("url('images/", "url('/images/"),
        ('url("images/', 'url("/images/'),
        ('url(images/', 'url(/images/'),
    ]
    for old, new in pairs:
        html = html.replace(old, new)
    return html


def main() -> None:
    for src_rel, dst_rel in MOVES:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.is_file():
            print("skip (missing):", src_rel)
            continue
        text = rootize_assets(src.read_text(encoding="utf-8"))
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        src.unlink()
        print("moved", src_rel, "->", dst_rel)

    # index.html stays at root; rootize assets so paths work from any future structure
    idx = ROOT / "index.html"
    if idx.is_file():
        t = rootize_assets(idx.read_text(encoding="utf-8"))
        idx.write_text(t, encoding="utf-8")
        print("updated index.html (root-absolute assets)")


if __name__ == "__main__":
    main()
