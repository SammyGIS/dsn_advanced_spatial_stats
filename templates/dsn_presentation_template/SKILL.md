---
name: dsn_presentation_template
description: Canonical design system, strict user preferences, anti-patterns to avoid, and reusable guidelines for DSN masterclass slide presentations and companion portals.
---

# DSN Presentation & Slide Template Design Skill

This document is the definitive single source of truth for creating, modifying, and maintaining Data Science Nigeria (DSN) masterclass slide decks and companion web portals.

It explicitly codifies all architectural standards, design principles, and—most importantly—**the strict anti-patterns and aesthetic elements that the user explicitly dislikes and prohibits**.

---

## 🚫 WHAT THE USER STRICTLY DISLIKES (NEVER DO THESE)

To prevent mistakes, always review this list of explicit prohibitions before generating or modifying any slides:

### 1. ❌ NEVER Make the Presentation "Full-Full" / Edge-to-Edge
- **User feedback:** *"can you reduce my presentation page and not make it that full full give gaps and spaces around it please"*
- **Prohibition:** Never configure Reveal.js with `margin: 0` or `margin: 0.02` so that slides press right against the sidebar, topbar, or window edges.
- **The Correct Rule:**
  - Reveal.js must be configured with `margin: 0.06` (or `0.08`).
  - The viewport container (`.portal-viewport`) must use a soft workspace backdrop (`background: #f1f5f9;`).
  - The 16:9 slide canvas floats in the center with an elegant shadow (`box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);`) and rounded corners (`border-radius: 6px;`), creating a calm, framed presentation view with generous gaps on all four sides.

### 2. ❌ NEVER Use Colored Left Borders or Vertical Accent Bars on Shapes/Cards
- **User feedback:** *"all left border on all shapes is not allowed remove them all across the slides"*, *"remove the border colour arrange better and demarcate across all slides please"*
- **Prohibition:** Never apply colored left borders (`border-left: 3px solid ...`, `border-left: 4px solid ...`) or accent classes (`card-rose`, `card-blue`, `card-amber`, `callout rose`, `callout teal`, etc.).
- **The Correct Rule:**
  - A soft 1px border all the way round is fine, tinted to match the card (DSN green or red tint, see Rule 14). Never a thick or one-sided accent bar.
  - Baseline card:
    ```css
    .card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 7px 11px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    }
    ```
  - All colored border classes must be stripped.

### 3. ❌ NEVER Put Subheading Pill Tags / Category Badges with Backgrounds at the Top
- **User feedback:** *"remove all this subheading like this Methodological Breakdown everything with background at the top of each page remove everything I don't want to see that again at all"*
- **Prohibition:** Never insert `<span class="tag ...">` pills or colored banner tags above slide headers (e.g. `Methodological Breakdown`, `Core Axiom`, `Curriculum Architecture`).
- **The Correct Rule:**
  - Slides must open cleanly with the main `<h2>` title aligned to the left, unobstructed by badges or pill banners.

### 4. ❌ NEVER Place Bulky Descriptive Paragraphs or Pill Arrays on the Cover Slide
- **User feedback:** *"remove the text in red reduce the one in green boundary and move things up and also move my name under the advanced statistics and it should be in two lines"*
- **Prohibition:**
  - Do not put long descriptive paragraphs (e.g., Earth Observation masterclass overviews) on Slide 1.
  - Do not use pill badges (`Instructor: ... Platform: ... Curriculum: ...`) that crowd the bottom.
- **The Correct Rule:**
  - Title (*Advanced Spatial Statistics*) and Subtitle (*Theory, Intuition & Spatial Statistics Modeling*) must be compact and positioned high up in the upper white curve.
  - Only the instructor name sits beneath the title/subtitle. **No "Data Science Nigeria (DSN)" line under the name** (user: *"remove this Data Science Nigeria (DSN) that is under my name"*):
    ```html
    <div class="dsn-cover-author">
        <div class="author-name">Adedoyin S. Ajeyomi</div>
    </div>
    ```
  - The subtitle must render in DSN green. `.reveal h3` sets a blue colour with higher specificity, so target it as `.reveal h3.dsn-cover-subtitle { color: var(--dsn-green) !important; }`.

