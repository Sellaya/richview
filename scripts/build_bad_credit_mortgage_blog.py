#!/usr/bin/env python3
"""Generate blog/bad-credit-mortgage-ontario/index.html from shell + article data."""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHELL_PATH = REPO / "blog/second-mortgage-ontario/index.html"
OUTPUT_PATH = REPO / "blog/bad-credit-mortgage-ontario/index.html"

SLUG = "bad-credit-mortgage-ontario"
BASE_URL = "https://richviewcapitalmic.com"
PAGE_URL = f"{BASE_URL}/blog/{SLUG}/"
IMAGE_URL = f"{BASE_URL}/images/blog/{SLUG}.jpg"
IMAGE_PATH = f"/images/blog/{SLUG}.jpg"
PUBLISHED = "2026-07-12T09:00:00-04:00"

TITLE = "Bad Credit Mortgage Ontario: A, B and Private Options | Richview Capital MIC"
OG_TITLE = "Bad Credit Mortgage Ontario: A, B and Private Options"
DESCRIPTION = (
    "Declined by your bank? See what score A, B and private lenders in Ontario need "
    "and how equity-based lending can still get you approved."
)
H1 = "Bad credit mortgage in Ontario: your real options after the bank says no"
JSONLD_HEADLINE = "Bad Credit Mortgage in Ontario: Your Real Options After the Bank Says No"
HERO_ALT = "Bad credit mortgage Ontario — declined application with model home and Richview Capital guide"
POST_LEAD = (
    "Declined by your bank? How A, B, and private lenders in Ontario treat bruised credit, "
    "what score each tier expects, and how equity-based approval still works."
)

UL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'
OL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'

EQUIFAX_SCORE = "https://www.equifax.ca/personal/education/credit-score/articles/-/learn/what-is-a-good-credit-score/"
EQUIFAX_RETENTION = "https://www.equifax.ca/personal/education/credit-report/articles/-/learn/how-long-does-information-stay-on-my-credit-report/"
FCAC_REPORT = "https://www.canada.ca/en/financial-consumer-agency/services/credit-reports-score.html"
FCAC_IMPROVE = "https://www.canada.ca/en/financial-consumer-agency/services/credit-reports-score/improve-credit-score.html"
OSFI_B20 = "https://www.osfi-bsif.gc.ca/en/guidance/guidance-library/residential-mortgage-underwriting-practices-procedures-guideline-2019"
CMHC = "https://www.cmhc-schl.gc.ca/professionals/project-funding-and-mortgage-financing/mortgage-loan-insurance/mortgage-loan-insurance-homeownership-programs/cmhc-purchase"
FSRA = "https://www.fsrao.ca/consumers/mortgage-brokering"
BOC = "https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/"

FAQS: list[tuple[str, str]] = [
    (
        "What credit score do you need for a mortgage in Ontario?",
        "Banks generally want roughly 680 or higher, and insured mortgages require at least 600 under CMHC rules. B lenders commonly work down to about 580, while private lenders have no fixed minimum because approval is based on equity rather than score.",
    ),
    (
        "Can I get a mortgage with a 500 credit score in Ontario?",
        "Yes, through equity-based private lending, provided total borrowing stays around 65 to 75 percent of the property's appraised value. The score is reviewed for context, but the equity position drives the decision.",
    ),
    (
        "Can I get a mortgage during an active consumer proposal?",
        "Banks and most B lenders will decline while a proposal is active, but private lenders can approve based on home equity. Many homeowners borrow enough to pay the proposal out in full, which starts the three-year Equifax removal clock sooner.",
    ),
    (
        "How long after bankruptcy can I get a mortgage in Ontario?",
        "Private, equity-based lending is available shortly after discharge if you own property with sufficient equity. B lenders typically want about two years post-discharge with re-established credit, and banks usually take longer.",
    ),
    (
        "Do private lenders check credit at all?",
        "Most pull a credit report, but they use it for context rather than as a pass-fail gate. The decision rests on the property's value and location, the loan-to-value ratio, and your exit plan.",
    ),
    (
        "How fast can a private mortgage close in Ontario?",
        "Days rather than weeks. With a complete file, a direct private lender can fund in as little as 48 hours, which matters most in power of sale situations and purchases with firm closing dates.",
    ),
]

