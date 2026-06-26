#!/usr/bin/env python3
"""Generate blog/self-employed-mortgage-gta/index.html from shell + article data."""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHELL_PATH = REPO / "blog/second-mortgage-ontario/index.html"
OUTPUT_PATH = REPO / "blog/self-employed-mortgage-gta/index.html"

SLUG = "self-employed-mortgage-gta"
BASE_URL = "https://richviewcapitalmic.com"
PAGE_URL = f"{BASE_URL}/blog/{SLUG}/"
IMAGE_URL = f"{BASE_URL}/images/blog/{SLUG}.jpg"
IMAGE_PATH = f"/images/blog/{SLUG}.jpg"
PUBLISHED = "2026-06-25T09:00:00-04:00"

TITLE = "Self-Employed Mortgage in the GTA: How to Actually Qualify | Richview Capital MIC"
OG_TITLE = "Self-Employed Mortgage in the GTA: How to Actually Qualify"
DESCRIPTION = (
    "Self-employed and worried about a GTA mortgage? Here's how banks, B-lenders, and private MICs "
    "evaluate you, and how to qualify in 2026, with real numbers."
)
H1 = "Self-employed mortgages in the GTA: how to qualify when your income isn't a paycheque"
JSONLD_HEADLINE = "Self-Employed Mortgages in the GTA: How to Qualify When Your Income Isn't a Paycheque"
HERO_ALT = "Self-employed GTA business owner reviewing mortgage options at home"
POST_LEAD = (
    "How banks, B-lenders, and private MICs evaluate self-employed borrowers in the GTA — "
    "what documents you need by tier, what it costs, and how to qualify in 2026."
)

UL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'

FAQS: list[tuple[str, str]] = [
    (
        "Can I get a mortgage if I've only been self-employed for one year?",
        "At a bank, usually not, because most A-lenders want a two-year track record. B-lenders and private lenders are more flexible, and an equity-based MIC mortgage can often proceed with a shorter history if the property and down payment support it.",
    ),
    (
        "Do I really need two years of tax returns?",
        "For the best bank rates, yes. But B-lender bank-statement programs and private/MIC mortgages exist precisely so that borrowers without two years of strong Notices of Assessment still have a path.",
    ),
    (
        "What credit score do I need for a self-employed mortgage?",
        "Banks generally look for scores in the high-600s for their best terms. B-lenders are more lenient, and private lenders may approve on equity even with bruised credit, because the property secures the loan.",
    ),
    (
        "Can I really get approved with no income verification?",
        "On an equity-driven private or MIC mortgage, formal income proof can be light or optional, because approval rests on the property's value and your exit plan. It is not 'no questions asked,' but it does not hinge on reconstructing your income.",
    ),
    (
        "How much can I borrow against my GTA home?",
        "As a rule of thumb, financing commonly reaches about 75% of value in the GTA and around 65% for condos and properties outside the GTA, across your combined mortgages.",
    ),
    (
        "Will I be stuck in a private mortgage?",
        "Not if you plan the exit from the start. Most private mortgages are short-term bridges designed to be refinanced to a bank or B-lender once the issue that triggered them is resolved.",
    ),
]

ARTICLE_TAGS = [
    "Self-Employed Mortgage GTA",
    "Self-Employed Mortgage Ontario",
    "Bank Statement Mortgage Ontario",
    "Stated Income Mortgage Ontario",
    "Private Mortgage Self-Employed",
    "Equity-Based Mortgage Approval",
    "No Income Verification Mortgage Ontario",
    "GTA Private Lender",
    "Richview Capital Borrowers",
    "Mortgage Stress Test Ontario",
]

STATCAN_URL = "https://www150.statcan.gc.ca/n1/pub/71-222-x/71-222-x2019002-eng.htm"
OSFI_URL = "https://www.osfi-bsif.gc.ca/en/supervision/financial-institutions/banks/minimum-qualifying-rate-uninsured-mortgages"
TRREB_URL = "https://trreb.ca/market-data/market-watch/"


