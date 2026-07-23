#!/usr/bin/env python3
"""Generate blog/private-commercial-mortgage-ontario/index.html from shell + article data."""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHELL_PATH = REPO / "blog/second-mortgage-ontario/index.html"
OUTPUT_PATH = REPO / "blog/private-commercial-mortgage-ontario/index.html"

SLUG = "private-commercial-mortgage-ontario"
BASE_URL = "https://richviewcapitalmic.com"
PAGE_URL = f"{BASE_URL}/blog/{SLUG}/"
IMAGE_URL = f"{BASE_URL}/images/blog/{SLUG}.jpg"
IMAGE_PATH = f"/images/blog/{SLUG}.jpg"
PUBLISHED = "2026-07-12T09:00:00-04:00"

TITLE = "Private Commercial Mortgage Ontario: Rates & Qualifying | Richview Capital MIC"
OG_TITLE = "Private Commercial Mortgage Ontario: Rates & Qualifying"
DESCRIPTION = (
    "What a private commercial mortgage in Ontario costs, how to qualify, and when a private lender "
    "beats the bank. Rates, fees, LTV, and timelines explained."
)
H1 = "Private commercial mortgage Ontario: rates, qualifying, and when it makes sense"
JSONLD_HEADLINE = "Private Commercial Mortgage Ontario: Rates, Qualifying, and When It Makes Sense"
HERO_ALT = (
    "Private commercial mortgage Ontario — commercial building with financing checklist "
    "and Richview Capital guide"
)
POST_LEAD = (
    "What a private commercial mortgage in Ontario costs, how lenders qualify deals on equity, "
    "and when private capital beats a bank timeline."
)

UL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'
OL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'

MLI_SELECT = (
    "https://www.cmhc-schl.gc.ca/professionals/project-funding-and-mortgage-financing/"
    "mortgage-loan-insurance/multi-unit-insurance/mli-select"
)
BOC = "https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/"
LTT = "https://www.ontario.ca/document/land-transfer-tax"
FSRA_REGISTRY = "https://mbsweblist.fsrao.ca/"

FAQS: list[tuple[str, str]] = [
    (
        "What interest rate do private lenders charge for commercial mortgages in Ontario?",
        "Private first mortgages on Ontario commercial property typically run 7 percent to 12 percent, with second mortgages from about 10 percent to 15 percent. Pricing depends on loan-to-value, location, property type, and the strength of your exit plan. Richview's commercial first mortgages start at 7.99 percent.",
    ),
    (
        "How much can I borrow against a commercial property?",
        "Most Ontario private lenders advance 65 percent to 75 percent of appraised value. Richview lends up to 75 percent LTV in the GTA, up to 65 percent on condos and properties outside the GTA, and funds loans up to $5,000,000.",
    ),
    (
        "How fast can a private commercial mortgage close?",
        "A clean file with a completed appraisal can fund in as little as 48 hours, and one to two weeks is typical. Banks and credit unions usually need 45 to 90 days for commercial approvals, which is the main reason borrowers with hard deadlines go private.",
    ),
    (
        "Can I qualify with bad credit or income I cannot document?",
        "Usually, yes. Private commercial lending is equity-based, so the property's value, your down payment or existing equity, and a credible exit strategy carry more weight than credit scores or tax returns. Credit history is reviewed as context, not as a pass-fail gate.",
    ),
    (
        "Are private commercial lenders regulated in Ontario?",
        "Yes. Mortgage brokerages, agents, and mortgage administrators must be licensed by the Financial Services Regulatory Authority of Ontario (FSRA), and every licence can be verified in FSRA's free public registry. Always confirm a lender's licence before signing a commitment.",
    ),
    (
        "How do I get out of a private commercial mortgage?",
        "Most borrowers exit by refinancing to a bank or credit union once the property's income stabilizes, or by selling the asset. Agree on the exit before you borrow, confirm whether the mortgage allows early repayment, and start your takeout financing conversations three to four months before the term ends.",
    ),
]

ARTICLE_TAGS = [
    "Private Commercial Mortgage Ontario",
    "Commercial Mortgage Rates",
    "Private Lender Ontario",
    "Commercial Bridge Loan",
    "Equity-Based Lending",
    "Commercial LTV",
    "FSRA Licensed Lender",
    "GTA Commercial Financing",
    "Richview Capital Borrowers",
    "Commercial Exit Strategy",
]


def ext(url: str, label: str) -> str:
    return f'<a href="{url}" rel="noopener noreferrer" target="_blank">{escape(label)}</a>'


