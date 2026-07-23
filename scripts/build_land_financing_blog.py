#!/usr/bin/env python3
"""Generate blog/land-financing-ontario/index.html from shell + article data."""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHELL_PATH = REPO / "blog/second-mortgage-ontario/index.html"
OUTPUT_PATH = REPO / "blog/land-financing-ontario/index.html"

SLUG = "land-financing-ontario"
BASE_URL = "https://richviewcapitalmic.com"
PAGE_URL = f"{BASE_URL}/blog/{SLUG}/"
IMAGE_URL = f"{BASE_URL}/images/blog/{SLUG}.jpg"
IMAGE_PATH = f"/images/blog/{SLUG}.jpg"
PUBLISHED = "2026-07-12T09:00:00-04:00"

TITLE = "Land Financing in Ontario: Vacant Land Loan Guide (2026) | Richview Capital MIC"
OG_TITLE = "Land Financing in Ontario: Vacant Land Loan Guide (2026)"
DESCRIPTION = (
    "How land financing works in Ontario: down payments, rates, raw vs. serviced land, "
    "private land loans, and the true costs of buying a vacant lot."
)
H1 = "Land financing in Ontario: how to get a loan for vacant land"
JSONLD_HEADLINE = "Land Financing in Ontario: How to Get a Loan for Vacant Land"
HERO_ALT = (
    "Land financing Ontario — vacant lot with land loan application "
    "and Richview Capital guide"
)
POST_LEAD = (
    "Down payments, rates, raw vs. serviced land, private land loans, and the "
    "Ontario closing costs most buyers forget to budget."
)

UL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'
OL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'

WOWA = "https://wowa.ca/buy-land-ontario"
CROWN_LAND = "https://www.ontario.ca/page/crown-land"
BOC = "https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/"
FSRA = "https://www.fsrao.ca/consumers/mortgage-brokering"
LTT = "https://www.ontario.ca/document/land-transfer-tax/calculating-land-transfer-tax"
CRA_HST = (
    "https://www.canada.ca/en/revenue-agency/services/forms-publications/"
    "publications/gi-003/sales-vacant-land-individuals.html"
)

FAQS: list[tuple[str, str]] = [
    (
        "How much down payment do I need to buy land in Ontario?",
        "Plan on 25% to 35% for a serviced lot, 30% to 50% for unserviced land, and 50% or more for remote raw land. The exact figure depends on the lender's maximum LTV for that property type and location, with GTA properties generally supporting higher LTVs than rural ones.",
    ),
    (
        "Can I get a mortgage for vacant land from a bank?",
        "Yes, but banks mostly finance serviced, residentially zoned lots for well-qualified borrowers with full income documentation. Raw or remote land is routinely declined, which is why many Ontario land purchases are financed privately.",
    ),
    (
        "What interest rate will I pay on a land loan in Ontario?",
        "Bank land loans price above standard mortgage rates, while private land loans in Ontario generally run from about 7% to 13% interest-only, plus a lender fee of around 2%. Your rate depends on LTV, location, land type, and the strength of your exit plan.",
    ),
    (
        "Do I pay HST or land transfer tax on vacant land in Ontario?",
        "Land transfer tax always applies; on a $300,000 lot it comes to $2,975. HST is often exempt when an individual sells personal-use land, but sales by developers, corporations, or sellers who subdivided the property are usually taxable, so confirm with your lawyer before firming up.",
    ),
    (
        "How fast can a private land loan close?",
        "Once the appraisal and documents are in, private lenders can issue commitments within days, and a complete file can fund in as little as 48 hours. That speed is one of the main reasons buyers with firm closing dates use private land financing.",
    ),
    (
        "Can I finance raw land with no road access or services?",
        "It is possible but hard. Expect a private lender, an LTV of 50% or lower, and pricing at the top of the range, because the security is difficult to resell. Improving access or securing entrance permits before you apply can meaningfully improve the terms.",
    ),
]

