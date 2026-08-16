#!/usr/bin/env python3
"""Publish Richview SEO Batch 3 (first 3 articles) from client markdown + hero images."""

from __future__ import annotations

import json
import re
import shutil
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEO_ROOT = Path("/Users/ali/Downloads/SEO Blogs")
BATCH_ROOT = SEO_ROOT / "Richview-SEO-Batch3-Aug2026"
SHELL_PATH = REPO / "blog/land-financing-ontario/index.html"
BASE_URL = "https://richviewcapitalmic.com"
UL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'
OL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'

BLOGS = [
    {
        "slug": "private-mortgage-rates-ontario",
        "md": BATCH_ROOT
        / "richview-capital-private-mortgage-rates-fees-ontario-20260816"
        / "Private Mortgage Rates in Ontario- What a Private Mortgage Really Costs in 2026.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28.jpeg",
        "title": "Private Mortgage Rates Ontario: True 2026 Costs & Fees | Richview Capital MIC",
        "og_title": "Private Mortgage Rates Ontario: True 2026 Costs & Fees",
        "description": (
            "Private mortgage rates in Ontario run higher than bank rates, and fees add more. "
            "See real 2026 costs, how pricing is set, and how to compare offers."
        ),
        "h1": "Private mortgage rates in Ontario: what a private mortgage really costs in 2026",
        "jsonld_headline": "Private Mortgage Rates in Ontario: What a Private Mortgage Really Costs in 2026",
        "breadcrumb": "Private Mortgage Rates in Ontario",
        "hero_alt": (
            "Private mortgage rates in Ontario — calculator, financial documents, and model house, "
            "Richview Capital 2026 cost guide"
        ),
        "published": "2026-08-16T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "Private Mortgage Rates Ontario",
            "Private Mortgage Fees",
            "Private Lender Rates 2026",
            "Ontario APR Comparison",
            "Second Mortgage Costs",
            "Richview Capital Borrowers",
            "Private Mortgage Cost",
            "FSRA Private Lending",
        ],
        "faqs": [
            (
                "What is the average private mortgage rate in Ontario in 2026?",
                "Most private first mortgages in Ontario are priced between 7 and 10 percent, and most second mortgages between 9 and 14 percent, depending on loan-to-value, property, and exit strategy. That compares with bank rates around 4 to 5 percent with the Bank of Canada policy rate at 2.25 percent.",
            ),
            (
                "How much are private mortgage fees in total?",
                "Budget roughly 3 to 6 percent of the loan amount in first-year fees: a lender fee of 1 to 3 percent, a broker fee of 1 to 2 percent, plus legal, appraisal, and registration costs that typically total $3,000 to $5,000 on a standard residential file.",
            ),
            (
                "Why do I pay the broker on a private mortgage?",
                "Private lenders generally do not pay brokers the finder's fees that banks do, so the borrower pays the brokerage directly, usually 1 to 2 percent of the loan. The fee must be disclosed in writing before closing under Ontario's mortgage brokering rules.",
            ),
            (
                "What does it cost to renew a private mortgage?",
                "Many lenders charge a renewal or extension fee of 1 to 2 percent of the balance to extend the term, sometimes with a rate adjustment. If your exit plan may take longer than a year, ask for the renewal fee and renewal rate in the commitment letter before you sign.",
            ),
            (
                "Is private mortgage interest tax deductible?",
                "Only when the borrowed money is used to earn income, such as funding a rental property or a business, under the same interest-deductibility rules as any loan. Interest on a private mortgage used for personal purposes is generally not deductible, and you should confirm your situation with an accountant.",
            ),
            (
                "Can I negotiate private mortgage rates and fees?",
                "Yes, within limits. Lender fees, broker fees, and renewal terms are all negotiable, and lowering your requested loan-to-value is the strongest lever on rate. Competing written quotes, compared on APR, give you the most leverage.",
            ),
        ],
        "card_title": "Private mortgage rates in Ontario: what a private mortgage really costs in 2026",
        "card_excerpt": "Real 2026 rate ranges, every fee line item, APR comparisons, and red flags in private mortgage pricing.",
    },
    {
        "slug": "mortgage-after-consumer-proposal-ontario",
        "md": BATCH_ROOT
        / "richview-capital-consumer-proposal-mortgage-ontario-20260816"
        / "Getting a Mortgage After a Consumer Proposal in Ontario.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (1).jpeg",
        "title": "Mortgage After a Consumer Proposal in Ontario: Full Guide | Richview Capital MIC",
        "og_title": "Mortgage After a Consumer Proposal in Ontario: Full Guide",
        "description": (
            "Yes, you can get a mortgage after a consumer proposal in Ontario. Timelines, "
            "A, B and private lender paths, and using equity to pay it out early."
        ),
        "h1": "Getting a mortgage after a consumer proposal in Ontario",
        "jsonld_headline": "Getting a Mortgage After a Consumer Proposal in Ontario",
        "breadcrumb": "Mortgage After a Consumer Proposal in Ontario",
        "hero_alt": (
            "Approved mortgage application after a consumer proposal in Ontario — "
            "Richview Capital guide to rebuilding approval"
        ),
        "published": "2026-08-16T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "Mortgage After Consumer Proposal",
            "Consumer Proposal Ontario",
            "Private Mortgage Proposal",
            "Equity Payout Proposal",
            "Bad Credit Mortgage Ontario",
            "B Lender Ontario",
            "Debt Consolidation Mortgage",
            "Richview Capital Borrowers",
        ],
        "faqs": [
            (
                "How soon after a consumer proposal can I get a mortgage in Ontario?",
                "With 20 percent or more down or equivalent equity, B lenders can approve you at or shortly after completion, and private lenders even sooner. For an insured bank mortgage with less than 20 percent down, plan on completing the proposal plus about two years of re-established credit.",
            ),
            (
                "Can I get a mortgage while still in a consumer proposal?",
                "Yes, mainly through private and equity-based lenders, and occasionally B lenders after a year or more of clean proposal payments. Most lenders will require the proposal to be paid out from the mortgage proceeds at closing.",
            ),
            (
                "Does paying off a consumer proposal early help me get a mortgage sooner?",
                "Usually, yes. Credit bureaus remove a proposal three years after completion or six years after filing, whichever comes first, so completing early starts that clock sooner. Early completion also ends the R7 status and frees up the monthly payment for other obligations.",
            ),
            (
                "How much down payment do I need after a consumer proposal?",
                "For an insured mortgage, as little as 5 percent, but only once you meet the roughly two years of re-established credit that insurers expect. Before that, plan on at least 20 percent for B lenders and 25 to 35 percent for private lenders.",
            ),
            (
                "Will my bank renew my mortgage during a consumer proposal?",
                "In most cases yes, because your mortgage was not part of the proposal. If your payments are current, existing lenders typically offer renewal without requalification, though moving to a new lender at renewal means a full application where the proposal will count.",
            ),
            (
                "What credit score do I need for a mortgage after a consumer proposal?",
                "Private lenders are score-flexible because they lend on equity. B lenders generally look for scores from the low 600s alongside clean post-filing history, while insured bank mortgages typically become realistic around 680 or higher with two years of rebuilt credit.",
            ),
        ],
        "card_title": "Getting a mortgage after a consumer proposal in Ontario",
        "card_excerpt": "Timelines, A/B/private lender paths, early equity payout strategy, and credit rebuilding after a proposal.",
    },
    {
        "slug": "home-renovation-financing-ontario",
        "md": BATCH_ROOT
        / "richview-capital-renovation-financing-ontario-20260816"
        / "Home Renovation Financing in Ontario- Every Option Compared.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (2).jpeg",
        "title": "Home Renovation Financing Ontario: Options Compared | Richview Capital MIC",
        "og_title": "Home Renovation Financing Ontario: Options Compared",
        "description": (
            "Compare every home renovation financing option in Ontario: HELOCs, refinancing, "
            "second mortgages, private loans and 2026 programs, with real numbers."
        ),
        "h1": "Home renovation financing in Ontario: every option compared",
        "jsonld_headline": "Home Renovation Financing in Ontario: Every Option Compared",
        "breadcrumb": "Home Renovation Financing in Ontario",
        "hero_alt": (
            "Kitchen renovation in progress in Ontario with plans and paint swatches — "
            "home renovation financing options compared"
        ),
        "published": "2026-08-16T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "Home Renovation Financing Ontario",
            "Renovation Loan Ontario",
            "HELOC Renovation",
            "Private Renovation Loan",
            "Secondary Suite Loan Program",
            "Home Equity Renovation",
            "Richview Capital Borrowers",
            "Ontario Renovation Costs 2026",
        ],
        "faqs": [
            (
                "How much can I borrow against my home for renovations in Ontario?",
                "Most lenders allow total secured borrowing up to 80 percent of your home's appraised value, minus your current mortgage balance. On a $900,000 home with a $550,000 mortgage, that leaves up to $170,000 in accessible equity. HELOCs specifically cap the revolving portion at 65 percent of value.",
            ),
            (
                "What credit score do I need for a renovation loan in Ontario?",
                "Banks generally look for scores of roughly 650 to 680 or higher, along with provable income that keeps debt-service ratios inside their limits. Private and alternative lenders qualify primarily on your equity, so meaningful credit issues do not automatically end your options.",
            ),
            (
                "Can I get renovation financing if I am self-employed or have bad credit?",
                "Yes. Private lenders and mortgage investment corporations underwrite on the property's equity and value rather than pay stubs and credit scores, typically at 8 to 12 percent plus fees. These loans work best as one-to-two-year bridges with a planned refinance or sale as the exit.",
            ),
            (
                "Is a HELOC or a refinance cheaper for a renovation?",
                "A refinance usually carries the lower rate, but breaking a fixed mortgage mid-term can trigger a penalty that erases the savings. A HELOC costs slightly more, charges interest only on what you draw, and leaves your existing mortgage untouched. At renewal, refinancing tends to win; mid-term, the HELOC often does.",
            ),
            (
                "Is the Canada Greener Homes Loan still available?",
                "No. The interest-free Greener Homes Loan closed to new applications on October 1, 2025, and the Greener Homes Grant closed in 2024. Current options include the Canada Secondary Suite Loan Program, up to $80,000 at 2 percent for legal secondary suites, and Ontario's Home Renovation Savings Program rebates.",
            ),
            (
                "How fast can I get renovation financing?",
                "Unsecured loans and credit lines can fund within days. HELOCs and refinances typically take two to six weeks because they require an appraisal, underwriting, and legal registration. Private renovation loans are the fastest secured option and can close in as little as a few days when equity is clear.",
            ),
        ],
        "card_title": "Home renovation financing in Ontario: every option compared",
        "card_excerpt": "HELOCs, refinances, second mortgages, private loans, and 2026 government programs with real cost comparisons.",
    },
]


