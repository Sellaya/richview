#!/usr/bin/env python3
"""Add trailing slashes to internal page URLs (directory index convention) site-wide."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# href= (longer paths first)
HREF = [
    ('href="/blog/second-mortgages-when-they-help"', 'href="/blog/second-mortgages-when-they-help/"'),
    ('href="/blog/construction-financing-ontario"', 'href="/blog/construction-financing-ontario/"'),
    ('href="/blog/mics-registered-accounts"', 'href="/blog/mics-registered-accounts/"'),
    ('href="/what-is-a-mic"', 'href="/what-is-a-mic/"'),
    ('href="/borrowers"', 'href="/borrowers/"'),
    ('href="/brokers"', 'href="/brokers/"'),
    ('href="/investors"', 'href="/investors/"'),
    ('href="/about"', 'href="/about/"'),
    ('href="/faq"', 'href="/faq/"'),
    ('href="/blog"', 'href="/blog/"'),
    ('href="/privacy"', 'href="/privacy/"'),
    ('href="/terms"', 'href="/terms/"'),
    ('href="/disclaimer"', 'href="/disclaimer/"'),
    ('href="/thank-you"', 'href="/thank-you/"'),
]

# Absolute site URLs in meta / JSON-LD (no trailing slash on domain root)
ABS = [
    ("https://richviewcapitalmic.com/blog/second-mortgages-when-they-help\"", "https://richviewcapitalmic.com/blog/second-mortgages-when-they-help/\""),
    ("https://richviewcapitalmic.com/blog/construction-financing-ontario\"", "https://richviewcapitalmic.com/blog/construction-financing-ontario/\""),
    ("https://richviewcapitalmic.com/blog/mics-registered-accounts\"", "https://richviewcapitalmic.com/blog/mics-registered-accounts/\""),
    ("https://richviewcapitalmic.com/what-is-a-mic\"", "https://richviewcapitalmic.com/what-is-a-mic/\""),
    ("https://richviewcapitalmic.com/borrowers\"", "https://richviewcapitalmic.com/borrowers/\""),
    ("https://richviewcapitalmic.com/brokers\"", "https://richviewcapitalmic.com/brokers/\""),
    ("https://richviewcapitalmic.com/investors\"", "https://richviewcapitalmic.com/investors/\""),
    ("https://richviewcapitalmic.com/about\"", "https://richviewcapitalmic.com/about/\""),
    ("https://richviewcapitalmic.com/faq\"", "https://richviewcapitalmic.com/faq/\""),
    ("https://richviewcapitalmic.com/blog\"", "https://richviewcapitalmic.com/blog/\""),
    ("https://richviewcapitalmic.com/privacy\"", "https://richviewcapitalmic.com/privacy/\""),
    ("https://richviewcapitalmic.com/terms\"", "https://richviewcapitalmic.com/terms/\""),
    ("https://richviewcapitalmic.com/disclaimer\"", "https://richviewcapitalmic.com/disclaimer/\""),
    ("https://richviewcapitalmic.com/thank-you\"", "https://richviewcapitalmic.com/thank-you/\""),
]

# JSON-LD url field (no extra quote)
ABS_JSON = [
    ('"url":"https://richviewcapitalmic.com/blog/second-mortgages-when-they-help"', '"url":"https://richviewcapitalmic.com/blog/second-mortgages-when-they-help/"'),
    ('"url":"https://richviewcapitalmic.com/blog/construction-financing-ontario"', '"url":"https://richviewcapitalmic.com/blog/construction-financing-ontario/"'),
    ('"url":"https://richviewcapitalmic.com/blog/mics-registered-accounts"', '"url":"https://richviewcapitalmic.com/blog/mics-registered-accounts/"'),
]

OTHER = [
    ("window.location.href = '/thank-you'", "window.location.href = '/thank-you/'"),
]


def main() -> None:
    paths = list(ROOT.rglob("*.html"))
    for path in paths:
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in HREF + ABS + ABS_JSON + OTHER:
            text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("updated", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