def build_json_ld() -> str:
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": JSONLD_HEADLINE,
                "description": (
                    "How banks, B-lenders, and private MICs evaluate self-employed borrowers in the GTA, "
                    "what documents you need by tier, what it costs, and how to qualify in 2026."
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
                    "Self-employed mortgage",
                    "Private mortgage",
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
                        "name": "Self-Employed Mortgages in the GTA",
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
        "self-employed mortgage GTA",
        "self-employed mortgage Ontario",
        "bank statement mortgage Ontario",
        "private mortgage self-employed",
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
    return f"""<p class="post-lead-em">If you run your own business in the Greater Toronto Area, you already know the irony. You can have a healthy bank balance, steady clients, and years of consistent work, and still be treated as a higher risk than a salaried employee earning less than you do. A <span class="key-term">self-employed mortgage in the GTA</span> isn&apos;t out of reach, but the path looks different from the one your employed friends took.</p>

  <p>This guide explains why lenders see your income differently, what your real options are when a bank says no, and how to qualify in 2026 without guesswork.</p>

  <h2>Why lenders treat self-employed income differently</h2>
  <p>A salaried borrower hands over a pay stub and a letter from an employer, and the lender has its answer. Your income is harder to read. It may rise and fall with the seasons, arrive from several clients, or run through a corporation before it reaches you. None of that makes you a worse borrower. It just makes your file take more interpretation.</p>
  <p>The bigger issue is the write-off paradox. Good tax planning lowers your reported income on purpose. Every legitimate deduction you claim shrinks the number a bank uses to qualify you, even though your actual cash flow is much higher. A contractor who nets $180,000 but writes down to $95,000 on paper looks, to an automated underwriting model, like someone earning $95,000.</p>
  <p>You are not a niche case, either. About 2.7 million Canadians were self-employed as of early 2025, roughly 13% of all workers, and more than seven in ten of them run businesses with no employees, according to <a href="{STATCAN_URL}" rel="noopener noreferrer" target="_blank">Statistics Canada</a>. Lenders have built products for exactly this group. The trick is knowing which product fits your situation.</p>
  <p>One thing that does not disappear when you work for yourself is the mortgage stress test. Under the federal banking regulator&apos;s B-20 guideline, a federally regulated lender has to qualify you at the greater of your contract rate plus two percentage points or a 5.25% benchmark floor. In the current rate environment, the &ldquo;rate plus two&rdquo; figure is the one that bites. That math is part of why a strong-cash-flow business owner can still be told no by a bank. See <a href="{OSFI_URL}" rel="noopener noreferrer" target="_blank">OSFI&apos;s minimum qualifying rate guidance</a> for the current benchmark.</p>

  <h2>Can you still qualify? The short answer is yes — and here&apos;s the ladder</h2>
  <p>It helps to stop thinking about approval as a single yes-or-no door and start thinking about it as a ladder. Most self-employed borrowers in the GTA fit on one of three rungs, and many move between them over time.</p>

  <h3>Tier 1: Banks and A-lenders</h3>
  <p>These offer the lowest rates and, often, insured financing, but they ask the most. Expect to show two years of Notices of Assessment (NOAs) and T1 General returns, business financial statements, proof that your taxes are current, and your GST/HST registration if your business earns more than $30,000 a year. A credit score in the high-600s or better and a clean two-year income trend make this rung realistic. If your reported income is strong and your books are tidy, start here.</p>

  <h3>Tier 2: B-lenders</h3>
  <p>B-lenders specialize in borrowers who are solid but don&apos;t tick every bank box. Many run bank-statement or alternative-income programs: instead of leaning only on your tax returns, they review 6 to 12 months of business bank statements, estimate your real income from your deposits, and qualify you on that. Rates sit modestly above bank rates, and the documentation is friendlier to someone whose returns understate their cash flow.</p>

  <h3>Tier 3: Private lenders and MICs</h3>
  <p>When timing is tight, credit is bruised, or income simply can&apos;t be documented in a way the first two rungs accept, private lenders and mortgage investment corporations lend against the property itself. Approval rests on your equity, the property, and a sensible exit plan rather than on reconstructing your income. This is the rung where a self-employed borrower who has been declined elsewhere can still move forward, and it&apos;s worth understanding <a href="/blog/private-mortgage-ontario/">how private mortgages work in Ontario</a> before you choose it.</p>
  <p>The ladder matters because it reframes a rejection. Being declined by a bank is not a verdict on whether you can own or keep a home. It usually just means you&apos;re on the wrong rung for right now.</p>

  <h2>How a private lender or MIC actually evaluates your file</h2>
  <p>Because <a href="/">Richview Capital</a> is a lender rather than a broker, it&apos;s worth explaining what actually happens to a self-employed file on the private rung, since the logic is different from a bank&apos;s.</p>
  <p>A <a href="/what-is-a-mic/">mortgage investment corporation (MIC)</a> is a regulated pool of investor capital that lends on real estate and is secured against property. When a MIC looks at your application, the central question is not &ldquo;what&apos;s your reported income&rdquo; but &ldquo;how protected is this loan by the asset.&rdquo; Four things drive the decision:</p>
  <ul {UL_STYLE}>
    <li><strong>Equity and loan-to-value (LTV).</strong> How much of the property&apos;s value the loan represents. In the GTA, financing commonly goes up to about 75% LTV; for condominiums and properties outside the GTA, the ceiling is typically nearer 65%, because those assets can be more volatile to resell.</li>
    <li><strong>The property itself.</strong> Type, condition, and location. A detached home in an established GTA neighbourhood supports more flexible lending than a rural property or an unusual build.</li>
    <li><strong>Position.</strong> Whether the loan is a first mortgage or a second mortgage sitting behind an existing one, which affects risk and rate.</li>
    <li><strong>Exit strategy.</strong> How and when the loan gets repaid or refinanced. A clear plan is often the difference between an approval and a decline.</li>
  </ul>
  <p>For a self-employed borrower, this is the appeal: the approval leans on the value you&apos;ve already built in the property, not on a tax return that hides your true earnings.</p>

  <h2>What documents you&apos;ll actually need, by tier</h2>
  <p>The paperwork drops sharply as you move down the ladder.</p>
  <p><strong>For a bank,</strong> prepare two years of NOAs and T1 Generals, business financial statements, evidence your income taxes and any HST are paid up, your business registration or articles of incorporation, and standard ID and down-payment confirmation.</p>
  <p><strong>For a B-lender,</strong> the centrepiece is usually 6 to 12 months of business bank statements, plus your most recent NOA to confirm you don&apos;t owe taxes, and basic business documentation.</p>
  <p><strong>For a private lender or MIC,</strong> the focus shifts to the property: details of the home, a recent mortgage statement, the property tax bill, valid ID, and a short, credible exit plan. Formal income proof is light or, on equity-driven files, sometimes optional. That&apos;s the practical meaning of a &ldquo;no income verification&rdquo; or &ldquo;stated income&rdquo; mortgage: the property carries the file.</p>

  <h2>What it costs in the GTA: rates, fees, LTV, and down payment</h2>
  <p>Cost rises as you move down the ladder, and that trade-off is the honest core of this decision. Banks offer the lowest rates. B-lenders charge a little more. Private and MIC mortgages carry the highest rates plus a one-time lender fee (commonly around 1–2% of the loan), shorter terms (often one year), and interest-focused payments. You are paying for speed, flexibility, and an approval the lower rungs wouldn&apos;t give.</p>
  <p>GTA property values are what make the equity rung so useful here. The average GTA selling price was about $1.07 million in May 2026, per the <a href="{TRREB_URL}" rel="noopener noreferrer" target="_blank">Toronto Regional Real Estate Board</a>. Even a conservative loan-to-value frees up meaningful funds against that kind of equity.</p>
  <p>Consider an illustrative example. Suppose you own a Vaughan home worth $1.1 million with a $500,000 first mortgage, and you need $150,000 to cover a tax bill and stabilize cash flow during a slow quarter. A private second mortgage would put your combined borrowing at $650,000, or roughly 59% of the home&apos;s value, comfortably inside typical GTA limits. At an illustrative 11% interest-only rate plus a 2% lender fee, you&apos;d pay about $1,375 a month in interest and a $3,000 fee, with the principal due when you refinance or sell. Those figures are a worked hypothetical, not a quote, but they show how the math is shaped by equity rather than by your tax return. If a second mortgage is the right structure for you, it&apos;s worth understanding <a href="/blog/second-mortgage-ontario/">how second mortgages are priced and qualified in Ontario</a>.</p>

  <h2>Using a private or MIC mortgage the smart way: the exit strategy</h2>
  <p>A private mortgage is a tool, and like any tool it works best for a specific job. The job here is usually a bridge: solve the immediate problem, then move back up the ladder to cheaper money once you can.</p>
  <p>That plan might be to close a purchase now and refinance to a B-lender in 12 months once you have a second strong year of statements; to clear CRA arrears or a tax lien that&apos;s blocking a bank approval, then qualify cleanly; or to season your income for a year so the two-year average a bank wants finally looks the way your business actually performs. The point is to enter a private mortgage with the exit already sketched, not to drift in it. A reputable lender will talk through that exit with you before funding, because a loan with no way out is bad for both sides.</p>

  <h2>Self-employed scenarios we see across the GTA</h2>
  <p>These are common, illustrative situations rather than specific clients, but they show how the ladder plays out in practice.</p>
  <ul {UL_STYLE}>
    <li><strong>The incorporated owner with strong cash flow and low reported income.</strong> Books show $90,000; the business clears far more. A bank balks at the reported figure, but a B-lender&apos;s bank-statement program reads the real deposits and approves the file.</li>
    <li><strong>The contractor with a firm closing date and thin documentation.</strong> A purchase has to close in two weeks and there isn&apos;t time to assemble two years of pristine financials. A private first mortgage funds the purchase on the strength of the down payment and property, with a plan to refinance to an A- or B-lender within the year.</li>
    <li><strong>The freelancer refinancing to consolidate.</strong> A commission earner wants to pay off high-interest debt and a tax bill using home equity. An equity-based refinance or second mortgage clears the balances at a far lower rate than the cards, improving monthly cash flow and, often, credit over time. For a fuller picture of who lends and what to watch for, this <a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">honest guide to private mortgage lenders in the GTA</a> is a useful companion read.</li>
  </ul>

  {faq_html}

  <h2>Talk to a lender who underwrites self-employed files directly</h2>
  <p><a href="/">Richview Capital</a> is a licensed Ontario mortgage investment corporation that lends its own capital on residential real estate across the GTA, so a self-employed application is reviewed by the people who actually make the decision, not passed down a chain. Approvals are equity-based and evaluated case by case, with same-day feedback and closings in as little as 48 hours when the file is ready.</p>
  <p>If a bank has said no, or you simply want to understand which rung of the ladder fits your situation, it&apos;s worth a conversation before you assume the answer. You can review Richview&apos;s <a href="/borrowers/">financing options for Ontario borrowers</a> and reach out for a no-obligation review of your file.</p>

  <div class="post-related">
    <h3>Related on this site</h3>
    <ul>
      <li><a href="/blog/private-mortgage-ontario/">How private mortgages work in Ontario</a></li>
      <li><a href="/what-is-a-mic/">What is a MIC?</a></li>
      <li><a href="/blog/second-mortgage-ontario/">Second mortgage rates and LTV in Ontario</a></li>
      <li><a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">Honest GTA private lending guide</a></li>
      <li><a href="/borrowers/">Borrowing with Richview Capital</a></li>
    </ul>
  </div>

  <div class="post-inline-cta">
    <p class="post-inline-cta-title">Self-employed and need a mortgage path?</p>
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
