#!/usr/bin/env python3
"""Apply pending on-site SEO fixes: FAQ schema, legacy blog schema, post-related blocks."""

from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BASE = "https://richviewcapitalmic.com"

POST_RELATED: dict[str, list[tuple[str, str]]] = {
    "private-mortgage-rates-ontario": [
        ("/blog/private-mortgage-ontario/", "Private mortgages in Ontario"),
        ("/blog/bad-credit-mortgage-ontario/", "Bad credit mortgage in Ontario"),
        ("/blog/second-mortgage-ontario/", "Second mortgage in Ontario"),
        ("/blog/private-mortgage-lender-toronto-honest-gta-guide/", "Private mortgage lender Toronto guide"),
        ("/borrowers/", "Borrowing with Richview Capital"),
        ("/faq/", "FAQ"),
    ],
    "mortgage-after-consumer-proposal-ontario": [
        ("/blog/bad-credit-mortgage-ontario/", "Bad credit mortgage in Ontario"),
        ("/blog/debt-consolidation-mortgage-ontario/", "Debt consolidation mortgage in Ontario"),
        ("/blog/private-mortgage-ontario/", "Private mortgages in Ontario"),
        ("/blog/second-mortgage-ontario/", "Second mortgage in Ontario"),
        ("/borrowers/", "Borrowing with Richview Capital"),
    ],
    "home-renovation-financing-ontario": [
        ("/blog/heloc-home-equity-loan-gta/", "HELOC and home equity loans in the GTA"),
        ("/blog/second-mortgage-ontario/", "Second mortgage in Ontario"),
        ("/blog/garden-suite-financing-ontario/", "Garden suite financing in Ontario"),
        ("/blog/private-mortgage-ontario/", "Private mortgages in Ontario"),
        ("/borrowers/", "Borrowing with Richview Capital"),
    ],
    "newcomer-mortgage-canada-ontario": [
        ("/blog/private-mortgage-ontario/", "Private mortgages in Ontario"),
        ("/blog/self-employed-mortgage-gta/", "Self-employed mortgages in the GTA"),
        ("/blog/private-mortgage-lender-toronto-honest-gta-guide/", "Private mortgage lender Toronto guide"),
        ("/what-is-a-mic/", "What is a MIC?"),
        ("/borrowers/", "Borrowing with Richview Capital"),
    ],
    "reverse-mortgage-alternatives-canada": [
        ("/blog/heloc-home-equity-loan-gta/", "HELOC and home equity loans in the GTA"),
        ("/blog/second-mortgage-ontario/", "Second mortgage in Ontario"),
        ("/blog/private-mortgage-ontario/", "Private mortgages in Ontario"),
        ("/blog/debt-consolidation-mortgage-ontario/", "Debt consolidation mortgage in Ontario"),
        ("/borrowers/", "Borrowing with Richview Capital"),
    ],
    "brrrr-method-canada-financing-ontario": [
        ("/blog/private-construction-loan-ontario/", "Private construction loan Ontario"),
        ("/blog/construction-financing-ontario/", "Construction financing in Ontario"),
        ("/blog/land-financing-ontario/", "Land financing in Ontario"),
        ("/blog/second-mortgage-ontario/", "Second mortgage in Ontario"),
        ("/what-is-a-mic/", "What is a MIC?"),
    ],
    "interest-only-mortgage-canada": [
        ("/blog/private-mortgage-rates-ontario/", "Private mortgage rates in Ontario"),
        ("/blog/second-mortgage-ontario/", "Second mortgage in Ontario"),
        ("/blog/heloc-home-equity-loan-gta/", "HELOC and home equity loans in the GTA"),
        ("/what-is-a-mic/", "What is a MIC?"),
        ("/borrowers/", "Borrowing with Richview Capital"),
    ],
    "garden-suite-financing-ontario": [
        ("/blog/home-renovation-financing-ontario/", "Home renovation financing in Ontario"),
        ("/blog/construction-financing-ontario/", "Construction financing in Ontario"),
        ("/blog/heloc-home-equity-loan-gta/", "HELOC and home equity loans in the GTA"),
        ("/blog/second-mortgage-ontario/", "Second mortgage in Ontario"),
        ("/borrowers/", "Borrowing with Richview Capital"),
    ],
    "vendor-take-back-mortgage-ontario": [
        ("/blog/land-financing-ontario/", "Land financing in Ontario"),
        ("/blog/private-mortgage-ontario/", "Private mortgages in Ontario"),
        ("/blog/mortgage-on-inherited-property-ontario/", "Mortgage on inherited property in Ontario"),
        ("/blog/private-commercial-mortgage-ontario/", "Private commercial mortgage Ontario"),
        ("/borrowers/", "Borrowing with Richview Capital"),
    ],
    "mortgage-on-inherited-property-ontario": [
        ("/blog/second-mortgage-ontario/", "Second mortgage in Ontario"),
        ("/blog/private-mortgage-ontario/", "Private mortgages in Ontario"),
        ("/blog/debt-consolidation-mortgage-ontario/", "Debt consolidation mortgage in Ontario"),
        ("/blog/vendor-take-back-mortgage-ontario/", "Vendor take-back mortgage in Ontario"),
        ("/borrowers/", "Borrowing with Richview Capital"),
    ],
}