def build_json_ld() -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": JSONLD_HEADLINE,
                "description": DESCRIPTION,
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
                    "Commercial mortgage",
                    "Private mortgage",
                    "Mortgage Investment Corporation",
                    "Ontario",
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
                        "name": "Private Commercial Mortgage Ontario",
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
        "private commercial mortgage Ontario",
        "commercial mortgage rates Ontario",
        "private commercial lender",
        "commercial bridge loan Ontario",
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
    <meta property="og:image:height" content="512">
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
    parts = ["  <h2>Frequently asked questions</h2>"]
    for question, answer in FAQS:
        parts.append(f"  <h3>{escape(question)}</h3>")
        parts.append(f"  <p>{escape(answer)}</p>")
    return "\n".join(parts)


def build_post_prose() -> str:
    faq_html = build_faq_html()
    tags_html = "\n".join(f"    <li>{tag}</li>" for tag in ARTICLE_TAGS)
    return f"""<p class="post-lead-em">You have a commercial deal that works on paper. The problem is the financing. Maybe the bank wants 90 days you do not have, maybe the building has vacancy that breaks their debt coverage math, or maybe your income documents do not fit the standard box. Whatever the reason, the institutional path has stalled and the closing date has not moved.</p>

  <p>A private commercial mortgage in Ontario exists for exactly this situation. It is short-term financing secured against commercial real estate, priced on the strength of the property and your equity rather than on a perfect file. Used well, it closes deals banks cannot close in time. Used carelessly, it is expensive money without a plan.</p>

  <p>This guide covers what private commercial mortgages actually cost in Ontario, how private lenders qualify a deal, how fast they close, how to check that a lender is legitimate, and, just as important, when you should not use one.</p>

  <h2>What is a private commercial mortgage?</h2>
  <p>A private commercial mortgage is a loan secured against commercial or mixed-use property that comes from private capital instead of a bank or credit union. In Ontario, the money typically comes from three sources: mortgage investment corporations (MICs), private mortgage funds, and individual lenders. If you want the structural details, here is a plain-language explanation of <a href="/what-is-a-mic/">how a mortgage investment corporation works</a>.</p>

  <p>Private commercial loans differ from bank loans in structure, not just in source:</p>
  <ul {UL_STYLE}>
    <li><strong>Short terms.</strong> Usually 6 to 24 months, with 12 months being the most common. This is bridge capital, not a 25-year commitment.</li>
    <li><strong>Interest-only payments.</strong> Most private commercial mortgages charge interest only, which keeps monthly carrying costs lower than an amortizing payment at the same rate.</li>
    <li><strong>Equity-based underwriting.</strong> The primary question is the property&apos;s value and marketability, not whether your covenant satisfies a 1.25x debt service test.</li>
    <li><strong>Speed.</strong> Days to weeks, not months.</li>
  </ul>

  <p>The market is regulated. Mortgage brokerages, agents, and mortgage administrators in Ontario must be licensed by the Financial Services Regulatory Authority of Ontario (FSRA), and you can verify any licence in FSRA&apos;s public registry (more on that below). Private lending on commercial property works much like <a href="/blog/private-mortgage-ontario/">private mortgages in Ontario</a> generally; the collateral and the underwriting math are what change.</p>

  <h2>When a private commercial mortgage makes sense</h2>
  <p>Private money costs more than bank money. It earns its keep only when it solves a problem banks cannot or will not solve. The common Ontario scenarios:</p>
  <ul {UL_STYLE}>
    <li><strong>A closing you cannot move.</strong> Bank commercial approvals commonly run 45 to 90 days. If your purchase agreement closes in three weeks, private capital may be the only financing that arrives on time.</li>
    <li><strong>Vacancy or value-add properties.</strong> A half-empty plaza or an industrial building between tenants often fails bank debt coverage requirements even when the purchase price is excellent. Private lenders can finance the acquisition and let you refinance once income stabilizes.</li>
    <li><strong>Bridge situations.</strong> You are selling one property and buying another, and the dates do not line up.</li>
    <li><strong>Credit events and CRA arrears.</strong> Tax arrears, a past consumer proposal, or bruised credit will stall most institutional files. Private lenders look past the history if the equity and exit are sound. See our guide to <a href="/blog/bad-credit-mortgage-ontario/">bad credit mortgages in Ontario</a> for the residential side of this pattern.</li>
    <li><strong>Non-standard income.</strong> Self-employed borrowers and holding companies with complex statements often cannot document income the way a bank wants it documented.</li>
    <li><strong>Construction and completion financing.</strong> Cost overruns or a stalled project mid-build are classic private scenarios; see our guide to <a href="/blog/construction-financing-ontario/">construction financing in Ontario</a> for how draws and budgets work.</li>
    <li><strong>Raising capital against property you own.</strong> A commercial second mortgage can pull equity out of a building without breaking a good first mortgage. The mechanics parallel <a href="/blog/second-mortgage-ontario/">second mortgages in Ontario</a> on residential property, with commercial collateral.</li>
  </ul>

  <h3>When to stay with a bank</h3>
  <p>If your property is stabilized, your debt service coverage is comfortably above 1.25x, and you plan to hold for years, institutional financing is cheaper and you should pursue it, even if it is slower. Apartment buildings with five or more units may also qualify for CMHC-insured financing such as {ext(MLI_SELECT, "MLI Select")}, which offers higher leverage and lower rates than any conventional or private option. A private mortgage is the right tool when time, condition, or file complexity rules those paths out.</p>

  <h2>Private commercial mortgage rates in Ontario (2026)</h2>
  <p>Bank commercial rates in Ontario currently sit in the roughly 5 percent to 7.5 percent range depending on property type and covenant strength. Private pricing starts above that because private lenders take on the risk and the timelines banks refuse. Typical Ontario ranges, alongside Richview Capital&apos;s published starting rates:</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Loan type</th><th>Typical private range in Ontario</th><th>Richview starting rate</th></tr>
      </thead>
      <tbody>
        <tr><td>First mortgage</td><td>7% to 12%</td><td>From 7.99%</td></tr>
        <tr><td>Second mortgage</td><td>10% to 15%</td><td>Case by case</td></tr>
        <tr><td>Bridge loan</td><td>8% to 13%</td><td>Case by case</td></tr>
        <tr><td>Construction loan</td><td>8% to 13%</td><td>From 8.99%</td></tr>
      </tbody>
    </table>
  </div>

  <p>Where you land inside a range depends on five things: loan-to-value (lower LTV earns a lower rate), location (GTA and strong regional markets price better), property type (industrial and mixed-use generally price better than single-purpose or rural assets), property condition, and the credibility of your exit plan. Private rates are also less tightly coupled to the {ext(BOC, "Bank of Canada policy rate")} than bank pricing; risk and equity drive the quote more than the overnight rate does.</p>
  <p>Because payments are usually interest-only, the monthly carry is simpler to model than it looks. As an illustrative example: a $1,000,000 first mortgage at 9 percent interest-only costs $7,500 per month. Over a 12-month term that is $90,000 in interest, a knowable, budgetable cost to weigh against what the loan lets you do.</p>

  <h2>The full cost: fees you should expect</h2>
  <p>The rate is only part of the price of private money. A trustworthy lender will lay out the whole stack before you sign a commitment. Expect:</p>
  <ul {UL_STYLE}>
    <li><strong>Lender fee:</strong> typically 1 percent to 3 percent of the loan amount, deducted from the advance. Richview charges a flat 2 percent lender fee.</li>
    <li><strong>Broker fee:</strong> if a mortgage broker arranged the deal, usually 1 percent to 2 percent on commercial files.</li>
    <li><strong>Legal fees:</strong> you pay your own lawyer and, on most private commercial deals, the lender&apos;s lawyer as well. Budget several thousand dollars combined, more on complex title or corporate structures.</li>
    <li><strong>Appraisal:</strong> commercial appraisals by an AACI-designated appraiser typically run $3,000 to $8,000 depending on the asset.</li>
    <li><strong>Land transfer tax (purchases only):</strong> Ontario charges 0.5 percent on the first $55,000, 1 percent up to $250,000, 1.5 percent up to $400,000, and 2 percent above $400,000, per the {ext(LTT, "Ontario Ministry of Finance land transfer tax schedule")}. Buying inside the City of Toronto adds a comparable municipal land transfer tax on top. This is paid from your own capital at closing; it cannot be mortgaged.</li>
  </ul>
  <p>Illustrative all-in math: on a $1,500,000 private first mortgage, a 2 percent lender fee is $30,000, legals and appraisal might add $12,000 to $18,000, so roughly $42,000 to $48,000 in transaction costs before interest. Get every one of these numbers in writing in the commitment letter, including any renewal fee if the loan extends past its original term.</p>

  <h2>How to qualify for a private commercial mortgage</h2>
  <p>Banks underwrite the borrower first and the building second. Private lenders reverse the order. Four things decide a private commercial approval in Ontario:</p>
  <ol {OL_STYLE}>
    <li><strong>Equity, measured as loan-to-value.</strong> Most Ontario private lenders cap commercial lending between 65 percent and 75 percent LTV. Richview lends up to 75 percent LTV in the GTA, and up to 65 percent on condos and on properties outside the GTA, with loans up to $5,000,000.</li>
    <li><strong>The property itself.</strong> Marketability matters more than current income. A well-located building with vacancy is financeable; a remote single-purpose asset is harder at any occupancy.</li>
    <li><strong>Your exit strategy.</strong> Private lenders want to know, specifically, how the loan gets repaid: a refinance to a bank once income stabilizes, a sale, or a defined liquidity event. A credible exit is often the difference between an approval and a decline.</li>
    <li><strong>Your story.</strong> Credit and income still get reviewed, but as context rather than as pass-fail gates. A past credit event with a clear explanation rarely kills a deal that has strong equity.</li>
  </ol>

  <p>Consider a hypothetical that fails at a bank and works privately. An investor agrees to buy a retail plaza for $2,000,000 with 30 percent of the space vacant. Current net operating income of $105,000 against roughly $98,000 of annual debt service puts coverage near 1.07x, well below the 1.20x to 1.25x minimum most institutional lenders require. A private lender advances 65 percent of value, the investor closes on schedule, leases the vacant units over the following year, and then refinances with a credit union at a stabilized coverage ratio. The private mortgage cost more per month; it also made the entire deal possible. This example is illustrative, not a client file.</p>

  <h3>Documents you will need</h3>
  <p>Private files are lighter than bank files. Most Ontario private lenders, Richview included, want a purchase agreement or current mortgage statements, a recent appraisal or the willingness to order one, a rent roll and basic operating figures if the property is tenanted, photo ID and corporate documents where applicable, and a short written summary of the plan and exit. You can see how this works end-to-end on our <a href="/borrowers/">borrower process</a> page. There is no requirement for two years of polished financial statements or a stabilized occupancy history.</p>

  <h3>How fast can you close?</h3>
  <p>With documents and an acceptable appraisal in hand, a private commercial mortgage in Ontario can fund in as little as 48 hours; one to two weeks is a comfortable norm for a clean file. Compare that with 45 to 90 days for a typical bank commercial approval. The usual bottlenecks are the appraisal booking and title or environmental questions, so ordering the appraisal early is the single best way to protect your timeline.</p>

  <h2>Private lender vs bank: side-by-side</h2>
  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Factor</th><th>Bank or credit union</th><th>Private lender</th></tr>
      </thead>
      <tbody>
        <tr><td>First-mortgage rate</td><td>Roughly 5% to 7.5%</td><td>7% to 12% (Richview from 7.99%)</td></tr>
        <tr><td>Maximum LTV</td><td>55% to 75% by property type</td><td>65% to 75%</td></tr>
        <tr><td>Primary test</td><td>DSCR of 1.20x or higher</td><td>Equity, property, exit</td></tr>
        <tr><td>Approval to funding</td><td>45 to 90 days</td><td>48 hours to 2 weeks</td></tr>
        <tr><td>Term</td><td>1 to 10 years, amortizing</td><td>6 to 24 months, interest-only</td></tr>
        <tr><td>Fees</td><td>Lower, some waivable</td><td>Lender fee 1% to 3% plus legals</td></tr>
        <tr><td>Best for</td><td>Stabilized assets, long holds</td><td>Speed, vacancy, credit events, bridges</td></tr>
      </tbody>
    </table>
  </div>

  <h2>How to vet a private commercial lender in Ontario</h2>
  <p>The private market is legitimate and regulated, but quality varies, so verify before you commit.</p>
  <p><strong>Check the licence.</strong> Mortgage brokerages, agents, and administrators in Ontario must hold a licence with the Financial Services Regulatory Authority of Ontario. Search any name or licence number in the {ext(FSRA_REGISTRY, "FSRA public registry")} before signing anything. Richview Capital, for example, operates as a licensed mortgage administrator under FSRA licence #13171.</p>
  <p><strong>Prefer structure over handshakes.</strong> A MIC or managed fund lends under a defined mandate with audited flows of capital, which usually means more predictable behaviour at renewal time than a one-off individual lender.</p>
  <p><strong>Demand the full fee stack in writing.</strong> Lender fee, broker fee, legal costs, renewal fee, and any exit or discharge fees should all appear in the commitment letter. A lender who is vague about fees before funding will not become clearer afterward.</p>
  <p><strong>Pressure-test the renewal and the exit.</strong> Ask what happens if you need three more months, what a renewal costs, and whether the mortgage is open for early repayment once your bank takeout is ready. Then hold your own plan to the same standard: if you cannot describe your exit in one sentence, you are not ready to borrow private money. For a deeper look at separating good operators from bad ones, read our guide to <a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">choosing a private mortgage lender in the GTA</a>.</p>

{faq_html}

  <h2>Commercial financing built for Ontario timelines</h2>
  <p>Most of the borrowers we work with did not plan to use private money. They planned to close a deal, and somewhere between the accepted offer and the bank&apos;s underwriting queue, the timeline broke. That gap between a good property and slow institutional capital is precisely what <a href="/">Richview Capital</a> was built to fill: a licensed Ontario mortgage investment corporation (FSRA #13171) based in Woodbridge, lending on commercial, mixed-use, and residential properties across the province.</p>
  <p>We fund commercial first mortgages from 7.99 percent and construction financing from 8.99 percent, up to $5,000,000 and up to 65 percent LTV (case by case), with a flat 2 percent lender fee and closings in as little as 48 hours. Bridge and land scenarios are evaluated case by case. Every commitment spells out the full cost, the term, and the renewal terms before you sign.</p>
  <p>If you have a commercial deal on a deadline, or a property the banks will not touch yet, <a href="/borrowers/#contact-form">tell us about the file</a> and we will give you a straight answer on rate, proceeds, and timing, usually within a day.</p>

  <div class="post-related">
    <h3>Related on this site</h3>
    <ul>
      <li><a href="/blog/private-mortgage-ontario/">Private mortgages in Ontario</a></li>
      <li><a href="/blog/construction-financing-ontario/">Construction financing in Ontario</a></li>
      <li><a href="/blog/second-mortgage-ontario/">Second mortgage rates and LTV in Ontario</a></li>
      <li><a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">Private mortgage lender Toronto: the honest GTA guide</a></li>
      <li><a href="/what-is-a-mic/">What is a MIC?</a></li>
      <li><a href="/borrowers/">Borrowing with Richview Capital</a></li>
    </ul>
  </div>

  <div class="post-inline-cta">
    <p class="post-inline-cta-title">Commercial deal on a deadline?</p>
    <p>Tell us about the property and your timeline — we respond same-day on complete applications.</p>
    <a href="/borrowers/#contact-form">Contact Richview borrowers team</a>
  </div>

  <ul class="post-tags">
{tags_html}
  </ul>

  <p class="post-byline"><strong>Richview Capital MIC</strong> is a licensed Mortgage Investment Corporation (Mortgage Administrator License #13171). This article is educational information for Ontario borrowers — not legal, financial, or tax advice. See <a href="/about-us/">About</a> and <a href="/disclaimer/">Disclaimer</a>.</p>"""