def normalize_url(url: str) -> tuple[str, bool]:
    """Return (href, is_external). Internal Richview URLs become root-relative paths."""
    for prefix in ("https://www.richviewcapital.com", "https://richviewcapital.com", BASE_URL):
        if url.startswith(prefix):
            path = url[len(prefix) :] or "/"
            if not path.startswith("/"):
                path = "/" + path
            if path.rstrip("/").endswith("/contact"):
                return "/borrowers/#contact-form", False
            return path, False
    if url.startswith("http://") or url.startswith("https://"):
        return url, True
    if url.startswith("/"):
        return url, False
    return url, True


def inline_md(text: str) -> str:
    out: list[str] = []
    pos = 0
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*")
    for match in pattern.finditer(text):
        out.append(escape(text[pos : match.start()]))
        if match.group(1) is not None:
            href, external = normalize_url(match.group(2))
            attrs = ' rel="noopener noreferrer" target="_blank"' if external else ""
            out.append(
                f'<a href="{escape(href, quote=True)}"{attrs}>'
                f"{escape(match.group(1))}</a>"
            )
        else:
            out.append(f"<strong>{escape(match.group(3))}</strong>")
        pos = match.end()
    out.append(escape(text[pos:]))
    return "".join(out)


def is_table_sep(line: str) -> bool:
    return bool(re.match(r"^\|[\s\-:|]+\|$", line.strip()))


