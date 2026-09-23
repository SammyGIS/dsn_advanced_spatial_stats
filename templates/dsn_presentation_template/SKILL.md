---
name: dsn_presentation_template
description: Standard guidelines, structural design rules, typography constraints, and template standards for DSN masterclass slides and portal views.
---

# DSN Presentation & Slide Template Guidelines

This document codifies all required design principles, structural rules, aesthetic standards, and constraints for building and maintaining Data Science Nigeria (DSN) masterclass slide decks and companion web portals.

---

## 1. Canvas Dimensions & Stage Margins (Not "Full Full")
- **Aspect Ratio:** Always 16:9 widescreen format (`1280px` width $\times$ `720px` height).
- **Presentation Stage & Margins:**
  - The presentation viewport must use a soft workspace backdrop (`background: #f1f5f9;`) instead of stretching slides edge-to-edge.
  - Reveal.js must be configured with `margin: 0.06` so the 16:9 slide canvas has balanced gaps and spaces on all 4 sides:
    ```javascript
    width: 1280,
    height: 720,
    margin: 0.06, // 6% breathing room around slide canvas
    minScale: 0.2,
    maxScale: 1.2,
    center: false,
    hash: false,
    slideNumber: 'c / t',
    transition: 'slide'
    ```
- **Slide Elevation & Borders:**
  - The slide canvas (`.reveal .slides section`) floats on the stage with a subtle modern shadow and rounded corners:
    ```css
    .reveal .slides section {
        border-radius: 6px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: none !important; /* No artificial borders cutting through backgrounds */
    }
    ```
- **Branded Background Canvas:**
  - Cover slide: `image2.png` embedded as Base64 on `section.dsn-cover-slide`.
  - Content slides: `image8.png` embedded as Base64 on `section.dsn-content-slide`, featuring the signature bottom green-to-red baseline.
  - Ending slide: `image11.png` embedded as Base64 on `section.dsn-ending-slide`.
  - Top-Right Logo: `image7.png` anchored at `width: 80px; top: 18px; right: 32px;`.

---

## 2. Strict Prohibition: NO Top Subheading Tags or Colored Banners
- **Rule:** Never include pill tags, colored badge boxes, or subheading banners with background colors at the top of slides (e.g., `Methodological Breakdown`, `Core Axiom`, `Curriculum Architecture`).
- The slide must open cleanly with the main `<h2>` title aligned to the left.

---

## 3. Strict Prohibition: NO Colored Left Borders on Shapes / Cards
- **Rule:** Never use colored left borders or accent bars (`border-left: 3px solid ...`, `border-left: 4px solid ...`) on cards, shapes, or callout containers.
- All shapes must use uniform, subtle, soft neutral borders:
  ```css
  .card {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 8px !important;
      padding: 7px 11px !important;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
  }
  .callout, .concept-card, .lead-callout {
      background: #f8fafc !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 8px !important;
      padding: 6px 10px !important;
  }
  ```
- Classes like `card-rose`, `card-blue`, `card-amber`, `callout rose`, etc., that introduce colored vertical accent stripes are strictly forbidden.

---

## 4. Typography Hierarchy & Font Scaling
Always keep fonts compact, smart, and proportioned to ensure zero awkward wrapping or vertical overflows:
- **Slide Title (`<h2>`):** `font-size: 0.95em` (~`17.5px`), `font-weight: 600`, color `#0f172a`.
- **Subtitle / Category (`<h3>`):** `font-size: 0.68em` (~`14px`), color `var(--primary)`.
- **Card Header (`<h4>`):** `font-size: 0.54em` (~`11.5px`), `font-weight: 600`, color `#0f172a`.
- **Body Text (`<p>`, `<li>`):** `font-size: 0.36em` (~`9.5px`), `line-height: 1.38`, color `#334155`.
- **Lead Callout Text:** `font-size: 0.37em`, `line-height: 1.38`, color `#1e293b`.

---

## 5. Whitespace & Breathing Room
- **Bottom Clearance:** Content inside slides must never crowd or touch the DSN bottom signature red/green line.
- The slide container (`.slide-container, .slide-body`) must have a hard height limit (`max-height: 540px;`), ensuring at least **75px of clean white breathing room** above the bottom footer elements.

---

## 6. Slide 1 (Cover Slide) Specification
- **Background:** Cover network globe background (`figures/dsn_theme/image2.png` embedded as Base64).
- **Logo:** Top-left DSN logo (`figures/dsn_theme/image3.png` or Base64 embedded), `height: 48px;`.
- **Title:** `Advanced Spatial Statistics`, `font-size: 1.30em; font-weight: 700;`.
- **Subtitle:** `Theory, Intuition & Spatial Statistics Modeling`, `font-size: 0.65em; font-weight: 600; color: #0a7a0a;`.
- **Instructor / Author:** Positioned directly under the title/subtitle in **two distinct lines**:
  - Line 1: `Adedoyin S. Ajeyomi` (`font-size: 0.48em; font-weight: 600; color: #0f172a;`)
  - Line 2: `Data Science Nigeria (DSN)` (`font-size: 0.38em; font-weight: 500; color: #64748b;`)
- **Prohibition:** No bulky descriptive paragraphs (e.g., Earth Observation overview) or pill badge arrays on the cover slide. Keep it clean, executive, and moved comfortably up in the upper white area.

---

## 7. Slide Sequence & Coherence
- Introductory flow:
  1. Slide 1: Cover Slide
  2. Slide 2: Why Spatial Statistics in the Real World? (The 3 Fallacies: Average, Spillover, Capital Misallocation)
  3. Slide 3: The Core Objective: Operational Decisions Across 9,308 Nigerian Wards (5 Sectoral Questions)
  4. Slide 4: The Superpower of Spatial Statistics: ESDA vs. Traditional EDA
  5. Slide 5+: Methodological sequence starting directly with Spatial Fallacies (Ecological & Aspatial).
- Note: The Modifiable Areal Unit Problem (MAUP) slide is excluded from the opening sequence to preserve logical flow.

---

## 8. Companion Portal & Technical Notes View
- **Technical Note View:** Never strip or inline partial raw HTML of technical notes into an unstyled container. Always host `technical_notes.html` in an `<iframe>` (`id="docFrame"`) to preserve its native styling, sticky TOC index, Inter fonts, and KaTeX mathematical precision intact.
- **Sidebar Repository Link:** Include an official GitHub icon link pointing directly to `https://github.com/SammyGIS/dsn_advanced_spatial_stats` instead of a static "Download PPT" button.
- **Asset Portability:** All brand logos (`image3.png`, `image5.png`, `image7.png`) and slide background images (`image2.png`, `image8.png`, `image11.png`) should be Base64 embedded within the generated files to prevent broken paths.
