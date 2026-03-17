# Richview Capital — Lottie Animation Strategy

**Version:** 1.0  
**Date:** March 2025  
**Scope:** Animation blueprint for Lottie integration across fintech/mortgage website.

---

## Design Philosophy

Lottie animations on this site must feel **minimal, elegant, professional, trustworthy, and premium**. They should enhance clarity and perceived quality—never distract. Style reference: Stripe, Linear, Vercel, Framer—high-end SaaS with restraint.

**Use Lottie for:**
- States CSS cannot express well (loading spinners, success checkmarks)
- Lightweight icon motion (form feedback, microinteractions)
- Subtle background texture or depth
- Empty or transitional states

**Avoid Lottie for:**
- Animations CSS handles well (fade-up, hover, accordions)
- Decorative motion that competes with content
- Large, complex scenes
- Anything that feels playful or cartoonish

---

## Global Lottie Motion Design System

### Animation Tone
- **Calm** — No bouncy easing or overshoot
- **Precise** — Clean paths, consistent line weights
- **Subtle** — Low opacity when used as background
- **Purposeful** — Every animation serves a clear UX or brand goal

### Preferred Motion Types
- Line-based icons (1–2px stroke)
- Minimal geometric shapes (circles, light grids, dots)
- Soft gradient or dot motion for backgrounds
- Single-path icon animations (checkmark, loader)

### Maximum Durations
| Type | Max Duration |
|------|--------------|
| Microinteractions | 800ms |
| Icon loops | 2–4s |
| Background loops | 8–12s |
| Play-once feedback | 1.5s |

### Looping Rules
- **Backgrounds:** Loop indefinitely, very slow (8s+ per cycle)
- **Icons:** Loop only when indicating loading; otherwise play once
- **Microinteractions:** Play once on trigger (hover, click, success)
- **Max 2–3 looping animations** visible at once; pause offscreen

### Background Animation Rules
- Opacity: 4–8% when visible
- Use blend modes sparingly; avoid flashing
- Prefer horizontal or slow radial motion
- **Never** animate above primary content (z-index, layering)

