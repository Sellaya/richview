#!/usr/bin/env python3
"""Generate blog/second-mortgage-ontario/index.html from shell + article data."""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHELL_PATH = REPO / "blog/private-mortgage-deal-submission-ontario-2026/index.html"
OUTPUT_PATH = REPO / "blog/second-mortgage-ontario/index.html"

SLUG = "second-mortgage-ontario"
BASE_URL = "https://richviewcapitalmic.com"
PAGE_URL = f"{BASE_URL}/blog/{SLUG}/"
IMAGE_URL = f"{BASE_URL}/images/blog/{SLUG}.jpg"
IMAGE_PATH = f"/images/blog/{SLUG}.jpg"
PUBLISHED = "2026-05-27T09:00:00-04:00"

TITLE = "Second Mortgage in Ontario: Rates, LTV & How to Qualify | Richview Capital MIC"
OG_TITLE = "Second Mortgage in Ontario: Rates, LTV & How to Qualify"
DESCRIPTION = (
    "How second mortgages work in Ontario in 2026: real private rates, LTV limits, costs, "
    "qualifying with bad credit, and exit plans, from a licensed MIC."
)
H1 = "Second mortgage in Ontario: rates, LTV, and how to qualify (2026)"
JSONLD_HEADLINE = "Second Mortgage in Ontario: Rates, LTV, and How to Qualify (2026)"
HERO_ALT = "Second mortgage Ontario — Richview Capital private lender rates and LTV guide 2026"
POST_LEAD = (
    "How a second mortgage works in Ontario in 2026: published rates, LTV limits, costs, "
    "qualifying when a bank says no, and exit strategies — from a licensed MIC."
)

UL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'

FAQS: list[tuple[str, str]] = [
    (
        "What are second mortgage rates in Ontario in 2026?",
        "Private second mortgage rates in Ontario typically run from about 10.99% for lower-LTV files up to the 11.99%+ range for higher-LTV files, plus a lender fee of around 2%. Your exact rate depends on your LTV, property type and location, and the strength of your file.",
    ),
    (
        "How much can I borrow with a second mortgage?",
        "It depends on your equity. Most Ontario lenders cap total mortgages at 75% of value in the GTA and 65% on condos and properties outside the GTA. You subtract your existing first mortgage balance from that limit to find what's available. Second mortgages at Richview go up to $1,000,000.",
    ),
    (
        "Can I get a second mortgage with bad credit in Ontario?",
        "Often yes. Private second mortgages are equity-based, so approval focuses on your home's value and marketability rather than your credit score. A minimum 600 score and sufficient equity are the core requirements, and a clear explanation of any past credit issues helps.",
    ),
    (
        "Does a second mortgage replace my first mortgage?",
        "No. It's a separate loan registered behind your existing first mortgage, which stays in place at its current rate. You access equity without breaking your first mortgage or paying a prepayment penalty.",
    ),
    (
        "How fast can a second mortgage close in Ontario?",
        "On a complete file with an appraisal in hand, a private second mortgage can close quickly. Richview targets same-day feedback and funding in as little as 48 hours. Timelines depend mostly on appraisal and lawyer readiness.",
    ),
    (
        "What's the difference between a lender fee and a broker fee?",
        "The lender fee is paid to the lender for underwriting and funding the loan and is usually deducted from the advance. The broker fee, if you use a broker, is paid by the borrower for sourcing and arranging the deal. Both are disclosed in writing before you sign.",
    ),
    (
        "How do I pay off a second mortgage?",
        "Through your exit strategy, most commonly by refinancing into a single A or B lender mortgage once your credit or income has recovered, or by selling the property. Establish which applies before you borrow.",
    ),
]

