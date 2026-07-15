#!/usr/bin/env python3
"""Generate blog/debt-consolidation-mortgage-ontario/index.html from shell + article data."""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHELL_PATH = REPO / "blog/second-mortgage-ontario/index.html"
OUTPUT_PATH = REPO / "blog/debt-consolidation-mortgage-ontario/index.html"

SLUG = "debt-consolidation-mortgage-ontario"
BASE_URL = "https://richviewcapitalmic.com"
PAGE_URL = f"{BASE_URL}/blog/{SLUG}/"
IMAGE_URL = f"{BASE_URL}/images/blog/{SLUG}.jpg"
IMAGE_PATH = f"/images/blog/{SLUG}.jpg"
PUBLISHED = "2026-07-12T09:00:00-04:00"

TITLE = "Debt Consolidation Mortgage in Ontario: Your 2026 Guide | Richview Capital MIC"
OG_TITLE = "Debt Consolidation Mortgage in Ontario: Your 2026 Guide"
DESCRIPTION = (
    "Compare refinancing, second mortgages, HELOCs and private options for a debt consolidation "
    "mortgage in Ontario, including what to do when banks say no."
)
H1 = "Debt consolidation mortgage in Ontario: how to use home equity to pay off high-interest debt"
JSONLD_HEADLINE = (
    "Debt Consolidation Mortgage in Ontario: How to Use Home Equity to Pay Off High-Interest Debt"
)
HERO_ALT = (
    "Debt consolidation mortgage Ontario — home equity solution with model house "
    "and Richview Capital guide"
)
POST_LEAD = (
    "Compare refinancing, second mortgages, HELOCs, and private options to consolidate "
    "high-interest debt with home equity in Ontario."
)

UL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'
OL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'

EQUIFAX = (
    "https://www.equifax.ca/about-equifax/newsroom/-/intlpress/"
    "the-resilient-north-equifax-canada-data-shows-consumers-leaning-on-financial-discipline-"
    "to-offset-macroeconomic-conditions"
)
BOC = "https://www.bankofcanada.ca/2026/06/fad-press-release-2026-06-10/"
FCAC_EQUITY = "https://www.canada.ca/en/financial-consumer-agency/services/mortgages/borrow-home-equity.html"
FCAC_HELOC = "https://www.canada.ca/en/financial-consumer-agency/services/mortgages/home-equity-line-credit.html"
FSRA = "https://www.fsrao.ca/industry/mortgage-brokering"

FAQS: list[tuple[str, str]] = [
    (
        "How much equity do I need for a debt consolidation mortgage in Ontario?",
        "You generally need at least 20 to 25 percent equity in your home. Banks lend to 80 percent of appraised value on a refinance, standalone HELOCs are capped at 65 percent, and private lenders in Ontario typically go up to 75 percent in the GTA and 65 percent for condos or properties outside the GTA.",
    ),
    (
        "Can I get a debt consolidation mortgage if my bank turned me down?",
        "Yes, in many cases. Private lenders and MICs qualify you primarily on home equity rather than credit score or stress-tested income, so a bank decline is not the end of the road. Expect higher rates and a lender fee, and insist on a clear 12 to 24 month exit plan back to a mainstream lender.",
    ),
    (
        "Will consolidating debt into my mortgage hurt my credit score?",
        "There is usually a small short-term dip from the new credit application. After that, paying cards to zero drops your credit utilization sharply, which tends to help your score within months, provided you make the new payment on time and keep the cards from climbing again.",
    ),
    (
        "What debts can I consolidate into a mortgage?",
        "Most types: credit cards, unsecured lines of credit, personal and car loans, payday loans, CRA tax arrears, and collections. Secured debts and government-backed obligations may need specific handling, so raise every debt with your broker or lender up front.",
    ),
    (
        "How fast can a debt consolidation mortgage close in Ontario?",
        "A bank refinance usually takes two to four weeks or more. Private and MIC lenders can move in days, and straightforward files with clear equity can close in as little as 48 hours when the situation is urgent.",
    ),
    (
        "Is a second mortgage or a refinance better for consolidating debt?",
        "Refinancing usually wins on rate but requires breaking your current mortgage, passing the stress test, and possibly paying a large penalty. A second mortgage costs more in rate but preserves a low first-mortgage rate and closes faster. If your existing rate is well below today's market, run the second-mortgage math first.",
    ),
]