def parse_table_row(line: str) -> list[str]:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def md_body_to_html(body: str) -> str:
    lines = body.splitlines()
    html_parts: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("# "):
            i += 1
            continue

        if stripped.startswith("## "):
            html_parts.append(f"  <h2>{inline_md(stripped[3:])}</h2>")
            i += 1
            continue

        if stripped.startswith("### "):
            html_parts.append(f"  <h3>{inline_md(stripped[4:])}</h3>")
            i += 1
            continue

        if re.match(r"^\*\*.+\*\*$", stripped):
            html_parts.append(f"  <h3>{inline_md(stripped[2:-2])}</h3>")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_sep(lines[i + 1]):
            rows: list[list[str]] = [parse_table_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(parse_table_row(lines[i].strip()))
                i += 1
            html_parts.append('  <div class="post-table-wrap">')
            html_parts.append("    <table>")
            html_parts.append("      <thead>")
            html_parts.append("        <tr>" + "".join(f"<th>{inline_md(c)}</th>" for c in rows[0]) + "</tr>")
            html_parts.append("      </thead>")
            html_parts.append("      <tbody>")
            for row in rows[1:]:
                html_parts.append("        <tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in row) + "</tr>")
            html_parts.append("      </tbody>")
            html_parts.append("    </table>")
            html_parts.append("  </div>")
            continue

        if re.match(r"^[-*]\s+", stripped):
            items: list[str] = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(inline_md(lines[i].strip()[2:].strip()))
                i += 1
            html_parts.append(f"  <ul {UL_STYLE}>")
            for item in items:
                html_parts.append(f"    <li>{item}</li>")
            html_parts.append("  </ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(inline_md(re.sub(r"^\d+\.\s+", "", lines[i].strip())))
                i += 1
            html_parts.append(f"  <ol {OL_STYLE}>")
            for item in items:
                html_parts.append(f"    <li>{item}</li>")
            html_parts.append("  </ol>")
            continue

        para_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt.startswith("#")
                or nxt.startswith("|")
                or re.match(r"^[-*]\s+", nxt)
                or re.match(r"^\d+\.\s+", nxt)
                or re.match(r"^\*\*.+\*\*$", nxt)
            ):
                break
            para_lines.append(nxt)
            i += 1
        html_parts.append(f"  <p>{inline_md(' '.join(para_lines))}</p>")

    return "\n".join(html_parts)


def split_lead_and_body(md_text: str) -> tuple[str, str]:
    lines = md_text.splitlines()
    title_idx = 0
    while title_idx < len(lines) and not lines[title_idx].strip().startswith("# "):
        title_idx += 1
    i = title_idx + 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    lead_lines: list[str] = []
    while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("## "):
        lead_lines.append(lines[i].strip())
        i += 1
    lead = " ".join(lead_lines)
    body = "\n".join(lines[i:])
    return lead, body


def build_json_ld(cfg: dict) -> str:
    page_url = f"{BASE_URL}/blog/{cfg['slug']}/"
    image_url = f"{BASE_URL}/images/blog/{cfg['slug']}.jpg"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": cfg["jsonld_headline"],
                "description": cfg["description"],
                "image": image_url,
                "author": {"@type": "Organization", "name": "Richview Capital MIC", "url": f"{BASE_URL}/"},
                "publisher": {
                    "@type": "Organization",
                    "name": "Richview Capital MIC",
                    "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/images/logo.png"},
                },
                "datePublished": cfg["published"],
                "dateModified": cfg["published"],
                "articleSection": "Borrowers",
                "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/blog/"},
                    {"@type": "ListItem", "position": 3, "name": cfg["breadcrumb"], "item": page_url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in cfg["faqs"]
                ],
            },
        ],
    }
    return (
        '    <script type="application/ld+json">\n'
        + json.dumps(graph, indent=2, ensure_ascii=False)
        + "\n    </script>"
    )


