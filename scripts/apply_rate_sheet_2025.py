#!/usr/bin/env python3
"""Apply Updated-RVC-Rate-Sheet.pdf values across the site (July 2025 sheet).

Rate sheet summary:
- 1st Mortgage: 6.49%, 2% fee, 6-12 mo, up to 75% LTV
- 2nd Mortgage: 8.99%, 2% fee, 6-12 mo, up to 75% LTV
- Construction 1st: 8.99%, 2% fee, up to 65% LTV
- Construction 2nd: 10.99%, 2% fee, up to 65% LTV
- HELOC 1st: 7.99%, 2.5% fee, up to 75% LTV
- HELOC 2nd: 8.99%, 2.5% fee, up to 75% LTV
- Commercial 1st: 7.99%, 2% fee, up to 65% LTV
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LTV_75 = "Up to 75% LTV (case by case)"
LTV_65 = "Up to 65% LTV (case by case)"
LTV_LEGACY = "LTV: GTA up to 75%; condominiums and cities outside the GTA up to 65% LTV (case by case)"

SECOND_TIER_OLD = """                        <li>Under 65% LTV: rates from 10.99%</li>
                        <li>65% LTV and above: rates from 11.99%</li>"""

SECOND_TIER_OLD_BORROWERS = """                    <li>Under 65% LTV: rates from 10.99%</li>
                        <li>65% LTV and above: rates from 11.99%</li>"""

SECOND_TIER_NEW = """                        <li>Rates from 8.99%</li>"""

SECOND_TIER_NEW_BORROWERS = """                    <li>Rates from 8.99%</li>"""

CONSTRUCTION_OLD = """                    <li>Land 1st mortgage: 65% LTV, from 7.99% + 2% fee</li>
                    <li>Construction 1st: up to 65% end value, from 9.99% + 2% fee</li>
                    <li>Construction 2nd: up to 65% end value, from 11.99% + 2% fee</li>"""

CONSTRUCTION_OLD_BROKERS = """                        <li>Land 1st mortgage: 65% LTV, from 7.99% + 2% lender fee</li>
                        <li>Construction 1st: up to 65% end value, from 9.99% + 2% lender fee</li>
                        <li>Construction 2nd: up to 65% end value, from 11.99% + 2% lender fee</li>"""

CONSTRUCTION_NEW = """                    <li>Construction 1st: {ltv}, from 8.99% + 2% fee</li>
                    <li>Construction 2nd: {ltv}, from 10.99% + 2% fee</li>"""

CONSTRUCTION_NEW_BROKERS = """                        <li>Construction 1st: {ltv}, from 8.99% + 2% lender fee</li>
                        <li>Construction 2nd: {ltv}, from 10.99% + 2% lender fee</li>"""

HELOC_2ND_OLD = """                    <li>2nd mortgage HELOC: rates from 11.99%</li>"""
HELOC_2ND_OLD_BROKERS = """                        <li>2nd mortgage HELOC: rates from 11.99%</li>"""
HELOC_2ND_NEW = """                    <li>2nd mortgage HELOC: rates from 8.99%</li>"""
HELOC_2ND_NEW_BROKERS = """                        <li>2nd mortgage HELOC: rates from 8.99%</li>"""

BRIDGE_RATE_OLD = """                    <li>1 to 90 day loan terms</li>
                    <li>Rates from 8.99%</li>"""
BRIDGE_RATE_OLD_BROKERS = """                        <li>1 to 90 day loan terms</li>
                        <li>Rates from 8.99%</li>"""
BRIDGE_RATE_NEW = """                    <li>1 to 90 day loan terms</li>
                    <li>Pricing evaluated case by case</li>"""
BRIDGE_RATE_NEW_BROKERS = """                        <li>1 to 90 day loan terms</li>
                        <li>Pricing evaluated case by case</li>"""

LAND_RATE_OLD = """                    <li>Rates from 7.99% + 2% lender fee</li>"""
LAND_RATE_OLD_BROKERS = """                        <li>Rates from 7.99% + 2% lender fee</li>"""
LAND_RATE_NEW = """                    <li>Pricing evaluated case by case</li>"""
LAND_RATE_NEW_BROKERS = """                        <li>Pricing evaluated case by case</li>"""

FIRST_FEE_OLD = """                    <li>Purchase lender fee: 2% / Refinance lender fee: 2.25%</li>"""
FIRST_FEE_NEW = """                    <li>2% lender fee</li>"""

REFINANCE_OLD = """                    <li>Rates from 6.99%</li>
                    <li>Lender fee from 2.25%</li>"""
REFINANCE_NEW = """                    <li>Rates from 6.49%</li>
                    <li>2% lender fee</li>"""

COMMERCIAL_LTV_OLD = """                    <li>LTV: GTA up to 75%; condominiums and cities outside the GTA up to 65% LTV (case by case)</li>
                    <li>Approvals within 1 business day</li>
                    <li>Rates from 9.99%</li>"""

COMMERCIAL_LTV_NEW = """                    <li>{ltv}</li>
                    <li>Approvals within 1 business day</li>
                    <li>Rates from 7.99%</li>"""

COMMERCIAL_LTV_OLD_BROKERS = """                        <li>LTV: GTA up to 75%; condominiums and cities outside the GTA up to 65% LTV (case by case)</li>
                        <li>Approvals within 1 business day</li>
                        <li>Rates from 9.99%</li>"""

COMMERCIAL_LTV_NEW_BROKERS = """                        <li>{ltv}</li>
                        <li>Approvals within 1 business day</li>
                        <li>Rates from 7.99%</li>"""


def replace_all(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        if old not in text:
            continue
        text = text.replace(old, new)
    return text


def update_product_pages(text: str, brokers: bool = False) -> str:
    indent = "                        " if brokers else "                    "
    ltv75_line = f"{indent}<li>{LTV_75}</li>"
    ltv65 = LTV_65

    text = text.replace("6.99%", "6.49%")

    if brokers:
        text = text.replace(SECOND_TIER_OLD, SECOND_TIER_NEW)
        text = text.replace(CONSTRUCTION_OLD_BROKERS, CONSTRUCTION_NEW_BROKERS.format(ltv=ltv65))
        text = text.replace(HELOC_2ND_OLD_BROKERS, HELOC_2ND_NEW_BROKERS)
        text = text.replace(BRIDGE_RATE_OLD_BROKERS, BRIDGE_RATE_NEW_BROKERS)
        text = text.replace(LAND_RATE_OLD_BROKERS, LAND_RATE_NEW_BROKERS)
        text = text.replace(COMMERCIAL_LTV_OLD_BROKERS, COMMERCIAL_LTV_NEW_BROKERS.format(ltv=ltv65))
    else:
        text = text.replace(SECOND_TIER_OLD_BORROWERS, SECOND_TIER_NEW_BORROWERS)
        text = text.replace(CONSTRUCTION_OLD, CONSTRUCTION_NEW.format(ltv=ltv65))
        text = text.replace(HELOC_2ND_OLD, HELOC_2ND_NEW)
        text = text.replace(BRIDGE_RATE_OLD, BRIDGE_RATE_NEW)
        text = text.replace(LAND_RATE_OLD, LAND_RATE_NEW)
        text = text.replace(FIRST_FEE_OLD, FIRST_FEE_NEW)
        text = text.replace(REFINANCE_OLD, REFINANCE_NEW)
        text = text.replace(COMMERCIAL_LTV_OLD, COMMERCIAL_LTV_NEW.format(ltv=ltv65))

    # HELOC open term wording from rate sheet
    text = text.replace("<li>Open term</li>", "<li>Open term / readvancable</li>")

    return text


def update_homepage(text: str) -> str:
    text = text.replace("First mortgages from 6.49%", "First mortgages from 6.49%")
    text = text.replace("First mortgages from 6.99%", "First mortgages from 6.49%")
    text = text.replace("Second mortgages from 10.99%", "Second mortgages from 8.99%")
    text = text.replace("Construction loans from 7.99%", "Construction loans from 8.99%")
    text = text.replace(
        "Second mortgages from 8.99%. Construction loans from 8.99%. Bridge financing from 8.99%.",
        "Second mortgages from 8.99%. Construction loans from 8.99%.",
    )
    return text


def update_generic_rates(text: str) -> str:
    """Global replacements safe in rate/marketing context."""
    pairs = [
        ("from 6.99%", "from 6.49%"),
        ("from <strong>6.99%</strong>", "from <strong>6.49%</strong>"),
        ("Rates from 6.99%", "Rates from 6.49%"),
        ("starting from <strong>6.99%</strong>", "starting from <strong>6.49%</strong>"),
        ("1st mortgage rates start from 6.99%", "1st mortgage rates start from 6.49%"),
        ("first mortgages from <strong>6.99%</strong>", "first mortgages from <strong>6.49%</strong>"),
        ("First mortgages from 6.99%", "First mortgages from 6.49%"),
        ("Refinance (residential)</td><td>from <strong>6.99%</strong>", "Refinance (residential)</td><td>from <strong>6.49%</strong>"),
        ("1st mortgage (residential, GTA)</td><td>from <strong>6.99%</strong>", "1st mortgage (residential, GTA)</td><td>from <strong>6.49%</strong>"),
        ("First mortgage (purchase)</td><td>from 6.99%", "First mortgage (purchase)</td><td>from 6.49%"),
        ("First mortgage (refinance)</td><td>from 6.99%", "First mortgage (refinance)</td><td>from 6.49%"),
        ("First mortgage (refinance)</td><td>from 6.49%</td><td>2.25%", "First mortgage (refinance)</td><td>from 6.49%</td><td>2%"),
        ("2nd mortgage rates start from 10.99%", "2nd mortgage rates start from 8.99%"),
        ("second mortgages from <strong>10.99%</strong>", "second mortgages from <strong>8.99%</strong>"),
        ("Second mortgages from 10.99%", "Second mortgages from 8.99%"),
        ("starting from <strong>10.99%</strong>", "starting from <strong>8.99%</strong>"),
        ("from <strong>10.99%</strong>", "from <strong>8.99%</strong>"),
        ("from 10.99%", "from 8.99%"),
        ("Construction 1st from 9.99%", "Construction 1st from 8.99%"),
        ("Construction 1st mortgage</td><td>9.99%", "Construction 1st mortgage</td><td>8.99%"),
        ("Construction (1st mortgage)</td><td>from 9.99%", "Construction (1st mortgage)</td><td>from 8.99%"),
        ("Construction 1st: up to 65% end value, from 9.99%", "Construction 1st: up to 65% LTV, from 8.99%"),
        ("Construction 2nd from 11.99%", "Construction 2nd from 10.99%"),
        ("Construction 2nd mortgage</td><td>11.99%", "Construction 2nd mortgage</td><td>10.99%"),
        ("Construction (2nd mortgage)</td><td>from 11.99%", "Construction (2nd mortgage)</td><td>from 10.99%"),
        ("Construction 2nd: up to 65% end value, from 11.99%", "Construction 2nd: up to 65% LTV, from 10.99%"),
        ("Land 1st from 7.99%", "Land 1st from 8.99%"),
        ("Land (1st mortgage)</td><td>from 7.99%", "Land (1st mortgage)</td><td>from 8.99%"),
        ("Land 1st mortgage</td><td>7.99%", "Land 1st mortgage</td><td>8.99%"),
        ("HELOC (2nd mortgage)</td><td>from 11.99%", "HELOC (2nd mortgage)</td><td>from 8.99%"),
        ("HELOC (2nd)</td><td>from 11.99%", "HELOC (2nd)</td><td>from 8.99%"),
        ("2nd mortgage HELOC: rates from 11.99%", "2nd mortgage HELOC: rates from 8.99%"),
        ("HELOC (2nd mortgage)</td><td>from <strong>11.99%</strong>", "HELOC (2nd mortgage)</td><td>from <strong>8.99%</strong>"),
        ("2nd mortgage &mdash; under 65% LTV</td><td>from <strong>10.99%</strong>", "2nd mortgage</td><td>from <strong>8.99%</strong>"),
        ("2nd mortgage &mdash; 65% LTV and above</td><td>from <strong>11.99%</strong>", ""),
        ("Second mortgage (under 65% LTV)</td><td>from 10.99%", "Second mortgage</td><td>from 8.99%"),
        ("Second mortgage (65% LTV and above)</td><td>from 11.99%", ""),
        ("Second mortgage (65% LTV+)</td><td>from 11.99%", ""),
        ("Second mortgage (under 65% LTV)</td><td>from 8.99%", "Second mortgage</td><td>from 8.99%"),
        ("Commercial</td><td>from 9.99%", "Commercial</td><td>from 7.99%"),
        ("Commercial</td><td>from <strong>9.99%</strong>", "Commercial</td><td>from <strong>7.99%</strong>"),
        ("Rates from 9.99%", "Rates from 7.99%"),
        ("Bridge</td><td>from 8.99%", "Bridge</td><td>Case by case"),
        ("Bridge financing</td><td>from <strong>8.99%</strong>", "Bridge financing</td><td>Case by case"),
        ("1st from 9.99%, 2nd from 11.99%", "1st from 8.99%, 2nd from 10.99%"),
        ("1st from 9.99%</strong>, <strong>2nd from 11.99%</strong>", "1st from 8.99%</strong>, <strong>2nd from 10.99%</strong>"),
        ("land 1st from 7.99%", "land 1st from 8.99%"),
        ("Land 1st mortgage</td><td>from <strong>7.99%</strong>", "Land 1st mortgage</td><td>from <strong>8.99%</strong>"),
        ("Indicative rate</td><td>9.99%</td><td>11.99%", "Indicative rate</td><td>8.99%</td><td>10.99%"),
        ("1st from 9.99%, 2nd from 11.99%, land 1st from 7.99%", "1st from 8.99%, 2nd from 10.99%"),
        ("Bridge financing starts from <strong>8.99%</strong>, lender fee <strong>1-2%</strong>", "Bridge financing is evaluated case by case"),
        ("Lender fee from 2.25%", "2% lender fee"),
        ("fee 2.25%", "fee 2%"),
        ("2.25%</td>", "2%</td>"),
        ("from 6.49% on 1sts and <strong>10.99%</strong> on 2nds", "from 6.49% on 1sts and <strong>8.99%</strong> on 2nds"),
        ("on 1sts and <strong>10.99%</strong> on 2nds", "on 1sts and <strong>8.99%</strong> on 2nds"),
        ("Construction 1st mortgage</td><td>from <strong>9.99%</strong>", "Construction 1st mortgage</td><td>from <strong>8.99%</strong>"),
        ("Construction 2nd mortgage</td><td>from <strong>11.99%</strong>", "Construction 2nd mortgage</td><td>from <strong>10.99%</strong>"),
        ("Land 1st mortgage</td><td>from <strong>8.99%</strong>", "Land 1st mortgage</td><td>Case by case"),
        ("Land 1st mortgage</td><td>from <strong>7.99%</strong>", "Land 1st mortgage</td><td>Case by case"),
        ("Lender fee &mdash; 1st mortgage refinance</td><td>from <strong>2.25%</strong>", "Lender fee &mdash; 1st mortgage refinance</td><td><strong>2%</strong>"),
        ("Indicative rate (annual)</td><td>6.99%</td><td>8.99%", "Indicative rate (annual)</td><td>6.49%</td><td>8.99%"),
        ("Year 1 interest (interest-only)</td><td>~$34,950", "Year 1 interest (interest-only)</td><td>~$32,450"),
        ("Total Year 1 all-in cost</strong></td><td>~$53,400", "Total Year 1 all-in cost</strong></td><td>~$50,900"),
        ("Monthly payment (interest-only)</td><td>~$2,913", "Monthly payment (interest-only)</td><td>~$2,704"),
        ("Richview 2nd pricing from <strong>8.99%</strong> under 65% combined LTV and from <strong>11.99%</strong> at 65% and above", "Richview 2nd pricing from <strong>8.99%</strong>"),
        ("<strong>Construction</strong> &mdash; 1st from <strong>9.99%</strong>, 2nd from <strong>11.99%</strong>", "<strong>Construction</strong> &mdash; 1st from <strong>8.99%</strong>, 2nd from <strong>10.99%</strong>"),
        ("<strong>Bridge</strong> &mdash; 1&ndash;90 days, from <strong>8.99%</strong>, lender fee <strong>1&ndash;2%</strong>", "<strong>Bridge</strong> &mdash; 1&ndash;90 days, pricing evaluated case by case"),
        ("<strong>Land 1st</strong> &mdash; 65% LTV, from <strong>7.99%</strong>, 2% fee", "<strong>Land 1st</strong> &mdash; pricing evaluated case by case"),
        ("<strong>HELOC</strong> &mdash; 1st from <strong>7.99%</strong>, 2nd from <strong>11.99%</strong>", "<strong>HELOC</strong> &mdash; 1st from <strong>7.99%</strong>, 2nd from <strong>8.99%</strong>"),
        ("<strong>Commercial</strong> &mdash; case-by-case, from <strong>9.99%</strong>", "<strong>Commercial</strong> &mdash; case-by-case, from <strong>7.99%</strong>"),
        ("starting from approximately 6.99% for well-positioned deals", "starting from approximately 6.49% for well-positioned deals"),
        # --- "percent" wording (blog prose) ---
        ("start at 6.99 percent", "start at 6.49 percent"),
        ("from 6.99 percent", "from 6.49 percent"),
        ("start around 6.99 percent", "start around 6.49 percent"),
        ("around 10.99 percent", "around 8.99 percent"),
        ("from 10.99 percent", "from 8.99 percent"),
        ("typically start around 10.99 percent", "typically start around 8.99 percent"),
        ("start at 6.99%", "start at 6.49%"),
        ("bridge loans at 8.99 percent", "bridge financing evaluated case by case"),
        ("bridge loans from 8.99 percent", "bridge financing evaluated case by case"),
        ("construction financing from 7.99 percent", "construction financing from 8.99 percent"),
        ("construction loans from 7.99%, and bridge financing from 8.99%",
         "construction loans from 8.99%, with land and bridge financing evaluated case by case"),
        # --- commercial (7.99% first; not residential 6.49%) ---
        ("Richview's commercial first mortgages start at 6.49 percent", "Richview's commercial first mortgages start at 7.99 percent"),
        ("Richview's commercial first mortgages start at 6.99 percent", "Richview's commercial first mortgages start at 7.99 percent"),
        ("commercial first mortgages from 6.49 percent", "commercial first mortgages from 7.99 percent"),
        ("commercial first mortgages from 6.99 percent", "commercial first mortgages from 7.99 percent"),
        ("<tr><td>First mortgage</td><td>7% to 12%</td><td>From 6.49%</td></tr>",
         "<tr><td>First mortgage</td><td>7% to 12%</td><td>From 7.99%</td></tr>"),
        ("<tr><td>First mortgage</td><td>7% to 12%</td><td>From 6.99%</td></tr>",
         "<tr><td>First mortgage</td><td>7% to 12%</td><td>From 7.99%</td></tr>"),
        ("7% to 12% (Richview from 6.49%)", "7% to 12% (Richview from 7.99%)"),
        ("7% to 12% (Richview from 6.99%)", "7% to 12% (Richview from 7.99%)"),
        ("<tr><td>Bridge loan</td><td>8% to 13%</td><td>From 8.99%</td></tr>",
         "<tr><td>Bridge loan</td><td>8% to 13%</td><td>Case by case</td></tr>"),
        ("<tr><td>Construction loan</td><td>8% to 13%</td><td>From 7.99%</td></tr>",
         "<tr><td>Construction loan</td><td>8% to 13%</td><td>From 8.99%</td></tr>"),
        ("We fund commercial first mortgages from 6.49 percent, bridge loans from 8.99 percent, and construction financing from 7.99 percent, up to $5,000,000 and up to 75 percent LTV in the GTA",
         "We fund commercial first mortgages from 7.99 percent and construction financing from 8.99 percent, up to $5,000,000 and up to 65 percent LTV (case by case)"),
        ("We fund commercial first mortgages from 6.99 percent, bridge loans from 8.99 percent, and construction financing from 7.99 percent, up to $5,000,000 and up to 75 percent LTV in the GTA",
         "We fund commercial first mortgages from 7.99 percent and construction financing from 8.99 percent, up to $5,000,000 and up to 65 percent LTV (case by case)"),
        # --- debt consolidation worked example at 8.99% ---
        ("Private second mortgage, interest only</td><td>10.99%</td><td>About $568</td><td>About $925</td></tr>",
         "Private second mortgage, interest only</td><td>8.99%</td><td>About $465</td><td>About $1,028</td></tr>"),
        ("weigh it against roughly $11,000 a year of cash flow relief", "weigh it against roughly $12,000 a year of cash flow relief"),
        ("<strong>land 1st from 8.99%</strong>", "land financing evaluated case by case"),
        ("land 1st from 8.99%", "land financing evaluated case by case"),
        ("from about 10.99% for lower-LTV files up to the 11.99%+ range", "from 8.99%"),
        ("10.99% for lower-LTV files up to the 11.99%+ range", "8.99%"),
        # Restore construction 2nd after any broad 10.99% → 8.99% matches
        ("Construction 2nd: up to 65% LTV, from 8.99%", "Construction 2nd: up to 65% LTV, from 10.99%"),
        ("Construction (2nd mortgage)</td><td>from 8.99%", "Construction (2nd mortgage)</td><td>from 10.99%"),
        ("Construction 2nd mortgage</td><td>8.99%", "Construction 2nd mortgage</td><td>10.99%"),
        ("1st from 8.99%, 2nd from 8.99%", "1st from 8.99%, 2nd from 10.99%"),
        ("Construction 2nd mortgage</td><td>from <strong>8.99%</strong>", "Construction 2nd mortgage</td><td>from <strong>10.99%</strong>"),
        ("<strong>Construction</strong> &mdash; 1st from <strong>8.99%</strong>, 2nd from <strong>8.99%</strong>",
         "<strong>Construction</strong> &mdash; 1st from <strong>8.99%</strong>, 2nd from <strong>10.99%</strong>"),
        ("Construction loans:</strong> 1st from <strong>8.99%</strong>, 2nd from <strong>8.99%</strong>",
         "Construction loans:</strong> 1st from <strong>8.99%</strong>, 2nd from <strong>10.99%</strong>"),
        ("Construction 2nd: Up to 65% LTV (case by case), from 8.99%", "Construction 2nd: Up to 65% LTV (case by case), from 10.99%"),
        ("Richview published construction pricing: <strong>1st from 8.99%</strong>, <strong>2nd from 8.99%</strong>",
         "Richview published construction pricing: <strong>1st from 8.99%</strong>, <strong>2nd from 10.99%</strong>"),
        ("Indicative rate</td><td>8.99%</td><td>8.99%", "Indicative rate</td><td>8.99%</td><td>10.99%"),
        ("At an illustrative 11% interest-only rate", "At an illustrative 8.99% interest-only rate"),
        ("about $1,375 a month in interest", "about $1,498 a month in interest"),
        ("Through a private home equity loan at 9.99%, the same $200,000 would carry at about <strong>$1,665 a month</strong>", "Through a private home equity loan at 8.99%, the same $200,000 would carry at about <strong>$1,498 a month</strong>"),
        ("private home equity loan or second mortgage generally runs about 8% to 12%", "private home equity loan or second mortgage generally runs from about 8.99%"),
        ("A bank HELOC is typically prime plus half to one point (about 5% to 6% at a June 2026 prime of 4.45%). A private home equity loan or second mortgage generally runs 8% to 12%", "A bank HELOC is typically prime plus half to one point (about 5% to 6% at a June 2026 prime of 4.45%). A private home equity loan or second mortgage at Richview starts from 8.99%"),
    ]
    return replace_all(text, pairs)


def cleanup_empty_table_rows(text: str) -> str:
    text = re.sub(r"\n\s*<tr><td><strong>2nd mortgage &mdash; 65% LTV and above</strong>.*?</tr>\s*", "\n", text)
    text = re.sub(r"\n\s*<tr><td>Second mortgage \(65% LTV and above\)</td>.*?</tr>\s*", "\n", text)
    text = re.sub(r"\n\s*<tr><td>Second mortgage \(65% LTV\+\)</td>.*?</tr>\s*", "\n", text)
    text = re.sub(
        r'(\s*<tr><td>2nd mortgage &mdash; under 65% LTV</td><td>from <strong>8\.99%</strong></td><td>6&ndash;12 month term, open or closed</td></tr>)\s*<tr><td></td><td>6&ndash;12 month term, open or closed</td></tr>',
        r'\1',
        text,
    )
    text = text.replace(
        "<tr><td>2nd mortgage &mdash; under 65% LTV</td><td>from <strong>8.99%</strong></td><td>6&ndash;12 month term, open or closed</td></tr>",
        "<tr><td>2nd mortgage</td><td>from <strong>8.99%</strong></td><td>6&ndash;12 month term, open or closed; up to 75% LTV (case by case)</td></tr>",
    )
    return text


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    if path.name == "index.html" and path.parent == ROOT:
        text = update_homepage(text)
    if path in {ROOT / "borrowers/index.html", ROOT / "brokers/index.html"}:
        text = update_product_pages(text, brokers=path.name.startswith("brokers"))
    text = update_generic_rates(text)
    text = cleanup_empty_table_rows(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print("updated:", path.relative_to(ROOT))
        return True
    return False


def main() -> int:
    targets = list(ROOT.glob("**/*.html")) + list((ROOT / "scripts").glob("build_*.py"))
    targets = [p for p in targets if "node_modules" not in p.parts and ".tmp-rate-sheet" not in p.parts]
    changed = sum(process_file(p) for p in sorted(targets))
    print(f"Done. {changed} files changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