LEGACY_BLOGS = [
    {
        "slug": "private-mortgage-ontario",
        "breadcrumb": "Private Mortgages in Ontario",
        "headline": "Private mortgages in Ontario: what borrowers should know",
        "date": "2026-04-13T12:00:00-04:00",
    },
    {
        "slug": "private-mortgage-lender-toronto-honest-gta-guide",
        "breadcrumb": "Private Mortgage Lender Toronto",
        "headline": "Private mortgage lender Toronto: the honest GTA guide",
        "date": "2026-04-14T12:00:00-04:00",
    },
    {
        "slug": "mic-investing-ontario-rrsp",
        "breadcrumb": "MIC Investing in Ontario",
        "headline": "MIC investing in Ontario: RRSP-eligible returns from Mortgage Investment Corporations",
        "date": "2026-04-14T12:00:00-04:00",
    },
    {
        "slug": "construction-financing-ontario",
        "breadcrumb": "Construction Financing in Ontario",
        "headline": "Construction financing in Ontario: draw schedules, private lenders, and what lenders look for",
        "date": "2026-04-15T12:00:00-04:00",
    },
]


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.replace("\u00a0", " ")


def extract_faq_from_article(html: str) -> list[tuple[str, str]]:
    m = re.search(r"<h2[^>]*>\s*Frequently Asked Questions\s*</h2>", html, re.I)
    if not m:
        m = re.search(r"<h2[^>]*>[^<]*\bFAQ\b[^<]*</h2>", html, re.I)
    if not m:
        return []

    section = html[m.end() :]
    stop = re.search(r"<h2[^>]|class=\"post-related\"|<div class=\"post-related\"", section, re.I)
    if stop:
        section = section[: stop.start()]

    faqs: list[tuple[str, str]] = []
    for qm in re.finditer(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", section, re.S):
        q = strip_html(qm.group(1))
        a = strip_html(qm.group(2))
        if q and a and not q.lower().startswith("related on this site"):
            faqs.append((q, a))
    return faqs


def extract_meta_description(html: str) -> str:
    m = re.search(r'<meta name="description"\s+content="([^"]*)"', html)
    if m:
        return m.group(1)
    m = re.search(r'<meta name="description"\s*\n\s*content="([^"]*)"', html)
    return m.group(1) if m else ""


def build_article_graph(
    slug: str,
    headline: str,
    description: str,
    breadcrumb: str,
    date: str,
    faqs: list[tuple[str, str]],
) -> dict:
    page_url = f"{BASE}/blog/{slug}/"
    image_url = f"{BASE}/images/blog/{slug}.jpg"
    graph: list[dict] = [
        {
            "@type": "Article",
            "headline": headline,
            "description": description,
            "image": image_url,
            "author": {"@type": "Organization", "name": "Richview Capital MIC", "url": f"{BASE}/"},
            "publisher": {
                "@type": "Organization",
                "name": "Richview Capital MIC",
                "logo": {"@type": "ImageObject", "url": f"{BASE}/images/logo.png"},
            },
            "datePublished": date,
            "dateModified": date,
            "articleSection": "Borrowers",
            "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": breadcrumb, "item": page_url},
            ],
        },
    ]
    if faqs:
        graph.append(
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in faqs
                ],
            }
        )
    return {"@context": "https://schema.org", "@graph": graph}