def build_head(cfg: dict) -> str:
    page_url = f"{BASE_URL}/blog/{cfg['slug']}/"
    image_url = f"{BASE_URL}/images/blog/{cfg['slug']}.jpg"
    tags = "\n".join(
        f'    <meta property="article:tag" content="{escape(t, quote=True)}">' for t in cfg["tags"][:4]
    )
    return f"""    <title>{escape(cfg['title'])}</title>
    <meta name="description" content="{escape(cfg['description'], quote=True)}">
    <link rel="icon" href="/images/logo.png" type="image/png">
    <meta name="theme-color" content="#0B1635">
    <!-- Meta Pixel -->
    <script src="/js/meta-pixel.js"></script>
    <script src="/js/google-tags.js"></script>
    <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=3033942923462161&ev=PageView&noscript=1" alt="" /></noscript>
    <link rel="canonical" href="{page_url}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape(cfg['og_title'], quote=True)}">
    <meta property="og:description" content="{escape(cfg['description'], quote=True)}">
    <meta property="og:url" content="{page_url}">
    <meta property="og:site_name" content="Richview Capital MIC">
    <meta property="og:locale" content="en_CA">
    <meta property="og:image" content="{image_url}">
    <meta property="og:image:width" content="1280">
    <meta property="og:image:height" content="702">
    <meta property="og:image:alt" content="{escape(cfg['hero_alt'], quote=True)}">
    <meta property="article:published_time" content="{cfg['published']}">
    <meta property="article:modified_time" content="{cfg['published']}">
    <meta property="article:author" content="Richview Capital MIC">
    <meta property="article:section" content="Borrowers">
{tags}
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(cfg['og_title'], quote=True)}">
    <meta name="twitter:description" content="{escape(cfg['description'], quote=True)}">
    <meta name="twitter:image" content="{image_url}">
    <meta name="twitter:image:alt" content="{escape(cfg['hero_alt'], quote=True)}">
{build_json_ld(cfg)}"""


