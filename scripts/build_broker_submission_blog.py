#!/usr/bin/env python3
"""Generate blog/private-mortgage-deal-submission-ontario-2026/index.html from shell + article data."""

from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHELL_PATH = REPO / "blog/private-construction-loan-ontario/index.html"
OUTPUT_PATH = REPO / "blog/private-mortgage-deal-submission-ontario-2026/index.html"

SLUG = "private-mortgage-deal-submission-ontario-2026"
BASE_URL = "https://richviewcapitalmic.com"
PAGE_URL = f"{BASE_URL}/blog/{SLUG}/"
IMAGE_URL = f"{BASE_URL}/images/blog/{SLUG}.jpg"
IMAGE_PATH = f"/images/blog/{SLUG}.jpg"
PUBLISHED = "2026-05-19T09:00:00-04:00"

TITLE = (
    "How to Submit a Private Mortgage Deal in Ontario (2026 Broker Guide) "
    "| Richview Capital MIC"
)
OG_TITLE = "How to Submit a Private Mortgage Deal in Ontario (2026 Broker Guide)"
DESCRIPTION = (
    "A 2026 step-by-step guide for Ontario brokers submitting private mortgage deals "
    "— FSRA Level 2 rules, deal notes, LTV bands, and Form 1.1."
)
H1 = "How to submit a private mortgage deal in Ontario: a broker's 2026 playbook"
JSONLD_HEADLINE = (
    "How to Submit a Private Mortgage Deal in Ontario: A Broker's 2026 Playbook"
)
HERO_ALT = (
    "How to submit a private mortgage deal in Ontario — broker submission playbook 2026"
)
POST_LEAD = (
    "A 2026 Ontario broker playbook for packaging private mortgage files: FSRA Level 2, "
    "Form 1.1, LTV bands, deal notes, and same-day commitments."
)

UL_STYLE = 'style="padding-left:24px; margin-bottom:22px;"'

FAQS: list[tuple[str, str]] = [
    (
        "What is the Mortgage Agent Level 2 licence and do I need it to submit a private mortgage deal in Ontario?",
        "Level 2 is the FSRA licence class introduced in April 2023 that authorizes agents and brokers to deal in private mortgages, including with MICs and individual private lenders. A Level 1 agent cannot legally place a private mortgage in Ontario. Confirm your class before submitting.",
    ),
    (
        "What's the typical LTV for a private mortgage in Ontario in 2026?",
        "First mortgages typically cap at 75% LTV in the GTA and 65% LTV on condominiums and properties outside the GTA. Second mortgages follow the same regional split. Construction loans cap at 65% of end value. All are subject to property type, location, and borrower profile, with a minimum credit score of 600.",
    ),
    (
        "Can I submit a private mortgage deal without Filogix?",
        "Yes. Many Ontario private lenders accept submissions by email directly to a Brokerage Relationship Manager, particularly on time-sensitive files. The package and the deal note still need to be complete.",
    ),
    (
        "How fast can a private lender commit on a complete file?",
        "On a clean file with a strong deal note, a verbal commitment same-day is realistic and a written commitment within 24 hours is the standard. Incomplete files take as long as it takes to complete them.",
    ),
    (
        "What's the difference between a lender fee and a broker fee on a private mortgage?",
        "The lender fee is paid to the lender for arranging the loan and is typically deducted from the advance. The broker fee is paid by the borrower to the brokerage for placing the file. Both must be disclosed on Form 1 and the commitment letter.",
    ),
    (
        "What documents are required for a self-employed (BFS) private mortgage submission?",
        "At minimum: 2 years of NOAs and T1 Generals, business registration or incorporation documents, ownership percentage if applicable, and 12 months of business bank statements. Accountant-prepared financials strengthen the file.",
    ),
    (
        "What is Form 1.1 and when do I have to give it to my client?",
        "Form 1.1 is the FSRA Mortgage Suitability Assessment required for private mortgage transactions. It documents why the private product is suitable for the borrower's situation. It must be completed before the borrower signs the commitment.",
    ),
    (
        "How are private mortgage exit strategies evaluated?",
        "Underwriters look for a credible path to repayment within the term, usually 6–12 months. Refinance to an A or B lender at term end is the most common; sale of the subject or another asset is the second; lump-sum events (inheritance, settlement, business sale) are accepted with supporting evidence.",
    ),
    (
        "What disqualifies a property from private mortgage financing?",
        "Common disqualifiers include environmental concerns, structural issues without remediation plans, properties on private services in remote areas, mixed-use with a high commercial percentage, and incomplete construction without a clear completion plan.",
    ),
]

