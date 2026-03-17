# Richview Capital — Motion Specification

**Version:** 1.0  
**Last updated:** March 2025  
**Scope:** Full website animation blueprint for fintech-appropriate, high-quality motion.

---

## 1. Global Motion System

### 1.1 Standard Durations (ms)

| Token | Value | Use Case |
|-------|-------|----------|
| `--motion-fast` | 150ms | Hovers, focus states, microinteractions |
| `--motion-medium` | 350ms | Card transitions, dropdowns, accordions |
| `--motion-reveal` | 500ms | Scroll-triggered reveals |
| `--motion-slow` | 700ms | Hero content, major section entrances |

### 1.2 Standard Easing

| Token | Value | Use Case |
|-------|-------|----------|
| `--ease-out` | cubic-bezier(0.16, 1, 0.3, 1) | Default for all animations |
| `--ease-spring` | cubic-bezier(0.34, 1.56, 0.64, 1) | Optional: playful microinteractions only |
| `--ease-in-out` | cubic-bezier(0.4, 0, 0.2, 1) | Accordions, nav transitions |

### 1.3 Hover Rules (Global)

| Property | Default | Hover |
|----------|---------|-------|
| transform | none | translateY(-2px) |
| box-shadow | base | elevated (see per-element) |
| Cards: scale | 1 | 1.02 (optional, subtle) |

### 1.4 Reveal Rules (Global)

| Property | Initial | Final |
|----------|---------|-------|
| opacity | 0 | 1 |
| transform | translateY(24px) | translateY(0) |
| Mobile translateY | 16px | 0 |

### 1.5 Parallax Rules

| Layer | Scroll factor | Notes |
|-------|---------------|-------|
| Background | 0.05–0.08 | Very subtle |
| Mid-layer | 0.10–0.12 | Optional |
| Foreground | 0 | No parallax |

### 1.6 Reduced Motion

All animations MUST be wrapped or have a fallback:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Or use `transition: none` for elements that don't need animation in reduced-motion mode.

### 1.7 Performance Rules

- **Use only:** `transform`, `opacity`
- **Avoid:** `width`, `height`, `top`, `left`, `margin`, `box-shadow` in keyframe animations (use for transitions only, sparingly)
- **will-change:** Apply only during active animation; remove after
- **Implementation:** CSS transitions + IntersectionObserver for reveals (no GSAP required)

---

## 2. Navbar

### 2.1 Nav Container

| Property | Value |
|----------|-------|
| **Element** | `nav` |
| **Animation** | Shadow + position transition |
| **Trigger** | Scroll (class `.scrolled` when `scrollY > 30`) |
| **Duration** | 350ms |
| **Delay** | 0ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Transform** | none (position/shadow only) |
| **Mobile** | Same |
| **Implementation** | CSS transition on `box-shadow`, `top` |

### 2.2 Nav Hide on Scroll Down

| Property | Value |
|----------|-------|
| **Element** | `nav.nav-hidden` |
| **Animation** | translateY slide up |
| **Transform** | translateX(-50%) translateY(0) → translateX(-50%) translateY(calc(-100% - 2rem)) |
| **Trigger** | Scroll down past 120px |
| **Duration** | 350ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Mobile** | Disable nav-hide on mobile (< 1024px) — keep nav visible |
| **Implementation** | JS scroll listener + class toggle |

### 2.3 Nav Link Hover

| Property | Value |
|----------|-------|
| **Element** | `.nav-links > li > a` |
| **Animation** | Color + background |
| **Duration** | 200ms |
| **Delay** | 0ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Mobile** | Same |
| **Implementation** | CSS transition |

### 2.4 Mobile Menu Open — Nav Items Stagger

