#!/usr/bin/env python3
"""Generate dated HTML broker emails from the calendar extract."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / ".email-calendar-extract.txt"
OUT_DIR = ROOT / "emails" / "broker-calendar-2026"
CALENDAR_JSON = OUT_DIR / "calendar.json"

NAVY = "#0B1635"
ORANGE = "#FF6600"
WHITE = "#FFFFFF"
MUTED = "#C5CAD6"
CTA_URL = "https://richviewcapitalmic.com/brokers/#contact-form"
LOGO_URL = "https://richviewcapitalmic.com/images/RC-logo-white.png"
SITE = "https://richviewcapitalmic.com"

DELIM = "─" * 20


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def inline_links(text: str) -> str:
    """Turn bare URLs and markdown-style [label] → url into links."""
    text = re.sub(
        r"\[([^\]]+)\]\s*→\s*(https?://\S+)",
        r'<a href="\2" style="color:#FF6600;font-weight:600;text-decoration:underline;">\1</a>',
        text,
    )
    text = re.sub(
        r"(?<![\"'=])(https?://\S+)",
        r'<a href="\1" style="color:#FF6600;font-weight:600;text-decoration:underline;">\1</a>',
        text,
    )
    return text


def parse_emails(raw: str) -> list[dict]:
    blocks = re.split(r"\n" + re.escape("─" * 60) + r"\n", raw)
    emails: list[dict] = []
    for block in blocks:
        m = re.search(
            r"^(?P<date>\d{4}-\d{2}-\d{2})\s*\([^)]+\)\s*—\s*EMAIL\s+\d+\s*—\s*(?P<title>.+)$",
            block,
            re.MULTILINE,
        )
        if not m:
            continue
        date = m.group("date")
        title = m.group("title").strip()
        subj = re.search(r"^Subject:\s*(.+)$", block, re.MULTILINE)
        preview = re.search(r"^Preview text:\s*(.+)$", block, re.MULTILINE)
        body_m = re.search(r"^Body:\s*\n(.*)$", block, re.MULTILINE | re.DOTALL)
        if not subj or not preview or not body_m:
            continue
        body = body_m.group(1).strip()
        track = "lady-arlington" if "LADY ARLINGTON" in title.upper() or "EVENT DAY" in title else "general"
        if "Post-Event" in title:
            track = "post-event"
        emails.append(
            {
                "date": date,
                "title": title,
                "track": track,
                "subject": subj.group(1).strip(),
                "preview": preview.group(1).strip(),
                "body": body,
            }
        )
    return emails


def body_to_html(body: str, track: str) -> tuple[str, bool]:
    """Returns (html_fragment, has_value_strip)."""
    lines = body.splitlines()
    parts: list[str] = []
    i = 0
    has_value_strip = False
    in_callout = False
    callout_lines: list[str] = []
    list_items: list[str] = []
    list_mode: str | None = None  # ul | ol

    def flush_list() -> None:
        nonlocal list_items, list_mode
        if not list_items:
            return
        tag = "ol" if list_mode == "ol" else "ul"
        lis = "".join(
            f'<li style="margin:0 0 8px;color:{WHITE};font-size:15px;line-height:1.55;">{inline_links(esc(x))}</li>'
            for x in list_items
        )
        parts.append(
            f'<{tag} style="margin:0 0 16px 20px;padding:0;">{lis}</{tag}>'
        )
        list_items = []
        list_mode = None

    def flush_callout() -> None:
        nonlocal callout_lines, in_callout
        if not callout_lines:
            in_callout = False
            return
        inner = "<br>".join(
            inline_links(esc(ln)) for ln in callout_lines if ln.strip()
        )
        parts.append(
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:20px 0;border-left:4px solid {ORANGE};background:rgba(255,102,0,0.12);">'
            f'<tr><td style="padding:16px 18px;font-size:15px;line-height:1.6;color:{WHITE};">'
            f"{inner}</td></tr></table>"
        )
        callout_lines = []
        in_callout = False

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if stripped == "[ORANGE CALLOUT BOX]":
            flush_list()
            in_callout = True
            i += 1
            continue
        if stripped == "[/ORANGE CALLOUT BOX]":
            flush_callout()
            i += 1
            continue
        if in_callout:
            callout_lines.append(line)
            i += 1
            continue

        if stripped.startswith("[VALUE PROP STRIP]"):
            has_value_strip = True
            i += 1
            if i < len(lines) and "|" in lines[i]:
                props = [p.strip() for p in lines[i].split("|") if p.strip()]
                cells = "".join(
                    f'<td width="25%" align="center" style="padding:8px 4px;font-size:10px;font-weight:700;'
                    f'letter-spacing:0.04em;text-transform:uppercase;color:{ORANGE};line-height:1.35;">'
                    f"{esc(p)}</td>"
                    for p in props
                )
                parts.append(
                    f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
                    f'style="margin:24px 0 8px;border-top:1px solid rgba(255,255,255,0.15);'
                    f'border-bottom:1px solid rgba(255,255,255,0.15);"><tr>{cells}</tr></table>'
                )
                i += 1
            continue

        cta_m = re.match(r"^\[([^\]]+)\](?:\s*→\s*(https?://\S+))?$", stripped)
        if cta_m:
            flush_list()
            label = cta_m.group(1)
            url = cta_m.group(2) or CTA_URL
            parts.append(
                f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:18px 0;">'
                f'<tr><td align="left" style="border-radius:8px;background:{ORANGE};">'
                f'<a href="{esc(url)}" style="display:inline-block;padding:14px 22px;font-size:14px;'
                f'font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:{WHITE};'
                f'text-decoration:none;">{esc(label)}</a></td></tr></table>'
            )
            i += 1
            continue

        if re.match(r"^•\s+", stripped):
            flush_callout()
            if list_mode not in (None, "ul"):
                flush_list()
            list_mode = "ul"
            list_items.append(re.sub(r"^•\s+", "", stripped))
            i += 1
            continue

        num_m = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        if num_m:
            flush_callout()
            if list_mode not in (None, "ol"):
                flush_list()
            list_mode = "ol"
            list_items.append(num_m.group(2))
            i += 1
            continue

        if not stripped:
            # Keep numbered/bullet lists intact across blank lines in the doc export
            if list_mode and list_items:
                i += 1
                continue
            flush_list()
            flush_callout()
            i += 1
            continue

        if stripped.startswith("— "):
            flush_list()
            # Sign-off rendered in email footer for Lady Arlington / post-event tracks
            if track in ("lady-arlington", "post-event"):
                i += 1
                continue
            parts.append(
                f'<p style="margin:20px 0 0;font-size:15px;line-height:1.6;color:{MUTED};font-style:italic;">'
                f"{inline_links(esc(stripped))}</p>"
            )
            i += 1
            continue

        if stripped in ("Richview Capital MIC Inc.", "Richview Capital MIC Inc"):
            i += 1
            continue

        flush_list()
        flush_callout()

        if stripped == "BROKER UPDATE" or stripped.startswith("BROKER UPDATE —"):
            i += 1
            continue

        # ALL CAPS headline (short block line)
        if stripped.isupper() and len(stripped) > 12 and not stripped.startswith("DAY "):
            parts.append(
                f'<h1 style="margin:0 0 18px;font-size:22px;font-weight:800;line-height:1.25;'
                f'letter-spacing:0.02em;color:{WHITE};text-transform:uppercase;">{esc(stripped)}</h1>'
            )
            i += 1
            continue

        parts.append(
            f'<p style="margin:0 0 14px;font-size:15px;line-height:1.65;color:{WHITE};">'
            f"{inline_links(esc(stripped))}</p>"
        )
        i += 1

    flush_list()
    flush_callout()
    if track.startswith("lady") and not has_value_strip:
        # Lady Arlington emails often lack value strip — OK
        pass
    return "".join(parts), has_value_strip


def render_email(meta: dict) -> str:
    track = meta["track"]
    eyebrow = "BROKER UPDATE"
    if track == "lady-arlington":
        eyebrow = "BROKER UPDATE — LADY ARLINGTON 2026"
    elif track == "post-event":
        eyebrow = "BROKER UPDATE"

    body_html, has_strip = body_to_html(meta["body"], track)
    if not has_strip and track == "general":
        body_html += (
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:24px 0 8px;border-top:1px solid rgba(255,255,255,0.15);'
            f'border-bottom:1px solid rgba(255,255,255,0.15);"><tr>'
            f'<td width="25%" align="center" style="padding:8px 4px;font-size:10px;font-weight:700;'
            f'letter-spacing:0.04em;text-transform:uppercase;color:{ORANGE};">FAST<br>COMMUNICATION</td>'
            f'<td width="25%" align="center" style="padding:8px 4px;font-size:10px;font-weight:700;'
            f'letter-spacing:0.04em;text-transform:uppercase;color:{ORANGE};">DIRECT<br>UNDERWRITER</td>'
            f'<td width="25%" align="center" style="padding:8px 4px;font-size:10px;font-weight:700;'
            f'letter-spacing:0.04em;text-transform:uppercase;color:{ORANGE};">REAL<br>CONVERSATIONS</td>'
            f'<td width="25%" align="center" style="padding:8px 4px;font-size:10px;font-weight:700;'
            f'letter-spacing:0.04em;text-transform:uppercase;color:{ORANGE};">CLOSINGS IN<br>48 HOURS</td>'
            f"</tr></table>"
        )

    if track == "general":
        footer = "Richview Capital MIC Inc."
    elif track == "post-event":
        footer = "— Guido, Natasha, Maurizio, Randall & the Richview Capital team"
    else:
        footer = "— The Richview Capital Team"
    footer_extra = (
        '<p style="margin:8px 0 0;font-size:12px;color:#8B93A8;">'
        f'Mortgage Investment Corporation · Ontario · <a href="{SITE}" style="color:#8B93A8;">richviewcapitalmic.com</a>'
        "</p>"
    )

    preheader = esc(meta["preview"])
    subject = esc(meta["subject"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>{subject}</title>
  <!--
    Richview Capital broker email — {meta["date"]}
    Track: {meta["track"]} | {esc(meta["title"])}
    Subject: {subject}
    Preview: {preheader}
  -->
</head>
<body style="margin:0;padding:0;background-color:{NAVY};">
  <div style="display:none !important;font-size:1px;color:{NAVY};line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;">
    {preheader}
  </div>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{NAVY};">
    <tr>
      <td align="center" style="padding:24px 12px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">
          <tr>
            <td style="padding:0 0 20px;">
              <img src="{LOGO_URL}" width="180" height="115" alt="Richview Capital" style="display:block;border:0;height:auto;max-width:180px;">
            </td>
          </tr>
          <tr>
            <td style="padding:0 0 8px;font-size:11px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:{ORANGE};">
              {esc(eyebrow)}
            </td>
          </tr>
          <tr>
            <td style="padding:0 0 24px;">
              {body_html}
            </td>
          </tr>
          <tr>
            <td style="padding:20px 0 0;border-top:1px solid rgba(255,255,255,0.12);font-size:13px;line-height:1.5;color:{MUTED};">
              <strong style="color:{WHITE};">{esc(footer)}</strong>
              {footer_extra}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def main() -> None:
    raw = EXTRACT.read_text(encoding="utf-8")
    emails = parse_emails(raw)
    if len(emails) != 27:
        raise SystemExit(f"Expected 27 emails, parsed {len(emails)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for meta in emails:
        path = OUT_DIR / f"{meta['date']}.html"
        path.write_text(render_email(meta), encoding="utf-8")

    CALENDAR_JSON.write_text(
        json.dumps(
            {
                "campaign": "Richview Capital 3-Month Broker Calendar",
                "range": {"start": "2026-05-18", "end": "2026-08-17"},
                "cadence": "Monday and Wednesday mornings",
                "total": len(emails),
                "emails": emails,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {len(emails)} HTML files to {OUT_DIR}")


if __name__ == "__main__":
    main()
