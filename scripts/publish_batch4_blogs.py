#!/usr/bin/env python3
"""Publish Richview SEO Batch 4 broker articles from output/ markdown + hero images."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEO_ROOT = Path("/Users/ali/Downloads/SEO Blogs/output")
BASE_URL = "https://richviewcapitalmic.com"

from blog_image_utils import BATCH4_IMAGE_MAP, export_hero

BATCH4_FOLDERS = [
    "richview-capital-place-declined-mortgage-files-ontario-20260824",
    "richview-capital-high-ltv-second-mortgage-lenders-gta-20260824",
    "richview-capital-fast-private-mortgage-closing-brokers-20260824",
    "richview-capital-fsra-private-mortgage-rules-brokers-20260824",
    "richview-capital-mic-vs-private-investor-broker-deals-20260824",
    "richview-capital-private-mortgage-commitment-letter-brokers-20260824",
    "richview-capital-appraisals-private-mortgage-deals-gta-20260824",
    "richview-capital-placing-arrears-power-of-sale-files-20260824",
    "richview-capital-direct-private-lender-toronto-brokers-20260824",
    "richview-capital-private-lending-brokerage-growth-2026-20260824",
]

HERO_ALTS = {
    "place-declined-mortgage-files-ontario": (
        "Where to place declined mortgage deals in Ontario — broker decision tree, Richview Capital"
    ),
    "high-ltv-second-mortgage-lenders-gta": (
        "85% LTV second mortgage lenders in Ontario — GTA broker guide, Richview Capital"
    ),
    "fast-private-mortgage-closing-ontario": (
        "Fast private mortgage closing in Ontario — same week funding checklist for brokers, Richview Capital"
    ),
    "fsra-private-mortgage-rules-ontario-brokers": (
        "FSRA private mortgage rules in 2026 — Level 2 licensing and suitability for Ontario brokers, Richview Capital"
    ),
    "mic-vs-private-lender-broker-deals-ontario": (
        "MIC vs private lender vs syndicated mortgage — where Ontario brokers should place private deals, Richview Capital"
    ),
    "private-mortgage-commitment-letter-fees-conditions-ontario": (
        "Private mortgage commitment letter fees and conditions — Ontario broker guide, Richview Capital"
    ),
    "appraisal-requirements-private-mortgage-ontario": (
        "Appraisal requirements for private mortgage deals in Ontario — GTA broker guide, Richview Capital"
    ),
    "mortgage-arrears-power-of-sale-broker-ontario": (
        "How Ontario brokers place arrears and power of sale files with a private lender — Richview Capital"
    ),
    "direct-private-mortgage-lender-toronto-brokers": (
        "Direct private mortgage lender vs middleman — what Toronto brokers should look for, Richview Capital"
    ),
    "private-lending-mortgage-brokers-ontario": (
        "Private lending for mortgage brokers in Ontario — grow your brokerage in 2026, Richview Capital"
    ),
}

CARD_EXCERPTS = {
    "place-declined-mortgage-files-ontario": (
        "A broker decision tree for declined files: when B works, when it is MIC or private, and how to set client expectations."
    ),
    "high-ltv-second-mortgage-lenders-gta": (
        "Where GTA brokers find 80–85% LTV seconds, how MICs price LTV bands, and how to package a high-LTV second for approval."
    ),
    "fast-private-mortgage-closing-ontario": (
        "Same-week private closing checklist: submissions, appraisals, title, payout statements, and what slows deals down."
    ),
    "fsra-private-mortgage-rules-ontario-brokers": (
        "2026 FSRA rules for private deals: Level 2 scope, suitability files, disclosure, and what examiners look for."
    ),
    "mic-vs-private-lender-broker-deals-ontario": (
        "Compare MIC, individual private, and syndicated structures — speed, flexibility, renewals, and where each fits."
    ),
    "private-mortgage-commitment-letter-fees-conditions-ontario": (
        "Commitment fees, conditions, validity periods, and subjects — what brokers should verify before the client signs."
    ),
    "appraisal-requirements-private-mortgage-ontario": (
        "Accepted appraisers, AVM vs full reports, transfers between lenders, and how value drives LTV and pricing."
    ),
    "mortgage-arrears-power-of-sale-broker-ontario": (
        "Payout statements, equity math, exit plans, and the package a private lender needs on arrears and POS files."
    ),
    "direct-private-mortgage-lender-toronto-brokers": (
        "Verify capital, underwriting, BDM access, and renewals before you send a Toronto file — direct MIC vs middleman."
    ),
    "private-lending-mortgage-brokers-ontario": (
        "2026 renewal-wave data, FSRA compliance, and a lender-bench process to close more private deals through brokers."
    ),
}


def load_batch3():
    spec = importlib.util.spec_from_file_location(
        "publish_batch3_blogs", REPO / "scripts/publish_batch3_blogs.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def preprocess_md(text: str) -> str:
    text = re.sub(
        r'<a href="([^"]+)"(?:\s[^>]*)?>([^<]+)</a>',
        lambda m: f"[{m.group(2)}]({m.group(1)})",
        text,
    )
    return text


def extract_slug(kit: str) -> str:
    patterns = [
        r"\*\*Suggested slug:\*\*\s*`?([a-z0-9-]+)`?",
        r"- Slug:\s*`?([a-z0-9-]+)`?",
        r"## Suggested URL slug\s*\n+([a-z0-9-]+)",
        r"## Proposed URL slug\s*\n+`?([a-z0-9-]+)`?",
        r"- Slug:\s*([a-z0-9-]+)",
    ]
    for pat in patterns:
        m = re.search(pat, kit, re.I)
        if m:
            return m.group(1).strip("`")
    raise ValueError("Could not parse slug from publishing kit")


def extract_title_tag(kit: str) -> str:
    m = re.search(
        r"## Title tag[^\n]*\n+\n?([^\n]+)",
        kit,
        re.I,
    )
    if not m:
        raise ValueError("Could not parse title tag")
    return m.group(1).strip()


def extract_meta(kit: str) -> str:
    m = re.search(
        r"## Meta description[^\n]*\n+\n?([^\n]+)",
        kit,
        re.I,
    )
    if not m:
        raise ValueError("Could not parse meta description")
    return m.group(1).strip()


def parse_faqs(body: str) -> list[tuple[str, str]]:
    for heading in ("## FAQ", "## Frequently asked questions"):
        if heading.lower() in body.lower():
            idx = body.lower().index(heading.lower())
            section = body[idx + len(heading) :]
            break
    else:
        return []

    stop = re.search(r"\n## [^#]", section)
    if stop:
        section = section[: stop.start()]

    faqs: list[tuple[str, str]] = []
    parts = re.split(r"\n### ", section)
    for part in parts[1:]:
        lines = part.strip().split("\n", 1)
        if len(lines) < 2:
            continue
        q = lines[0].strip().rstrip("?") + "?"
        a = " ".join(lines[1].split())
        faqs.append((q, a))
    return faqs


def extract_h1(article: str) -> str:
    for line in article.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No H1 in article")


def extract_tags(body: str, slug: str) -> list[str]:
    defaults = {
        "place-declined-mortgage-files-ontario": [
            "Declined Mortgage Ontario",
            "B Lender Placement",
            "Private Mortgage Broker",
            "MIC Ontario",
            "Richview Capital Brokers",
        ],
    }
    return defaults.get(
        slug,
        [
            "Private Mortgage Ontario",
            "Mortgage Brokers Ontario",
            "Richview Capital Brokers",
            "GTA Private Lending",
        ],
    )


def build_cfg(folder: str) -> dict:
    root = SEO_ROOT / folder
    kit = (root / "publishing-kit.md").read_text(encoding="utf-8")
    article_raw = (root / "article.md").read_text(encoding="utf-8")
    article = preprocess_md(article_raw)
    slug = extract_slug(kit)
    h1 = extract_h1(article_raw)
    title_tag = extract_title_tag(kit)
    description = extract_meta(kit)
    _, body = load_batch3().split_lead_and_body(article)
    faqs = parse_faqs(body)

    return {
        "slug": slug,
        "md": root / "article.md",
        "article_text": article,
        "title": f"{title_tag} | Richview Capital MIC",
        "og_title": title_tag,
        "description": description,
        "h1": h1,
        "jsonld_headline": h1,
        "breadcrumb": h1.split(":")[0] if ":" in h1 else h1[:60],
        "hero_alt": HERO_ALTS.get(slug, h1),
        "published": "2026-08-28T09:00:00-04:00",
        "post_meta": "August 2026 · Brokers · Ontario",
        "tags": extract_tags(body, slug),
        "faqs": faqs,
        "card_title": h1,
        "card_excerpt": CARD_EXCERPTS.get(slug, description),
        "image_src": BATCH4_IMAGE_MAP.get(slug),
    }


def build_article_brokers(cfg: dict, lead: str, prose_html: str) -> str:
    batch3 = load_batch3()
    html = batch3.build_article(cfg, lead, prose_html)
    html = html.replace("August 2026 · Borrowers", "August 2026 · Brokers")
    html = html.replace(
        "educational information for Ontario borrowers",
        "educational information for Ontario mortgage brokers",
    )
    html = html.replace(
        "educational information for Ontario homeowners",
        "educational information for Ontario mortgage brokers",
    )
    html = html.replace(
        '<p class="post-cta">Next steps: <a href="/borrowers/">Borrowers</a> · '
        '<a href="/borrowers/#contact-form">Speak With Our Team</a> · <a href="/faq/">FAQ</a></p>',
        '<p class="post-cta">Next steps: <a href="/brokers/">Brokers</a> · '
        '<a href="/brokers/#contact-form">Submit a Deal</a> · <a href="/faq/">FAQ</a></p>',
    )
    html = html.replace('"articleSection": "Borrowers"', '"articleSection": "Brokers"')
    return html


def build_page_brokers(shell: str, cfg: dict, lead: str, prose_html: str) -> str:
    batch3 = load_batch3()
    marker_article = '<article class="post-wrap">'
    marker_cta = '<section class="cta-section" id="contact">'
    idx_a = shell.find(marker_article)
    idx_c = shell.find(marker_cta)
    head = batch3.patch_head(shell[:idx_a].rstrip(), cfg)
    head = head.replace(
        '<meta property="article:section" content="Borrowers">',
        '<meta property="article:section" content="Brokers">',
    )
    head = re.sub(
        r'"articleSection": "Borrowers"',
        '"articleSection": "Brokers"',
        head,
    )
    return head + "\n" + build_article_brokers(cfg, lead, prose_html) + shell[idx_c:]


def blog_card_grid_brokers(cfg: dict) -> str:
    batch3 = load_batch3()
    card = batch3.blog_card_grid(cfg)
    return card.replace("August 2026 · Borrowers", "August 2026 · Brokers")


def blog_card_home_brokers(cfg: dict, index: int) -> str:
    return blog_card_grid_brokers(cfg)  # unused pattern; use batch3 home card


def main() -> int:
    batch3 = load_batch3()
    shell_path = REPO / "blog/land-financing-ontario/index.html"
    if not shell_path.is_file():
        print(f"Shell missing: {shell_path}", file=sys.stderr)
        return 1
    shell = shell_path.read_text(encoding="utf-8")

    grid_cards = ""
    home_cards = ""
    slugs: list[str] = []
    index_text = (REPO / "blog/index.html").read_text(encoding="utf-8")

    for folder in BATCH4_FOLDERS:
        try:
            cfg = build_cfg(folder)
        except Exception as exc:
            print(f"Config error for {folder}: {exc}", file=sys.stderr)
            return 1

        slug = cfg["slug"]
        out = REPO / f"blog/{slug}/index.html"
        image_src = cfg.get("image_src")
        has_source = image_src and Path(image_src).is_file()
        hero_on_disk = (REPO / f"images/blog/{slug}.jpg").is_file()

        if out.is_file() and hero_on_disk:
            print(f"Skipping /blog/{slug}/ (already published with hero)")
            continue
        if out.is_file() and not hero_on_disk and has_source:
            print(f"Updating /blog/{slug}/ with hero image")

        if has_source:
            export_hero(slug, Path(image_src))
        elif not hero_on_disk:
            print(f"Publishing /blog/{slug}/ without hero (image not in SEO Blogs folder)", file=sys.stderr)

        md_text = cfg["article_text"]
        lead, body = batch3.split_lead_and_body(md_text)
        prose_html = batch3.md_body_to_html(body)

        page = build_page_brokers(shell, cfg, lead, prose_html)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")

        if hero_on_disk or has_source:
            grid_cards += blog_card_grid_brokers(cfg)
            home_cards += batch3.blog_card_home(cfg, 0)
        elif not out.is_file():
            grid_cards += blog_card_grid_brokers(cfg)
            home_cards += batch3.blog_card_home(cfg, 0)
        slugs.append(slug)
        print(f"Published /blog/{slug}/")

    if not slugs:
        print("No new Batch 4 posts to publish.")
        return 0

    new_slugs = [s for s in slugs if f"/blog/{s}/" not in index_text]
    if new_slugs:
        cards_for_new = ""
        home_for_new = ""
        for folder in BATCH4_FOLDERS:
            cfg = build_cfg(folder)
            if cfg["slug"] in new_slugs:
                cards_for_new += blog_card_grid_brokers(cfg)
                home_for_new += batch3.blog_card_home(cfg, 0)
        if cards_for_new:
            batch3.update_blog_index(cards_for_new)
            batch3.update_homepage(home_for_new)
    batch3.update_sitemap(slugs, "2026-08-28")
    print("Updated blog index, homepage carousel, and sitemap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