ARTICLE_TAGS = [
    "Private Mortgage Submission Ontario",
    "FSRA Level 2",
    "Form 1.1",
    "Broker Deal Note",
    "Ontario Private Lender",
    "MIC Broker Guide",
    "Filogix Private Lender",
    "Private Mortgage LTV",
    "BFS Private Mortgage",
    "Richview Capital Brokers",
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
                "articleSection": "Brokers",
                "mainEntityOfPage": {"@type": "WebPage", "@id": PAGE_URL},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{BASE_URL}/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Blog",
                        "item": f"{BASE_URL}/blog/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": "How to Submit a Private Mortgage Deal in Ontario",
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
        ("private mortgage submission"),
        ("FSRA Level 2"),
        ("broker deal note"),
        ("Form 1.1"),
    ]
    article_tags = "\n".join(
        f'    <meta property="article:tag" content="{escape(t, quote=True)}">'
        for t in tags
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
    <meta property="og:image:height" content="562">
    <meta property="og:image:alt" content="{escape(HERO_ALT, quote=True)}">
    <meta property="article:published_time" content="{PUBLISHED}">
    <meta property="article:modified_time" content="{PUBLISHED}">
    <meta property="article:author" content="Richview Capital MIC">
    <meta property="article:section" content="Brokers">
{article_tags}
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(OG_TITLE, quote=True)}">
    <meta name="twitter:description" content="{escape(DESCRIPTION, quote=True)}">
    <meta name="twitter:image" content="{IMAGE_URL}">
    <meta name="twitter:image:alt" content="{escape(HERO_ALT, quote=True)}">
{build_json_ld()}"""


def patch_head(shell: str) -> str:
    start = shell.find("    <title>")
    if start == -1:
        start = shell.find("<title>")
    end = shell.find('<link rel="preconnect"')
    if start == -1 or end == -1:
        raise ValueError("Could not locate head meta block in shell")
    return shell[:start] + build_head_meta_block() + "\n" + shell[end:]


def build_faq_html() -> str:
    parts = ['  <h2>FAQ</h2>']
    for question, answer in FAQS:
        parts.append(f"  <h3>{escape(question)}</h3>")
        parts.append(f"  <p>{escape(answer)}</p>")
    return "\n".join(parts)


def build_post_prose() -> str:
    faq_html = build_faq_html()
    tags_html = "\n".join(f"    <li>{tag}</li>" for tag in ARTICLE_TAGS)
    return f"""<p class="post-lead-em">You have a client whose deal fell out at the bank — self-employed, a credit hiccup two years ago, a condo the institutional lenders do not love, or a closing date too tight for the stress test. You need a private mortgage option, and you need it to move.</p>

  <p>This is the submission playbook for Ontario brokers in 2026. It assumes you already know what a private mortgage is and what the broad value of a <span class="key-term">Mortgage Investment Corporation (MIC)</span> looks like — and instead focuses on the part that actually decides whether your file funds: how to package it, where to send it, what <a href="https://www.fsrao.ca/" target="_blank" rel="noopener noreferrer">FSRA</a> expects in writing, and how to write a deal note that earns a same-day commitment instead of a polite no.</p>

  <p>Most of the submission guides floating around were published before FSRA&apos;s April 2023 rule changes, so parts of them are quietly out of date. This guide on how to submit a private mortgage deal in Ontario is current to 2026 and Ontario-specific.</p>

  <h2>Takeaways</h2>
  <ul {UL_STYLE}>
    <li>Only <span class="key-term">Mortgage Agent Level 2</span> (or full broker) licensees can place private mortgages in Ontario since April 2023.</li>
    <li><span class="key-term">Form 1</span> and <span class="key-term">Form 1.1</span> are mandatory; reference both in your submission notes.</li>
    <li>Typical GTA 1st/2nd caps: <strong>75% LTV</strong> in the GTA, <strong>65%</strong> on condos and outskirts; construction to <strong>65% of end value</strong>.</li>
    <li>A one-page deal note with a credible exit is the fastest path to a same-day commitment.</li>
    <li>Richview publishes starting rates from <strong>6.99%</strong> on 1sts and <strong>10.99%</strong> on 2nds — all subject to approval.</li>
  </ul>

  <h2>What changed in 2026: FSRA Level 2 and the Ontario private deal landscape</h2>
  <p>Two regulatory shifts have reshaped how private mortgage files move in Ontario, and both affect what you do at submission.</p>

  <h3>Who needs Mortgage Agent Level 2 to submit private deals</h3>
  <p>Since April 1, 2023, only mortgage agents and brokers holding the <span class="key-term">Mortgage Agent Level 2</span> (or full broker) licence can deal or trade in mortgages with private lenders, including MICs and individual private investors. A Level 1 agent can no longer place a private mortgage. If you are newer to private lending, confirm your licence class with <a href="https://www.fsrao.ca/consumers/mortgage-brokers-and-agents" target="_blank" rel="noopener noreferrer">FSRA</a> before you submit — and if you are supervising agents, confirm theirs.</p>

  <h3>Form 1 (investor/lender disclosure) and Form 1.1 (suitability assessment)</h3>
  <p>These are non-negotiable for private deals. <span class="key-term">Form 1</span> is the disclosure your client (the borrower) signs acknowledging they understand the terms of a non-institutional mortgage. <span class="key-term">Form 1.1</span> is the suitability assessment documenting why this product fits their situation. Both need to be on file before funding, and both should be referenced in your submission notes so the lender knows you have handled them.</p>

  <h3>FSRA recordkeeping that affects your submission</h3>
  <p>FSRA&apos;s 2025–26 supervision plan continues to emphasize private mortgage transactions, with sample audits ongoing across brokerages. The practical effect at the file level: keep your client correspondence, your suitability rationale, and your disclosure timeline organized from day one. A clean submission file is also a clean audit file.</p>

  <h2>Before you submit: how to qualify a private mortgage deal in Ontario</h2>
  <p>The fastest way to waste two days is to submit a file that was never going to fund. A quick self-screen up front saves you and the lender time.</p>

  <h3>Typical LTV bands for Ontario private 1st and 2nd mortgages</h3>
  <p>Most Ontario private lenders, Richview included, will look at:</p>
  <ul {UL_STYLE}>
    <li><strong>First mortgages:</strong> up to 75% <span class="key-term">LTV</span> on residential property in the GTA; up to 65% LTV on condominiums and properties outside the GTA. Maximum loan amount up to $5,000,000. (For Toronto and GTA specifics, see our <a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">honest GTA private lending guide</a>.)</li>
    <li><strong>Second mortgages:</strong> up to 75% LTV in the GTA; up to 65% on condos and outskirts. Loans up to $1M. Low-LTV files may not require an appraisal.</li>
    <li><strong>Construction loans:</strong> up to 65% of end value, with 3–5 draws per project and 24-hour on-site inspections. See <a href="/blog/private-construction-loan-ontario/">private construction loan Ontario</a>.</li>
    <li><strong>Bridge, land, HELOC, commercial, and refinancing:</strong> all evaluated case by case within the same regional LTV framework.</li>
  </ul>
  <p>Minimum borrower credit score is <strong>600</strong> on every file. Each application is evaluated individually rather than on rigid scorecards.</p>

  <h3>Property types most private lenders fund</h3>
  <p>Residential 1–4 unit owner-occupied and investment properties are the bread and butter. Condos in established buildings, freehold towns, semis, and detached homes all fund routinely. The harder files: rural properties on private services, mixed-use over a certain commercial percentage, properties with environmental concerns, and pre-construction or partially built homes (which usually move to a dedicated <a href="/blog/private-construction-loan-ontario/">private construction loan</a> product). If the property is unusual, flag it in your first email so the lender can quote feasibility before you spend underwriting time.</p>

  <h3>Credit, income, and equity-based decisioning</h3>
  <p>Private mortgages are primarily equity-based, but credit and income still matter for pricing and the exit story. Bruised credit does not kill a deal — an unexplained pattern of derogatory items does. <span class="key-term">BFS</span> income does not kill a deal — vague documentation does. Treat credit and income as inputs to the narrative, not pass/fail gates.</p>

  <h3>Geography</h3>
  <p>Coverage varies by lender. Within the GTA, Hamilton, Niagara, Ottawa, London, and Waterloo region, most Ontario private lenders are active. Farther afield, expect tighter LTVs and longer appraisal timelines. Confirm geography with the lender before you submit.</p>

  <h2>The Ontario private mortgage deal package: what to include</h2>
  <p>Stronger packages get faster commitments. Here is what to put together before you submit.</p>

  <h3>Core documents</h3>
  <ul {UL_STYLE}>
    <li>Mortgage application (Filogix Expert export or the equivalent)</li>
    <li>Credit bureau (Equifax or TransUnion, dated within 30 days)</li>
    <li>Two pieces of government ID (front and back of each — driver&apos;s licence and passport, for example; health cards are not accepted)</li>
    <li>Income proof: T4s, pay stubs (last two), employment letter if employed; NOAs and T1 Generals if self-employed</li>
    <li>90 days of bank statements for income verification</li>
  </ul>

  <h3>Property-specific documents</h3>
  <ul {UL_STYLE}>
    <li>Agreement of Purchase and Sale (for purchases)</li>
    <li>Current mortgage statement (for refinances and 2nd mortgages)</li>
    <li>MLS listing</li>
    <li>Property tax statement</li>
    <li>Status certificate (condos)</li>
    <li>Appraisal (or note who is ordering and ETA)</li>
    <li>Insurance binder if available</li>
  </ul>

  <h3>Self-employed (BFS) extras</h3>
  <ul {UL_STYLE}>
    <li>2 years of NOAs and T1 Generals</li>
    <li>Business registration or articles of incorporation</li>
    <li>Ownership percentage if a partnership or corporation</li>
    <li>12 months of business bank statements (for cash-flow income)</li>
    <li>Accountant-prepared financials, if available</li>
  </ul>

  <h3>Refinance vs. purchase</h3>
  <p>Refinances need the current mortgage statement, payout details, and a clear use of funds (renovation, debt consolidation, business injection, etc.). Purchases need the APS and deposit verification. Both need the exit strategy section in your deal note treated seriously — see below.</p>

  <h3>Common gaps that delay approval</h3>
  <p>The top reasons a file slows down at underwriting: vague BFS income, missing condo status certificate, undisclosed second mortgage already on title, low or stale appraisal, no exit strategy, and broker fee not pre-agreed in writing with the client.</p>

  <h2>How to write a deal note that gets approved fast</h2>
  <p>This is the section most submission guides skip. A strong deal note tells the underwriter what the documents alone do not — who the borrower is, why they need this, and how it ends.</p>

  <h3>The 6 sections every strong deal note covers</h3>
  <ol {UL_STYLE}>
    <li><strong>Borrower snapshot.</strong> Name, age, employment status, marital status and dependents, time in current home or business.</li>
    <li><strong>Loan purpose.</strong> What the money is for, in plain English.</li>
    <li><strong>Property context.</strong> Type, condition, why this property and not another, comparable sales if useful.</li>
    <li><strong>Credit narrative.</strong> Any derogatory items, the why, and what has changed since.</li>
    <li><strong>Income story.</strong> How income is structured, how you have documented it, what supports it.</li>
    <li><strong>Exit strategy.</strong> How the loan ends — sell, refi conventional, refi private, lump sum from inheritance/settlement/asset sale.</li>
  </ol>

  <h3>How to explain derogatory credit without burying the deal</h3>
  <p>State what happened (job loss, illness, business setback, divorce), state when, and state what is different now. Do not editorialize. If multiple items hit the bureau from a single event, say so explicitly. Underwriters can work with a clean explanation; they cannot work with a wall of unexplained R9s.</p>

  <h3>How to frame the exit strategy</h3>
  <p>A credible exit is the single biggest factor in a fast commitment on a 12-month private mortgage. Three credible exits, ranked by underwriter comfort:</p>
  <ol {UL_STYLE}>
    <li>Refinance to A or B lender at term end (state which lender you are targeting and why the client will qualify by then)</li>
    <li>Sale of the subject property or another asset (with realistic timeline)</li>
    <li>Lump sum event (inheritance, settlement, business sale — include supporting evidence if you can)</li>
  </ol>
  <p>&ldquo;Refinance back to a private lender&rdquo; is a valid backup, but it should not be plan A.</p>

  <h3>When to flag risks proactively</h3>
  <p>If the deal has a wrinkle — high TDS, low credit despite explanation, property concerns, atypical income — flag it in the deal note. Underwriters discover everything eventually. Surfacing it early earns trust and often shortens the conditions list.</p>

  <blockquote><p>A note Richview&apos;s underwriting team can act on same-day generally fits on a single page and reads like a real story — not a form. The shortest credible note will cover the six elements above in two or three sentences each, and explicitly name a primary and backup exit.</p></blockquote>

  <h2>Submitting through Filogix vs. directly to your BRM</h2>
  <p>Both channels work. The choice is about speed and complexity.</p>

  <h3>Filogix Expert: step-by-step</h3>
  <ol {UL_STYLE}>
    <li>Open the application in Filogix Expert.</li>
    <li>Under lenders, set lender type to <strong>Private</strong>.</li>
    <li>Select the specific lender (Richview Capital, for Richview deals).</li>
    <li>Attach the deal package and submit.</li>
    <li>Send the deal note as a follow-up email to your assigned BRM with the Filogix reference number.</li>
  </ol>
  <p class="post-filogix-note">When submitting in Filogix Expert, set lender type to <strong>Private</strong> and select your private lender (e.g. Richview Capital).</p>

  <h3>Direct email to your BRM: when it is faster</h3>
  <p>For straightforward files with a tight closing, emailing your Brokerage Relationship Manager directly with the application PDF, deal note, and supporting documents can be faster than the Filogix round-trip. A BRM who knows your book can often issue a verbal commitment within the hour and a written one same-day.</p>

  <h3>What happens in the first hour after you submit</h3>
  <p>A typical sequence on a complete file: the BRM acknowledges receipt, the underwriter reviews the deal note and quick-scans the package, a follow-up email confirms either a verbal commitment with conditions or a list of additional documents needed. Incomplete files stall here. Complete files move.</p>

  <h2>Rates, fees, and broker compensation on Ontario private mortgages</h2>
  <p>Most Ontario MICs publish ranges, not exact rates, because pricing flexes with position, LTV, term, and borrower profile. Here are Richview Capital&apos;s current starting rates and standard lender fees by product, as a benchmark you can quote against:</p>

  <div class="post-table-wrap">
    <table>
      <thead>
        <tr>
          <th>Product</th>
          <th>Starting rate</th>
          <th>Lender fee</th>
          <th>Typical term</th>
          <th>LTV cap</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>First mortgage (purchase)</td><td>from 6.99%</td><td>2%</td><td>6–12 months, up to 3 years</td><td>75% GTA / 65% outskirts &amp; condos</td></tr>
        <tr><td>First mortgage (refinance)</td><td>from 6.99%</td><td>2.25%</td><td>6–12 months, up to 3 years</td><td>75% GTA / 65% outskirts &amp; condos</td></tr>
        <tr><td>Second mortgage (under 65% LTV)</td><td>from 10.99%</td><td>2%</td><td>6–12 months</td><td>75% GTA / 65% outskirts &amp; condos</td></tr>
        <tr><td>Second mortgage (65% LTV+)</td><td>from 11.99%</td><td>2%</td><td>6–12 months</td><td>75% GTA / 65% outskirts &amp; condos</td></tr>
        <tr><td>Land (1st mortgage)</td><td>from 7.99%</td><td>2%</td><td>Case by case</td><td>65% LTV</td></tr>
        <tr><td>Construction (1st mortgage)</td><td>from 9.99%</td><td>2%</td><td>Project term</td><td>65% of end value</td></tr>
        <tr><td>Construction (2nd mortgage)</td><td>from 11.99%</td><td>2%</td><td>Project term</td><td>65% of end value</td></tr>
        <tr><td>Bridge</td><td>from 8.99%</td><td>1–2%</td><td>1–90 days</td><td>Case by case</td></tr>
        <tr><td>HELOC (1st)</td><td>from 7.99%</td><td>2.5%</td><td>Open</td><td>75% GTA / 65% outskirts &amp; condos</td></tr>
        <tr><td>HELOC (2nd)</td><td>from 11.99%</td><td>2.5%</td><td>Open</td><td>75% GTA / 65% outskirts &amp; condos</td></tr>
        <tr><td>Commercial</td><td>from 9.99%</td><td>2%</td><td>Case by case</td><td>Case by case</td></tr>
      </tbody>
    </table>
  </div>
  <p>Maximum loan amount up to <strong>$5,000,000</strong> on residential first mortgages; second mortgages cap at <strong>$1M</strong>. No renewal fee on 3-year terms. All rates subject to change; all mortgages subject to credit approval and appraisal.</p>

  <h3>Broker fee structures and how splits work</h3>
  <p>Most Ontario private mortgage files involve a borrower-paid broker fee, separate from the lender fee, disclosed in writing on <span class="key-term">Form 1</span> and the commitment letter. Standard broker fees on private files range from 1% to 2% of the mortgage amount. The split between brokerage and agent is internal to your brokerage and does not affect the lender or the client.</p>

  <h3>Borrower-paid vs. lender-paid commission — what to disclose under FSRA</h3>
  <p>On a private mortgage, the lender typically does not pay a finder&apos;s fee to the broker the way an A-lender does. Compensation is borrower-paid and must be fully disclosed on Form 1 before the borrower signs the commitment. Do not shortcut this — FSRA reviews disclosure timing in private file audits. Our <a href="/brokers/">broker partnership page</a> outlines how Richview structures these conversations.</p>

  <h2>Timeline: what to expect from submission to funding</h2>
  <p>Richview&apos;s standing commitment to brokers is same-day feedback on every complete application and closing in as little as 48 hours once the file and appraisal are in. The full path on a clean submission looks like this:</p>
  <ul {UL_STYLE}>
    <li><strong>Submission → same-day feedback:</strong> confirmation that the deal is workable, or a clear list of what is needed</li>
    <li><strong>Verbal → written commitment:</strong> typically same day or next morning on complete files</li>
    <li><strong>Conditions satisfied:</strong> depends on appraisal completion and solicitor readiness</li>
    <li><strong>Funding:</strong> as little as 48 hours from a complete file and appraisal</li>
  </ul>
  <p>Closing windows depend on appraisal and solicitor readiness — those are the two variables that most often stretch a 48-hour timeline. Submit through your usual BDM, keep one consolidated email thread per deal, and flag any rush or financing-due dates in the subject line.</p>

  <h2>Common reasons private mortgage deals stall in Ontario (and how to avoid them)</h2>
  <ul {UL_STYLE}>
    <li><strong>Vague BFS income</strong> — fix with NOAs averaged over two years plus 12 months of business bank statements</li>
    <li><strong>No exit strategy</strong> — fix by writing one, even if it is plan A and plan B</li>
    <li><strong>Missing condo status certificate</strong> — order it the day you take the application</li>
    <li><strong>Undisclosed second mortgage on title</strong> — pull title before you submit</li>
    <li><strong>Low or stale appraisal</strong> — coordinate appraisal early; if it is coming in low, get ahead of it with the BRM</li>
    <li><strong>Form 1.1 not completed</strong> — your file is not compliant without it</li>
    <li><strong>Broker not Level 2 licensed</strong> — hand off to a colleague who is, or stop placing private files</li>
  </ul>

  {faq_html}

  <h2>Working with Richview Capital on your next private deal</h2>
  <p>Most of the submission friction in this guide — the deal-note format, the LTV bands, the same-day commitment promise — is what we built Richview Capital around. We are a licensed Ontario <span class="key-term">MIC</span> (Lic #13171), not a broker, and we never compete for your clients. Our process is built so that a clean, complete file gets same-day feedback and can close in as little as 48 hours, with first mortgages from <strong>6.99%</strong>, second mortgages from <strong>10.99%</strong>, and loans up to <strong>$5,000,000</strong> across the GTA.</p>
  <p>If you have a file that fits the bands above and a borrower with a credible story, reach out through your usual BDM or <a href="/brokers/#contact-form">send us your deal directly</a> to start a conversation.</p>

  <div class="post-related">
    <h3>Related on this site</h3>
    <ul>
      <li><a href="/brokers/">Broker partnership with Richview Capital</a></li>
      <li><a href="/blog/private-mortgage-lender-toronto-honest-gta-guide/">Honest GTA private lending guide</a></li>
      <li><a href="/blog/private-construction-loan-ontario/">Private construction loan Ontario</a></li>
      <li><a href="/what-is-a-mic/">What is a MIC?</a></li>
      <li><a href="/faq/">Richview FAQ</a></li>
    </ul>
    <p class="post-external-note"><strong>External resources:</strong>
      <a href="https://www.fsrao.ca/" target="_blank" rel="noopener noreferrer">Financial Services Regulatory Authority of Ontario (FSRA)</a> ·
      <a href="https://www.fsrao.ca/consumers/mortgage-brokers-and-agents" target="_blank" rel="noopener noreferrer">FSRA mortgage brokers and agents</a> ·
      <a href="https://www.fsrao.ca/industry/mortgage-brokering/forms" target="_blank" rel="noopener noreferrer">FSRA mortgage brokering forms (Form 1 / 1.1)</a>
    </p>
  </div>

  <div class="post-inline-cta">
    <p class="post-inline-cta-title">Have a private file ready to submit?</p>
    <p>Send your deal package and deal note — we respond same-day on complete applications.</p>
    <a href="/brokers/#contact-form">Contact Richview broker team</a>
  </div>

  <ul class="post-tags">
{tags_html}
  </ul>

  <p class="post-byline"><strong>Richview Capital MIC</strong> is a licensed Mortgage Investment Corporation (Mortgage Administrator License #13171) and a member of ONMICA. Educational information for Ontario mortgage brokers — not legal or compliance advice. See <a href="/about/">About</a> and <a href="/disclaimer/">Disclaimer</a>.</p>"""


def build_article() -> str:
    return f"""        <article class="post-wrap">
            <div class="container">
                <a href="/blog/" class="post-back"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> Back to Blog</a>
                <p class="post-meta">May 2026 · Brokers · Ontario</p>
                <h1 class="post-title">{escape(H1)}</h1>

                <figure class="post-hero-figure post-hero-figure--object-left" aria-label="Article hero image">
                    <img src="{IMAGE_PATH}" width="1024" height="562" alt="{escape(HERO_ALT, quote=True)}" loading="eager" decoding="async">
                </figure>
                <p class="post-lead">{escape(POST_LEAD)}</p>
                <div class="post-prose">
{build_post_prose()}
                </div>
                <p class="post-cta">Next steps: <a href="/brokers/">Brokers</a> · <a href="/brokers/#contact-form">Submit a deal</a> · <a href="/faq/">FAQ</a></p>
                <p class="post-disclaimer">This article is educational information for Ontario mortgage brokers — not legal, compliance, or tax advice. Rates, fees, LTV limits, and approvals vary by file and underwriting. Products and published ranges are subject to change and are not an offer of credit.</p>
            </div>
        </article>

"""


def build_page(shell: str) -> str:
    marker_article = '<article class="post-wrap">'
    marker_cta = '<section class="cta-section" id="contact">'
    idx_a = shell.find(marker_article)
    idx_c = shell.find(marker_cta)
    if idx_a == -1 or idx_c == -1:
        raise ValueError("Shell markers not found — expected article and contact section")
    pre = patch_head(shell[:idx_a])
    post = shell[idx_c:]
    return pre + build_article() + post


def validate_html(html: str) -> list[str]:
    errors: list[str] = []
    if not html.strip().startswith("<!DOCTYPE html>"):
        errors.append("Missing DOCTYPE")
    if html.count("<html") != 1 or "</html>" not in html:
        errors.append("Invalid html root")
    if "<main id=\"main\">" not in html:
        errors.append("Missing main")
    if f'class="post-title">{escape(H1)}</h1>' not in html:
        errors.append("Missing expected h1")
    if '"@graph"' not in html:
        errors.append("Missing JSON-LD @graph")
    if len(FAQS) != 9:
        errors.append(f"Expected 9 FAQs, got {len(FAQS)}")
    for q, _ in FAQS:
        if f"<h3>{escape(q)}</h3>" not in html:
            errors.append(f"FAQ heading missing: {q[:40]}...")
            break
    if "post-filogix-note" not in html and "Filogix Expert" not in html:
        errors.append("Missing Filogix note")
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
    line_count = len(page.splitlines())
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Lines: {line_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