ARTICLE_TAGS = [
    "Land Financing Ontario",
    "Vacant Land Loan",
    "Private Land Loan",
    "Raw Land Financing",
    "Serviced Lot Mortgage",
    "Land Transfer Tax Ontario",
    "Construction Exit Strategy",
    "Ontario LTV",
    "Richview Capital Borrowers",
    "GTA Land Purchase",
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
                    "Land financing",
                    "Vacant land loan",
                    "Private mortgage",
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
                        "name": "Land Financing in Ontario",
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
        "land financing Ontario",
        "vacant land loan Ontario",
        "private land loan",
        "raw land financing",
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
    return f"""<p class="post-lead-em">You found the lot. Maybe it is a serviced parcel in a growing subdivision, an infill lot in the GTA, or 40 acres of bush two hours north of Barrie. Then you called your bank, and the conversation changed. Suddenly the down payment doubled, the approval timeline stretched into weeks, or the answer was simply no.</p>

  <p>That experience is normal. Land financing in Ontario works differently than a standard home mortgage, and most of the advice online glosses over the parts that actually decide your deal: how much lenders will really advance, what the loan costs month to month, the Ontario taxes that hit at closing, and how you exit a short-term land loan once you own the property. This guide covers all of it, with worked numbers.</p>

  <h2>Why land is harder to finance than a house</h2>
  <p>A residential mortgage is secured by a building that generates obvious value: people can live in it, rent it, and resell it quickly. Vacant land has none of that built in. There is no structure to appraise, no rental income, and a much thinner pool of future buyers if the lender ever has to sell the property to recover its money.</p>
  <p>Vacant land also cannot be insured through CMHC mortgage default insurance the way an owner-occupied home can, so every land loan is effectively a conventional, uninsured loan. Lenders respond to that risk the only way they can: lower loan-to-value ratios (LTV), larger down payments, higher interest rates, and shorter terms.</p>
  <p>The result is that how you finance a land purchase in Ontario depends heavily on two things: what kind of land it is, and which type of lender you approach.</p>

  <h2>Types of land and how lenders see them</h2>
  <p>Lenders do not treat all land equally. The closer a parcel is to being buildable, the easier it is to finance.</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Land type</th><th>What it is</th><th>Typical down payment</th><th>Financing difficulty</th></tr>
      </thead>
      <tbody>
        <tr><td>Serviced vacant lot</td><td>Utilities connected, road access, often in or near a town</td><td>25-35%</td><td>Easiest</td></tr>
        <tr><td>Unserviced vacant lot</td><td>Some prior development, utilities nearby but not connected</td><td>30-50%</td><td>Moderate</td></tr>
        <tr><td>Raw land</td><td>No services, no structures, often remote</td><td>50%+</td><td>Hardest</td></tr>
        <tr><td>Infill / urban lot</td><td>Building lot in an established city neighbourhood</td><td>25-35%</td><td>Easier, especially in the GTA</td></tr>
        <tr><td>Agricultural land</td><td>Zoned for farming, may include outbuildings</td><td>Varies by lender and use</td><td>Specialized</td></tr>
      </tbody>
    </table>
  </div>

  <p>Industry data backs this up: WOWA's guide to buying land in Ontario reports that land loan lenders generally require a {ext(WOWA, "down payment of 30% to 50%")}, with the higher end reserved for remote or inaccessible parcels. Raw land sits at the expensive end of that range because a lender may be holding security that takes a year or more to resell.</p>

  <h3>A note on Crown land</h3>
  <p>Roughly {ext(CROWN_LAND, "87% of Ontario is Crown land")} owned by the provincial government, concentrated in northern Ontario. You generally cannot mortgage your way into Crown land; it is leased or sold only in limited circumstances under provincial policy. Everything in this guide applies to privately owned land.</p>

  <h2>What a land loan costs in Ontario</h2>
  <p>There are two main paths: institutional lenders and private lenders. Most borrowers should understand both before committing.</p>

  <h3>Banks and credit unions</h3>
  <p>Institutional lenders offer the lowest rates on land, typically a premium of one to a few percentage points over their standard mortgage rates, which move with the {ext(BOC, "Bank of Canada's policy rate")}. The trade-offs are strict:</p>
  <ul {UL_STYLE}>
    <li>They strongly prefer serviced lots with road access and clear residential zoning.</li>
    <li>Full income documentation is required: employment letters, tax returns, debt-service ratios.</li>
    <li>Many banks route land through their commercial lending group, which can mean slower approvals and extra conditions.</li>
    <li>Approvals commonly take two to six weeks, which is a problem if your purchase agreement closes sooner.</li>
  </ul>
  <p>If you have strong documented income, a large down payment, and a serviced lot, start here.</p>

  <h3>Private lenders and MICs</h3>
  <p>Private lenders, including mortgage investment corporations, fill the gap the banks leave. If you are not sure <a href="/what-is-a-mic/">what a mortgage investment corporation (MIC) is</a>, it is a pooled fund of investor capital, regulated under the Income Tax Act, that lends against real estate. In Ontario, the mortgage brokerages and administrators that arrange and manage these loans are licensed by the {ext(FSRA, "Financial Services Regulatory Authority of Ontario (FSRA)")}, and you can verify any lender&apos;s licence on FSRA&apos;s public registry.</p>
  <p>Private land loans look different from bank mortgages:</p>
  <ul {UL_STYLE}>
    <li><strong>Underwriting is equity- and exit-based.</strong> The lender cares most about the property&apos;s value, your down payment, and how the loan gets repaid, not primarily your T4.</li>
    <li><strong>Terms are short.</strong> Usually 12 months, sometimes 24, with interest-only payments.</li>
    <li><strong>Pricing is higher.</strong> Private first mortgage rates in Ontario generally start around 7% and run into the low teens for riskier land, plus a lender fee, commonly around 2% of the loan amount. As a reference point, Richview Capital&apos;s first mortgages start at 6.49%, with land deals priced to the specific risk.</li>
    <li><strong>Speed is the advantage.</strong> A private lender can issue a commitment in days and, when the file is clean, fund in as little as 48 hours.</li>
  </ul>

  <h3>Bank vs. private land loan at a glance</h3>
  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Factor</th><th>Bank / credit union</th><th>Private lender / MIC</th></tr>
      </thead>
      <tbody>
        <tr><td>Interest rate</td><td>Lowest available</td><td>Roughly 7-13%, priced to risk</td></tr>
        <tr><td>Lender fee</td><td>Usually none</td><td>Commonly ~2% of loan</td></tr>
        <tr><td>Max LTV on land</td><td>Often 50-65%</td><td>Up to 65-75% depending on location and property</td></tr>
        <tr><td>Income documents</td><td>Full verification</td><td>Flexible; equity and exit matter most</td></tr>
        <tr><td>Raw land</td><td>Rarely</td><td>Case by case, at lower LTV</td></tr>
        <tr><td>Approval speed</td><td>2-6 weeks</td><td>Days; funding possible in 48 hours</td></tr>
        <tr><td>Term</td><td>1-5 years, amortizing</td><td>12-24 months, interest-only</td></tr>
      </tbody>
    </table>
  </div>
  <p>In the GTA, where land is more liquid, private LTVs tend to be higher (up to about 75% on strong properties), while rural and small-town parcels are usually capped near 65%.</p>

  <h2>The Ontario costs nobody budgets for</h2>
  <p>This is where generic land-loan articles fall short. Buying land in Ontario triggers costs beyond the loan itself, and they are due at closing.</p>

  <h3>Land transfer tax</h3>
  <p>Ontario charges land transfer tax on every purchase, vacant land included. The provincial brackets are:</p>
  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Portion of purchase price</th><th>Rate</th></tr>
      </thead>
      <tbody>
        <tr><td>First $55,000</td><td>0.5%</td></tr>
        <tr><td>$55,000 to $250,000</td><td>1.0%</td></tr>
        <tr><td>$250,000 to $400,000</td><td>1.5%</td></tr>
        <tr><td>$400,000 to $2,000,000</td><td>2.0%</td></tr>
      </tbody>
    </table>
  </div>
  <p>On a $300,000 vacant lot, that works out to $2,975: $275 on the first bracket, $1,950 on the second, and $750 on the third. Buy inside the City of Toronto and a municipal land transfer tax of a similar scale applies on top. Full bracket details are on the {ext(LTT, "Ontario government's land transfer tax page")}. Note that the first-time homebuyer refund does not help here; it applies to homes, not vacant land.</p>

  <h3>HST on vacant land</h3>
  <p>HST depends on who is selling and how the land was used. Under the Canada Revenue Agency&apos;s rules, {ext(CRA_HST, "sales of vacant land by individuals")} are generally HST-exempt when the land was held for personal use. The sale usually becomes taxable when the seller subdivided the parcel into more than two lots, used the land primarily in a business, or is a developer or corporation. On a $400,000 lot, that difference is $52,000, so have your lawyer confirm the HST treatment before you firm up the offer.</p>

  <h3>Everything else</h3>
  <p>Budget for a survey (often $2,000+ if a current one does not exist), an appraisal, legal fees on both the purchase and the mortgage, and annual property taxes that start the day you own the land. If you plan to build on an unserviced lot, get quotes early for a well, septic system, and hydro connection; these routinely run into six figures in rural Ontario and lenders will ask how you intend to cover them.</p>

  <h2>How to qualify: what lenders actually look at</h2>
  <p>Whether you apply to a bank or a private lender, five factors drive the decision:</p>
  <ol {OL_STYLE}>
    <li><strong>Down payment and equity.</strong> The single biggest lever. More cash in means lower LTV, which offsets almost every other weakness in a file.</li>
    <li><strong>Exit strategy.</strong> For private lenders this is the heart of the application. A land loan is a bridge, so the lender wants a credible answer to &ldquo;how does this loan get repaid&rdquo;: a construction start with financing lined up, a bank takeout once income documents mature, or a planned resale.</li>
    <li><strong>The property itself.</strong> Location, road access, zoning, services, and marketability. A serviced lot in Vaughan underwrites very differently than landlocked acreage in the north.</li>
    <li><strong>Zoning and approvals.</strong> Lenders check that your intended use is actually permitted. Conservation authority constraints, missing severance approvals, or agricultural zoning on a residential plan will reduce LTV or stop a deal.</li>
    <li><strong>Credit and income.</strong> Decisive at banks. At a private lender they inform pricing more than approval; borrowers with bruised credit or self-employment income get financed on land regularly when the equity and exit are strong. This is the same logic that drives <a href="/blog/private-mortgage-ontario/">how private mortgages work in Ontario</a> generally.</li>
  </ol>

  <h2>Step-by-step: financing a land purchase in Ontario</h2>
  <ol {OL_STYLE}>
    <li><strong>Do your diligence before the offer.</strong> Confirm zoning with the municipality, check for conservation authority overlays, and verify legal road access and available services.</li>
    <li><strong>Include a financing condition.</strong> Land financing falls through more often than home financing. Give yourself at least 5 to 10 business days conditional on financing unless you have funds or a commitment in hand.</li>
    <li><strong>Order or review the survey.</strong> Boundaries, easements, and encroachments all affect value and lendability.</li>
    <li><strong>Choose your lender path.</strong> Serviced lot, strong income, flexible timeline: try the bank first. Raw land, tight closing, or non-traditional income: <a href="/borrowers/">go straight to a private lender</a> or have a broker run both in parallel.</li>
    <li><strong>Get the appraisal.</strong> The lender will order an appraisal addressing land value, zoning, and resale prospects. LTV is set against appraised value, not necessarily your purchase price.</li>
    <li><strong>Review the commitment.</strong> Check the rate, lender fee, term length, prepayment terms, and any conditions such as proof of exit plan or servicing quotes.</li>
    <li><strong>Close.</strong> Your lawyer registers the mortgage and remits land transfer tax. If the timeline is tight, a private file that is complete can fund in as little as two business days.</li>
  </ol>

  <h2>A worked example (hypothetical)</h2>
  <p>Suppose a buyer is purchasing a $400,000 serviced building lot in Simcoe County and plans to start construction within a year. The bank declines because the buyer is self-employed with one year of business income. A private lender offers 65% LTV. The numbers, purely as an illustration:</p>
  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Item</th><th>Amount</th></tr>
      </thead>
      <tbody>
        <tr><td>Purchase price</td><td>$400,000</td></tr>
        <tr><td>Loan (65% LTV)</td><td>$260,000</td></tr>
        <tr><td>Down payment</td><td>$140,000</td></tr>
        <tr><td>Interest rate (interest-only, 12-month term)</td><td>9.5%</td></tr>
        <tr><td>Monthly payment</td><td>$2,058</td></tr>
        <tr><td>Lender fee (2%)</td><td>$5,200</td></tr>
        <tr><td>Ontario land transfer tax</td><td>$4,475</td></tr>
        <tr><td>Legal fees (approx.)</td><td>$2,500</td></tr>
      </tbody>
    </table>
  </div>
  <p>Total cash to close is roughly $152,000, and carrying the lot costs about $24,700 in interest over the year. That is real money, but it buys the property now and a 12-month runway to finalize building permits and construction financing. If the alternative is losing the lot or missing a build season, the bridge often pays for itself.</p>

  <h2>From land loan to construction: planning your exit</h2>
  <p>A land loan is rarely the end state. The three standard exits:</p>
  <ul {UL_STYLE}>
    <li><strong>Build.</strong> Roll the land loan into <a href="/blog/construction-financing-ontario/">construction financing in Ontario</a>, where funds advance in draws as the build progresses and the land equity you already hold counts toward your contribution. Many private lenders will structure the land loan with this handoff in mind from day one.</li>
    <li><strong>Refinance.</strong> Once you can document income to bank standards, or once the property has a structure on it, refinance into cheaper institutional money.</li>
    <li><strong>Sell.</strong> Investors banking on rezoning, severance, or appreciation exit by resale; the loan term just needs to outlast the plan.</li>
  </ul>
  <p>Two alternatives worth knowing before you take a land loan at all. If you have significant equity in your current home, a <a href="/blog/heloc-home-equity-loan-gta/">HELOC or home equity loan</a> can fund a land purchase outright, often at a lower rate than a land mortgage, since the security is your house rather than the vacant parcel. And in private sales, some sellers will hold a vendor take-back mortgage, effectively financing you directly, which can bridge a gap when neither bank nor private terms fit.</p>

{faq_html}

  <h2>Financing land through Richview Capital</h2>
  <p><a href="/">Richview Capital</a> is a Woodbridge-based mortgage investment corporation, FSRA-licensed under #13171, lending across Ontario. Land financing is one of our core products, alongside first mortgages from 6.49%, construction loans from 8.99%, with land and bridge financing evaluated case by case, with loans up to $5,000,000 and LTVs up to 75% (case by case). Because we lend our own capital, a complete land file can close in as little as 48 hours.</p>
  <p>If a bank has turned down your land purchase, or your closing date will not wait for one, we can usually tell you the same day whether a deal works. <a href="/borrowers/#contact-form">Send us the property details</a> and we will come back with honest terms, including every cost, before you commit.</p>

  <div class="post-related">
    <h3>Related on this site</h3>
    <ul>
      <li><a href="/blog/construction-financing-ontario/">Construction financing in Ontario</a></li>
      <li><a href="/blog/private-mortgage-ontario/">Private mortgages in Ontario</a></li>
      <li><a href="/blog/heloc-home-equity-loan-gta/">HELOC and home equity loans in the GTA</a></li>
      <li><a href="/blog/private-construction-loan-ontario/">Private construction loan Ontario</a></li>
      <li><a href="/what-is-a-mic/">What is a MIC?</a></li>
      <li><a href="/borrowers/">Borrowing with Richview Capital</a></li>
    </ul>
  </div>

  <div class="post-inline-cta">
    <p class="post-inline-cta-title">Bank said no on your land purchase?</p>
    <p>Send us the property details — we respond same-day on complete applications.</p>
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