def patch_head(shell: str, cfg: dict) -> str:
    start = shell.find("    <title>")
    end = shell.find('<link rel="preconnect"')
    if start == -1 or end == -1:
        raise ValueError("Could not locate head block in shell")
    return shell[:start] + build_head(cfg) + "\n" + shell[end:]


def build_article(cfg: dict, lead: str, prose_html: str) -> str:
    slug = cfg["slug"]
    tags_html = "\n".join(f"    <li>{escape(t)}</li>" for t in cfg["tags"])
    image_path = f"/images/blog/{slug}.jpg"
    return f"""        <article class="post-wrap">
            <div class="container">
                <a href="/blog/" class="post-back"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> Back to Blog</a>
                <p class="post-meta">{escape(cfg['post_meta'])}</p>
                <h1 class="post-title">{escape(cfg['h1'])}</h1>

                <figure class="post-hero-figure post-hero-figure--object-contain" aria-label="Article hero image">
                    <img src="{image_path}" width="1280" height="702" alt="{escape(cfg['hero_alt'], quote=True)}" loading="eager" decoding="async">
                </figure>
                <p class="post-lead">{escape(lead)}</p>
                <div class="post-prose">
{prose_html}

  <ul class="post-tags">
{tags_html}
  </ul>

  <p class="post-byline"><strong>Richview Capital MIC</strong> is a licensed Mortgage Investment Corporation (Mortgage Administrator License #13171). This article is educational information for Ontario borrowers — not legal, financial, or tax advice. See <a href="/about-us/">About</a> and <a href="/disclaimer/">Disclaimer</a>.</p>
                </div>
                <p class="post-cta">Next steps: <a href="/borrowers/">Borrowers</a> · <a href="/borrowers/#contact-form">Speak With Our Team</a> · <a href="/faq/">FAQ</a></p>
                <p class="post-disclaimer">Richview Capital MIC is a licensed Mortgage Investment Corporation (Mortgage Administrator License #13171). This article is educational information for Ontario homeowners, not legal, financial, or tax advice. Rates, fees, LTV limits, and approvals vary by file and underwriting, and published ranges are subject to change and are not an offer of credit.</p>
            </div>
        </article>

"""


def build_page(shell: str, cfg: dict, lead: str, prose_html: str) -> str:
    marker_article = '<article class="post-wrap">'
    marker_cta = '<section class="cta-section" id="contact">'
    idx_a = shell.find(marker_article)
    idx_c = shell.find(marker_cta)
    if idx_a == -1 or idx_c == -1:
        raise ValueError("Shell markers not found")
    return patch_head(shell[:idx_a].rstrip(), cfg) + "\n" + build_article(cfg, lead, prose_html) + shell[idx_c:]


def blog_card_grid(cfg: dict) -> str:
    slug = cfg["slug"]
    return f"""                    <article class="blog-card reveal">
                        <div class="blog-card-image blog-card-image--object-contain">
                            <a href="/blog/{slug}/" aria-hidden="true" tabindex="-1"><img src="/images/blog/{slug}.jpg" width="1280" height="702" alt="" loading="lazy"></a>
                        </div>
                        <div class="blog-card-body">
                            <span class="blog-card-meta">August 2026 · Borrowers</span>
                            <h3 class="blog-card-title"><a href="/blog/{slug}/">{escape(cfg['card_title'])}</a>
                            </h3>
                            <p class="blog-card-excerpt">{escape(cfg['card_excerpt'])}</p>
                            <a href="/blog/{slug}/" class="blog-card-link">Read article <svg viewBox="0 0 24 24" fill="none"
                                    stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <line x1="5" y1="12" x2="19" y2="12" />
                                    <polyline points="12 5 19 12 12 19" />
                                </svg></a>
                        </div>
                    </article>

"""