def build_article() -> str:
    return f"""        <article class="post-wrap">
            <div class="container">
                <a href="/blog/" class="post-back"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> Back to Blog</a>
                <p class="post-meta">July 2026 · Borrowers · Ontario</p>
                <h1 class="post-title">{escape(H1)}</h1>

                <figure class="post-hero-figure" aria-label="Article hero image">
                    <img src="{IMAGE_PATH}" width="1024" height="512" alt="{escape(HERO_ALT, quote=True)}" loading="eager" decoding="async">
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
    return patch_head(shell[:idx_a].rstrip()) + "\n" + build_article() + shell[idx_c:]


def validate_html(html: str) -> list[str]:
    errors: list[str] = []
    if '"@graph"' not in html:
        errors.append("Missing JSON-LD @graph")
    if f'<h1 class="post-title">{escape(H1)}</h1>' not in html:
        errors.append("Missing expected h1")
    if len(FAQS) != 6:
        errors.append(f"Expected 6 FAQs, got {len(FAQS)}")
    if "Book a Consultation" in html or "Book a Free Consultation" in html:
        errors.append("Legacy consultation CTA wording found")
    return errors


def main() -> int:
    if not SHELL_PATH.is_file():
        print(f"Shell not found: {SHELL_PATH}", file=sys.stderr)
        return 1
    shell = SHELL_PATH.read_text(encoding="utf-8")
    page = build_page(shell)
    errors = validate_html(page)
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