| Property | Value |
|----------|-------|
| **Element** | `.nav-links.active > li` |
| **Animation** | Fade + slide in |
| **Transform** | translateX(-10px) → translateX(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 320ms |
| **Delay** | nth-child * 30ms (0.03s, 0.06s, 0.09s…) |
| **Easing** | cubic-bezier(0.4, 0, 0.2, 1) |
| **Implementation** | CSS animation `navItemReveal` with `animation-delay: calc(0.03s * var(--i))` |
| **Performance** | Use `transform` + `opacity` only |

### 2.5 Dropdown Chevron

| Property | Value |
|----------|-------|
| **Element** | `.nav-dropdown > a::after` |
| **Animation** | Rotate |
| **Transform** | rotate(45deg) → rotate(-135deg) when `.open` |
| **Duration** | 250ms |
| **Easing** | cubic-bezier(0.4, 0, 0.2, 1) |
| **Implementation** | CSS transition on transform |

### 2.6 CTA Nav Button Hover

| Property | Value |
|----------|-------|
| **Element** | `.cta-nav` |
| **Animation** | Background, color, box-shadow |
| **Duration** | 200ms |
| **Transform** | Optional: scale(1.02) on hover |
| **Implementation** | CSS transition |

---

## 3. Hero

### 3.1 Hero H1 (Homepage slider)

| Property | Value |
|----------|-------|
| **Element** | `.hero-slide h1`, `.page-hero h1` |
| **Animation** | Fade-up reveal |
| **Transform** | translateY(30px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 700ms |
| **Delay** | 0ms (or slide-specific) |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Page load / slide change |
| **Mobile** | translateY(16px) → 0 |
| **Implementation** | CSS class `.reveal` + IntersectionObserver, or inline on slide change |

### 3.2 Hero Paragraph

| Property | Value |
|----------|-------|
| **Element** | `.hero-slide p`, `.page-hero p` |
| **Animation** | Fade-up reveal |
| **Transform** | translateY(30px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 700ms |
| **Delay** | 80ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Page load / slide change |
| **Mobile** | translateY(16px), delay 60ms |
| **Implementation** | Stagger via transition-delay on parent reveal |

### 3.3 Hero CTAs / Buttons

| Property | Value |
|----------|-------|
| **Element** | `.hero-ctas`, `.page-hero .hero-ctas` |
| **Animation** | Fade-up reveal |
| **Transform** | translateY(30px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 700ms |
| **Delay** | 160ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Page load |
| **Mobile** | translateY(16px), delay 120ms |
| **Implementation** | Stagger via transition-delay |

### 3.4 Hero Background (Parallax)

| Property | Value |
|----------|-------|
| **Element** | `.hero-bg-grid`, `.page-hero` background |
| **Animation** | Parallax on scroll |
| **Transform** | translateY(calc(var(--scroll-y, 0) * -0.08)) |
| **Trigger** | Scroll |
| **Scroll factor** | 0.05–0.08 |
| **Mobile** | Disable parallax (background-attachment: scroll) |
| **Implementation** | CSS custom property `--scroll-y` via minimal JS, or skip for performance |

### 3.5 Hero Trust Stats / Numbers (Homepage)

| Property | Value |
|----------|-------|
| **Element** | `.hero-trust-number`, `.cta-trust-item` |
| **Animation** | Fade-up with stagger |
| **Transform** | translateY(20px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 600ms |
| **Delay** | 250ms, 450ms, 650ms (per item) |
| **Easing** | cubic-bezier(0.25, 0.46, 0.45, 0.94) |
| **Implementation** | CSS animation or reveal + delay |

### 3.6 Hero Slider Progress Fill

| Property | Value |
|----------|-------|
| **Element** | `.hero-slider-progress-fill` |
| **Animation** | Width fill |
| **Trigger** | Slide change / timer |
| **Duration** | 5000ms (linear, for progress) |
| **Implementation** | CSS animation or JS width transition |

---

## 4. Section Headings

### 4.1 Section Heading Container

| Property | Value |
|----------|-------|
| **Element** | `.section-heading`, `.sec-head`, `.section-header` |
| **Animation** | Fade-up reveal |
| **Transform** | translateY(24px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 500ms |
| **Delay** | 0ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Scroll enter (IntersectionObserver, threshold 0.15) |
| **Mobile** | translateY(16px) → 0 |
| **Implementation** | Class `.reveal`, add `.visible` on intersect |

### 4.2 Section Heading H2

| Property | Value |
|----------|-------|
| **Element** | `.section-heading h2`, `.sec-head h2` |
| **Animation** | Inherits parent reveal (no separate animation) |
| **Note** | Stagger h2 and p only if separated in DOM |
| **Alternative** | h2 delay 0ms, p delay 50ms if in same block |

### 4.3 Section Heading Paragraph

| Property | Value |
|----------|-------|
| **Element** | `.section-heading p`, `.sec-head p` |
| **Animation** | Inherits parent or staggered |
| **Delay** | 50ms after h2 |
| **Implementation** | Same reveal block; use transition-delay on p |

---

## 5. Cards

### 5.1 Benefit Cards

| Property | Value |
|----------|-------|
| **Element** | `.benefit-card` |
| **Animation** | Fade-up reveal (staggered) |
| **Transform** | translateY(24px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 500ms |
| **Delay** | calc(50ms * var(--i, 0)) |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Scroll enter |
| **Hover** | translateY(-2px), box-shadow 0 8px 24px rgba(0,0,0,0.08) |
| **Hover duration** | 200ms |
| **Mobile** | Delay calc(40ms * var(--i)); hover unchanged |
| **Implementation** | `.reveal` + `style="--i: 0"` etc., IntersectionObserver |

### 5.2 Benefit Badge / Number Circle

| Property | Value |
|----------|-------|
| **Element** | `.benefit-badge`, `.benefit-number` |
| **Animation** | Hover feedback |
| **Transform** | scale(1) → scale(1.08) on card hover |
| **Background** | navy → gold on hover |
| **Duration** | 250ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Implementation** | CSS `.benefit-card:hover .benefit-badge` |

### 5.3 Product Cards (Borrowers, Brokers)

| Property | Value |
|----------|-------|
| **Element** | `.product-card`, `.about-value-card` |
| **Animation** | Fade-up reveal (staggered) |
| **Transform** | translateY(24px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 500ms |
| **Delay** | calc(50ms * var(--i, 0)) |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Hover** | translateY(-2px), box-shadow elevated |
| **Hover duration** | 200ms |
| **Implementation** | Same as benefit cards |

### 5.4 Blog Cards

| Property | Value |
|----------|-------|
| **Element** | `.blog-card` |
| **Animation** | Fade-up reveal (staggered) |
| **Transform** | translateY(24px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 500ms |
| **Delay** | calc(60ms * var(--i, 0)) |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Hover** | translateY(-2px) |
| **Implementation** | `.reveal` + `--i` |

### 5.5 Lifecycle / Guideline Cards

| Property | Value |
|----------|-------|
| **Element** | `.lifecycle-item`, `.guideline-card` |
| **Animation** | Fade-up reveal |
| **Transform** | translateY(20px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 450ms |
| **Delay** | calc(40ms * var(--i, 0)) |
| **Hover** | translateY(-2px), optional left border opacity |
| **Implementation** | Same pattern as benefit cards |

### 5.6 Value Cards (About, Investors)

| Property | Value |
|----------|-------|
| **Element** | `.value-card` |
| **Animation** | Fade-up + scale |
| **Transform** | translateY(20px) scale(0.98) → translateY(0) scale(1) |
| **Opacity** | 0 → 1 |
| **Duration** | 500ms |
| **Delay** | calc(50ms * var(--i, 0)) |
| **Hover** | translateY(-4px), scale(1.02), box-shadow |
| **Implementation** | GPU-friendly: transform + opacity only |

---

## 6. Tables

### 6.1 Term Sheet / Comparison Table Wrap

| Property | Value |
|----------|-------|
| **Element** | `.term-sheet-table-wrap`, `.comparison-table-wrap` |
| **Animation** | Fade-up reveal |
| **Transform** | translateY(24px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 500ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Scroll enter |
| **Hover** | box-shadow elevation (wrap hover) |
| **Implementation** | `.reveal` on wrapper |

### 6.2 Table Rows (Stagger)

| Property | Value |
|----------|-------|
| **Element** | `.term-sheet-table tbody tr`, `.comparison-table tbody tr` |
| **Animation** | Fade-up stagger (children of visible wrap) |
| **Transform** | translateY(12px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 400ms |
| **Delay** | calc(50ms * var(--i, 0)); mobile: calc(30ms * var(--i)) |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Parent `.term-sheet-table-wrap.visible` / `.comparison-table-wrap.visible` |
| **Row hover** | background rgba(255,102,0,0.04) |
| **Implementation** | Parent gets `.visible` from IntersectionObserver; rows animate via CSS when parent visible |

---

## 7. Stats

### 7.1 Hero Stat Bar Items

| Property | Value |
|----------|-------|
| **Element** | `.hero-stat-item` |
| **Animation** | Fade-up with stagger |
| **Transform** | translateY(16px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 500ms |
| **Delay** | calc(80ms * var(--i, 0)) |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Scroll enter or page load |
| **Implementation** | `.reveal` + `--i` |

### 7.2 Trust Strip / Marquee

| Property | Value |
|----------|-------|
| **Element** | `.trust-strip-inner`, `.partners-track` |
| **Animation** | Marquee scroll |
| **Duration** | 60s (trust), 50s (partners) linear infinite |
| **Pause** | animation-play-state: paused on hover |
| **Implementation** | CSS @keyframes translateX |
| **Performance** | Use transform only |

---

## 8. FAQ

### 8.1 FAQ Item Container

| Property | Value |
|----------|-------|
| **Element** | `.faq-item` |
| **Animation** | Fade-up reveal (staggered) |
| **Transform** | translateY(20px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 450ms |
| **Delay** | calc(50ms * var(--i, 0)) |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Scroll enter |
| **Implementation** | `.reveal` + `--i` |

### 8.2 FAQ Question (Accordion Trigger)

| Property | Value |
|----------|-------|
| **Element** | `.faq-q` |
| **Animation** | Hover / focus feedback |
| **Duration** | 200ms |
| **Implementation** | Background, border-color transition |

### 8.3 FAQ Chevron

| Property | Value |
|----------|-------|
| **Element** | `.faq-item .chevron` or `::after` |
| **Animation** | Rotate |
| **Transform** | rotate(0deg) → rotate(180deg) when open |
| **Duration** | 350ms |
| **Easing** | cubic-bezier(0.4, 0, 0.2, 1) |
| **Implementation** | CSS transition |

### 8.4 FAQ Answer Expand

| Property | Value |
|----------|-------|
| **Element** | `.faq-a` |
| **Animation** | max-height expand |
| **Duration** | 350ms |
| **Easing** | cubic-bezier(0.4, 0, 0.2, 1) |
| **Note** | Prefer grid-template-rows: 0fr → 1fr if structure allows (smoother) |
| **Implementation** | CSS transition on max-height or grid |

---

## 9. Forms

### 9.1 Form Input Focus

| Property | Value |
|----------|-------|
| **Element** | `input:focus`, `select:focus`, `textarea:focus` |
| **Animation** | Border/outline transition |
| **Duration** | 200ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Implementation** | CSS transition on border-color, outline |
| **Note** | Visible focus ring (2px gold) for accessibility |

### 9.2 Form Label

| Property | Value |
|----------|-------|
| **Element** | `label` |
| **Animation** | None (static) |
| **Optional** | Slight color change on focus-within |

### 9.3 Select Dropdown Chevron

| Property | Value |
|----------|-------|
| **Element** | Custom select arrow |
| **Animation** | Rotate on open (if applicable) |
| **Duration** | 200ms |

---

## 10. Buttons

### 10.1 Primary Button

| Property | Value |
|----------|-------|
| **Element** | `.btn-primary`, `.btn-pri` |
| **Animation** | Hover + active |
| **Hover** | Background, color, box-shadow transition |
| **Duration** | 200ms |
| **Active** | transform: scale(0.98) (optional, subtle) |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Implementation** | CSS transition |

### 10.2 Secondary / Outline Button

| Property | Value |
|----------|-------|
| **Element** | `.btn-secondary`, `.btn-sec` |
| **Animation** | Hover background, border |
| **Hover** | translateY(-2px) optional |
| **Duration** | 200ms |
| **Implementation** | CSS transition |

### 10.3 CTA Nav Button

| Property | Value |
|----------|-------|
| **Element** | `.cta-nav` |
| **Animation** | Same as primary |
| **Hover** | Background, box-shadow |
| **Duration** | 200ms |

### 10.4 Footer Back-to-Top

| Property | Value |
|----------|-------|
| **Element** | `.footer-back-top` |
| **Animation** | Hover lift |
| **Hover** | translateY(-2px), box-shadow |
| **Duration** | 200ms |
| **Implementation** | CSS transition |

---

## 11. CTA Sections

### 11.1 CTA Intro Block

| Property | Value |
|----------|-------|
| **Element** | `.cta-intro` |
| **Animation** | Fade-up reveal |
| **Transform** | translateY(24px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 600ms |
| **Delay** | 0ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Scroll enter |
| **Implementation** | `.reveal` + IntersectionObserver |
| **Optional** | Use `ctaBoxReveal` keyframe for slight overshoot |

### 11.2 CTA Box (Form Container)

| Property | Value |
|----------|-------|
| **Element** | `.cta-box` |
| **Animation** | Fade-up reveal |
| **Transform** | translateY(20px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 600ms |
| **Delay** | 100ms (after intro) |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Trigger** | Scroll enter |
| **Implementation** | `.reveal` with transition-delay |

### 11.3 CTA Primary Button (Soft Pulse — Optional)

| Property | Value |
|----------|-------|
| **Element** | `.cta-box .btn-primary` (main CTA only) |
| **Animation** | Subtle attention pulse |
| **Transform** | scale(1) → scale(1.01) → scale(1) |
| **Duration** | 3s ease-in-out infinite |
| **Delay** | 2s after CTA enters view |
| **Condition** | Only if no user interaction (e.g. scroll) in last 5s |
| **prefers-reduced-motion** | Disable this animation |
| **Implementation** | CSS @keyframes or IntersectionObserver + optional JS |
| **Note** | Very subtle; skip if too distracting |

---

## 12. Footer

### 12.1 Footer Sections

| Property | Value |
|----------|-------|
| **Element** | `.footer-col`, `.footer-brand` |
| **Animation** | None (static) or very subtle fade-in |
| **Note** | Footer typically doesn't need reveal (user has scrolled) |

### 12.2 Footer Links Hover

| Property | Value |
|----------|-------|
| **Element** | `.footer-col a`, `.footer-legal a` |
| **Animation** | Color transition |
| **Duration** | 200ms |
| **Implementation** | CSS transition |

### 12.3 Footer Dot Pulse (Trust Badge)

| Property | Value |
|----------|-------|
| **Element** | `.footer-dot`, `.footer-pulse` (if exists) |
| **Animation** | Optional subtle pulse |
| **Duration** | 2.5s ease-in-out infinite |
| **prefers-reduced-motion** | animation: none |
| **Implementation** | CSS @keyframes opacity or scale |

### 12.4 Back-to-Top Button

| Property | Value |
|----------|-------|
| **Element** | `.footer-back-top` |
| **Animation** | Fade-in when scroll past threshold |
| **Opacity** | 0 → 1 when shown |
| **Hover** | translateY(-2px) |
| **Duration** | 300ms |
| **Implementation** | JS visibility + CSS transition |

---

## 13. Protected List / Numbered List

| Property | Value |
|----------|-------|
| **Element** | `.protected-list li::before` |
| **Animation** | Hover feedback on number circle |
| **Transform** | scale(1) → scale(1.08) on li:hover |
| **Background** | navy → gold on hover |
| **Duration** | 250ms |
| **Easing** | cubic-bezier(0.16, 1, 0.3, 1) |
| **Implementation** | CSS `.protected-list li:hover::before` |

---

## 14. Process Cards, Lifecycle, Hero Dots, Partner Logos

| Element | Animation | Trigger | Duration | Notes |
|---------|-----------|---------|----------|-------|
| `.process-card` | fade-up stagger | scroll | 500ms | calc(60ms * var(--i)) |
| `.process-number`, `.lifecycle-number` | color change | parent hover | 250ms | var(--muted) → var(--gold) |
| `.hero-dot-item` | active state | click | 200ms | background/border transition |
| `.partner-logo-card img` | scale | hover | 200ms | scale(1.02) |

---

## 15. Scroll Progress Bar (Optional)

| Property | Value |
|----------|-------|
| **Element** | `.scroll-progress-bar` (new) |
| **Animation** | Width based on scroll |
| **Height** | 2–3px |
| **Background** | var(--gold) or var(--navy) |
| **Trigger** | Scroll |
| **Formula** | width: (scrollY / (docHeight - viewHeight)) * 100% |
| **Visibility** | Show when scrollY > 200 |
| **Mobile** | Optional: hide on mobile |
| **Implementation** | JS scroll listener + transform scaleX or width |
| **Performance** | Throttle scroll to 100ms; use transform scaleX(calc(var(--progress))) |

---

## 16. Implementation Checklist

### 16.1 CSS Variables (Add to `:root`)

```css
:root {
  --motion-fast: 150ms;
  --motion-medium: 350ms;
  --motion-reveal: 500ms;
  --motion-slow: 700ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### 16.2 Reduced Motion Override

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 16.3 Reveal Observer (Existing Pattern)

```javascript
const obs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      obs.unobserve(e.target);
    }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
```

### 16.4 Stagger Convention

Use `style="--i: 0"` through `--i: n` on sibling elements. Apply:

```css
transition-delay: calc(50ms * var(--i, 0));
```

---

## 17. File Mapping

| Section | Primary Files |
|---------|---------------|
| Navbar | All HTML (inline), `mobile-menu-fullscreen.css` |
| Hero | `home.html`, `hero-services.css`, page-specific heroes |
| Section headings | All pages, `what-is-a-mic-layout.css` |
| Cards | `benefit-cards-shared.css`, `product-cards-mortgage.css` |
| Tables | `what-is-a-mic-layout.css`, inline (term-sheet, comparison) |
| Stats | `hero-stat-bar.css`, `hero-services.css` |
| FAQ | `faq-section.css` |
| Forms | Inline per page |
| Buttons | `button-contrast.css`, `hero-services.css` |
| CTA | Inline, shared CTA patterns |
| Footer | Inline per page |

---

## 18. Additional Components

### 18.1 Process Cards (Borrowers, Brokers)

| Property | Value |
|----------|-------|
| **Element** | `.process-card`, `.process-number` |
| **Animation** | Fade-up reveal (staggered) |
| **Transform** | translateY(24px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 500ms |
| **Delay** | calc(60ms * var(--i, 0)) |
| **Implementation** | `.reveal` + `--i` |

### 18.2 Hero Dots / Slider Tabs

| Property | Value |
|----------|-------|
| **Element** | `.hero-dot-item` |
| **Animation** | Color/background on active |
| **Duration** | 200ms |
| **Implementation** | CSS transition |

### 18.3 Hero Form Wrap (Homepage Sidebar CTA)

| Property | Value |
|----------|-------|
| **Element** | `.hero-form-wrap`, `.cta-box` (in hero) |
| **Animation** | Fade-up on load |
| **Transform** | translateY(20px) → translateY(0) |
| **Opacity** | 0 → 1 |
| **Duration** | 600ms |
| **Delay** | 400ms |
| **Implementation** | CSS animation or reveal |

### 18.4 Partner Logo Cards

| Property | Value |
|----------|-------|
| **Element** | `.partner-logo-card` |
| **Animation** | Hover scale |
| **Hover** | scale(1.02) |
| **Duration** | 200ms |
| **Implementation** | CSS transition |

### 18.5 Leadership / Team Photos

| Property | Value |
|----------|-------|
| **Element** | `.leadership-photo`, `.tc-photo img` |
| **Animation** | Card hover — image subtle scale |
| **Hover** | scale(1.03) with overflow hidden on parent |
| **Duration** | 300ms |
| **Implementation** | CSS on parent card hover |

---

## 19. Quick Reference Card

| Element | Animation | Trigger | Duration | Delay | Transform |
|---------|-----------|---------|----------|------|-----------|
| `.hero h1` | fade-up | load | 700ms | 0 | 30px→0 |
| `.hero p` | fade-up | load | 700ms | 80ms | 30px→0 |
| `.hero-ctas` | fade-up | load | 700ms | 160ms | 30px→0 |
| `.section-heading` | fade-up | scroll | 500ms | 0 | 24px→0 |
| `.benefit-card` | fade-up stagger | scroll | 500ms | 50ms*--i | 24px→0 |
| `.benefit-card:hover` | lift | hover | 200ms | 0 | -2px |
| `.benefit-badge:hover` | scale | card hover | 250ms | 0 | 1.08 |
| Table rows | fade-up stagger | parent visible | 400ms | 50ms*--i | 12px→0 |
| `.faq-item` | fade-up stagger | scroll | 450ms | 50ms*--i | 20px→0 |
| `.cta-intro` | fade-up | scroll | 600ms | 0 | 24px→0 |
| `.cta-box` | fade-up | scroll | 600ms | 100ms | 20px→0 |
| `.btn-primary:hover` | color/shadow | hover | 200ms | 0 | — |
| `.btn-primary:active` | scale | click | 150ms | 0 | 0.98 |
| `.nav-links.active > li` | slide-in stagger | menu open | 320ms | 30ms*--i | -10px→0 |

**Easing (all):** `cubic-bezier(0.16, 1, 0.3, 1)`  
**Mobile:** Reduce translateY 30px→16px, 24px→16px where applicable.

---

**End of specification.**
