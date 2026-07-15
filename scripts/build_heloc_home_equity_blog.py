#!/usr/bin/env python3
"""Generate blog/heloc-home-equity-loan-gta/index.html from shell + article data."""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHELL_PATH = REPO / "blog/self-employed-mortgage-gta/index.html"
OUTPUT_PATH = REPO / "blog/heloc-home-equity-loan-gta/index.html"

SLUG = "heloc-home-equity-loan-gta"
BASE_URL = "https://richviewcapitalmic.com"
PAGE_URL = f"{BASE_URL}/blog/{SLUG}/"
IMAGE_URL = f"{BASE_URL}/images/blog/{SLUG}.jpg"
IMAGE_PATH = f"/images/blog/{SLUG}.jpg"
PUBLISHED = "2026-06-25T09:00:00-04:00"

TITLE = "HELOC & Home Equity Loans in the GTA: When the Bank Says No | Richview Capital MIC"
OG_TITLE = "HELOC & Home Equity Loans in the GTA: When the Bank Says No"
DESCRIPTION = (
    "HELOC vs home equity loan vs second mortgage in the GTA: how each works, what it costs in 2026, "
    "and your options when the bank freezes or declines you."
)
H1 = "HELOC and home equity loans in the GTA: how to tap your equity (even if the bank says no)"
JSONLD_HEADLINE = (
    "HELOC and Home Equity Loans in the GTA: How to Tap Your Equity (Even If the Bank Says No)"
)
HERO_ALT = "GTA homeowner comparing HELOC and home equity loan options at home"
POST_LEAD = (
    "HELOC vs home equity loan vs second mortgage in the GTA: how each works, how much you can borrow, "
    "what it costs in 2026, and equity-based options when the bank declines you."
)

UL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'

FCAC_URL = "https://www.canada.ca/en/financial-consumer-agency/services/mortgages/home-equity-line-credit.html"
OSFI_URL = "https://www.osfi-bsif.gc.ca/en/supervision/financial-institutions/banks/minimum-qualifying-rate-uninsured-mortgages"
TRREB_URL = "https://trreb.ca/market-data/market-watch/"
WOWA_URL = "https://wowa.ca/banks/prime-rates-canada"

FAQS: list[tuple[str, str]] = [
    (
        "HELOC vs home equity loan: which is better?",
        "Neither is universally better. A HELOC suits ongoing or uncertain needs and lets you draw and repay repeatedly at a variable rate. A home equity loan suits a one-time, known amount and usually offers a fixed rate and fixed payments. Choose based on whether your need is recurring or a single sum.",
    ),
    (
        "How much equity do I need for a HELOC or home equity loan?",
        "Banks generally want you to keep at least 20% equity, with a HELOC capped at 65% of value and combined borrowing capped at 80%. At Richview, private HELOC and home equity products are available up to 75% LTV (case by case).",
    ),
    (
        "Can I get a home equity loan with bad credit or no income proof?",
        "Often yes, through a private or MIC lender, because approval rests on your equity and property rather than on credit and income. You will pay a higher rate than a bank charges, and you should have a repayment or refinance plan.",
    ),
    (
        "Why did my bank freeze or decline my HELOC?",
        "Usually because of the stress test, income verification, high debt ratios, a credit change, or a tightening of the bank's own limits, not because your equity disappeared. Equity is necessary at a bank, but it is not enough on its own.",
    ),
    (
        "What does a home equity loan cost in the GTA?",
        "A bank HELOC is typically prime plus half to one point (about 5% to 6% at a June 2026 prime of 4.45%). A private home equity loan or second mortgage at Richview starts from 8.99% plus a one-time lender fee, with legal and appraisal costs on top.",
    ),
    (
        "Is my home at risk with a HELOC or home equity loan?",
        "Any loan secured by your home, bank or private, can put the property at risk if you fall behind. That is why a clear, realistic repayment plan matters more than the rate alone.",
    ),
]

ARTICLE_TAGS = [
    "HELOC Ontario",
    "Home Equity Loan GTA",
    "HELOC vs Home Equity Loan",
    "HELOC Bad Credit Ontario",
    "Private HELOC Lender",
    "Home Equity Line of Credit GTA",
    "Second Mortgage Ontario",
    "Equity-Based Lending",
    "Richview Capital Borrowers",
    "GTA Home Equity 2026",
]