### 5. ❌ NEVER Use Large, Overcrowded, or Awkwardly Wrapping Fonts
- **User feedback:** *"reduce font size"*, *"reduce font if need be please"*
- **Prohibition:** Never use large headings (`1.85em`+) or long body text that wraps into multiple unnecessary lines or cramps the slide.
- **The Correct Rule (Font Scale):**
  - **Slide Title (`<h2>`):** `0.86em`, `line-height: 1.25`, `font-weight: 600`, header `max-width: 1060px` so most titles fit on one line.
  - **Subtitle (`<h3>`):** `0.68em` (~`14px`), `font-weight: 600`.
  - **Card Title (`<h4>`):** `0.54em` (~`11.5px`), `font-weight: 600`.
  - **Body Text (`<p>`, `<li>`):** `0.36em` (~`9.5px`), `line-height: 1.38`.
  - **Lead Callout Text:** `0.37em` (~`10px`), `line-height: 1.38`.

### 6. ❌ NEVER Crowd the Bottom Signature DSN Green/Red Footer Line
- **User feedback:** *"give gaps and spaces around it please"*
- **Prohibition:** Never allow cards or content to stretch down to the bottom edge where they touch or overlap the DSN signature green-to-red baseline.
- **The Correct Rule:**
  - Set a strict height ceiling on `.slide-container, .slide-body`:
    ```css
    .slide-container, .slide-body {
        max-height: 540px;
        overflow: hidden;
    }
    ```
  - Per-slide body heights (`.why-body` 540px, `.body-2line` for two-line titles, dense slides up to 560px) are fine, as long as every card ends **clearly above** the green/red footer line and nothing is clipped.
  - Always verify with a headless-browser screenshot of every changed slide (Playwright, `deck.slide(n)`) before reporting done.

### 7. ❌ NEVER Create Artificial Inner Border Boxes That Cut Through Slide Backgrounds
- **Prohibition:** Do not place borders on `.reveal .slides section` if Reveal's `data-background-image` separates the background from the section, creating a visible rectangular outline cutting across the background art (e.g. cutting into the green globe).
- **The Correct Rule:**
  - Base64-embed slide backgrounds directly on `.reveal .slides section.dsn-cover-slide`, `.dsn-content-slide`, and `.dsn-ending-slide`.
  - Keep `border: none !important;` on `.reveal .slides section` so the slide canvas is a continuous, elevated 16:9 sheet.

### 8. ❌ NEVER Strip or Alter Companion Document Styling (e.g., Technical Notes)
- **User feedback:** *"you have used a design to saturate my personal preference like the technical note for example I want the way it used to be with everything proper"*
- **Prohibition:** Never extract partial body HTML from companion documents (like `technical_notes.html`) and paste it into an unstyled div.
- **The Correct Rule:**
  - Companion documents must be loaded in an `<iframe>` (`id="docFrame"`), ensuring 100% preservation of their native CSS, typography (Inter), KaTeX mathematical formulas, and sticky Table of Contents (TOC).

### 9. ❌ NEVER Include Download PPT Links When a GitHub Link Is Specified
- **User feedback:** *"instead of download ppt add this github icon and this link to direct it please: https://github.com/SammyGIS/dsn_advanced_spatial_stats"*
- **The Correct Rule:**
  - Always render the official GitHub SVG icon with a clean link button pointing to the repository.

### 11. ❌ NEVER Clump Navigation Arrows Together in the Bottom-Right Corner
- **User feedback:** *"move the let facing arrow to the other side pleae"*
- **Prohibition:** Do not leave Reveal.js's default controls clustered together in the bottom-right corner.
- **The Correct Rule:**
  - Separate `.navigate-left` and `.navigate-right`:
    - Move `.reveal .controls .navigate-left` to the **bottom-left** corner (`bottom: 14px; left: 24px;`).
    - Keep `.reveal .controls .navigate-right` in the **bottom-right** corner (`bottom: 14px; right: 24px;`).
    - Position the slide number (`.reveal .slide-number`) cleanly inside the bottom-right corner (`right: 68px; bottom: 18px;`) so it never collides with the arrow.

### 12. ❌ Slide 2 MUST Always Be the Agenda Slide (from Master Template)
- **User feedback:** *"the seocnd appge on mys ldie shoudl be my agneda page please"*
- **The Correct Rule:**
  - Slide 1 is the Cover Slide.
  - Slide 2 is the **Agenda Slide** (`dsn-agenda-slide`) matching `DSN New Presentation Slides .pptx`:
    - Left ~45%: Dark green tech background with tablet icon and bold white "Agenda" title.
    - Right ~55%: DSN color logo at top-right, with 4 structured agenda rows:
      - `01` | My Journey into Geospatial
      - `02` | Career Pathways & Opportunities in Geospatial
      - `03` | Skills, Tools & Staying Relevant
      - `04` | Q&A / Open Discussion
    - Red numbered badge blocks (`#ff0000`, 64x60px, rounded corners) straddling the seam.
    - Subtle horizontal divider lines between items.
  - Core curriculum slides follow starting from Slide 3.

