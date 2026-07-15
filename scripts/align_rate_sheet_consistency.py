#!/usr/bin/env python3
"""Align published rate/LTV/terms language site-wide to the July 2025 rate sheet."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Richview published LTV (rate sheet)
LTV_75 = "Up to 75% LTV (case by case)"
LTV_65 = "Up to 65% LTV (case by case)"

REPLACEMENTS: list[tuple[str, str]] = [
    # --- FAQ (site-wide) ---
    (
        "GTA: up to 75% LTV. Condominiums and cities outside the GTA up to 65% LTV. Construction projects: up to 65% of end value. Second mortgage LTV varies by property and risk profile.",
        f"1st and 2nd mortgages and HELOC: up to 75% LTV (case by case). Construction and commercial: up to 65% LTV (case by case).",
    ),
    (
        "GTA: up to 75% LTV. Condominiums and cities outside the GTA up to 65% LTV. Second mortgages and commercial: evaluated case by case. Construction loans up to 65% of end value.",
        f"1st and 2nd mortgages and HELOC: up to 75% LTV (case by case). Construction and commercial: up to 65% LTV (case by case).",
    ),
    (
        "All mortgages secured by real estate with regional LTV limits (GTA up to 75%; outskirts and condos up to 65%).",
        "All mortgages secured by real estate with LTV limits up to 75% on 1st, 2nd, and HELOC (case by case), and up to 65% on construction and commercial (case by case).",
    ),
    (
        "Secured by real estate with regional LTV limits (GTA up to 75%; outskirts &amp; condos up to 65%)",
        "Secured by real estate — up to 75% LTV on 1st, 2nd, and HELOC; up to 65% on construction and commercial (case by case)",
    ),
    (
        'References to figures such as "up to $5,000,000" maximum loan amounts, "up to 75% LTV" in the GTA and "up to 65% LTV" in other regions or on condos,',
        'References to figures such as "up to $5,000,000" maximum loan amounts, "up to 75% LTV (case by case)" on 1st, 2nd, and HELOC mortgages and "up to 65% LTV (case by case)" on construction and commercial,',
    ),
    # --- what-is-a-mic ---
    (
        "<td>Max LTV</td><td>75% (GTA); 65% (outskirts &amp; condos)</td>",
        f"<td>Max LTV</td><td>{LTV_75} on 1st/2nd/HELOC; {LTV_65} on construction/commercial</td>",
    ),
    (
        "Conservative loan-to-value limits: up to 75% in the GTA; condominiums and cities outside the GTA up to 65% LTV",
        f"Conservative loan-to-value limits: {LTV_75} on 1st, 2nd, and HELOC; {LTV_65} on construction and commercial",
    ),
    # --- homepage investor hero ---
    (
        "Every dollar secured by real estate with regional LTV limits (GTA up to 75%; outskirts and condos up to 65%).",
        "Every dollar secured by real estate with LTV limits up to 75% on 1st, 2nd, and HELOC, and up to 65% on construction and commercial (case by case).",
    ),
    # --- Toronto GTA guide ---
    (
        "Approval is <strong>equity-driven</strong>: typical Richview LTV is up to <strong>75%</strong> in the GTA on standard residential, and up to <strong>65%</strong> on condos and properties outside the GTA (case by case).",
        f"Approval is <strong>equity-driven</strong>: Richview published LTV is {LTV_75} on 1st, 2nd, and HELOC; {LTV_65} on construction and commercial.",
    ),
    (
        "<tr><td>Construction 1st mortgage</td><td>from <strong>8.99%</strong></td><td>Up to 65% of end value</td></tr>",
        f"<tr><td>Construction 1st mortgage</td><td>from <strong>8.99%</strong></td><td>{LTV_65}</td></tr>",
    ),
    (
        "<tr><td>Construction 2nd mortgage</td><td>from <strong>10.99%</strong></td><td>Up to 65% of end value</td></tr>",
        f"<tr><td>Construction 2nd mortgage</td><td>from <strong>10.99%</strong></td><td>{LTV_65}</td></tr>",
    ),
    (
        "<strong>Construction</strong> &mdash; 1st from <strong>8.99%</strong>, 2nd from <strong>10.99%</strong>, 2% fee, up to 65% of end value",
        f"<strong>Construction</strong> &mdash; 1st from <strong>8.99%</strong>, 2nd from <strong>10.99%</strong>, 2% fee, {LTV_65.lower()}",
    ),
    (
        "At Richview: up to <strong>75%</strong> standard GTA residential; <strong>65%</strong> condos and outside-GTA (case by case); construction up to <strong>65%</strong> of end value.",
        f"At Richview: {LTV_75} on 1st, 2nd, and HELOC; {LTV_65} on construction and commercial.",
    ),
    # --- Broker submission blog (HTML + will mirror in build script) ---
    (
        "Typical GTA 1st/2nd caps: <strong>75% LTV</strong> in the GTA, <strong>65%</strong> on condos and outskirts; construction to <strong>65% of end value</strong>.",
        f"Published LTV caps: <strong>75% LTV (case by case)</strong> on 1st, 2nd, and HELOC; <strong>65% LTV (case by case)</strong> on construction and commercial.",
    ),
    (
        "<li><strong>First mortgages:</strong> up to 75% <span class=\"key-term\">LTV</span> on residential property in the GTA; up to 65% LTV on condominiums and properties outside the GTA. Maximum loan amount up to $5,000,000.",
        "<li><strong>First mortgages:</strong> from <strong>6.49%</strong>, 2% lender fee, open &amp; closed 6&ndash;12 month terms, up to 75% LTV (case by case). Maximum loan amount up to $5,000,000.",
    ),
    (
        "<li><strong>Second mortgages:</strong> up to 75% LTV in the GTA; up to 65% on condos and outskirts. Loans up to $1M.",
        "<li><strong>Second mortgages:</strong> from <strong>8.99%</strong>, 2% lender fee, open and closed 6&ndash;12 month terms, up to 75% LTV (case by case). Loans up to $1M.",
    ),
    (
        "<li><strong>Construction loans:</strong> up to 65% of end value, with 3–5 draws per project and 24-hour on-site inspections.",
        f"<li><strong>Construction loans:</strong> 1st from <strong>8.99%</strong>, 2nd from <strong>10.99%</strong>, 2% lender fee, {LTV_65.lower()}, with 3&ndash;5 draws per project and 24-hour on-site inspections.",
    ),
    (
        "First mortgages typically cap at 75% LTV in the GTA and 65% LTV on condominiums and properties outside the GTA. Second mortgages follow the same regional split. Construction loans cap at 65% of end value.",
        "1st and 2nd mortgages and HELOC cap at up to 75% LTV (case by case). Construction and commercial cap at up to 65% LTV (case by case).",
    ),
    (
        "<td>6–12 months, up to 3 years</td>",
        "<td>6–12 months</td>",
    ),
    # --- Construction blog ---
    (
        "At Richview, up to 65% of end value on construction 1sts and 2nds, and up to 65% of end value combined.",
        f"At Richview, {LTV_65} on construction 1sts and 2nds.",
    ),
    (
        "Richview construction programs typically cap at up to <strong>65% of end value</strong> on qualifying files.",
        f"Richview construction programs typically cap at {LTV_65.lower()} on qualifying files.",
    ),
    (
        "Typical cap is up to 65% of end value on qualifying construction files",
        f"Typical cap is {LTV_65.lower()} on qualifying construction files",
    ),
    # --- HELOC blog Richview FAQ ---
    (
        "Private lenders are more flexible and lend on the equity available, commonly up to about 75% of value in the GTA.",
        "At Richview, private HELOC and home equity products are available up to 75% LTV (case by case).",
    ),
    (
        "Private lenders work on equity rather than those federal caps, and commonly lend up to about 75% of value in the GTA, with the ceiling closer to 65% for condominiums and properties outside the GTA.",
        f"Private lenders like Richview work on equity rather than those federal caps, with published products up to {LTV_75.lower()} on HELOC and home equity loans.",
    ),
    # --- MIC investing blog ---
    (
        "At Richview Capital, we focus on the GTA and broader province-wide residential market, with maximum LTV of 75% on first mortgages.",
        f"At Richview Capital, we focus on the GTA and broader province-wide residential market, with {LTV_75.lower()} on 1st, 2nd, and HELOC, and {LTV_65.lower()} on construction and commercial.",
    ),
    (
        "At Richview Capital, residential first mortgages are funded up to a maximum of 75% LTV.",
        f"At Richview Capital, 1st, 2nd, and HELOC mortgages are funded up to {LTV_75.lower()}; construction and commercial up to {LTV_65.lower()}.",
    ),
    # --- Product card terms (rate sheet: 6-12 months only) ---
    (
        "<li>Open &amp; closed terms: 6-12 months, up to 3 years</li>",
        "<li>Open &amp; closed 6-12 month terms</li>",
    ),
    (
        "<li>No renewal fee on 3-year terms</li>",
        "",
    ),
    (
        "Purchase or refinance residential properties with competitive rates and flexible terms. No annual renewal fee on 3-year terms.",
        "Purchase or refinance residential properties with competitive rates and flexible 6-12 month terms.",
    ),
    (
        "No renewal fee on 3-year terms. All rates subject to change",
        "All rates subject to change",
    ),
    # --- Toronto guide LTV list (multi-line) ---
]

TORONTO_LTV_OLD = """  <ul style="padding-left:24px; margin-bottom:22px;">
    <li>Standard GTA residential (detached, semi, town): up to <strong>75% LTV</strong></li>
    <li>Condominiums and properties outside the GTA: up to <strong>65% LTV</strong> (case by case)</li>
    <li>Construction (1st or 2nd): up to <strong>65%</strong> of end value</li>
    <li>Land 1st mortgages: <strong>65% LTV</strong></li>
  </ul>"""

TORONTO_LTV_NEW = f"""  <ul style="padding-left:24px; margin-bottom:22px;">
    <li>1st, 2nd, and HELOC mortgages: {LTV_75}</li>
    <li>Construction and commercial: {LTV_65}</li>
    <li>Land and bridge: evaluated case by case</li>
  </ul>"""


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        if old and old in text:
            text = text.replace(old, new)
    text = text.replace(TORONTO_LTV_OLD, TORONTO_LTV_NEW)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print("updated:", path.relative_to(ROOT))
        return True
    return False


def main() -> int:
    targets = list(ROOT.glob("**/*.html"))
    targets += list((ROOT / "scripts").glob("build_*.py"))
    targets = [p for p in targets if "node_modules" not in p.parts and ".tmp-rate-sheet" not in p.parts]
    changed = sum(process_file(p) for p in sorted(targets))
    print(f"Done. {changed} files changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