def build_json_ld() -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": JSONLD_HEADLINE,
                "description": (
                    "HELOC vs home equity loan vs second mortgage in the GTA: how each works, "
                    "how much you can borrow, what it costs in 2026, and equity-based options when the bank declines you."
                ),
                "image": IMAGE_URL,
                "author": {
                    "@type": "Organization",
                    "name": "Richview Capital MIC",
                    "url": f"{BASE_URL}/",
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Richview Capital MIC",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{BASE_URL}/images/logo.png",
                    },
                },
                "datePublished": PUBLISHED,
                "dateModified": PUBLISHED,
                "articleSection": "Borrowers",
                "about": [
                    "HELOC",
                    "Home equity loan",
                    "Second mortgage",
                    "Mortgage Investment Corporation",
                    "Greater Toronto Area",
                ],
                "mainEntityOfPage": {"@type": "WebPage", "@id": PAGE_URL},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/blog/"},
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": "HELOC and Home Equity Loans in the GTA",
                        "item": PAGE_URL,
                    },
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
                    for q, a in FAQS
                ],
            },
        ],
    }
    return (
        '    <script type="application/ld+json">\n'
        + json.dumps(graph, indent=2, ensure_ascii=False)
        + "\n    </script>"
    )


def build_head_meta_block() -> str:
    tags = [
        "HELOC Ontario",
        "home equity loan GTA",
        "HELOC vs home equity loan",
        "private HELOC lender",
    ]
    article_tags = "\n".join(
        f'    <meta property="article:tag" content="{escape(t, quote=True)}">' for t in tags
    )
    return f"""    <title>{escape(TITLE)}</title>
    <meta name="description" content="{escape(DESCRIPTION, quote=True)}">
    <link rel="icon" href="/images/logo.png" type="image/png">
    <meta name="theme-color" content="#0B1635">
    <!-- Meta Pixel -->
    <script src="/js/meta-pixel.js"></script>
    <script src="/js/google-tags.js"></script>
    <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=3033942923462161&ev=PageView&noscript=1" alt="" /></noscript>
    <link rel="canonical" href="{PAGE_URL}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape(OG_TITLE, quote=True)}">
    <meta property="og:description" content="{escape(DESCRIPTION, quote=True)}">
    <meta property="og:url" content="{PAGE_URL}">
    <meta property="og:site_name" content="Richview Capital MIC">
    <meta property="og:locale" content="en_CA">
    <meta property="og:image" content="{IMAGE_URL}">
    <meta property="og:image:width" content="1024">
    <meta property="og:image:height" content="682">
    <meta property="og:image:alt" content="{escape(HERO_ALT, quote=True)}">
    <meta property="article:published_time" content="{PUBLISHED}">
    <meta property="article:modified_time" content="{PUBLISHED}">
    <meta property="article:author" content="Richview Capital MIC">
    <meta property="article:section" content="Borrowers">
{article_tags}
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(OG_TITLE, quote=True)}">
    <meta name="twitter:description" content="{escape(DESCRIPTION, quote=True)}">
    <meta name="twitter:image" content="{IMAGE_URL}">
    <meta name="twitter:image:alt" content="{escape(HERO_ALT, quote=True)}">
{build_json_ld()}"""


def patch_head(shell: str) -> str:
    start = shell.find("    <title>")
    end = shell.find('<link rel="preconnect"')
    if start == -1 or end == -1:
        raise ValueError("Could not locate head meta block in shell")
    return shell[:start] + build_head_meta_block() + "\n" + shell[end:]


def build_faq_html() -> str:
    parts = ["  <h2>FAQ</h2>"]
    for question, answer in FAQS:
        parts.append(f"  <h3>{escape(question)}</h3>")
        parts.append(f"  <p>{escape(answer)}</p>")
    return "\n".join(parts)