ARTICLE_TAGS = [
    "Bad Credit Mortgage Ontario",
    "Bruised Credit Mortgage",
    "Private Mortgage Bad Credit",
    "Equity-Based Mortgage Approval",
    "B Lender Ontario",
    "Consumer Proposal Mortgage",
    "Bankruptcy Mortgage Ontario",
    "Ontario LTV",
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
                    "Bad credit mortgage",
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
                        "name": "Bad Credit Mortgage in Ontario",
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
        "bad credit mortgage Ontario",
        "bruised credit mortgage",
        "private mortgage bad credit",
        "B lender Ontario",
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
    parts = ["  <h2>Frequently asked questions</h2>"]
    for question, answer in FAQS:
        parts.append(f"  <h3>{escape(question)}</h3>")
        parts.append(f"  <p>{escape(answer)}</p>")
    return "\n".join(parts)


def build_post_prose() -> str:
    faq_html = build_faq_html()
    tags_html = "\n".join(f"    <li>{tag}</li>" for tag in ARTICLE_TAGS)
    return f"""<p class="post-lead-em">A mortgage decline rarely arrives at a convenient time. Maybe a firm closing date is suddenly in doubt, or your renewal is approaching and your bank has changed its mind about you. Or you need to consolidate debt, and the missed payments that created the problem are the same reason the bank will not help you fix it.</p>

  <p>Here is what the decline letter does not tell you: Ontario has three distinct tiers of mortgage lenders, and each treats your credit differently. Banks lend on your score. B lenders lend on your story. Private lenders lend mainly on your equity. A file that gets an automatic &ldquo;no&rdquo; at one tier can be a routine approval at the next.</p>

  <p>This guide covers the whole ladder: what counts as bad credit, what score each tier expects, how equity-based approval works, what it honestly costs, and how borrowers get back to a bank rate. One scope note: this article is about credit problems. If your score is fine but you cannot document income the way a bank wants, see our separate guide to <a href="/blog/self-employed-mortgage-gta/">self-employed mortgages in the GTA</a>.</p>

  <h2>What counts as bad credit in Canada</h2>
  <p>Canadian credit scores run from 300 to 900. {ext(EQUIFAX_SCORE, "Equifax Canada groups scores into five bands")}, and while every lender draws its own lines, the bands are a useful shared vocabulary:</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th>Equifax band</th><th>Score range</th><th>How mortgage lenders tend to see it</th></tr>
      </thead>
      <tbody>
        <tr><td>Excellent</td><td>760 to 900</td><td>Prime borrower, best available pricing</td></tr>
        <tr><td>Very good</td><td>725 to 759</td><td>Prime borrower at most institutions</td></tr>
        <tr><td>Good</td><td>660 to 724</td><td>Generally bankable, may face pricing or condition tweaks</td></tr>
        <tr><td>Fair</td><td>560 to 659</td><td>The classic &ldquo;bruised credit&rdquo; zone; bank declines start here, B lenders live here</td></tr>
        <tr><td>Poor</td><td>300 to 559</td><td>Usually beyond B-lender territory; equity-based private lending becomes the realistic path</td></tr>
      </tbody>
    </table>
  </div>

  <p>Two caveats. Canada has two bureaus, Equifax and TransUnion, and your score can differ between them. More important, lenders read the report behind the number: a 640 caused by one bad year that ended 30 months ago reads very differently than a 640 with fresh lates last month. The {ext(FCAC_REPORT, "Financial Consumer Agency of Canada")} explains what sits in that report: payment history, utilization, account age, public records, and recent credit-seeking activity.</p>

  <h2>Why the bank said no (it is not just the score)</h2>
  <p>Most banks and other prime &ldquo;A&rdquo; lenders want scores in the high 600s or better, and their adjudication is largely automated. Even insured mortgages have a published floor: {ext(CMHC, "CMHC requires at least one borrower on an insured file to have a credit score of 600 or more")}. Below the bank&apos;s internal cutoff there is usually no human to argue with. The system declines, and the conversation ends.</p>

  <h3>The stress test raises the bar further</h3>
  <p>Credit is only half the squeeze. Under {ext(OSFI_B20, "OSFI's Guideline B-20")}, federally regulated lenders must qualify you at the greater of your contract rate plus 2 percent or the minimum qualifying rate of 5.25 percent. The bank is testing a payment meaningfully higher than the one you will actually make, so borrowers with thin credit and stretched ratios often fail the math even when they could carry the real payment.</p>
  <p>The detail that matters here: the stress test binds federally regulated institutions. Private lenders are not required to apply it, and that single difference moves a large share of files from the bank tier to the alternative tiers every year.</p>

  <h2>The three mortgage lender tiers in Ontario</h2>
  <div class="post-table-wrap">
    <table>
      <thead>
        <tr><th></th><th>A lenders</th><th>B lenders</th><th>Private lenders and MICs</th></tr>
      </thead>
      <tbody>
        <tr><td>Who they are</td><td>Banks, most credit unions</td><td>Regulated alternative institutions</td><td>Individuals, syndicates, mortgage investment corporations</td></tr>
        <tr><td>Typical credit expectation</td><td>Roughly 680+</td><td>Roughly 580 to 680</td><td>No fixed minimum; equity-driven</td></tr>
        <tr><td>Approval driven by</td><td>Score, ratios, stress test</td><td>Credit story plus income</td><td>Property value and equity (LTV)</td></tr>
        <tr><td>Rate ballpark</td><td>Lowest available</td><td>About 1 to 2 points above bank rates</td><td>1st from 6.49%*, 2nd from 8.99%*</td></tr>
        <tr><td>Typical fees</td><td>Usually none</td><td>About 1% lender fee</td><td>Lender fee of about 2%, plus broker and legal costs</td></tr>
        <tr><td>Term length</td><td>1 to 5+ years</td><td>1 to 3 years</td><td>Usually 1 year</td></tr>
        <tr><td>Speed</td><td>Weeks</td><td>1 to 3 weeks</td><td>Days; as little as 48 hours</td></tr>
      </tbody>
    </table>
  </div>

  <h3>A lenders: banks and credit unions</h3>
  <p>The prime tier offers the best rates in exchange for the strictest filters: strong scores, clean recent history, documented income, stress-tested ratios. If you are close to bankable, the cheapest fix is often time.</p>

  <h3>B lenders: the bruised-credit specialists</h3>
  <p>B lenders (trust companies and alternative banks) exist for borrowers who narrowly miss bank criteria. They will read a letter of explanation, accept scores into the high 500s, and work with a completed consumer proposal or an older bankruptcy. Expect rates about one to two points above bank pricing, a lender fee of about 1 percent, and one-to-three-year terms designed as a stepping stone back to prime. B lenders still verify income, so a badly damaged score or an active insolvency usually pushes the file to the third tier.</p>

  <h3>Private lenders and MICs: equity-based lending</h3>
  <p>Private lending flips the underwriting model. Instead of asking &ldquo;how reliable is this borrower&apos;s history,&rdquo; it asks &ldquo;how much equity protects this loan.&rdquo; The decision rests mainly on the property&apos;s value, location, and marketability, plus your exit plan. Credit is reviewed for context, not used as a gate.</p>
  <p>Private capital in Ontario comes from individuals, syndicates, and mortgage investment corporations. A MIC pools money from many investors and lends it as mortgages under a defined mandate, which usually means more consistent underwriting and faster decisions than one-off lenders; here is a plain-language explainer on <a href="/what-is-a-mic/">what a mortgage investment corporation is</a>. Transactions at this tier are arranged through brokerages licensed by FSRA, which publishes {ext(FSRA, "consumer guidance on mortgage brokering and private mortgages")}. For a deeper look, see our guide to <a href="/blog/private-mortgage-ontario/">private mortgages in Ontario</a>.</p>

  <h2>What credit score do you need for a mortgage in Ontario?</h2>
  <p>The honest answer is that it depends on the tier:</p>
  <ul {UL_STYLE}>
    <li><strong>680 and above.</strong> Bank territory, assuming income and ratios cooperate. A decline here usually has a non-credit cause worth diagnosing before you pay alternative-lending rates.</li>
    <li><strong>600 to 679.</strong> Bank approval gets inconsistent, especially with recent lates on file. This is prime B-lender range, and insured files remain possible above CMHC&apos;s 600 floor.</li>
    <li><strong>500 to 599.</strong> Most B lenders fade out. Private, equity-based lending becomes the realistic route, and it works fine in this range provided the equity is there.</li>
    <li><strong>Below 500, or no usable score.</strong> Banks and B lenders are effectively unavailable. Private lenders can still approve the file, because the question has changed: it is no longer &ldquo;what is your score&rdquo; but &ldquo;what is your equity.&rdquo;</li>
  </ul>
  <p>That change of question is the most useful thing to understand after a decline, so let us make the math concrete.</p>

  <h2>How equity-based lending works</h2>
  <p>Equity lending is governed by loan-to-value, or LTV: all mortgage debt on the property divided by its appraised value. As a reference point, Richview Capital lends up to 75 percent LTV in the GTA and up to 65 percent on condos and properties outside the GTA, on loans up to $5,000,000.</p>
  <p><strong>A labeled hypothetical.</strong> Suppose a Mississauga homeowner has a house appraised at $900,000 with $520,000 left on the first mortgage, and a 570 score after a rough two years. At 75 percent LTV, total lending capacity is $675,000. Subtract the existing $520,000 and up to $155,000 of equity is accessible, either by refinancing into a new private first mortgage or by adding a <a href="/blog/second-mortgage-ontario/">second mortgage</a> behind the bank loan. The 570 score is still on the file; it just stopped being the deciding factor, because roughly $225,000 of remaining equity protects the loan even after funding.</p>
  <p>On a purchase, the down payment plays the same role. Put 25 percent or more down and the lender is at 75 percent LTV from day one, which is exactly the position equity lenders want, whatever your score says.</p>

  <h2>Getting approved with specific credit problems</h2>

  <h3>Missed payments and maxed-out cards</h3>
  <p>Recent lates and utilization above about 30 percent of your limits are the two fastest score-killers, per {ext(FCAC_IMPROVE, "FCAC's guidance on improving credit")}. Lenders care most about the trend line: lates that stopped six months ago read as recovery. Many equity loans in this situation are structured as debt consolidations, clearing the very cards that drag the score down.</p>

  <h3>Consumer proposals</h3>
  <p>An active proposal is a near-automatic bank decline, and most B lenders want it paid in full first. Private lenders can approve during an active proposal, and homeowners often use equity to pay it out early. On timing: {ext(EQUIFAX_RETENTION, "Equifax removes a completed consumer proposal three years after all debts in it are paid")}, so the sooner it is done, the sooner your file is clean.</p>

  <h3>Bankruptcy</h3>
  <p>B lenders typically want roughly two years since discharge plus re-established credit, such as a secured card used well. Equifax reports a first bankruptcy for six years after discharge, so the score recovers long before the record disappears. Private lending is available sooner, including shortly after discharge, when the property has enough equity.</p>

  <h3>Collections, judgments, and CRA arrears</h3>
  <p>Unpaid collections, judgments, and tax arrears usually block the regulated tiers outright, and CRA debt can turn into liens. Equity lenders handle these files routinely, most often by paying the arrears directly from mortgage proceeds at closing, so the loan solves the problem instead of sitting on top of it.</p>

  <h2>What a bad credit mortgage costs in Ontario</h2>
  <p>Alternative lending costs more, and you should see the numbers before signing anything. Prime-market pricing keys off the {ext(BOC, "Bank of Canada's policy rate")}; private pricing keys off risk and equity. As a reference point, Richview Capital&apos;s first mortgages start at 6.49 percent, second mortgages at 8.99 percent, and bridge financing is evaluated case by case, with a 2 percent lender fee. Budget as well for a broker fee if a brokerage arranges the deal, an appraisal (commonly $400 to $700), and legal costs.</p>
  <p><strong>A labeled hypothetical.</strong> A $400,000 private first mortgage at 6.49 percent, interest only, costs about $2,163 per month. The 2 percent lender fee is $8,000, typically deducted from the advance, so a one-year term runs roughly $34,000 in interest and fees. That is real money, and it only makes sense against the alternative: losing a deposit on a collapsed purchase, carrying $60,000 of credit cards at 20 percent or more, or facing power of sale. Priced against those outcomes, a one-year equity loan is frequently the cheaper option. Priced against a bank mortgage you could actually get, it never is, which is why every private loan should come with an exit plan.</p>

  <h2>The exit plan: from private back to prime</h2>
  <p>A bad credit mortgage is a bridge, not a destination. The pattern that works:</p>
  <ol {OL_STYLE}>
    <li><strong>Months 0 to 6:</strong> every payment on time, on everything. Payment history is the largest single input into your score.</li>
    <li><strong>Months 3 to 12:</strong> rebuild the file. Keep one or two active credit facilities (a secured card works) with utilization under 30 percent, and check both bureau reports for errors.</li>
    <li><strong>Months 12 to 24:</strong> refinance upward. Many borrowers step from private to a B lender, then to an A lender at the following renewal once the score clears the high 600s.</li>
  </ol>
  <p>Short one-year terms at the private tier are not a bug. They exist so you can leave as soon as a cheaper tier will take you.</p>

  <h2>How to improve your approval odds</h2>
  <ul {UL_STYLE}>
    <li><strong>Know your numbers before applying.</strong> A realistic property value, current mortgage balances, and your LTV headroom do more for a private application than your score does.</li>
    <li><strong>Bring the story, unprompted.</strong> A short, honest explanation of what caused the credit damage and why it has stopped carries real weight in case-by-case underwriting.</li>
    <li><strong>Have a use of funds and an exit.</strong> &ldquo;Consolidate $45,000, pay out the proposal, refinance to a B lender in 18 months&rdquo; is a fundable sentence.</li>
    <li><strong>Prepare the basics:</strong> photo ID, current mortgage statement, property tax bill, and a recent appraisal if you have one. With a complete file, Richview provides same-day feedback and can close in as little as 48 hours.</li>
    <li><strong>Work with licensed people.</strong> Verify that anyone arranging your mortgage is FSRA-licensed, and see <a href="/borrowers/">how our borrower process works</a> for what a direct MIC lender will ask of you.</li>
  </ul>

{faq_html}

  <h2>When the score is not the whole story, talk to a lender that knows it</h2>
  <p>After a bank decline, the right question is not &ldquo;how do I fix my score by Friday&rdquo; but &ldquo;what will my equity support today, and what is my path back to prime.&rdquo; Answering that takes a lender that underwrites files one at a time instead of running them through a scorecard.</p>
  <p><a href="/">Richview Capital</a> is a mortgage investment corporation licensed with FSRA (licence #13171), based in Woodbridge and lending across Ontario. We provide equity-based first, second, and bridge mortgages up to $5,000,000, with case-by-case underwriting, same-day feedback, and closings in as little as 48 hours when the clock matters.</p>
  <p>If your bank has said no, your equity may still say yes. <a href="/borrowers/#contact-form">Contact us through our short form</a> and we will give you a straight answer on what your property can support.</p>

  <div class="post-related">
    <h3>Related on this site</h3>
    <ul>
      <li><a href="/blog/private-mortgage-ontario/">Private mortgages in Ontario</a></li>
      <li><a href="/blog/second-mortgage-ontario/">Second mortgage rates and LTV in Ontario</a></li>
      <li><a href="/blog/self-employed-mortgage-gta/">Self-employed mortgages in the GTA</a></li>
      <li><a href="/what-is-a-mic/">What is a MIC?</a></li>
      <li><a href="/borrowers/">Borrowing with Richview Capital</a></li>
    </ul>
  </div>

  <div class="post-inline-cta">
    <p class="post-inline-cta-title">Declined by your bank?</p>
    <p>Tell us about your property and equity — we respond same-day on complete applications.</p>
    <a href="/borrowers/#contact-form">Contact Richview borrowers team</a>
  </div>

  <ul class="post-tags">
{tags_html}
  </ul>

  <p class="post-byline"><strong>Richview Capital MIC</strong> is a licensed Mortgage Investment Corporation (Mortgage Administrator License #13171). This article is educational information for Ontario homeowners — not legal, financial, or tax advice. See <a href="/about-us/">About</a> and <a href="/disclaimer/">Disclaimer</a>.</p>"""


def build_article() -> str:
    return f"""        <article class="post-wrap">
            <div class="container">
                <a href="/blog/" class="post-back"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> Back to Blog</a>
                <p class="post-meta">July 2026 · Borrowers · Ontario</p>
                <h1 class="post-title">{escape(H1)}</h1>

                <figure class="post-hero-figure" aria-label="Article hero image">
                    <img src="{IMAGE_PATH}" width="1024" height="561" alt="{escape(HERO_ALT, quote=True)}" loading="eager" decoding="async">
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