ARTICLE_TAGS = [
    "Debt Consolidation Mortgage Ontario",
    "Home Equity Debt Consolidation",
    "Second Mortgage Ontario",
    "HELOC Debt Consolidation",
    "Private Mortgage Ontario",
    "Cash Flow Relief",
    "Ontario LTV",
    "Bank Decline Options",
    "Richview Capital Borrowers",
    "Mortgage Exit Strategy",
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
                    "Debt consolidation",
                    "Home equity",
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
                        "name": "Debt Consolidation Mortgage in Ontario",
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
        "debt consolidation mortgage Ontario",
        "home equity debt consolidation",
        "second mortgage debt consolidation",
        "private mortgage Ontario",
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
    return f"""<p class="post-lead-em">If you own a home in Ontario, there is a good chance you are sitting on two numbers that do not belong together: six figures of home equity and a stack of credit card balances charging 20 percent or more. You are not alone. {ext(EQUIFAX, "Equifax Canada reported")} that total Canadian consumer debt reached $2.66 trillion in the first quarter of 2026, with insolvency volumes at their highest level since 2009, up 18.8 percent year over year. Much of that strain is concentrated among homeowners in Ontario.</p>

  <p>A debt consolidation mortgage in Ontario lets you use the equity in your home to pay off high-interest debts and replace them with one lower-cost, secured payment. It is not right for everyone, and it is not risk-free. But for homeowners bleeding cash flow on cards, loans, and tax arrears, it is often the difference between treading water and actually paying down principal.</p>

  <p>This guide covers all four ways to do it (refinancing, a second mortgage, a HELOC, and private lending when the banks decline), the real math, the full cost picture, and how the process works in Ontario.</p>

  <h2>What is a debt consolidation mortgage?</h2>
  <p>A debt consolidation mortgage is any mortgage or home equity product used to pay off multiple higher-interest debts, leaving you with a single payment secured against your home.</p>
  <p>The strategy works because of the gap between secured and unsecured borrowing costs. Lenders charge less when a loan is registered against real property, because the property protects them if you default. With the {ext(BOC, "Bank of Canada holding its policy rate at 2.25 percent")} as of its June 2026 announcement, prime mortgage rates sit in the low-to-mid 4 percent range, while most retail credit cards still charge 19.99 percent to 22.99 percent regardless of where the policy rate goes.</p>
  <p>That spread is the whole opportunity. Moving $50,000 of debt from 21 percent to even a private-lender rate of 11 or 12 percent cuts your interest cost roughly in half; a bank refinance rate cuts it by three quarters or more.</p>

  <h2>The math: what consolidating debt into your mortgage can save</h2>
  <p>Numbers make this concrete. The following example is hypothetical and for illustration only; figures are rounded and actual rates, payments, and approvals vary by borrower.</p>
  <p>Suppose a Mississauga homeowner has a house worth $850,000 with a $510,000 first mortgage, plus:</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Debt</th><th>Balance</th><th>Rate</th><th>Approx. monthly payment</th></tr>
      </thead>
      <tbody>
        <tr><td>Credit cards</td><td>$32,000</td><td>20.99%</td><td>$960 (minimums)</td></tr>
        <tr><td>Car loan</td><td>$22,000</td><td>8.99%</td><td>$456</td></tr>
        <tr><td>Unsecured line of credit</td><td>$8,000</td><td>11.50%</td><td>$77 (interest only)</td></tr>
        <tr><td><strong>Total</strong></td><td><strong>$62,000</strong></td><td></td><td><strong>$1,493</strong></td></tr>
      </tbody>
    </table>
  </div>

  <p>Here is what consolidating that $62,000 could look like through two different routes:</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Route</th><th>Rate (illustrative)</th><th>New monthly cost of the $62,000</th><th>Monthly cash flow freed</th></tr>
      </thead>
      <tbody>
        <tr><td>Bank refinance, added to mortgage over 25 years</td><td>4.50%</td><td>About $345</td><td>About $1,148</td></tr>
        <tr><td>Private second mortgage, interest only</td><td>8.99%</td><td>About $465</td><td>About $1,028</td></tr>
      </tbody>
    </table>
  </div>

  <p>Two things stand out. First, even the private second mortgage, at more than double the bank rate, frees up over $900 a month compared with juggling the original debts. Second, the bank refinance is cheaper monthly, but stretching $62,000 over 25 years means more total interest unless you use prepayments to clear it faster. A good plan treats the consolidation as a bridge to being debt-free, not a way to make debt feel painless.</p>

  <h2>Four ways to consolidate debt with home equity in Ontario</h2>
  <p>There are four main vehicles, and the right one depends on your existing mortgage rate, your credit profile, and whether a bank will approve you.</p>

  <h3>1. Refinance your existing mortgage (cash-out refinance)</h3>
  <p>Refinancing means breaking your current mortgage and replacing it with a larger one, taking the difference in cash to pay out your debts. The Financial Consumer Agency of Canada confirms you can {ext(FCAC_EQUITY, "borrow up to 80 percent of your home's appraised value")} when refinancing, minus what you still owe.</p>
  <p>This route usually offers the lowest rate. The catches: you must requalify under the federal stress test at the higher of 5.25 percent or your contract rate plus 2 percent, you may face a prepayment penalty for breaking your current term, and if you locked a very low rate in 2020 or 2021, giving it up on your entire balance can cost more than it saves.</p>

  <h3>2. Add a second mortgage</h3>
  <p>A second mortgage is a separate loan registered behind your existing first mortgage. Your first mortgage, including its rate and term, stays untouched. This is often the smarter play for homeowners with a low first-mortgage rate they do not want to break, or a steep penalty they want to avoid.</p>
  <p>Second mortgage rates are higher than first-mortgage rates because the lender is second in line if things go wrong. In the private space, Ontario second mortgages at Richview typically start around 8.99 percent, and many are structured with interest-only payments to maximize monthly cash flow relief. Our guide to getting a <a href="/blog/second-mortgage-ontario/">second mortgage in Ontario</a> covers qualification, costs, and structures in detail.</p>

  <h3>3. Use a HELOC</h3>
  <p>A home equity line of credit is revolving credit secured by your home. Under federal rules, {ext(FCAC_HELOC, "a HELOC on its own is capped at 65 percent of your home's value")}, with combined mortgage-plus-HELOC borrowing capped at 80 percent. Interest is charged only on what you draw, and rates float with prime.</p>
  <p>HELOCs are flexible, which is both the appeal and the danger for debt consolidation. Because the credit stays open after you pay it down, they work best for disciplined borrowers. If revolving credit is part of how the debt built up, a closed, amortizing loan is usually safer. We compare the options in our guide to <a href="/blog/heloc-home-equity-loan-gta/">HELOCs and home equity loans in the GTA</a>.</p>

  <h3>4. Go private when the banks decline</h3>
  <p>Banks decline debt consolidation applications every day, often for reasons that have nothing to do with the logic of the transaction. Private lenders and mortgage investment corporations fill that gap by lending primarily against the equity in the property rather than against a credit score or a pay stub. If that is where you have landed, understanding how <a href="/blog/private-mortgage-ontario/">private mortgages in Ontario</a> work will help you compare offers intelligently.</p>

  <h2>How much equity do you need?</h2>
  <p>Every route comes down to loan-to-value (LTV): total mortgage debt divided by the appraised value of your home. Typical maximums in Ontario look like this:</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Route</th><th>Typical maximum LTV</th></tr>
      </thead>
      <tbody>
        <tr><td>Bank refinance</td><td>80%</td></tr>
        <tr><td>Standalone HELOC</td><td>65%</td></tr>
        <tr><td>Private lending, GTA properties</td><td>Up to 75%</td></tr>
        <tr><td>Private lending, condos and outside the GTA</td><td>Up to 65%</td></tr>
      </tbody>
    </table>
  </div>

  <p>Quick check: multiply your home&apos;s realistic value by the applicable LTV cap, then subtract every mortgage already registered on the property. What is left is roughly your consolidation room. A $900,000 GTA home with a $550,000 first mortgage has about $170,000 of room at 80 percent LTV, or about $125,000 at a private lender&apos;s 75 percent cap.</p>
  <p>As a rule of thumb, you need at least 20 to 25 percent equity for consolidation to be workable, and more for condos or properties outside major centres.</p>

  <h2>When the bank says no: consolidating through a private mortgage</h2>
  <p>Here is the frustrating irony of bank-based debt consolidation: the debts you want to eliminate are often the reason the bank declines you. High balances push your total debt service ratio over the line, high utilization drags your credit score down, and the stress test forces you to qualify at roughly 2 points above your actual rate. Add self-employment income that does not fit neatly on a T4 and many strong homeowners get a no. It is a common story for <a href="/blog/self-employed-mortgage-gta/">self-employed borrowers in the GTA</a> in particular.</p>
  <p>Private lenders approach the file differently. A <a href="/what-is-a-mic/">mortgage investment corporation (MIC)</a> is a pool of investor capital that lends against real estate, and its underwriting is equity-first: the primary questions are what the property is worth, how much is owed against it, and whether there is a sensible exit plan. Bruised credit, a past consumer proposal, or hard-to-document income are workable when the equity is there. For the credit side of the story, see our guide to <a href="/blog/bad-credit-mortgage-ontario/">bad credit mortgages in Ontario</a>.</p>
  <p>Expect honest, transparent costs rather than bank pricing. In the current Ontario market, private first mortgages start around 6.49 percent and second mortgages around 8.99 percent, with lender fees commonly around 2 percent of the loan amount, plus your own legal and appraisal costs. On a $62,000 second mortgage, a 2 percent lender fee is $1,240. That is real money, but weigh it against roughly $12,000 a year of cash flow relief in the example above.</p>

  <h3>The exit strategy matters more than the rate</h3>
  <p>A private consolidation mortgage should be a 12 to 24 month tool, not a permanent home. The plan usually looks like this:</p>
  <ol {OL_STYLE}>
    <li>Consolidate, so every card and loan reports as paid in full.</li>
    <li>Let your credit utilization collapse, which is typically the fastest lever for rebuilding a credit score.</li>
    <li>Make every payment on time for 12 or more months.</li>
    <li>Refinance with an A or B lender at a lower rate, or roll the second mortgage into your first at renewal.</li>
  </ol>
  <p>Any private lender who cannot explain your exit path in the first conversation is not doing their job.</p>

  <h2>Costs and risks to weigh before you consolidate</h2>
  <p>An honest accounting of the downside:</p>
  <ul {UL_STYLE}>
    <li><strong>Your home becomes the collateral.</strong> Unsecured debt becomes secured debt. If you default, the lender has remedies against the property, up to and including power of sale. Only consolidate a payment you can comfortably carry.</li>
    <li><strong>Breaking your mortgage can be expensive.</strong> Fixed-rate prepayment penalties are the greater of three months&apos; interest or the interest rate differential, which can run into five figures. Often a second mortgage beats a refinance for exactly this reason.</li>
    <li><strong>Fees add up.</strong> Appraisal (roughly $300 to $600), legal fees for two sets of counsel on private deals (often $1,500 to $2,500 combined), discharge fees, and lender or broker fees. Get every cost in writing before you sign.</li>
    <li><strong>Longer amortization means more lifetime interest.</strong> A lower monthly payment stretched over 25 years can cost more in total than the ugly debt it replaced. Use prepayment privileges to attack the consolidated balance.</li>
    <li><strong>Consolidation does not fix spending.</strong> If the cards get run back up, you end up with the new mortgage payment plus fresh card debt. Cut limits or close accounts if that risk is real for you.</li>
  </ul>
  <p>When is consolidation the wrong tool? If you plan to sell within a few months, if you could clear the debt within a year by budgeting, or if the debt load is so far beyond your income that no restructuring works. In that last case, talk to a licensed insolvency trustee about options like a consumer proposal first.</p>

  <h2>How the process works in Ontario, step by step</h2>
  <ol {OL_STYLE}>
    <li><strong>Inventory your equity and your debts.</strong> List every balance, rate, and minimum payment. Estimate your home&apos;s value conservatively and calculate your available room using the LTV table above.</li>
    <li><strong>Gather documents.</strong> Mortgage statement, property tax bill, ID, and income documentation. Private lenders need far less income paperwork than banks.</li>
    <li><strong>Choose your route and your lender.</strong> Compare the all-in cost of a refinance, second mortgage, HELOC, and private option, not just the headline rate. In Ontario, verify that any brokerage or lender you deal with is licensed through the {ext(FSRA, "Financial Services Regulatory Authority of Ontario")}, which maintains a public registry.</li>
    <li><strong>Appraisal and approval.</strong> The lender orders an appraisal and issues a commitment letter setting out the rate, fees, and conditions. Read it completely, including the renewal terms.</li>
    <li><strong>Funding and payout.</strong> On closing, lawyers typically pay your creditors directly from the proceeds, which guarantees the debts are actually retired and protects the lender&apos;s position.</li>
  </ol>
  <p>Timelines vary by route. A bank refinance typically takes two to four weeks or longer. Private lenders move much faster; well-prepared Ontario files can close in as little as 48 hours, which matters when a collection action or power of sale notice is on the clock.</p>

{faq_html}

  <h2>Where Ontario homeowners turn when cash flow is the problem</h2>
  <p>Everything above comes down to one question: can you convert expensive, scattered debt into one payment your budget can actually handle, with a clear path back to cheaper financing? For many Ontario homeowners the answer is yes, even after a bank has said no.</p>
  <p><a href="/">Richview Capital</a> is a licensed mortgage investment corporation (FSRA licence #13171) based in Woodbridge that lends across Ontario. We fund debt consolidation through first mortgages from 6.49 percent, second mortgages from 8.99 percent, and HELOC solutions from 7.99 percent (1st) and 8.99 percent (2nd), with loans up to $5,000,000, up to 75 percent LTV (case by case), and closings in as little as 48 hours for time-sensitive files. Our lending decisions are based on your equity and your exit plan, not just your credit score.</p>
  <p>If high-interest debt is eating your monthly budget, <a href="/borrowers/#contact-form">tell us about your numbers</a> and we will walk through your options and the honest all-in cost before you commit to anything.</p>

  <div class="post-related">
    <h3>Related on this site</h3>
    <ul>
      <li><a href="/blog/second-mortgage-ontario/">Second mortgage rates and LTV in Ontario</a></li>
      <li><a href="/blog/heloc-home-equity-loan-gta/">HELOC and home equity loans in the GTA</a></li>
      <li><a href="/blog/private-mortgage-ontario/">Private mortgages in Ontario</a></li>
      <li><a href="/blog/bad-credit-mortgage-ontario/">Bad credit mortgage in Ontario</a></li>
      <li><a href="/what-is-a-mic/">What is a MIC?</a></li>
      <li><a href="/borrowers/">Borrowing with Richview Capital</a></li>
    </ul>
  </div>

  <div class="post-inline-cta">
    <p class="post-inline-cta-title">High-interest debt eating your budget?</p>
    <p>Tell us about your property and debts — we respond same-day on complete applications.</p>
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