def replace_json_ld_blocks(html: str, graph: dict) -> str:
    html = re.sub(
        r"\s*<script type=\"application/ld\+json\">.*?</script>",
        "",
        html,
        flags=re.S,
    )
    insert = (
        '    <script type="application/ld+json">\n'
        + json.dumps(graph, ensure_ascii=False, indent=2)
        + "\n    </script>"
    )
    marker = '<link rel="preconnect" href="https://fonts.googleapis.com">'
    if marker not in html:
        raise ValueError("preconnect marker not found")
    return html.replace(marker, insert + "\n    " + marker, 1)


def related_block(links: list[tuple[str, str]]) -> str:
    items = "\n".join(f'      <li><a href="{href}">{label}</a></li>' for href, label in links)
    return f"""  <div class="post-related">
    <h3>Related on this site</h3>
    <ul>
{items}
    </ul>
  </div>

"""


def inject_faq_schema() -> None:
    path = REPO / "faq/index.html"
    html = path.read_text(encoding="utf-8")
    if '"@type": "FAQPage"' in html or '"@type":"FAQPage"' in html:
        print("FAQ schema already present; skipping.")
        return

    faqs: list[tuple[str, str]] = []
    for qm in re.finditer(
        r'<button class="faq-q"[^>]*><span>(.*?)</span>',
        html,
        re.S,
    ):
        q = strip_html(qm.group(1))
        start = qm.end()
        am = re.search(r'<div class="faq-a">\s*(.*?)\s*</div>', html[start:], re.S)
        if not am:
            continue
        inner = am.group(1)
        parts = re.findall(r"<p[^>]*>(.*?)</p>", inner, re.S)
        a = strip_html(" ".join(parts)) if parts else strip_html(inner)
        if q and a:
            faqs.append((q, a))

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "FAQPage",
                "@id": f"{BASE}/faq/#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in faqs
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "FAQ", "item": f"{BASE}/faq/"},
                ],
            },
        ],
    }
    insert = (
        '    <script type="application/ld+json">\n'
        + json.dumps(graph, ensure_ascii=False, indent=2)
        + "\n    </script>\n"
    )
    marker = '    <link rel="preconnect" href="https://fonts.googleapis.com">'
    path.write_text(html.replace(marker, insert + marker, 1), encoding="utf-8")
    print(f"FAQ schema: {len(faqs)} questions on /faq/")


def upgrade_legacy_blogs() -> None:
    for cfg in LEGACY_BLOGS:
        path = REPO / f"blog/{cfg['slug']}/index.html"
        html = path.read_text(encoding="utf-8")
        if '"@graph"' in html and '"@type": "Article"' in html:
            print(f"Legacy schema already upgraded: {cfg['slug']}")
            continue
        faqs = extract_faq_from_article(html)
        if cfg["slug"] == "construction-financing-ontario" and not faqs:
            for block in re.findall(
                r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
                html,
                re.S,
            ):
                data = json.loads(block)
                if data.get("@type") == "FAQPage":
                    faqs = [
                        (e["name"], e["acceptedAnswer"]["text"])
                        for e in data.get("mainEntity", [])
                    ]
        desc = extract_meta_description(html)
        graph = build_article_graph(
            cfg["slug"],
            cfg["headline"],
            desc,
            cfg["breadcrumb"],
            cfg["date"],
            faqs,
        )
        path.write_text(replace_json_ld_blocks(html, graph), encoding="utf-8")
        print(f"Upgraded schema: /blog/{cfg['slug']}/ ({len(faqs)} FAQs)")


def add_post_related() -> None:
    for slug, links in POST_RELATED.items():
        path = REPO / f"blog/{slug}/index.html"
        html = path.read_text(encoding="utf-8")
        if "post-related" in html:
            print(f"post-related exists: {slug}")
            continue
        marker = "  <ul class=\"post-tags\">"
        if marker not in html:
            print(f"post-tags marker missing: {slug}", flush=True)
            continue
        html = html.replace(marker, related_block(links) + marker, 1)
        path.write_text(html, encoding="utf-8")
        print(f"Added post-related: {slug}")


def set_lang_en_ca() -> None:
    count = 0
    for path in REPO.rglob("*.html"):
        if "emails/" in str(path):
            continue
        text = path.read_text(encoding="utf-8")
        if '<html lang="en">' in text:
            path.write_text(text.replace('<html lang="en">', '<html lang="en-CA">', 1), encoding="utf-8")
            count += 1
    print(f"Updated lang=en-CA on {count} HTML files")


def main() -> int:
    inject_faq_schema()
    upgrade_legacy_blogs()
    add_post_related()
    set_lang_en_ca()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
