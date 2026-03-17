# Richview Capital — Full Website Audit Report

**Date:** March 4, 2025  
**Scope:** Lottie integration, form handlers, consistency, mobile-first UX, bugs

---

## Executive Summary

| Category | Status |
|----------|--------|
| Lottie/Form Spinner | ✅ All 8 forms across 7 pages wired correctly |
| Script Load Order | ✅ `lottie-utils.js` loads before form handlers on all pages |
| CSS Consistency | ✅ `lottie-forms.css` on all form pages; `.lottie-spinner-wrap` styled |
| Form Field IDs | ✅ Consistent (`consultFirstName`, etc.; hero uses `heroConsult*`) |
| GHL Webhook | ✅ Same URL across all forms |
| Canadian Phone Formatter | ✅ Present on all 7 form pages |
| `prefers-reduced-motion` | ✅ Respected in lottie-utils + CSS |
| Dead Code | ✅ Removed: index.html nav script, home.html newsletterForm block |

---

## 1. Form Spinner Implementation

### Pages Audited (8 forms, 7 pages)

| Page | Form(s) | lottie-utils.js | lottie-forms.css | Spinner Logic | Error Restore |
|------|---------|-----------------|------------------|---------------|---------------|
| home.html | heroConsultationForm, consultationForm | ✅ | ✅ | ✅ | ✅ |
| richview-borrowers.html | consultationForm | ✅ | ✅ | ✅ | ✅ |
| richview-capital-brokers.html | consultationForm | ✅ | ✅ | ✅ | ✅ |
| richview-capital-mic.html | consultationForm | ✅ | ✅ | ✅ | ✅ |
| richview-what-is-a-mic.html | consultationForm | ✅ | ✅ | ✅ | ✅ |
| richview-about.html | consultationForm | ✅ | ✅ | ✅ | ✅ |
| richview-faq.html | consultationForm | ✅ | ✅ | ✅ | ✅ |

### Pattern Verified

- `spinnerHandle = window.RichviewLottie.showButtonSpinner(submitBtn, { size: window.innerWidth < 640 ? 18 : 20 })`
- Fallback: `submitBtn.disabled = true; submitBtn.textContent = 'Sending...'`
- On error: `if (spinnerHandle && spinnerHandle.restore) spinnerHandle.restore(); else if (submitBtn) { ... }`

---

## 2. Form Field Consistency

- **Standard CTA form:** `consultFirstName`, `consultLastName`, `consultEmail`, `consultPhone`, `consultInterest`, `consultMessage`
- **Hero form (home):** `heroConsultFirstName`, `heroConsultLastName`, etc.
- **Payload:** All use `service` from `consultInterest` / `heroConsultInterest`; field mapping is correct

---

## 3. Select Options (consultInterest)

All forms use the same options:

- Borrowing: Private mortgage or construction financing
- Investing: MIC investment opportunities
- Brokering: Partner with us

---

## 4. Assets & References

| Asset | Exists | Used By |
|-------|--------|---------|
| js/lottie-utils.js | ✅ | All 7 form pages |
| css/lottie-forms.css | ✅ | All 7 form pages |
| lottie/forms/README.md | ✅ | Docs |
| images/logo.png | ✅ | All pages |
| images/partner-*.png | ✅ | home.html |
| css/mobile-menu-fullscreen.css | ✅ | All main pages |
| css/button-contrast.css | ✅ | Form pages |

---

## 5. Mobile-First & Accessibility

- **Spinner:** 18px < 640px, 20px ≥ 640px
- **Touch target:** `.btn-loading` min-height 44px
- **Reduced motion:** `prefers-reduced-motion: reduce` disables spinner animation; static fallback used
- **Lottie-utils:** Skips Lottie when `prefersReducedMotion()` is true

---

## 6. Fixes Applied During Audit

1. **index.html** — Removed nav/menu script that referenced non-existent elements (`#mainNav`, `#mobileMenuBtn`, `#navLinks`).
2. **home.html** — Removed dead `newsletterForm` block (IDs `newsletterForm`, `heroSubmitBtn`, `heroFormSuccess` do not exist).

---

## 7. Thank-You Page

- Uses inline SVG check with `ty-check-path` stroke-draw (`tyDraw` keyframe).
- No dependency on `lottie-forms.css` or `lottie-utils.js`.
- Name personalization from `?name=` works as intended.

---

## 8. Pages Without Forms (No Lottie Needed)

| Page | Notes |
|------|------|
| index.html | Redirect only; no nav/forms |
| thank-you.html | Own SVG check animation |
| richview-blog.html | No consultation form |
| privacy.html | Legal page |
| terms.html | Legal page |
| disclaimer.html | Legal page |

---

## 9. Recommendations

- Optional: add `spinner-loading.json` and `success-check.json` under `lottie/forms/` per README.
- Optional: Phase 2 enhancements (hero background, CTA background) per `LOTTIE_STRATEGY.md`.

---

**Audit complete. No critical bugs. All form pages consistent and mobile-first.**