def blog_card_home(cfg: dict, index: int) -> str:
    slug = cfg["slug"]
    title = escape(cfg["card_title"])
    excerpt = escape(cfg["card_excerpt"])
    return f"""                    <article class="blog-card reveal" style="--i: {index};">
                        <a href="/blog/{slug}/" class="blog-card-thumb blog-card-thumb--object-contain" aria-label="Read: {title}">
                            <img src="/images/blog/{slug}.jpg" alt="" width="120" height="66" sizes="(max-width: 480px) 45vw, 190px" loading="lazy" decoding="async">
                        </a>
                        <div class="blog-card-body">
                            <span class="blog-date">August 2026</span>
                            <h3><a href="/blog/{slug}/">{title}</a></h3>
                            <p class="blog-excerpt">{excerpt}</p>
                            <a href="/blog/{slug}/" class="blog-link">Read <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
                        </div>
                    </article>

"""


def sitemap_entry(slug: str) -> str:
    return f"""  <url>
    <loc>{BASE_URL}/blog/{slug}/</loc>
    <lastmod>2026-08-16</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""


def update_blog_index(cards_html: str) -> None:
    path = REPO / "blog/index.html"
    text = path.read_text(encoding="utf-8")
    marker = '<div class="blog-grid">'
    insert_at = text.find(marker)
    if insert_at == -1:
        raise ValueError("blog-grid not found")
    insert_at = text.find("\n", insert_at) + 1
    path.write_text(text[:insert_at] + cards_html + text[insert_at:], encoding="utf-8")


def update_homepage(cards_html: str) -> None:
    path = REPO / "index.html"
    text = path.read_text(encoding="utf-8")
    marker = '<div class="blog-track">'
    idx = text.find(marker)
    if idx == -1:
        raise ValueError("blog-track not found")
    insert_at = text.find("\n", idx) + 1
    text = text[:insert_at] + cards_html + text[insert_at:]
    dup_marker = "<!-- Duplicate set for seamless loop -->"
    dup_idx = text.find(dup_marker)
    if dup_idx == -1:
        raise ValueError("duplicate set marker not found")
    insert_at = text.find("\n", dup_idx) + 1
    text = text[:insert_at] + cards_html + text[insert_at:]
    path.write_text(text, encoding="utf-8")


def update_sitemap(slugs: list[str]) -> None:
    path = REPO / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    blog_idx = text.find("<loc>https://richviewcapitalmic.com/blog/</loc>")
    if blog_idx == -1:
        raise ValueError("blog index url not found in sitemap")
    insert_at = text.find("</url>", blog_idx) + len("</url>")
    insert_at = text.find("\n", insert_at) + 1
    entries = "".join(sitemap_entry(s) for s in slugs)
    text = text[:insert_at] + entries + text[insert_at:]
    text = text.replace(
        "<lastmod>2026-07-12</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.85</priority>\n  </url>\n  <url>\n    <loc>https://richviewcapitalmic.com/blog/land-financing-ontario/",
        "<lastmod>2026-08-16</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.85</priority>\n  </url>\n  <url>\n    <loc>https://richviewcapitalmic.com/blog/land-financing-ontario/",
        1,
    )
    path.write_text(text, encoding="utf-8")


def main() -> int:
    if not SHELL_PATH.is_file():
        print(f"Shell missing: {SHELL_PATH}", file=sys.stderr)
        return 1
    shell = SHELL_PATH.read_text(encoding="utf-8")

    grid_cards = ""
    home_cards = ""
    slugs: list[str] = []
    index_text = (REPO / "blog/index.html").read_text(encoding="utf-8")

    for i, cfg in enumerate(BLOGS):
        if not cfg["md"].is_file():
            print(f"Markdown missing: {cfg['md']}", file=sys.stderr)
            return 1
        if not cfg["image_src"].is_file():
            print(f"Image missing: {cfg['image_src']}", file=sys.stderr)
            return 1

        md_text = cfg["md"].read_text(encoding="utf-8")
        lead, body = split_lead_and_body(md_text)
        prose_html = md_body_to_html(body)

        page = build_page(shell, cfg, lead, prose_html)
        out = REPO / f"blog/{cfg['slug']}/index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")

        img_out = REPO / f"images/blog/{cfg['slug']}.jpg"
        img_out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cfg["image_src"], img_out)

        grid_cards += blog_card_grid(cfg)
        home_cards += blog_card_home(cfg, i)
        slugs.append(cfg["slug"])
        print(f"Published /blog/{cfg['slug']}/")

    if f"/blog/{BLOGS[0]['slug']}/" not in index_text:
        update_blog_index(grid_cards)
    else:
        print("Blog index already lists batch 3 posts; skipping index update.")
    update_homepage(home_cards)
    update_sitemap(slugs)
    print("Updated blog index, homepage carousel, and sitemap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