### 13. ❌ NEVER Add Extra Words; Fill Space With Visuals Instead
- **User feedback:** *"the current slide is too busy ... i only said we should make the styling and arrangement fitted to the page, not add more words"*, *"dont add those words or content but design them well with diagrams or images"*
- **Prohibition:** Never pad cards with extra text such as `TRAP 01` pills, sub-subtitles, "Blindspot / Ground Reality / Spatial Remedy" boxes or summary banners the user did not write.
- **The Correct Rule:**
  - When the user supplies slide text, use it **verbatim**, with no additions and no paraphrase.
  - Fill empty space with **visuals**: an inline SVG diagram panel at the top of each card, then a numbered badge + title row, a thin divider, then the text.
  - Enlarge fonts and let cards stretch (`flex: 1`) so the slide looks fitted, never half empty.

### 14. ✅ Use the Exact DSN Logo Colours, Never Grey Backgrounds
- **User feedback:** *"i dont like those grey background the red and green colour from the dsn logo can be used to beautify the slides"*, *"the colour of red and green in the logo, maintain it"*
- **The Correct Rule:**
  - Sampled from the logo: green `#00a859`, red `#ed3237`. Tints: green `#eef9f3` / line `#c4e9d5`; red `#fdf0f0` / line `#f8cfd0`; dark green text `#007f43`.
  - Replace every grey slide background (`#f8fafc`, `#f1f5f9`) with these tints. Alternate green / red / green across sibling cards (`:nth-child(2)` red).
  - Number badges: solid green or red circles with white numerals.

### 15. ✅ Visual Assets: Diagrams, Real Project Maps, Official Logos
- Diagrams are inline SVG built by `svg_*()` helpers in `scripts/build_dsn_presentation.py` (hex grids, ripples, shuffle grids, bar charts), all in the DSN palette.
- Real maps are cropped from the project's own analysis figures into `docs/figures/dsn_theme/slides/` (healthcare deserts, retail tiers, religious geography, Lorenz curves, Moran scatterplot, LISA clusters).
- Tool logos are downloaded from official sources (Wikimedia Commons, project GitHub repos) into `docs/figures/dsn_theme/logos/`. `get_b64()` must emit `image/svg+xml` for `.svg`.

### 16. ✅ Ending Slide Is Minimal
- **User feedback:** *"remove the content in the red part region"*
- Only the white DSN logo, "Thank you" and "Q&A / Open Discussion". No info card, no course summary, no name/organisation row.

### 17. ✅ Current Deck Structure
1. Cover · 2. Agenda (8 items: My Journey; Why Spatial Statistics; ESDA, Moran's I & LISA; Testing & Modelling Spatial Dependence; Space-Time Pattern Mining; Tools & Notebook Use Cases; Career Pathways & Skills; Q&A) · 3–8. Why Spatial Statistics, Core Objective, ESDA Superpower, What EDA Misses, What ESDA Unlocks ×2 · 9. Workflow · 10. **Spatial Dependence Testing Toolkit** (Global: Moran's I, Geary's C, General G, Join Counts; Local: LISA, Gi*, Bivariate LISA, Local Geary; Model diagnostics: residual Moran's I + LM tests) · 11–14. SAR, SEM, SDM, GWR & MGWR · 15. Space-Time Pattern Mining · 16. Tools · Ending.
- "Course Overview" must never appear in a slide heading.
- Treat Nigeria's wards as a **worked example**, never as an absolute claim (write "e.g. areas with...", "using Nigeria's administrative wards as a worked example").
- Say **"purchasing power"**, not "relative wealth" / "Relative Wealth Index", on slides.
- Agenda badges use the DSN logo red; eight compact rows (50×44 badges) fit the template.

### 18. ✅ Examples Must Be Honest and Instantly Readable
- **User feedback:** *"the values are examples, not actually done, state it that way, and let it be explainable so one reads and understands instantly"*
- Hypothetical numbers are labelled **"Illustrative examples (numbers are hypothetical)"** on slides and **"Illustrative Example"** in the Technical Note. Real outputs from the class data are labelled **"Course Result"**.
- Write examples in plain words ("a campaign at one store also lifts sales at nearby stores"), with at most one number per sentence.
- Simulated data (the malaria columns from `enrich_malaria_epidemiology.py`) must always be declared as simulated.