### Icon Animation Rules
- Stroke-based (2–4px) for clarity
- Navy (#0B1635) or gold (#FF6600) as primary color
- Max 2–3 frames for simple icons; 1–2s for completion
- Static SVG fallback required for reduced-motion

### Microinteraction Rules
- Trigger: hover, focus, click, or state change
- Duration: 200–600ms
- Easing: ease-out or linear
- Must work without Lottie (graceful degradation)

### Performance Budget
- Single Lottie file: < 50KB (ideal < 20KB)
- Total Lottie payload per page: < 80KB
- Lazy-load all Lotties except hero (if used)
- Pause looping animations when not in viewport

---

## Section-by-Section Recommendations

---

### 1. Hero Section

#### 1.1 Hero Background (Optional)
| Property | Value |
|----------|-------|
| **Element** | `.hero-bg-grid` or new `.hero-lottie-bg` |
| **Purpose** | Add subtle depth; avoid flat hero |
| **Animation type** | Abstract geometric loop |
| **Style** | Thin line grid (1px), soft dot lattice, or gentle gradient wave |
| **Playback** | Autoplay, loop |
| **Duration** | ~10s per cycle |
| **Placement** | Full-width, behind hero content; z-index below copy |
| **Size** | 100% viewport width; height ~120vh |
| **Opacity** | 6–8% on desktop; 4% on mobile |
| **Mobile** | Simpler variant (fewer elements); lower opacity |
| **Performance** | Lazy-load; pause when hero exits viewport |
| **Fallback** | Existing CSS grid/gradient; no Lottie if reduced-motion |

#### 1.2 Hero Trust Icons (CTA Box)
| Property | Value |
|----------|-------|
| **Element** | `.cta-trust-item` SVG icons |
| **Purpose** | Reinforce "Instant Response," "Confidential," "Licensed" |
| **Animation type** | Icon microinteraction |
| **Style** | Line icon, 1–2px stroke, single loop or idle motion |
| **Playback** | Play on card hover or when CTA box enters view |
| **Duration** | 1–1.5s play once, or 3s loop if idle |
| **Placement** | Replace or augment existing SVG; ~24×24px |
| **Mobile** | Static SVG fallback preferred |
| **Fallback** | Keep current static SVGs |

---

### 2. Feature / Service Cards

#### 2.1 Services Section Icons
| Property | Value |
|----------|-------|
| **Element** | `.services-features .icon` (checkmark or product icon) |
| **Purpose** | Light emphasis on feature list items |
| **Recommendation** | **Skip Lottie** — keep static SVG checkmarks. Animation risks clutter. |
| **Alternative** | If used, one subtle check-draw (400ms) on scroll-into-view, once per section |

---

### 3. Mortgage Product Cards

#### 3.1 Product Card Icons
| Property | Value |
|----------|-------|
| **Element** | `.benefit-card`, `.product-card` icon/number area |
| **Purpose** | Gentle attention on hover |
| **Animation type** | Icon microinteraction |
| **Style** | Line icon; simple draw or fade-in |
| **Playback** | Play once on card hover |
| **Duration** | 400–600ms |
| **Placement** | Inside badge/number circle; max 32×32px |
| **Mobile** | Disable; use static icon |
| **Fallback** | Static SVG |

---

### 4. Process / Steps Section

#### 4.1 Process Number Indicator
| Property | Value |
|----------|-------|
| **Element** | `.process-number` or `.lifecycle-number` |
| **Purpose** | Soft motion when step is focused or hovered |
| **Animation type** | Number/ordinal icon |
| **Style** | Line numeral; slight scale or stroke-draw |
| **Playback** | Play once when card gains hover/focus |
| **Duration** | 300–500ms |
| **Placement** | Replace or augment number; ~28×28px |
| **Fallback** | Static numeral |

#### 4.2 Process Step Connector
| Property | Value |
|----------|-------|
| **Element** | Connector line between steps |
| **Purpose** | Optional "flow" feeling |
| **Recommendation** | **Skip Lottie** — CSS transition on hover is enough |

---

### 5. CTA Sections

#### 5.1 CTA Section Background
| Property | Value |
|----------|-------|
| **Element** | `.cta-section` background |
| **Purpose** | Separate CTA from body; add premium feel |
| **Animation type** | Soft geometric loop |
| **Style** | Dots or thin lines; very low opacity |
| **Playback** | Autoplay loop when section in view |
| **Duration** | ~8s |
| **Placement** | Full section; opacity 3–5% |
| **Mobile** | Optional; can skip |
| **Fallback** | Static gradient |

#### 5.2 CTA Button (Primary Submit)
| Property | Value |
|----------|-------|
| **Element** | `.cta-box button[type="submit"]` |
| **Purpose** | Loading and success states |
| **Animation type** | Loading spinner / success checkmark |
| **Style** | Line spinner (thin stroke); minimal checkmark |
| **Playback** | Loading: loop; Success: play once |
| **Duration** | Spinner: 1–1.5s loop; Check: 600–800ms once |
| **Placement** | Inline with button text; ~20×20px |
| **Fallback** | CSS spinner; static checkmark |

---

### 6. Form States

#### 6.1 Form Submit Loading
| Property | Value |
|----------|-------|
| **Element** | Submit button during `loading` |
| **Purpose** | Clear loading feedback |
| **Animation type** | Line spinner |
| **Style** | Circular, 2px stroke, single rotation |
| **Playback** | Loop while loading |
| **Duration** | 1s per rotation |
| **Placement** | Inside button; replace "Schedule Consultation" / "Submit" |
| **Fallback** | CSS `animation: spin` or text "Sending..." |

#### 6.2 Form Success
| Property | Value |
|----------|-------|
| **Element** | `.cta-form-success` icon |
| **Purpose** | Positive confirmation |
| **Animation type** | Checkmark draw |
| **Style** | Line check; single stroke path |
| **Playback** | Play once when success state appears |
| **Duration** | 500–700ms |
| **Placement** | Above "Thank you!" heading; ~48×48px |
| **Fallback** | Static checkmark SVG |

#### 6.3 Form Validation Error
| Property | Value |
|----------|-------|
| **Recommendation** | **Skip Lottie** — use CSS (border color, icon) or static icon |

---

### 7. Trust / Partner Sections

#### 7.1 Trust Strip
| Property | Value |
|----------|-------|
| **Recommendation** | **Skip Lottie** — existing CSS marquee is sufficient |

#### 7.2 Partners Section Badge
| Property | Value |
|----------|-------|
| **Element** | Optional badge near "Partners & Who We Work With" |
| **Purpose** | Light emphasis |
| **Recommendation** | **Skip** unless a single, very small (16×16px) icon adds value |

---

### 8. Section Backgrounds

| Section | Recommendation |
|---------|----------------|
| Hero | Optional soft grid/dot loop; see Hero 1.1 |
| Services | Skip — body grid is enough |
| About | Skip |
| Testimonials | Skip |
| Blog | Skip |
| FAQ | Skip |
| CTA | Optional; see CTA 5.1 |

**Rule:** Max 1–2 background Lotties per page.

---

### 9. Empty States

#### 9.1 No Results / Empty List
| Property | Value |
|----------|-------|
| **Element** | Empty state container (e.g. blog, search) |
| **Purpose** | Friendly "nothing here" message |
| **Animation type** | Minimal illustration |
| **Style** | Line icon; document, folder, or magnifier |
| **Playback** | Play once on mount or subtle 4s loop |
| **Duration** | 1.5s once, or 4s loop |
| **Placement** | Center; max 120×120px |
| **Fallback** | Static SVG illustration |

---

### 10. Loading States

#### 10.1 Page / Section Skeleton
| Property | Value |
|----------|-------|
| **Recommendation** | **Skip Lottie** — use CSS skeleton or simple spinner |

#### 10.2 Inline Content Load
| Property | Value |
|----------|-------|
| **Element** | Any async-loaded block |
| **Purpose** | Loading indicator |
| **Animation type** | Line spinner |
| **Style** | Single circle, 2px stroke |
| **Playback** | Loop |
| **Duration** | 1s |
| **Placement** | Centered in loading area; ~32×32px |
| **Fallback** | CSS spinner |

---

### 11. Icons Across UI

| Icon Location | Lottie? | Notes |
|---------------|---------|-------|
| Nav dropdown chevron | No | CSS rotate is enough |
| FAQ accordion chevron | No | CSS |
| CTA trust icons | Optional | See Hero 1.2 |
| Form success check | **Yes** | High value; clear feedback |
| Form loading spinner | **Yes** | Prefer Lottie over CSS if consistent with success |
| Benefit card badge | Optional | Hover play-once only |
| Process number | Optional | Hover play-once |
| Footer, links | No | Keep static |

---

## Implementation Priority

### Phase 1 — High Impact, Low Risk
1. **Form success checkmark** — Play-once, clear feedback
2. **Form loading spinner** — Replaces generic "Sending..."
3. **CTA section background** (optional) — Subtle loop

### Phase 2 — Enhanced Premium Feel
4. Hero background (if hero feels flat)
5. Hero CTA trust icons (hover or in-view)
6. Empty state illustration (if applicable)

### Phase 3 — Optional Refinements
7. Product card icon on hover
8. Process number on hover
9. CTA button loading state (reuse spinner)

---

## Performance Checklist

- [ ] All Lotties < 50KB each
- [ ] Lazy-load except hero (if used)
- [ ] Pause loops when offscreen (IntersectionObserver)
- [ ] `prefers-reduced-motion: reduce` → static fallback
- [ ] No more than 2–3 simultaneous loops per viewport
- [ ] Prefer `lottie-light` or tree-shakeable build

---

## File Naming & Organization

```
lottie/
  hero/
    hero-bg-grid.json
  forms/
    spinner-loading.json
    success-check.json
  cta/
    cta-bg-dots.json
  empty/
    empty-document.json
  icons/
    trust-instant.json
    trust-secure.json
    trust-license.json
```

---

## Reduced Motion

For `prefers-reduced-motion: reduce`:

- Do **not** load Lottie files
- Use static SVG or CSS-only fallbacks
- Ensure all states (loading, success, error) have static equivalents
- No background Lotties

---

## Summary: Recommended Lottie Count

| Category | Count | Priority |
|----------|-------|----------|
| Form feedback (spinner + success) | 2 | P1 |
| CTA background | 0–1 | P2 |
| Hero background | 0–1 | P2 |
| Hero trust icons | 0–3 | P2 |
| Empty state | 0–1 | P2 |
| Card/process hover | 0–2 | P3 |

**Total:** 2–8 Lottie files site-wide. Start with 2 (form states), then add background/icon refinements if they clearly improve perceived quality.

---

**End of Lottie Strategy.**