ARTICLE_TAGS = [
    "Second Mortgage Ontario",
    "Private Second Mortgage",
    "Ontario LTV",
    "Bad Credit Second Mortgage",
    "Equity-Based Lending",
    "GTA Second Mortgage",
    "Debt Consolidation Mortgage",
    "Richview Capital Borrowers",
    "Private Mortgage Rates 2026",
    "Mortgage Exit Strategy",
]


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
                        "name": "Second Mortgage in Ontario",
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
        "second mortgage Ontario",
        "private second mortgage",
        "Ontario LTV",
        "bad credit mortgage",
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
    <meta property="og:image:height" content="561">
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
    return f"""<p class="post-lead-em">Your bank said no. Maybe a credit hiccup two years ago, self-employed income that&apos;s hard to document, or a debt load the stress test won&apos;t forgive. But you have real equity in your home, and you need to use it. A second mortgage lets you do that without touching the low-rate first mortgage you already have.</p>

  <p>This guide explains how a <span class="key-term">second mortgage in Ontario</span> works in 2026: what it actually costs, how much you can borrow, how to qualify when a bank won&apos;t approve you, and how to pay it back. Unlike most pages on this topic, the rates, fees, and loan-to-value limits below are real published numbers from a licensed Ontario <a href="/what-is-a-mic/">Mortgage Investment Corporation</a>, not vague ranges.</p>

  <h2>What a second mortgage actually is</h2>
  <p>A second mortgage is a separate loan registered on your property&apos;s title behind your existing first mortgage. Your bank stays in first position; the second mortgage sits in second position and gives you access to the equity you&apos;ve built. Critically, it does not replace or break your current mortgage, so you avoid the prepayment penalty that comes with refinancing a first mortgage early, and you keep your existing low rate untouched.</p>
  <p>Most private second mortgages are short-term, typically 6 to 12 months, sometimes up to two years, and many are structured interest-only, which keeps the monthly payment lower because you&apos;re not paying down principal over such a short window. They&apos;re designed to solve a specific problem and then be paid out, not to sit on title for decades.</p>

  <h2>How much can you borrow? Honest Ontario LTV bands</h2>
  <p>The number that decides your loan is <span class="key-term">loan-to-value (LTV)</span>, which is all the debt against your home divided by its appraised value. You&apos;ll see other lenders advertise &ldquo;up to 85% LTV.&rdquo; That&apos;s optimistic for much of Ontario, especially condos. Here&apos;s the realistic framework a disciplined Ontario lender actually uses:</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Property type / location</th><th>Typical max LTV (all mortgages combined)</th></tr>
      </thead>
      <tbody>
        <tr><td>Residential in the GTA (detached, semi, freehold town)</td><td>up to 75%</td></tr>
        <tr><td>Condominiums</td><td>up to 65%</td></tr>
        <tr><td>Properties outside the GTA / outskirts</td><td>up to 65%</td></tr>
      </tbody>
    </table>
  </div>

  <p>Here&apos;s how the math works on a GTA home appraised at $1,000,000 with a $500,000 first mortgage:</p>
  <ul {UL_STYLE}>
    <li>Maximum total lending at 75% LTV: <strong>$750,000</strong></li>
    <li>Less your existing first mortgage: <strong>–$500,000</strong></li>
    <li>Available for a second mortgage: <strong>$250,000</strong></li>
  </ul>
  <p>Second mortgages from Richview cap at <strong>$1,000,000</strong>, with a minimum credit score of <strong>600</strong> and each file assessed individually rather than on a rigid scorecard. Lower-LTV files may not require a full appraisal.</p>

  <h2>Second mortgage rates and fees in Ontario (2026)</h2>
  <p>Private second mortgages cost more than a bank loan because the lender takes on more risk sitting behind your first mortgage. The trade-off is speed, flexibility, and approval based on equity rather than your credit score. Most lenders quote a vague &ldquo;10–15%.&rdquo; Here are Richview&apos;s actual published starting rates and fees so you have a real benchmark:</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Product</th><th>Starting rate</th><th>Lender fee</th><th>Typical term</th><th>LTV cap</th></tr>
      </thead>
      <tbody>
        <tr><td>Second mortgage (under 65% LTV)</td><td>from 10.99%</td><td>2%</td><td>6–12 months</td><td>75% GTA / 65% condos &amp; outskirts</td></tr>
        <tr><td>Second mortgage (65% LTV and above)</td><td>from 11.99%</td><td>2%</td><td>6–12 months</td><td>75% GTA / 65% condos &amp; outskirts</td></tr>
      </tbody>
    </table>
  </div>

  <p>Beyond the rate, budget for these one-time costs, which are standard on any Ontario private second mortgage:</p>
  <ul {UL_STYLE}>
    <li><strong>Lender fee:</strong> around 2% of the loan, typically deducted from the advance rather than paid out of pocket.</li>
    <li><strong>Broker fee (if you use a broker):</strong> usually 1%–2%, also borrower-paid and disclosed in writing before you sign.</li>
    <li><strong>Appraisal:</strong> roughly $350–$500, though low-LTV files may skip it.</li>
    <li><strong>Legal fees:</strong> to register the new mortgage on title.</li>
  </ul>
  <p>On a $100,000 second mortgage with a 2% lender fee, you&apos;d net about $98,000 after that fee, with appraisal and legal costs handled separately. Because Richview is a <a href="/borrowers/">direct MIC lender</a> rather than a broker, there&apos;s no separate broker layer on a deal funded directly. That&apos;s one fewer fee to account for.</p>

  <h2>How to qualify for a second mortgage when the bank says no</h2>
  <p>The single biggest difference between a bank and a private lender: banks are income-focused; private lenders are equity-focused. A bank scrutinizes your credit score and provable income. A private lender&apos;s first question is how much equity you have and whether the property is marketable.</p>
  <p>That&apos;s why a second mortgage works in situations a bank won&apos;t touch:</p>
  <ul {UL_STYLE}>
    <li>Bruised or rebuilding credit (a clean explanation matters more than a perfect score)</li>
    <li>Self-employed or commission income that&apos;s hard to document conventionally</li>
    <li>Recent mortgage, property tax, or CRA arrears</li>
    <li>A debt load that fails the stress test</li>
    <li>A tight closing date a bank can&apos;t meet</li>
  </ul>
  <p>A minimum 600 credit score and genuine equity are the core requirements at Richview. Bruised credit doesn&apos;t kill a deal. An unexplained pattern of missed payments does. The same is true of income: vague documentation slows a file, but a clear story supported by what you have keeps it moving. For more on how equity-based private lending differs from a bank, see Richview&apos;s guide on <a href="/blog/private-mortgage-ontario/">how private mortgages work in Ontario</a>.</p>

  <h2>Second mortgage vs. HELOC vs. refinance</h2>
  <p>Tapping equity isn&apos;t one decision. It&apos;s three options. Here&apos;s how to think about which fits:</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Option</th><th>Best when</th><th>Watch out for</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>Second mortgage</strong></td><td>Your first mortgage has a great rate you don&apos;t want to break, and you need funds fast despite credit/income issues</td><td>Higher rate; short term needs a payoff plan</td></tr>
        <tr><td><strong>HELOC</strong></td><td>You have strong credit/income and want flexible, revolving access</td><td>Banks decline on credit/income; harder to get when you most need it</td></tr>
        <tr><td><strong>Refinance (replace the first)</strong></td><td>Current rates are favourable and you qualify with an A or B lender</td><td>Breaking your first mortgage early can trigger a large penalty</td></tr>
      </tbody>
    </table>
  </div>

  <p>If you have the credit and income to refinance cheaply, do that. If you don&apos;t, or your first mortgage rate is too good to give up, a second mortgage is usually the more sensible tool. Richview&apos;s <a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">honest GTA private lending guide</a> breaks down the rate and LTV trade-offs in more detail.</p>

  <h2>What people use second mortgages for in Ontario</h2>
  <ul {UL_STYLE}>
    <li><strong>Debt consolidation.</strong> Rolling high-interest credit cards into one lower-cost, equity-secured payment to free up monthly cash flow</li>
    <li><strong>Stopping a power of sale or clearing arrears.</strong> Funding to pay off what&apos;s owed and buy breathing room</li>
    <li><strong>Urgent home repairs.</strong> A failed furnace or roof you can&apos;t cover in cash</li>
    <li><strong>Business or investment capital.</strong> Common for self-employed owners whose income is hard to prove to a bank</li>
    <li><strong>Bridging a short-term gap.</strong> Covering a timing mismatch until a sale or refinance closes</li>
  </ul>
  <p>In each of these cases the same principle applies: Richview underwrites on the equity in the property and the strength of your exit, not on a perfect credit score. That&apos;s why a second mortgage can fund when a bank won&apos;t, and why a clean, complete file in the GTA can get same-day feedback and close in as little as 48 hours, with second mortgages starting from <strong>10.99%</strong> and loans up to <strong>$1,000,000</strong>.</p>

  <h2>Your exit strategy: the part that matters most</h2>
  <p>A second mortgage is a bridge, not a destination. Before you sign, you need a realistic plan to pay it off at the end of the term. A responsible lender won&apos;t fund one without it. There are two credible exits:</p>
  <p><strong>Refinance with an A or B lender.</strong> The most common path. You use the 12–24 months to fix whatever kept you from bank financing. Rebuild credit with consistent on-time payments, or build a two-year income history, then refinance into a single, lower-rate mortgage that pays off both your first and second.</p>
  <p><strong>Sell the property.</strong> When the home sells, proceeds pay off the first mortgage, then the second, with the rest of the equity going to you. Common for homeowners already planning to move or downsize.</p>
  <p>Be honest with yourself about which applies before you borrow. A second mortgage with a clear exit solves a problem; one without a plan can postpone it.</p>

  <h2>Risks to weigh</h2>
  <p>A second mortgage is a serious financial tool, not a free fix. The rate is higher than a bank&apos;s, the term is short, and the loan is secured by your home, meaning default has real consequences. It makes sense when it solves a specific problem with a clear payoff plan and the total cost is less than the alternative (breaking a cheap first mortgage, or carrying high-interest unsecured debt). It&apos;s the wrong move if it&apos;s simply adding debt with no path out. If you&apos;re unsure, talk to a licensed lender or a credit counsellor before signing.</p>

  {faq_html}

  <h2>Talk to Richview about your second mortgage</h2>
  <p>What makes a second mortgage work is realistic LTV bands, published rates, and a fast, equity-based decision. That&apos;s what we built <a href="/borrowers/">Richview Capital</a> around. We&apos;re a licensed Ontario Mortgage Investment Corporation (Lic #13171), and because we lend directly, you deal with the people who actually fund your file.</p>
  <p>If you have real equity in a GTA or Ontario home and a clear reason for the funds, we can tell you quickly whether a second mortgage fits, with second mortgages from <strong>10.99%</strong>, loans up to <strong>$1,000,000</strong>, and same-day feedback on a complete application.</p>
  <p>Get in touch with Richview Capital to talk through your options, or read more in our <a href="/faq/">lending FAQ</a>.</p>

  <div class="post-related">
    <h3>Related on this site</h3>
    <ul>
      <li><a href="/what-is-a-mic/">What is a MIC?</a></li>
      <li><a href="/blog/private-mortgage-ontario/">How private mortgages work in Ontario</a></li>
      <li><a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">Honest GTA private lending guide</a></li>
      <li><a href="/borrowers/">Borrowing with Richview Capital</a></li>
      <li><a href="/faq/">Richview FAQ</a></li>
    </ul>
  </div>

  <div class="post-inline-cta">
    <p class="post-inline-cta-title">Have equity and need a second mortgage?</p>
    <p>Tell us about your property and timeline — we respond same-day on complete applications.</p>
    <a href="/borrowers/#contact-form">Contact Richview borrowers team</a>
  </div>

  <ul class="post-tags">
{tags_html}
  </ul>

  <p class="post-byline"><strong>Richview Capital MIC</strong> is a licensed Mortgage Investment Corporation (Mortgage Administrator License #13171). This article is educational information for Ontario homeowners — not legal, financial, or tax advice. See <a href="/about/">About</a> and <a href="/disclaimer/">Disclaimer</a>.</p>"""