### 19. ✅ Diagrams: Prefer Real Map Boundaries
- **User feedback:** *"using a map boundary to show this would have been better"*
- Where a concept can be shown on real geography, draw it from the ward polygons (e.g. `scripts/export_lisa_neighbourhoods.py` renders one significant ward per LISA category with its actual queen neighbours).
- Use abstract grids only when no real example exists.

### 20. ✅ Space-Time Slide Pattern
- Rebuild reference visuals cleanly; never paste screenshots (user: *"don't show that it was a screenshot, clean it up, rebuild it well"*).
- Layout: a 3-step strip (Create Space Time Cube → Gi* per bin → Mann-Kendall), then the 8 hot + 8 cold + "No Pattern Detected" legend in conventional ArcGIS styles (glow = intensifying, pale centre = diminishing, speckle = sporadic/oscillating), next to an isometric bin map, then a "Reading the map" banner.
- Wrap small labels in their own class (e.g. `.st-sub`), never style bare `span` elements, or KaTeX output breaks.

### 21. ✅ Technical Note & Class Notebook
- The Technical Note keeps its style but carries a diagram in every section (shared SVG helpers in `scripts/technical_note_diagrams.py`), full Moran's I / LISA / Gi* interpretation, a Space-Time Pattern Mining section, and no "Model Selection Protocol" section.
- The portal sidebar shows **one** class notebook (`notebooks_html/spatial_statistics_use_cases.html`) under "Class Notebook"; the old four module notebooks are not linked. The sidebar heading reads "Class Presentation", not "Course Presentation".
- The notebook opens with a use-case table of contents; each use case follows: problem → hypothesis → the usual aspatial/ML approach → the spatial statistics method → code that runs → a markdown interpretation of the actual outputs.

---

## 📐 CORE SPECIFICATIONS & ASSET REFERENCE

### 1. 16:9 Canvas Dimensions
- **Width:** `1280px`
- **Height:** `720px`
- **Reveal Configuration:**
  ```javascript
  let deck = new Reveal(document.getElementById('revealDeck'), {
      width: 1280,
      height: 720,
      margin: 0.06,
      minScale: 0.2,
      maxScale: 1.2,
      controls: true,
      progress: true,
      center: false,
      hash: false,
      slideNumber: 'c / t',
      transition: 'slide'
  });
  deck.initialize();
  ```

### 2. DSN Brand Media Assets
All media extracted from official DSN slide decks located in `docs/figures/dsn_theme/`:
- `image2.png`: Cover slide network globe background.
- `bg_agenda.png`: Slide 2 master template Agenda background.
- `image3.png`: Cover slide DSN color logo (top-left).
- `image7.png`: Content slide DSN color logo (top-right, `width: 80px; top: 18px; right: 32px;`).
- `image8.png`: Content slide 16:9 canvas with signature bottom green/red line.
- `image11.png`: Ending slide dark AI network background.
- `image5.png`: Ending slide white DSN logo.

All images must be Base64-encoded in the build script to guarantee path independence across local servers and GitHub Pages.

---

## ✅ RELEASE VERIFICATION CHECKLIST

Before committing or pushing any new presentation updates, verify:
- [ ] Are slides framed on a `#f1f5f9` stage with `margin: 0.06` (no edge-to-edge "full full")?
- [ ] Is the left navigation arrow (`<`) at the bottom-left corner and the right arrow (`>`) at the bottom-right corner?
- [ ] Is Slide 2 the Agenda page matching `DSN New Presentation Slides .pptx`?
- [ ] Are all colored left border stripes (`card-rose`, `card-blue`, `card-amber`, etc.) completely absent?
- [ ] Are all top subheading pill tags (`<span class="tag">`) completely removed?
- [ ] Does Slide 1 show only Title, green Subtitle and the author name (no organisation line)?
- [ ] Are titles `0.86em` and does every slide fit above the green/red footer line (screenshot-verified)?
- [ ] Is user-supplied text verbatim, with no added pills, subtitles or banners?
- [ ] Are backgrounds DSN green/red tints (`#00a859` / `#ed3237`), with no grey boxes?
- [ ] Does every content card carry a diagram or real map rather than extra words?
- [ ] Is the ending slide only logo + "Thank you" + "Q&A / Open Discussion"?
- [ ] Are hypothetical numbers labelled illustrative and simulated data declared?
- [ ] Does the sidebar link only the single class notebook?
- [ ] Does clicking "Technical Note" load `technical_notes.html` in an iframe with sticky TOC and KaTeX math intact?
- [ ] Does the sidebar link to GitHub with an SVG icon?
- [ ] Is the template folder committed only on `template` branch, keeping `main` clean?

