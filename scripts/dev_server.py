#!/usr/bin/env python3
"""
Optional local preview. The site uses folder/index.html routes; python -m http.server
already serves /borrowers/ without .html. This adds 301s from old flat *.html names.

Usage (from repo root):
  python3 scripts/dev_server.py
  PORT=3000 python3 scripts/dev_server.py
"""
from __future__ import annotations

import http.server
import os
import socketserver
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(os.environ.get("PORT", "8080"))

# Removed root *.html files → extensionless path (301)
REDIRECT: dict[str, str] = {
    "/home.html": "/",
    "/richview-about.html": "/about/",
    "/richview-borrowers.html": "/borrowers/",
    "/richview-capital-brokers.html": "/brokers/",
    "/richview-capital-mic.html": "/investors/",
    "/richview-faq.html": "/faq/",
    "/richview-blog.html": "/blog/",
    "/richview-what-is-a-mic.html": "/what-is-a-mic/",
    "/blog-second-mortgages-when-they-help.html": "/blog/",
    "/blog-construction-financing-ontario.html": "/blog/construction-financing-ontario/",
    "/blog-mics-registered-accounts.html": "/blog/",
    "/privacy.html": "/privacy/",
    "/terms.html": "/terms/",
    "/disclaimer.html": "/disclaimer/",
    "/thank-you.html": "/thank-you/",
}


def _normalize_path(path: str) -> str:
    if len(path) > 1 and path.endswith("/"):
        return path.rstrip("/")
    return path


class DevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _maybe_redirect(self) -> bool:
        parsed = urlparse(self.path)
        path = _normalize_path(parsed.path)
        query = parsed.query
        if path not in REDIRECT:
            return False
        loc = REDIRECT[path]
        if query:
            loc = f"{loc}?{query}"
        self.send_response(301)
        self.send_header("Location", loc)
        self.end_headers()
        return True

    def do_GET(self) -> None:  # noqa: N802
        if self._maybe_redirect():
            return
        super().do_GET()

    def do_HEAD(self) -> None:  # noqa: N802
        if self._maybe_redirect():
            return
        super().do_HEAD()


def main() -> None:
    os.chdir(ROOT)
    with socketserver.TCPServer(("", PORT), DevHandler) as httpd:
        print(f"Serving {ROOT} at http://127.0.0.1:{PORT}/")
        print("Use: python3 -m http.server (same folder routes). This server adds legacy *.html → clean 301s.")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