def build_post_prose() -> str:
    faq_html = build_faq_html()
    tags_html = "\n".join(f"    <li>{tag}</li>" for tag in ARTICLE_TAGS)
    return f"""<p class="post-lead-em">If you own a home in the Greater Toronto Area, you are probably sitting on more equity than you realize, and far less access to it than you expected. A <span class="key-term">HELOC or home equity loan in the GTA</span> lets you borrow against the value you have built without selling, but the products are easy to confuse and the approval rules trip up plenty of owners who clearly have the equity.</p>

  <p>This guide explains the three main ways to tap your equity, what each costs in 2026, why banks decline people who look qualified on paper, and what your options are when the bank freezes or says no.</p>

  <h2>The three ways to tap home equity, and how they differ</h2>
  <p>Most GTA homeowners are choosing among three tools. They all borrow against your home, but they behave differently.</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Product</th><th>How it works</th><th>Best when</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>HELOC</strong></td><td>Revolving credit secured by your home; draw, repay, and reborrow at a variable rate tied to prime</td><td>Ongoing or uncertain needs: phased renovations, cash-flow cushion, staggered tuition</td></tr>
        <tr><td><strong>Home equity loan</strong></td><td>Single lump sum, often at a fixed rate, repaid over a set term with no reborrowing</td><td>One-time, known need: debt consolidation, tax bill, single large project</td></tr>
        <tr><td><strong>Second mortgage</strong></td><td>Lump sum registered behind your existing first mortgage; on the private side, equity-based</td><td>Bank product out of reach; approval driven by equity and combined LTV</td></tr>
      </tbody>
    </table>
  </div>

  <h3>HELOC (home equity line of credit)</h3>
  <p>A HELOC is revolving credit secured by your home, much like a credit card with your house behind it. You are approved for a limit, draw what you need, pay interest only on the balance you have used, and can repay and reborrow. Rates are almost always variable, tied to prime, so your payment moves when rates move.</p>

  <h3>Home equity loan</h3>
  <p>A home equity loan gives you a single lump sum, often at a fixed rate, repaid over a set term. There is no reborrowing once it is paid down. The fixed structure also imposes useful discipline if you are rebuilding your finances.</p>

  <h3>Second mortgage</h3>
  <p>A second mortgage is a lump sum registered behind your existing first mortgage. On the private side it is equity-based, which makes it the practical route when a bank product is out of reach. It is worth understanding <a href="/blog/second-mortgage-ontario/">how second mortgages are priced and qualified in Ontario</a> before choosing this path, since position and combined loan-to-value drive the rate.</p>

  <h2>How much you can borrow against a GTA home</h2>
  <p>How much you can pull out depends on your equity and on the lender&apos;s <span class="key-term">loan-to-value (LTV)</span> limits.</p>
  <p>At a federally regulated bank, a HELOC is generally capped at 65% of your home&apos;s value, and your HELOC plus your mortgage together cannot exceed 80% of the home&apos;s value, according to the <a href="{FCAC_URL}" rel="noopener noreferrer" target="_blank">Financial Consumer Agency of Canada</a>. Private lenders like Richview work on equity rather than those federal caps, with published products up to 75% LTV (case by case) on HELOC and home equity loans.</p>
  <p>The GTA&apos;s high values make this meaningful. The average GTA selling price was about $1.07 million in May 2026, per the <a href="{TRREB_URL}" rel="noopener noreferrer" target="_blank">Toronto Regional Real Estate Board</a>. Take a home worth $1.1 million with a $500,000 mortgage. At the bank&apos;s 80% combined ceiling, total borrowing can reach $880,000, which leaves roughly $380,000 of room above your existing mortgage. That is a large amount of accessible equity, assuming you also meet the income and credit tests, which is where many owners get stuck.</p>

  <h2>What it costs in 2026: rates and fees</h2>
  <p>Cost rises as you move from a bank to a private lender, and that trade-off is the heart of the decision.</p>
  <p>A bank HELOC is tied to prime, commonly prime plus half a point to a full point. With the prime rate at 4.45% as of June 2026 (the Bank of Canada held its policy rate at 2.25% that month, per <a href="{WOWA_URL}" rel="noopener noreferrer" target="_blank">WOWA</a>), that puts most bank HELOCs in roughly the 5% to 6% range. A private home equity loan or second mortgage generally runs from about 8.99%, plus a one-time lender fee and the usual legal and appraisal costs. You pay more on the private side, and in exchange you get approval based on equity rather than on income and credit.</p>
  <p>To make it concrete, take that $380,000 of available room and assume you draw $200,000. At a bank HELOC rate of 5.5%, interest-only carrying cost is about <strong>$917 a month</strong>. Through a private home equity loan at 8.99%, the same $200,000 would carry at about <strong>$1,498 a month</strong>, plus a one-time fee in the range of 1% to 3%. Those figures are illustrative, not a quote; your actual numbers depend on the property, your equity, and the lender. The point is that the private route costs more but stays available when the bank&apos;s does not.</p>

  <h2>Why banks decline homeowners who clearly have equity</h2>
  <p>This is the part that surprises people. You can have hundreds of thousands of dollars of equity and still be turned down, because at a bank, equity is necessary but not sufficient.</p>
  <p>Bank HELOCs and home equity loans are full-qualification products. You generally need at least 20% equity, but you also need to pass the mortgage stress test, qualifying at the greater of your rate plus two percentage points or a benchmark floor, under the federal B-20 guideline. See <a href="{OSFI_URL}" rel="noopener noreferrer" target="_blank">OSFI&apos;s minimum qualifying rate guidance</a> for the current benchmark. On top of that, the bank checks your income, your credit score, and your total debt ratios. If your income is irregular or self-employed, your credit has slipped, your debts are high, or your renewal payment jumped, the file can fail even with a vault of equity behind it.</p>
  <p>In 2026, with renewal pressure elevated, some owners are also finding their existing HELOC frozen or reduced. The equity did not change; the bank&apos;s appetite did.</p>

  <h2>Your options when the bank says no: equity-based lending</h2>
  <p>When a bank product is out of reach, an equity-based lender looks at the same home very differently. A <a href="/what-is-a-mic/">mortgage investment corporation (MIC)</a> or private lender underwrites on the property, the loan-to-value, and your exit plan, rather than on income reconstruction and credit score. If the equity is there and the plan is sound, the file can move.</p>
  <p>The right way to use this route is as a planned bridge, not a permanent fix. A private home equity loan or second mortgage can clear a tax bill, consolidate high-interest debt, or fund a renovation now, with a plan to refinance back to a bank or B-lender once the issue that blocked you is resolved. It often helps to understand <a href="/blog/private-mortgage-ontario/">how private mortgages work in Ontario</a> before deciding, and to vet who you borrow from using this <a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">honest guide to private mortgage lenders in the GTA</a>.</p>

  <h2>What you will need to qualify</h2>
  <p><strong>For a bank HELOC or home equity loan,</strong> prepare for full qualification: at least 20% equity, a reasonable credit score, verifiable income, the stress test, and a current appraisal.</p>
  <p><strong>For a private home equity loan or second mortgage,</strong> the focus shifts to the asset: enough equity in the property, basic property details, your most recent mortgage statement, the property tax bill, identification, and a credible plan to repay or refinance. Formal income proof is light, because the property and your equity carry the file.</p>

  <h2>Risks, and how to use equity responsibly</h2>
  <p>Borrowing against your home is powerful, and it deserves respect. A HELOC&apos;s variable rate means your payment can rise if rates do. Any home-secured loan, bank or private, puts the property at risk if you cannot keep up, so a clear repayment plan matters more than the headline rate. It is also easy to over-borrow on a revolving line, so draw for a defined purpose rather than for lifestyle creep. On the private side, treat the loan as short-term and keep the exit in view from day one.</p>

  <h2>Common GTA scenarios</h2>
  <p>These are common, illustrative situations rather than specific clients.</p>
  <ul {UL_STYLE}>
    <li><strong>The renovation or basement-apartment add.</strong> An owner with strong equity funds a legal basement suite that adds rental income and long-term value, using a HELOC for the phased draws or a lump-sum loan for a fixed-price build.</li>
    <li><strong>Debt consolidation.</strong> A homeowner replaces high-interest credit card balances with equity-secured borrowing at a far lower rate, cutting monthly cash outflow and, over time, improving credit.</li>
    <li><strong>The self-employed owner declined despite equity.</strong> A business owner with real cash flow but modest reported income is turned down by the bank, then funds a CRA bill and stabilizes cash flow through an equity-based second mortgage, with a plan to refinance to a bank within a year or two.</li>
  </ul>

  {faq_html}

  <h2>Talk to a GTA lender who reads equity, not just income</h2>
  <p><a href="/">Richview Capital</a> is a licensed Ontario mortgage investment corporation that lends its own capital on residential real estate across the GTA. That means home equity requests are assessed on your property, your equity, and your plan, by the people who actually make the decision, with same-day feedback and closings in as little as 48 hours when the file is ready.</p>
  <p>If your bank has frozen or declined your HELOC, or you simply want to understand which equity tool fits your situation, it is worth a conversation before you assume the door is closed. You can review Richview&apos;s <a href="/borrowers/">financing options for Ontario borrowers</a> and reach out for a no-obligation look at your file.</p>

  <div class="post-related">
    <h3>Related on this site</h3>
    <ul>
      <li><a href="/blog/second-mortgage-ontario/">Second mortgage rates and LTV in Ontario</a></li>
      <li><a href="/blog/private-mortgage-ontario/">How private mortgages work in Ontario</a></li>
      <li><a href="/what-is-a-mic/">What is a MIC?</a></li>
      <li><a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">Honest GTA private lending guide</a></li>
      <li><a href="/blog/self-employed-mortgage-gta/">Self-employed mortgages in the GTA</a></li>
      <li><a href="/borrowers/">Borrowing with Richview Capital</a></li>
    </ul>
  </div>

  <div class="post-inline-cta">
    <p class="post-inline-cta-title">Bank declined or frozen your HELOC?</p>
    <p>Tell us about your property and equity position. We respond same-day on complete applications.</p>
    <a href="/borrowers/#contact-form">Contact Richview borrowers team</a>
  </div>

  <ul class="post-tags">
{tags_html}
  </ul>

  <p class="post-byline"><strong>Richview Capital MIC</strong> is a licensed Mortgage Investment Corporation (Mortgage Administrator License #13171). This article is educational information for Ontario homeowners, not legal, financial, or tax advice. See <a href="/about/">About</a> and <a href="/disclaimer/">Disclaimer</a>.</p>"""


