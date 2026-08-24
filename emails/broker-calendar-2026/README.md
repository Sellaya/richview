# Richview Capital — Broker Email Calendar (May 18 – Aug 17, 2026)

HTML broker nurture emails generated from the 3-month calendar document. Each send is a **date-named file** ready to import into your ESP (Mailchimp, Klaviyo, HubSpot, etc.).

## Files

| File | Send date | Track |
|------|-----------|--------|
| `2026-05-18.html` … `2026-08-17.html` | Mon/Wed per calendar | See `calendar.json` |
| `calendar.json` | — | Subject, preview, title, track, raw body text |

## Design (matches Richview site)

- Background: navy `#0B1635`
- Accent: orange `#FF6600` (callout border, CTAs, value strip)
- Body: white `#FFFFFF`, 600px table layout
- Logo: `RC-logo-white.png` on production domain
- Default CTA: [Discuss your next deal](https://richviewcapitalmic.com/brokers/#contact-form)
- Value strip on general emails: Fast communication · Direct underwriter · Real conversations · Closings in 48 hours

## Cadence

- **May 18 – Jun 8:** General nurture only (warm list)
- **Jun 10 – Aug 5:** Mondays = general · Wednesdays = Lady Arlington campaign
- **Aug 10 – Aug 17:** Post-event recap + return to general

**27 emails** total.

## Regenerate

After updating `.email-calendar-extract.txt` (export from the Word doc):

```bash
python3 scripts/generate_broker_emails.py
```

## Preview locally

With the dev server running (`npm run dev`), open:

`http://127.0.0.1:8080/emails/broker-calendar-2026/2026-05-18.html`

Or open any `.html` file directly in a browser.
