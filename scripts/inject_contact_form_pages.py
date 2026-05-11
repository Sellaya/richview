#!/usr/bin/env python3
"""Inject shared #contact block + assets into pages that do not yet include the consultation form."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEAD_SNIPPET = """
    <link rel="stylesheet" href="/css/contact-cta-section.css">
    <link rel="stylesheet" href="/css/consult-schedule-section.css">
    <link rel="stylesheet" href="/css/calendly-style-picker.css">
"""

BODY_SCRIPTS = """
    <script src="/js/lottie-utils.js"></script>
    <script src="/js/contact-consultation-form.js"></script>
"""


def extract_contact_section(index_html: str) -> str:
    start = index_html.find('<section class="cta-section" id="contact">')
    if start < 0:
        raise ValueError("contact section not in index.html")
    end = index_html.find("</section>", start) + len("</section>")
    return index_html[start:end]


def inject(path: Path, contact_block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if 'id="consultationForm"' in text and "hero-form-step" in text:
        print("skip (already has hero multistep form):", path.relative_to(ROOT))
        return
    if 'id="contact"' in text and "consultationForm" in text:
        print("skip (has legacy form — manual review):", path.relative_to(ROOT))
        return

    if "/css/contact-cta-section.css" not in text:
        head_end = text.find("</head>")
        if head_end < 0:
            raise ValueError("no </head> in " + str(path))
        text = text[:head_end] + HEAD_SNIPPET + text[head_end:]

    if "/js/contact-consultation-form.js" not in text:
        body_end = text.rfind("</body>")
        if body_end < 0:
            raise ValueError("no </body> in " + str(path))
        text = text[:body_end] + BODY_SCRIPTS + "\n" + text[body_end:]

    if 'id="contact"' not in text:
        foot = "\n    <footer>"
        idx = text.find(foot)
        if idx < 0:
            foot = "\n<footer>"
            idx = text.find(foot)
        if idx < 0:
            raise ValueError("no <footer> in " + str(path))
        text = text[:idx] + "\n\n" + contact_block + text[idx:]

    # Same-page #contact for primary CTAs (keep /#services etc.)
    text = text.replace('href="/#contact"', 'href="#contact"')
    text = text.replace("href='/#contact'", "href='#contact'")

    path.write_text(text, encoding="utf-8")
    print("injected:", path.relative_to(ROOT))


def main():
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    contact_block = extract_contact_section(index_html)
    targets = [
        ROOT / "blog/index.html",
        ROOT / "blog/construction-financing-ontario/index.html",
        ROOT / "blog/mic-investing-ontario-rrsp/index.html",
        ROOT / "blog/private-mortgage-ontario/index.html",
        ROOT / "blog/private-mortgage-lender-toronto-honest-gta-guide/index.html",
        ROOT / "privacy/index.html",
        ROOT / "terms/index.html",
        ROOT / "disclaimer/index.html",
        ROOT / "thank-you/index.html",
    ]
    for p in targets:
        if not p.exists():
            print("missing:", p)
            continue
        inject(p, contact_block)


if __name__ == "__main__":
    main()