def build_article() -> str:
    return f"""        <article class="post-wrap">
            <div class="container">
                <a href="/blog/" class="post-back"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> Back to Blog</a>
                <p class="post-meta">June 2026 · Borrowers · GTA</p>
                <h1 class="post-title">{escape(H1)}</h1>

                <figure class="post-hero-figure" aria-label="Article hero image">
                    <img src="{IMAGE_PATH}" width="1024" height="682" alt="{escape(HERO_ALT, quote=True)}" loading="eager" decoding="async">
                </figure>
                <p class="post-lead">{escape(POST_LEAD)}</p>
                <div class="post-prose">
{build_post_prose()}
                </div>
                <p class="post-cta">Next steps: <a href="/borrowers/">Borrowers</a> · <a href="/borrowers/#contact-form">Speak With Our Team</a> · <a href="/faq/">FAQ</a></p>
                <p class="post-disclaimer">Richview Capital MIC is a licensed Mortgage Investment Corporation (Mortgage Administrator License #13171). This article is general information, not financial, tax, or legal advice; confirm specifics with a licensed professional for your own situation. Rates, fees, LTV limits, and approvals vary by file and underwriting, and published ranges are subject to change and are not an offer of credit.</p>
            </div>
        </article>

"""


def build_page(shell: str) -> str:
    marker_article = '<article class="post-wrap">'
    marker_cta = '<section class="cta-section" id="contact">'
    idx_a = shell.find(marker_article)
    idx_c = shell.find(marker_cta)
    if idx_a == -1 or idx_c == -1:
        raise ValueError("Shell markers not found")
    return patch_head(shell[:idx_a]) + build_article() + shell[idx_c:]


def validate_html(html: str) -> list[str]:
    errors: list[str] = []
    if '"@graph"' not in html:
        errors.append("Missing JSON-LD @graph")
    if f"<h1 class=\"post-title\">{escape(H1)}</h1>" not in html:
        errors.append("Missing expected h1")
    if len(FAQS) != 6:
        errors.append(f"Expected 6 FAQs, got {len(FAQS)}")
    return errors


def main() -> int:
    if not SHELL_PATH.is_file():
        print(f"Shell not found: {SHELL_PATH}", file=sys.stderr)
        return 1
    shell = SHELL_PATH.read_text(encoding="utf-8")
    page = build_page(shell)
    prose = build_post_prose()
    errors = validate_html(page)
    if "—" in prose or "–" in prose:
        errors.append("Article prose contains em/en dash characters")
    if errors:
        for err in errors:
            print(f"Validation error: {err}", file=sys.stderr)
        return 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(page, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Lines: {len(page.splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
