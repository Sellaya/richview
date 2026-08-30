#!/usr/bin/env python3
"""Publish Richview SEO Batch 3 articles from client markdown + hero images."""

from __future__ import annotations

import json
import re
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

from blog_image_utils import BLOG_CARD_IMAGE_CLASS, BLOG_CARD_THUMB_CLASS, export_hero, export_hero_placeholder

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
    {
        "slug": "newcomer-mortgage-canada-ontario",
        "md": BATCH_ROOT
        / "richview-capital-newcomer-mortgage-ontario-20260816"
        / "Newcomer Mortgage Canada- The Ontario Guide to Buying Without a Canadian Credit.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (3).jpeg",
        "title": "Newcomer Mortgage Canada: Ontario Guide for New Arrivals | Richview Capital MIC",
        "og_title": "Newcomer Mortgage Canada: Ontario Guide for New Arrivals",
        "description": (
            "Newcomer mortgage Canada guide for Ontario: qualify with no credit history, "
            "compare bank programs, B lenders and private lenders, then exit to prime."
        ),
        "h1": "Newcomer Mortgage Canada: The Ontario Guide to Buying Without a Canadian Credit History",
        "jsonld_headline": "Newcomer Mortgage Canada: The Ontario Guide to Buying Without a Canadian Credit History",
        "breadcrumb": "Newcomer Mortgage Canada",
        "hero_alt": (
            "Newcomer couple reviewing mortgage documents with a mortgage advisor in Ontario — "
            "Richview Capital guide to buying without Canadian credit history"
        ),
        "published": "2026-08-18T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "Newcomer Mortgage Canada",
            "New to Canada Mortgage Ontario",
            "Mortgage No Credit History",
            "Private Mortgage Newcomers",
            "CMHC Newcomers",
            "Work Permit Mortgage Canada",
            "Richview Capital Borrowers",
            "Ontario Newcomer Home Buying",
        ],
        "faqs": [
            (
                "Can I get a mortgage in Canada with no credit history?",
                "Yes. Insurer programs from CMHC, Sagen, and Canada Guaranty let banks accept international credit reports or 12 months of rent and bill payment history instead of a Canadian score. If those programs do not fit, B lenders and private lenders qualify you on income and equity rather than credit.",
            ),
            (
                "Can I get a mortgage on a work permit in Canada?",
                "Yes, work permit holders can qualify through newcomer insurance programs, B lenders, or private lenders. Expect a larger down payment than a permanent resident would need, and be ready to show meaningful time remaining on your permit or evidence of a PR application in progress.",
            ),
            (
                "How much down payment does a newcomer need?",
                "Permanent residents can put down as little as 5 percent on the first $500,000 and 10 percent on the portion above that, with mortgage default insurance. Work permit holders usually need 10 percent or more, and private lenders typically want 20 to 35 percent equity.",
            ),
            (
                "Do private lenders check credit?",
                "Most pull a credit report, but it is rarely the deciding factor. Private lending decisions rest on the property's value and marketability, your down payment or equity, and a credible exit plan, which is why a blank Canadian credit file is not a barrier.",
            ),
            (
                "How long before I can refinance into a bank mortgage?",
                "Typically 12 to 24 months. You need two active credit tradelines reporting for at least a year, on-time payment history, a filed Canadian tax return, and stable employment past probation. Many newcomers refinance at the end of a 1 year private term or shortly after.",
            ),
            (
                "Can I use money from overseas for my down payment?",
                "Yes, foreign funds are accepted, but anti-money-laundering rules require a full paper trail: 90 days of account history, wire transfer records, and source-of-funds documentation. Transfer the money to a Canadian account well before you apply to avoid delays.",
            ),
        ],
        "card_title": "Newcomer Mortgage Canada: The Ontario Guide to Buying Without a Canadian Credit History",
        "card_excerpt": "Bank newcomer programs, B lenders, and private bridges — plus AML docs and the exit plan back to prime.",
    },
    {
        "slug": "reverse-mortgage-alternatives-canada",
        "md": BATCH_ROOT
        / "richview-capital-reverse-mortgage-alternatives-ontario-20260816"
        / "Reverse Mortgage Alternatives in Canada- What Ontario Homeowners 55+ Should.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (4).jpeg",
        "title": "Reverse Mortgage Alternatives in Canada: Ontario Guide | Richview Capital MIC",
        "og_title": "Reverse Mortgage Alternatives in Canada: Ontario Guide",
        "description": (
            "Reverse mortgage alternatives in Canada compared with real cost math: HELOCs, "
            "private seconds, refinancing and downsizing for Ontario homeowners 55+."
        ),
        "h1": "Reverse Mortgage Alternatives in Canada: What Ontario Homeowners 55+ Should Compare First",
        "jsonld_headline": "Reverse Mortgage Alternatives in Canada: What Ontario Homeowners 55+ Should Compare First",
        "breadcrumb": "Reverse Mortgage Alternatives in Canada",
        "hero_alt": (
            "Ontario couple aged 55+ comparing reverse mortgage alternatives at their kitchen table — "
            "Richview Capital guide to home equity options"
        ),
        "published": "2026-08-24T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "Reverse Mortgage Alternatives Canada",
            "Reverse Mortgage Ontario",
            "HELOC Seniors Ontario",
            "Private Second Mortgage Seniors",
            "Home Equity Options 55+",
            "Downsizing vs Reverse Mortgage",
            "Richview Capital Borrowers",
            "Ontario Retirement Lending",
        ],
        "faqs": [
            (
                "What is the biggest downside of a reverse mortgage in Canada?",
                "Compounding interest with no payments. At current rates in the mid-6 percent range, the balance roughly doubles every 11 years, so a long stay in a flat housing market can consume most of your remaining equity. Setup costs and prepayment charges add to the drag if you exit early.",
            ),
            (
                "How much can I borrow with a reverse mortgage at 55?",
                "Far less than the advertised maximum. The 55 percent ceiling generally applies to the oldest borrowers, while applicants in their late 50s are commonly offered a much smaller percentage. If the offer is too low, an equity-based private mortgage can usually reach a higher combined loan-to-value.",
            ),
            (
                "Can I get a HELOC in retirement on CPP and OAS income?",
                "Sometimes, but banks stress test HELOC applications against income, and government benefits alone often fall short even when the home is mortgage-free. Strong pension or investment income improves your odds. If declined, your equity-based options are a reverse mortgage or a private mortgage.",
            ),
            (
                "Are private second mortgages safe for seniors?",
                "They are legitimate loans arranged through licensed lenders and brokers, but they are short-term tools with higher rates and fees, typically from about 9 percent plus 2 to 4 percent in costs. They are safest with a clear exit, such as a planned sale, an estate settlement, or a future refinance, and reputable lenders document that exit up front.",
            ),
            (
                "What happens if I sell my home after taking a reverse mortgage?",
                "The balance, including all accrued interest, is repaid from the sale proceeds, and you keep the rest. If you sell during a closed term, prepayment charges usually apply, and they are steepest in the first few years. Ask for the full prepayment schedule in writing before you sign.",
            ),
            (
                "Is downsizing better than a reverse mortgage?",
                "Financially, usually yes: you pay one-time selling costs of roughly 5 to 7 percent instead of years of compounding interest, and you free all of your equity. The trade-off is personal, since downsizing means leaving your home and possibly your neighbourhood. Paying more to stay is a valid choice as long as it is an informed one.",
            ),
        ],
        "card_title": "Reverse Mortgage Alternatives in Canada: What Ontario Homeowners 55+ Should Compare First",
        "card_excerpt": "Real cost math on HELOCs, private seconds, refinancing, and downsizing vs a reverse mortgage for Ontario homeowners 55+.",
    },
    {
        "slug": "brrrr-method-canada-financing-ontario",
        "md": BATCH_ROOT
        / "richview-capital-brrrr-refinance-rental-ontario-20260816"
        / "The BRRRR Method in Canada- How to Finance Every Stage in Ontario.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (5).jpeg",
        "title": "BRRRR Method Canada: Financing Every Stage in Ontario | Richview Capital MIC",
        "og_title": "BRRRR Method Canada: Financing Every Stage in Ontario",
        "description": (
            "How the BRRRR method works in Canada in 2026: financing each stage in Ontario, "
            "why banks stall the refinance step, DSCR math, and realistic GTA numbers."
        ),
        "h1": "The BRRRR Method in Canada: How to Finance Every Stage in Ontario",
        "jsonld_headline": "The BRRRR Method in Canada: How to Finance Every Stage in Ontario",
        "breadcrumb": "The BRRRR Method in Canada",
        "hero_alt": (
            "Renovated bungalow with a legal basement suite entrance — "
            "typical BRRRR method investment property in the GTA, Richview Capital"
        ),
        "published": "2026-08-24T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "BRRRR Method Canada",
            "Refinance Rental Property Ontario",
            "Investment Property Private Lender",
            "DSCR Rental Qualification",
            "GTA Investment Property 2026",
            "Private Mortgage BRRRR",
            "Richview Capital Borrowers",
            "Ontario Rental Refinance",
        ],
        "faqs": [
            (
                "Does the BRRRR method still work in Canada in 2026?",
                "Yes, but the math has changed. With GTA prices down 4.5 percent year over year, expect partial capital recovery on refinance rather than the full recovery common in rising markets. The strategy still builds equity and cash flow; it just requires more starting capital per cycle.",
            ),
            (
                "Why will my bank not refinance my rental property in Ontario?",
                "Banks must qualify you at the OSFI minimum qualifying rate, the greater of your contract rate plus 2 percent or 5.25 percent, and they discount rental income to 50 to 80 percent of its actual amount. Add caps on financed properties and 6 to 12 month seasoning requirements, and many profitable rentals fail bank math. Alternative lenders qualifying on the property's own income are the usual solution.",
            ),
            (
                "What is DSCR-style rental qualification?",
                "DSCR is the debt service coverage ratio: the property's net rental income divided by its proposed mortgage payment. Most alternative rental programs want roughly 1.1, meaning the rent covers the mortgage with about 10 percent to spare. The property qualifies on its own income rather than on your salary and stress-tested debts.",
            ),
            (
                "What does a private lender charge on a BRRRR purchase?",
                "Typical Ontario private first mortgages on investment properties run roughly 8 to 12 percent interest-only, with combined lender and broker fees of 2 to 4 percent, on 6 to 12 month terms at 65 to 80 percent loan-to-value. Pricing depends on the property, location, leverage, and the strength of the renovation and exit plan.",
            ),
            (
                "How is BRRRR different from a fix and flip?",
                "A flip ends in a sale, so profit is realized immediately and the financing needs only a short-term structure. BRRRR ends in a refinance and a hold, so returns arrive as recovered capital, rental cash flow, and long-term equity, and the deal requires a viable takeout mortgage planned from the start.",
            ),
            (
                "How soon can I refinance after renovating?",
                "Many banks want 6 to 12 months of ownership before lending against a new appraised value. Alternative and private lenders are generally more flexible and may refinance soon after the renovation is complete and the units are leased. Confirm the takeout lender's seasoning policy before you buy.",
            ),
        ],
        "card_title": "The BRRRR Method in Canada: How to Finance Every Stage in Ontario",
        "card_excerpt": "Finance every BRRRR stage in Ontario: why banks stall the refinance, DSCR math, and realistic 2026 GTA numbers.",
    },
    {
        "slug": "interest-only-mortgage-canada",
        "md": BATCH_ROOT
        / "richview-capital-interest-only-mortgage-ontario-20260816"
        / "Interest Only Mortgage in Canada- How It Works, the Math, and When It Makes.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (6).jpeg",
        "title": "Interest Only Mortgage Canada: Payments, Uses and Risks | Richview Capital MIC",
        "og_title": "Interest Only Mortgage Canada: Payments, Uses and Risks",
        "description": (
            "How interest only mortgages work in Canada, who offers them, real payment math vs "
            "amortizing loans, and when they make sense for Ontario borrowers."
        ),
        "h1": "Interest Only Mortgage in Canada: How It Works, the Math, and When It Makes Sense",
        "jsonld_headline": "Interest Only Mortgage in Canada: How It Works, the Math, and When It Makes Sense",
        "breadcrumb": "Interest Only Mortgage in Canada",
        "hero_alt": (
            "Interest-only mortgage payment schedule and calculator on a desk in Ontario — "
            "Richview Capital guide to how payment math works in Canada"
        ),
        "published": "2026-08-24T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "Interest Only Mortgage Canada",
            "Interest Only Mortgage Ontario",
            "Interest Only Private Mortgage",
            "HELOC Interest Only",
            "Private Lender Interest Only",
            "Bridge Mortgage Ontario",
            "Richview Capital Borrowers",
            "Interest Only Payment Math",
        ],
        "faqs": [
            (
                "Can you get an interest-only mortgage in Canada?",
                "Yes, but availability is narrow. The main sources are private lenders and mortgage investment corporations, which commonly structure loans as interest-only with terms around a year, and HELOCs from banks and credit unions, which allow interest-only minimum payments on the revolving portion.",
            ),
            (
                "Do the big banks offer interest-only mortgages?",
                "Not as stand-alone residential term mortgages. The closest bank product is the HELOC, where OSFI rules cap the interest-only revolving portion at 65 percent of the home's value and full income and stress-test qualification applies.",
            ),
            (
                "Is a HELOC the same as an interest-only mortgage?",
                "No, but it behaves like one if you pay only the minimum. A HELOC is revolving credit secured by your home with interest-only minimum payments, while a private interest-only mortgage is a fixed-amount term loan. The HELOC is usually cheaper but much harder to qualify for.",
            ),
            (
                "What does an interest only private mortgage cost?",
                "Expect a rate meaningfully above bank pricing, with first mortgages typically in the high single digits to low double digits and second mortgages higher, plus lender and broker fees. In Ontario, all rates and fees must be disclosed to you by an FSRA-licensed broker before you commit.",
            ),
            (
                "What happens at the end of an interest-only term?",
                "You still owe the full original balance, so you need an exit: sell the property, refinance with a bank or other lender, or renew the private term. The exit should be planned before the loan is funded, not at maturity.",
            ),
            (
                "Can I pay down principal on an interest-only mortgage if I want to?",
                "Usually yes. Most interest-only loans set interest as the minimum payment but allow voluntary principal prepayments, subject to the terms of the specific agreement. Confirm the prepayment provisions before signing.",
            ),
        ],
        "card_title": "Interest Only Mortgage in Canada: How It Works, the Math, and When It Makes Sense",
        "card_excerpt": "Who offers interest-only mortgages in Canada, real payment math vs amortizing loans, and when they make sense.",
    },
    {
        "slug": "garden-suite-financing-ontario",
        "md": BATCH_ROOT
        / "richview-capital-garden-suite-adu-financing-ontario-20260816"
        / "Garden Suite Financing in Ontario- How to Fund a Laneway Home or Secondary Suite.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.29.jpeg",
        "title": "Garden Suite Financing Ontario: Costs, Loans & Options | Richview Capital MIC",
        "og_title": "Garden Suite Financing Ontario: Costs, Loans & Options",
        "description": (
            "What a garden suite or laneway home costs to build in Ontario, the $80,000 federal "
            "loan at 2 percent, refinance rules, and financing options that work."
        ),
        "h1": "Garden Suite Financing in Ontario: How to Fund a Laneway Home or Secondary Suite",
        "jsonld_headline": "Garden Suite Financing in Ontario: How to Fund a Laneway Home or Secondary Suite",
        "breadcrumb": "Garden Suite Financing in Ontario",
        "hero_alt": (
            "Modern garden suite in a Toronto backyard at dusk — "
            "Richview Capital guide to laneway and secondary suite financing in Ontario"
        ),
        "published": "2026-08-24T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "Garden Suite Financing Ontario",
            "Laneway House Financing",
            "Secondary Suite Loan Ontario",
            "ADU Financing Canada",
            "Canada Secondary Suite Loan Program",
            "CMHC Secondary Suite Refinance",
            "Richview Capital Borrowers",
            "Toronto Garden Suite Costs",
        ],
        "faqs": [
            (
                "Is the Canada Secondary Suite Loan Program open for applications?",
                "The program was announced in Budget 2024 and enhanced in the 2024 Fall Economic Statement to offer up to $80,000 at 2 percent over 15 years, with launch planned for early 2025. Application details have rolled out slowly, so check the Government of Canada and CMHC websites for current status before counting on it.",
            ),
            (
                "How much does a garden suite cost to build in Ontario?",
                "In the Toronto area, garden suites run about $400 to $550 per square foot in hard costs, and a 600 square foot unit typically lands between $365,000 and $525,000 all-in with design, permits, servicing, and contingency. Basement conversions are substantially cheaper, often $100,000 to $200,000 for a full legal suite.",
            ),
            (
                "Can I use future rental income from the suite to qualify for financing?",
                "Often, yes. Many lenders count 50 to 100 percent of the legal suite's actual or appraiser-projected market rent toward your debt service ratios, though policies vary widely. Equity-based private lenders focus less on your ratios and more on the property's value and the project's exit plan.",
            ),
            (
                "What credit score do I need for the 90 percent insured refinance?",
                "CMHC's program requires a minimum credit score of 600, debt ratios within 39 percent GDS and 44 percent TDS at the stress-test rate, an as-improved value under $2 million, and owner occupancy of one unit. Funds must go to suite construction, and approval is required before construction begins.",
            ),
            (
                "What happens if my post-build appraisal comes in lower than expected?",
                "Insured lending uses the lesser of the as-improved appraised value or the as-is value plus documented costs, so a weak appraisal or an overrun can shrink your borrowing room. Build a 10 to 15 percent contingency into the financing, and identify a fallback such as a HELOC, second mortgage, or private facility before you break ground.",
            ),
            (
                "Do laneway homes qualify for the same programs as basement suites?",
                "Generally yes. Federal programs apply to self-contained legal suites whether attached or detached, provided the unit is a long-term rental and local bylaws permit it. The practical difference is scale: detached builds cost several times more, so they rely far more on refinancing or construction financing than on the $80,000 federal loan.",
            ),
        ],
        "card_title": "Garden Suite Financing in Ontario: How to Fund a Laneway Home or Secondary Suite",
        "card_excerpt": "Build costs, the $80k federal loan at 2%, insured refinance rules, and financing options that work in Ontario.",
    },
    {
        "slug": "vendor-take-back-mortgage-ontario",
        "md": BATCH_ROOT
        / "richview-capital-vendor-take-back-mortgage-ontario-20260816"
        / "Vendor Take-Back Mortgage in Ontario- How VTBs Work for Buyers and Sellers.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (7).jpeg",
        "title": "Vendor Take-Back Mortgage Ontario: Terms, Rates, Risks | Richview Capital MIC",
        "og_title": "Vendor Take-Back Mortgage Ontario: Terms, Rates, Risks",
        "description": (
            "How vendor take-back mortgages work in Ontario: terms, rates, first vs second position, "
            "taxes, default risk, and pairing a VTB with private financing."
        ),
        "h1": "Vendor Take-Back Mortgage in Ontario: How VTBs Work for Buyers and Sellers",
        "jsonld_headline": "Vendor Take-Back Mortgage in Ontario: How VTBs Work for Buyers and Sellers",
        "breadcrumb": "Vendor Take-Back Mortgage in Ontario",
        "hero_alt": (
            "Sold sign outside an Ontario home purchased with a vendor take-back mortgage — "
            "Richview Capital guide to VTB terms and risks"
        ),
        "published": "2026-08-24T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "Vendor Take Back Mortgage Ontario",
            "VTB Mortgage Ontario",
            "Seller Financing Canada",
            "Second Position VTB",
            "Land Financing VTB",
            "Private Mortgage VTB",
            "Richview Capital Borrowers",
            "Ontario Seller Financing",
        ],
        "faqs": [
            (
                "Is a vendor take-back mortgage legal in Ontario?",
                "Yes. A VTB is an ordinary mortgage in which the seller is the lender, registered on title and enforceable like any other Ontario mortgage. A seller financing the sale of their own property generally does not need a lending licence, though both sides should retain their own lawyers.",
            ),
            (
                "What interest rate is typical on a VTB mortgage?",
                "Most Ontario VTBs price between roughly 5 and 12 percent, depending on position, equity, and buyer strength. First-position VTBs sit at the lower end, while second-position VTBs price like private second mortgages. Everything is negotiable because the lender is the seller.",
            ),
            (
                "Does the buyer's bank need to approve a VTB?",
                "Yes, in practice. Most institutional and private first mortgage commitments prohibit undisclosed secondary financing, and the first lender will include the VTB payment in the buyer's debt ratios. Concealing a VTB from the first lender can amount to mortgage fraud and jeopardize the whole transaction.",
            ),
            (
                "What happens if the buyer defaults on a VTB?",
                "The seller can enforce like any mortgagee, most commonly through power of sale under the Ontario Mortgages Act, and can also sue the buyer on their personal covenant. A second-position VTB holder is only paid after the first mortgage, so recovery depends on the equity above the first charge.",
            ),
            (
                "Can a VTB cover the full purchase price?",
                "It can when the seller owns the property free and clear, which is most common on land, farm, and some commercial sales. If the seller still has a mortgage on the property, their lender's terms will usually limit or prevent full seller financing.",
            ),
            (
                "Can the seller sell or assign the VTB later?",
                "Yes. A VTB is an asset, and sellers can assign it to a private investor for cash before maturity. Assignments typically happen at a discount to face value reflecting the rate, remaining term, and risk.",
            ),
        ],
        "card_title": "Vendor Take-Back Mortgage in Ontario: How VTBs Work for Buyers and Sellers",
        "card_excerpt": "VTB terms, rates, first vs second position, default risk, and pairing seller financing with private lending.",
    },
    {
        "slug": "mortgage-on-inherited-property-ontario",
        "md": BATCH_ROOT
        / "richview-capital-estate-probate-financing-ontario-20260816"
        / "Mortgage on Inherited Property in Ontario- How Estate and Probate Financing.md",
        "image_src": SEO_ROOT / "WhatsApp Image 2026-08-16 at 14.26.28 (8).jpeg",
        "title": "Mortgage on Inherited Property in Ontario: Probate Guide | Richview Capital MIC",
        "og_title": "Mortgage on Inherited Property in Ontario: Probate Guide",
        "description": (
            "How a mortgage on inherited property in Ontario works: probate timelines, "
            "estate administration tax math, sibling buyout examples, and executor loans."
        ),
        "h1": "Mortgage on Inherited Property in Ontario: How Estate and Probate Financing Actually Works",
        "jsonld_headline": "Mortgage on Inherited Property in Ontario: How Estate and Probate Financing Actually Works",
        "breadcrumb": "Mortgage on Inherited Property in Ontario",
        "hero_alt": (
            "Inherited detached home in Ontario that a beneficiary is financing through probate — "
            "Richview Capital estate and probate financing guide"
        ),
        "published": "2026-08-24T09:00:00-04:00",
        "post_meta": "August 2026 · Borrowers · Ontario",
        "tags": [
            "Probate Financing",
            "Estate Administration Tax Ontario",
            "Inherited Property Mortgage",
            "Executor Loans Ontario",
            "Sibling Buyout Mortgage",
            "Mortgage on Inherited Property",
            "Richview Capital Borrowers",
            "Ontario Estate Probate",
        ],
        "faqs": [
            (
                "Can I get a mortgage on an inherited house before probate in Ontario?",
                "Not a conventional one, because title is still in the deceased's name and banks will not lend against it. Specialized private lenders can provide executor loans or estate advances secured against the property, generally with the estate trustee's involvement and beneficiary consent. Full mortgage options open up after the Certificate of Appointment issues and title is transmitted.",
            ),
            (
                "How much is estate administration tax in Ontario?",
                "The first $50,000 of estate value is exempt, and the rest is taxed at $15 per $1,000, which is 1.5 percent. On a $1,000,000 estate the tax is $14,250, payable as a deposit when the probate application is filed. The figures come from the Ontario government's published rules.",
            ),
            (
                "What is a probate loan and how is it repaid?",
                "A probate loan, also called an executor loan or estate loan, is a short-term loan secured against estate property that covers estate administration tax, legal fees, and carrying costs while the estate is illiquid. Interest is often accrued or prepaid through a reserve rather than paid monthly. The loan is repaid from estate funds once the certificate issues and assets are sold or refinanced.",
            ),
            (
                "Do all beneficiaries have to agree to a mortgage on an inherited property?",
                "Before distribution, yes as a practical matter: lenders financing an estate want the estate trustee's signature and the written consent of the beneficiaries, since the loan affects everyone's share. After title has been transferred to one beneficiary, that owner can mortgage the property alone like any other homeowner.",
            ),
            (
                "How long does probate take in Ontario?",
                "Ontario courts state that applications are typically processed within 15 business days of filing. However, preparing the application, valuing assets, and resolving complications usually takes months, so families should plan for a period of several months from death to certificate, and budget carrying costs accordingly.",
            ),
            (
                "What happens to the existing mortgage when the homeowner dies?",
                "The mortgage stays on the property and payments must continue, usually from estate funds. At maturity, most lenders will not renew in a deceased person's name and can demand full repayment. Estates commonly bridge the payout with short-term financing or sell the property, and a beneficiary may qualify to take over financing after probate.",
            ),
        ],
        "card_title": "Mortgage on Inherited Property in Ontario: How Estate and Probate Financing Actually Works",
        "card_excerpt": "Probate timelines, estate administration tax math, sibling buyouts, and executor loans for inherited Ontario homes.",
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


def article_image_url(cfg: dict) -> str:
    slug = cfg["slug"]
    hero = REPO / f"images/blog/{slug}.jpg"
    if hero.is_file():
        return f"{BASE_URL}/images/blog/{slug}.jpg"
    return f"{BASE_URL}/images/logo.png"


def build_json_ld(cfg: dict) -> str:
    page_url = f"{BASE_URL}/blog/{cfg['slug']}/"
    image_url = article_image_url(cfg)
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
    image_url = article_image_url(cfg)
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
    hero_html = ""
    if (REPO / f"images/blog/{slug}.jpg").is_file():
        hero_html = f"""
                <figure class="post-hero-figure post-hero-figure--object-contain" aria-label="Article hero image">
                    <img src="{image_path}" width="1280" height="702" alt="{escape(cfg['hero_alt'], quote=True)}" loading="eager" decoding="async">
                </figure>"""
    return f"""        <article class="post-wrap">
            <div class="container">
                <a href="/blog/" class="post-back"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> Back to Blog</a>
                <p class="post-meta">{escape(cfg['post_meta'])}</p>
                <h1 class="post-title">{escape(cfg['h1'])}</h1>
{hero_html}
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


def card_image_path(slug: str) -> str:
    hero = REPO / f"images/blog/{slug}.jpg"
    if hero.is_file():
        return f"/images/blog/{slug}.jpg"
    return "/images/logo.png"


def ensure_placeholder_hero(slug: str) -> None:
    """Create a centered-logo 1280×702 JPG when no hero exists yet."""
    out = REPO / f"images/blog/{slug}.jpg"
    if out.is_file():
        return
    export_hero_placeholder(slug)


def blog_card_grid(cfg: dict) -> str:
    slug = cfg["slug"]
    image_path = card_image_path(slug)
    return f"""                    <article class="blog-card reveal">
                        <div class="blog-card-image {BLOG_CARD_IMAGE_CLASS}">
                            <a href="/blog/{slug}/" aria-hidden="true" tabindex="-1"><img src="{image_path}" width="1280" height="702" alt="" loading="lazy"></a>
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
    image_path = card_image_path(slug)
    return f"""                    <article class="blog-card reveal" style="--i: {index};">
                        <a href="/blog/{slug}/" class="blog-card-thumb {BLOG_CARD_THUMB_CLASS}" aria-label="Read: {title}">
                            <img src="{image_path}" alt="" width="1280" height="702" loading="lazy" decoding="async">
                        </a>
                        <div class="blog-card-body">
                            <span class="blog-date">August 2026</span>
                            <h3><a href="/blog/{slug}/">{title}</a></h3>
                            <p class="blog-excerpt">{excerpt}</p>
                            <a href="/blog/{slug}/" class="blog-link">Read <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
                        </div>
                    </article>

"""


def sitemap_entry(slug: str, lastmod: str = "2026-08-16") -> str:
    return f"""  <url>
    <loc>{BASE_URL}/blog/{slug}/</loc>
    <lastmod>{lastmod}</lastmod>
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
    dup_markers = (
        "<!-- Duplicate set for seamless loop -->",
        "<!-- Third set for continuous flow -->",
        "<!-- Set 2 — duplicate for seamless infinite loop -->",
    )
    dup_idx = -1
    for dup_marker in dup_markers:
        pos = text.find(dup_marker, idx)
        if pos != -1:
            dup_idx = pos
            break
    if dup_idx == -1:
        raise ValueError("duplicate set marker not found in blog-track")
    insert_at = text.find("\n", dup_idx) + 1
    text = text[:insert_at] + cards_html + text[insert_at:]
    path.write_text(text, encoding="utf-8")


def update_sitemap(slugs: list[str], lastmod: str = "2026-08-16") -> None:
    path = REPO / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    blog_idx = text.find("<loc>https://richviewcapitalmic.com/blog/</loc>")
    if blog_idx == -1:
        raise ValueError("blog index url not found in sitemap")
    insert_at = text.find("</url>", blog_idx) + len("</url>")
    insert_at = text.find("\n", insert_at) + 1
    new_slugs = [s for s in slugs if f"/blog/{s}/" not in text]
    if not new_slugs:
        print("Sitemap already lists new posts; skipping sitemap update.")
        return
    entries = "".join(sitemap_entry(s, lastmod) for s in new_slugs)
    text = text[:insert_at] + entries + text[insert_at:]
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
        out = REPO / f"blog/{cfg['slug']}/index.html"
        slug = cfg["slug"]
        image_src = cfg.get("image_src")
        has_hero_file = image_src and Path(image_src).is_file()
        hero_on_disk = (REPO / f"images/blog/{slug}.jpg").is_file()

        if out.is_file() and (hero_on_disk or not has_hero_file):
            print(f"Skipping /blog/{slug}/ (already published)")
            continue
        if out.is_file() and has_hero_file and not hero_on_disk:
            print(f"Updating /blog/{slug}/ with new hero image")
        if not cfg["md"].is_file():
            print(f"Markdown missing: {cfg['md']}", file=sys.stderr)
            return 1
        image_src = cfg.get("image_src")
        has_hero_file = image_src and Path(image_src).is_file()
        if image_src and not has_hero_file:
            print(
                f"Publishing /blog/{cfg['slug']}/ without hero image "
                f"(missing: {Path(image_src).name}); add image and re-run to update cards.",
                file=sys.stderr,
            )

        md_text = cfg["md"].read_text(encoding="utf-8")
        lead, body = split_lead_and_body(md_text)
        prose_html = md_body_to_html(body)

        img_out = REPO / f"images/blog/{cfg['slug']}.jpg"
        if has_hero_file:
            export_hero(cfg["slug"], Path(image_src))

        page = build_page(shell, cfg, lead, prose_html)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")

        if has_hero_file:
            grid_cards += blog_card_grid(cfg)
            home_cards += blog_card_home(cfg, 0)
        slugs.append(cfg["slug"])
        print(f"Published /blog/{cfg['slug']}/")

    if not slugs:
        print("No new posts to publish.")
        return 0

    new_slugs = [s for s in slugs if f"/blog/{s}/" not in index_text]
    card_slugs = [
        s
        for s in slugs
        if f"/blog/{s}/" not in index_text
    ]
    if card_slugs:
        cards_for_new = ""
        home_for_new = ""
        for cfg in BLOGS:
            if cfg["slug"] in card_slugs:
                cards_for_new += blog_card_grid(cfg)
                home_for_new += blog_card_home(cfg, 0)
        update_blog_index(cards_for_new)
        update_homepage(home_for_new)
    elif new_slugs:
        print("New posts published without hero images; blog index and carousel unchanged.")
    else:
        print("Blog index already lists all new posts; skipping index and homepage cards.")
    lastmod = slugs[0] if slugs else "2026-08-16"
    if BLOGS and slugs:
        for cfg in BLOGS:
            if cfg["slug"] == slugs[0]:
                lastmod = cfg["published"][:10]
                break
    update_sitemap(slugs, lastmod)
    print("Updated blog index, homepage carousel, and sitemap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