def build_article() -> str:
    return f"""        <article class="post-wrap">
            <div class="container">
                <a href="/blog/" class="post-back"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> Back to Blog</a>
                <p class="post-meta">May 2026 · Borrowers · Ontario</p>
                <h1 class="post-title">{escape(H1)}</h1>

                <figure class="post-hero-figure" aria-label="Article hero image">
                    <img src="{IMAGE_PATH}" width="1024" height="561" alt="{escape(HERO_ALT, quote=True)}" loading="eager" decoding="async">
                </figure>
                <p class="post-lead">{escape(POST_LEAD)}</p>
                <div class="post-prose">
{build_post_prose()}
                </div>
                <p class="post-cta">Next steps: <a href="/borrowers/">Borrowers</a> · <a href="/borrowers/#contact-form">Book a consultation</a> · <a href="/faq/">FAQ</a></p>
                <p class="post-disclaimer">Richview Capital MIC is a licensed Mortgage Investment Corporation (Mortgage Administrator License #13171). This article is educational information for Ontario homeowners, not legal, financial, or tax advice. Rates, fees, LTV limits, and approvals vary by file and underwriting, and published ranges are subject to change and are not an offer of credit.</p>
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
    if len(FAQS) != 7:
        errors.append(f"Expected 7 FAQs, got {len(FAQS)}")
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
