"""
DSN Spatial Statistics Masterclass Deck & Portal - Refined Minimalist Theme.

Strict Design Rules:
1. NO colored borders on shapes/cards/callouts. Clean 1px solid #e2e8f0 only.
2. NO tags or subheadings with background at the top of slides.
3. Smart, smaller fonts: h2 (21px), h4 (13.5px), body p/li (11.5px - 12px).
4. Generous whitespace: slides leave comfortable 45px+ breathing room above the DSN bottom line.
5. GitHub link with official GitHub icon in the sidebar pointing to:
   https://github.com/SammyGIS/dsn_advanced_spatial_stats
6. Base64 embedded logos and backgrounds for 100% path independence.
7. Embedded Technical Notes view with KaTeX equations (ZERO 404).
"""

import os
import re
import base64

def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(path)[1].lower().replace(".", "")
        if ext == "jpg": ext = "jpeg"
        return f"data:image/{ext};base64,{data}"
    return ""

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dsn_theme_dir = os.path.join(base_dir, "docs", "figures", "dsn_theme")

    # Base64 assets
    logo_b64 = get_b64(os.path.join(dsn_theme_dir, "image7.png"))
    cover_logo_b64 = get_b64(os.path.join(dsn_theme_dir, "image3.png")) or logo_b64
    ending_logo_b64 = get_b64(os.path.join(dsn_theme_dir, "image5.png")) or logo_b64
    bg_content_b64 = get_b64(os.path.join(dsn_theme_dir, "image8.png"))
    bg_cover_b64 = get_b64(os.path.join(dsn_theme_dir, "image2.png"))
    bg_agenda_b64 = get_b64(os.path.join(dsn_theme_dir, "bg_agenda.png"))
    bg_ending_b64 = get_b64(os.path.join(dsn_theme_dir, "image11.png"))

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    slide_1 = f"""
            <!-- SLIDE 1: COVER SLIDE -->
            <section class="dsn-cover-slide">
                <div class="dsn-cover-container">
                    <img src="{cover_logo_b64}" alt="Data Science Nigeria" class="dsn-cover-logo">
                    <h1 class="dsn-cover-title">Advanced Spatial Statistics</h1>
                    <h3 class="dsn-cover-subtitle">Theory, Intuition &amp; Spatial Statistics Modeling</h3>
                    <div class="dsn-cover-author">
                        <div class="author-name">Adedoyin S. Ajeyomi</div>
                        <div class="author-org">Data Science Nigeria (DSN)</div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 2: AGENDA SLIDE (MATCHING DSN NEW PRESENTATION SLIDES PPTX)
    # =========================================================================
    slide_agenda = f"""
            <!-- SLIDE 2: AGENDA -->
            <section class="dsn-agenda-slide">
                <div class="agenda-items-wrap">
                    <div class="agenda-item-row">
                        <div class="agenda-num-box">01</div>
                        <div class="agenda-text-box">My Journey into Geospatial</div>
                    </div>
                    <div class="agenda-row-divider"></div>

                    <div class="agenda-item-row">
                        <div class="agenda-num-box">02</div>
                        <div class="agenda-text-box">Career Pathways &amp; Opportunities in Geospatial</div>
                    </div>
                    <div class="agenda-row-divider"></div>

                    <div class="agenda-item-row">
                        <div class="agenda-num-box">03</div>
                        <div class="agenda-text-box">Skills, Tools &amp; Staying Relevant</div>
                    </div>
                    <div class="agenda-row-divider"></div>

                    <div class="agenda-item-row">
                        <div class="agenda-num-box">04</div>
                        <div class="agenda-text-box">Q&amp;A / Open Discussion</div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 3: WHY SPATIAL STATISTICS IN THE REAL WORLD? (THE 3 FALLACIES)
    # =========================================================================
    slide_2 = f"""
            <!-- SLIDE 3: WHY SPATIAL STATISTICS IN THE REAL WORLD? -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>Why Spatial Statistics in the Real World?</h2>
                </header>
                <div class="slide-body">
                    <div class="lead-callout">
                        <p><strong>The Core Reality:</strong> Traditional statistics and standard ML operate under the assumption of <em>independent and identically distributed ($i.i.d.$)</em> observations. In reality, human settlements, economic commerce, disease vectors, and infrastructure <strong>do not stop at administrative borders</strong>. Decision-makers relying on state or national averages fall into three fatal traps:</p>
                    </div>

                    <div class="grid-3" style="margin-top: 6px; gap: 10px;">
                        <div class="card trap-card">
                            <div class="trap-pill">TRAP 01</div>
                            <h4 class="trap-title">1. The Fallacy of the Average</h4>
                            <div class="trap-subtitle">Masked Within-Unit Inequality</div>
                            <div class="trap-points">
                                <div class="trap-point"><strong>The Blindspot:</strong> Aggregating to LGA or State hides acute localized deprivation beneath a single deceptive average score.</div>
                                <div class="trap-point"><strong>Ground Reality:</strong> Affluent urban corridors sit directly adjacent to rural "healthcare deserts" where hundreds of thousands lack any facility.</div>
                                <div class="trap-point"><strong>Spatial Remedy:</strong> Local Anselin LISA ($I_i$) maps expose isolated micro-pockets of acute deprivation hidden inside high averages.</div>
                            </div>
                        </div>

                        <div class="card trap-card">
                            <div class="trap-pill">TRAP 02</div>
                            <h4 class="trap-title">2. The Spillover Blindspot</h4>
                            <div class="trap-subtitle">Ignoring Tobler's First Law</div>
                            <div class="trap-points">
                                <div class="trap-point"><strong>The Blindspot:</strong> Standard regression (OLS) treats every ward as an isolated, independent island ($cov(\\epsilon_i, \\epsilon_j) = 0$).</div>
                                <div class="trap-point"><strong>Ground Reality:</strong> <em>"Near things are more related than distant things"</em>. Building a regional hub creates positive economic externalities across neighbor borders.</div>
                                <div class="trap-point"><strong>Spatial Remedy:</strong> Spatial Lag (SAR) &amp; Spatial Durbin (SDM) models quantify cross-border spillover multipliers.</div>
                            </div>
                        </div>

                        <div class="card trap-card">
                            <div class="trap-pill">TRAP 03</div>
                            <h4 class="trap-title">3. Capital Misallocation Trap</h4>
                            <div class="trap-subtitle">Cluster Saturation vs. Deserts</div>
                            <div class="trap-points">
                                <div class="trap-point"><strong>The Blindspot:</strong> Deploying bank branches, retail outlets, or boreholes based solely on aggregate population tables.</div>
                                <div class="trap-point"><strong>Ground Reality:</strong> Saturates already hyper-competitive, over-served urban clusters while completely missing high-demand, underserved wards next door.</div>
                                <div class="trap-point"><strong>Spatial Remedy:</strong> Catchment distance buffers and Lorenz spatial inequality curves reveal exact unserved frontiers.</div>
                            </div>
                        </div>
                    </div>

                    <div class="strategic-takeaway-banner" style="margin-top: 8px;">
                        <div class="banner-label">STRATEGIC PARADIGM SHIFT ACROSS 9,308 WARDS</div>
                        <div class="banner-grid">
                            <div class="banner-step">
                                <span class="step-badge">1</span>
                                <div><strong>Acknowledge Spatial Dependence:</strong> Replace flawed $i.i.d.$ independence with spatial connectivity weight matrices ($W$).</div>
                            </div>
                            <div class="banner-step">
                                <span class="step-badge">2</span>
                                <div><strong>Expose Local Heterogeneity:</strong> Disaggregate national and state summaries into micro-ward administrative boundaries.</div>
                            </div>
                            <div class="banner-step">
                                <span class="step-badge">3</span>
                                <div><strong>Optimize Capital Allocation:</strong> Target public and private investments where spatial return and social equity are maximized.</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 3: THE CORE OBJECTIVE: OPERATIONAL DECISIONS ACROSS 9,308 WARDS
    # =========================================================================
    slide_3 = f"""
            <!-- SLIDE 3: THE CORE OBJECTIVE -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>The Core Objective: Operational Decisions Across 9,308 Wards</h2>
                </header>
                <div class="slide-body">
                    <div class="lead-callout">
                        <p>This curriculum bridges raw <strong>Earth Observation (EO) data</strong> (satellite-derived asset wealth, gridded population rasters) and <strong>actionable strategic investments</strong>. By analyzing all 9,308 administrative wards in Nigeria, students master answers to 5 critical questions:</p>
                    </div>

                    <div class="grid-2" style="margin-top: 10px; gap: 10px;">
                        <div class="card">
                            <h4>Healthcare Deserts</h4>
                            <p>Where are the most urgent healthcare deserts? Identifying wards with $>17,000$ residents and zero registered clinics to deploy mobile medical clinics.</p>
                        </div>

                        <div class="card">
                            <h4>Untapped Retail Catchments</h4>
                            <p>Where are prime commercial markets? Detecting wards with high relative asset wealth but low commercial retail density for expansion.</p>
                        </div>

                        <div class="card">
                            <h4>Civic &amp; Cultural Sorting</h4>
                            <p>How do religious and civic institutions sort geographically? Mapping cultural cohesion and Shannon Entropy diversity zones across communities.</p>
                        </div>

                        <div class="card">
                            <h4>Infrastructural Inequality</h4>
                            <p>How unequal is clean water infrastructure? Quantifying regional service monopolies with Lorenz inequality curves and Gini coefficients.</p>
                        </div>
                    </div>

                    <div class="card" style="margin-top: 8px;">
                        <p><strong>True Economic Multiplier:</strong> Estimating Spatial Lag (SAR) and Spatial Durbin (SDM) models to mathematically decompose public investments into <em>direct impacts</em> and <em>indirect regional spillover multipliers</em>.</p>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDE 4: THE SUPERPOWER OF SPATIAL STATISTICS (ESDA VS TRADITIONAL EDA)
    # =========================================================================
    slide_4 = f"""
            <!-- SLIDE 4: THE SUPERPOWER OF SPATIAL STATISTICS -->
            <section class="dsn-content-slide">
                <img src="{logo_b64}" class="dsn-header-logo" alt="DSN">
                <header class="slide-header">
                    <h2>The Superpower of Spatial Statistics: ESDA vs. Traditional EDA</h2>
                </header>
                <div class="slide-body">
                    <div class="diagram-strip">
                        <div><strong style="color: #0369a1;">Traditional EDA:</strong> [Values] ──────► Summary Stats (Mean, SD, Histograms) ──► <strong>BLIND to space</strong></div>
                        <div><strong style="color: #0a7a0a;">Spatial EDA:</strong> [Values + Space] ──► Moran's I + Anselin LISA Maps ──► <strong>UNLOCKS structural patterns</strong></div>
                    </div>

                    <div class="grid-2" style="margin-top: 10px; gap: 12px;">
                        <div class="card">
                            <h4 style="color: #be123c;">What Traditional EDA Misses</h4>
                            <ul>
                                <li><strong>Geographic Blindness:</strong> You can randomly shuffle 9,308 wards across Nigeria, and the mean, SD, and histogram remain 100% identical. Traditional EDA cannot detect regional poverty belts.</li>
                                <li><strong>Hidden Structural Regimes:</strong> A national correlation ($r = 0.45$) can conceal that the relationship is positive in the South, but zero or inverted in the North.</li>
                                <li><strong>Inability to Detect Local Outliers:</strong> Global outlier checks ($z > 3$) miss spatial anomalies: an affluent island surrounded by poverty, or a destitute pocket inside wealth.</li>
                            </ul>
                        </div>

                        <div class="card">
                            <h4 style="color: #0f766e;">What Spatial EDA (ESDA) Unlocks</h4>
                            <ul>
                                <li><strong>Hypothesis-Free Pattern Discovery:</strong> Statistically proves whether an observed map pattern is genuine clustering or mere random chance ($p < 0.001$).</li>
                                <li><strong>Global Moran's $I$:</strong> Quantifies national spatial autocorrelation into a single benchmark statistic.</li>
                                <li><strong>Local Anselin LISA ($I_i$):</strong> Pinpoints Hotspots ($HH$), Coldspots ($LL$), and Spatial Outliers ($HL$ &amp; $LH$).</li>
                                <li><strong>Spatial Heterogeneity:</strong> Uncovers localized structural breaks across state borders, river basins, and economic corridors.</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>
"""

    # =========================================================================
    # SLIDES 5 TO 35: REMAINING METHODOLOGICAL SEQUENCE (STRIPPED OF ALL TAGS & BORDER COLORS)
    # =========================================================================
    source_script = os.path.join(base_dir, "scripts", "build_web_presentation.py")
    with open(source_script, "r", encoding="utf-8") as f:
        src_content = f.read()

    section_pattern = re.compile(r'<section.*?>([\s\S]*?)</section>', re.MULTILINE)
    raw_sections = section_pattern.findall(src_content)

    remaining_slides = []
    # raw_sections[3] was "The Modifiable Areal Unit Problem (MAUP)" -> REMOVED per user request
    # raw_sections[4:] start with Section 4: "Spatial Fallacies: Ecological & Aspatial Fallacies"
    for i, sec in enumerate(raw_sections[4:], start=6):
        # 1. Remove all tag spans completely
        sec_clean = re.sub(r'<span class=[\'"]tag.*?[\'"]>.*?</span>\s*', '', sec)
        # 2. Remove colored card/callout classes and inline border-left
        sec_clean = re.sub(r'class=[\'"]card\s+card-[a-z]+[\'"]', 'class="card"', sec_clean)
        sec_clean = re.sub(r'class=[\'"]callout\s+[a-z]+[\'"]', 'class="callout"', sec_clean)
        sec_clean = re.sub(r'border-left:\s*[^;]+;', '', sec_clean)
        
        # 3. Inject DSN header logo
        logo_html = f'<img src="{logo_b64}" class="dsn-header-logo" alt="DSN">'
        if '<header class="slide-header">' in sec_clean:
            sec_clean = sec_clean.replace(
                '<header class="slide-header">',
                f'{logo_html}\n        <header class="slide-header">'
            )
        else:
            sec_clean = f'{logo_html}\n' + sec_clean

        slide_html = f"""
            <!-- SLIDE {i} -->
            <section class="dsn-content-slide">
{sec_clean}
            </section>
"""
        remaining_slides.append(slide_html)

    # =========================================================================
    # SLIDE 37: DSN ENDING SLIDE (THANK YOU / Q&A)
    # =========================================================================
    slide_ending = f"""
            <!-- SLIDE 37: DSN ENDING SLIDE -->
            <section class="dsn-ending-slide">
                <div class="dsn-ending-container">
                    <img src="{ending_logo_b64}" class="dsn-ending-logo" alt="DSN Logo">
                    <h1 class="dsn-ending-title">Thank you</h1>
                    <h2 class="dsn-ending-subtitle">Q&amp;A / Open Discussion</h2>
                    <div class="dsn-ending-card">
                        <h4 style="color: #ffffff; font-size: 1.05em; margin-bottom: 8px;">Advanced Spatial Statistics Masterclass</h4>
                        <p style="color: #a7f3d0; font-size: 0.78em; line-height: 1.5; margin-bottom: 12px;">
                            Exploratory Spatial Data Analysis (ESDA) • Spatial Econometrics (SAR / SEM / SDM) • Geographically Weighted Regression (GWR / MGWR)
                        </p>
                        <div class="dsn-ending-links">
                            <span>Data Science Nigeria (DSN)</span>
                            <span>•</span>
                            <span>Spatial Intelligence &amp; Data Science</span>
                            <span>•</span>
                            <span>Adedoyin S. Ajeyomi</span>
                        </div>
                    </div>
                </div>
            </section>
"""

    all_slides_combined = slide_1 + slide_agenda + slide_2 + slide_3 + slide_4 + "\n".join(remaining_slides) + slide_ending

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Spatial Statistics — DSN Course Portal &amp; Presentation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/theme/white.min.css">
    <!-- KaTeX Formulas for crisp mathematical precision -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
    <style>
        :root {{
            --text-dark: #0f172a;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --primary: #0284c7;
            --primary-dark: #0369a1;
            --dsn-green: #0a7a0a;
            --dsn-green-dark: #065406;
            --dsn-green-light: #e8f5e9;
            --border: #e2e8f0;
            --card-bg: #ffffff;
            --sidebar-width: 270px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body, html {{
            height: 100%;
            width: 100%;
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #ffffff;
            color: var(--text-dark);
            overflow: hidden;
            -webkit-font-smoothing: antialiased;
        }}

        /* ========================================================= */
        /* PORTAL WRAPPER & SIDEBAR */
        /* ========================================================= */
        .portal-layout {{
            display: flex;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            position: relative;
        }}

        .portal-sidebar {{
            width: var(--sidebar-width);
            min-width: var(--sidebar-width);
            height: 100vh;
            background: #ffffff;
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            z-index: 1000;
            transition: margin-left 0.25s ease;
            box-shadow: 2px 0 8px rgba(0, 0, 0, 0.03);
        }}

        .portal-sidebar.collapsed {{
            margin-left: calc(-1 * var(--sidebar-width));
        }}

        .sidebar-brand {{
            padding: 16px 18px;
            display: flex;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid var(--border);
            background: #ffffff;
        }}

        .brand-logo {{
            height: 38px;
            width: auto;
            max-width: 80px;
            object-fit: contain;
            display: block;
        }}

        .brand-title-wrap {{
            display: flex;
            flex-direction: column;
        }}

        .brand-name {{
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-dark);
            line-height: 1.2;
        }}

        .brand-badge {{
            font-size: 11px;
            font-weight: 600;
            color: var(--dsn-green);
        }}

        .sidebar-menu {{
            flex: 1;
            padding: 12px 10px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .menu-heading {{
            font-size: 10.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            padding: 10px 8px 4px 8px;
            margin-top: 4px;
        }}

        .nav-link-btn {{
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
            padding: 8px 12px;
            border: 1px solid transparent;
            border-radius: 8px;
            background: transparent;
            color: var(--text-secondary);
            font-family: 'Poppins', sans-serif;
            font-size: 12px;
            font-weight: 500;
            text-align: left;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.15s ease;
        }}

        .nav-link-btn:hover {{
            background: #f8fafc;
            color: var(--text-dark);
            border-color: #e2e8f0;
        }}

        .nav-link-btn.active {{
            background: var(--dsn-green-light);
            color: var(--dsn-green-dark);
            font-weight: 600;
            border-color: #c8e6c9;
        }}

        .nav-icon {{
            font-size: 15px;
            width: 18px;
            text-align: center;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .github-btn {{
            margin-top: 4px;
            color: #0f172a;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
        }}

        .github-btn:hover {{
            background: #f1f5f9;
            border-color: #cbd5e1;
        }}

        .sidebar-footer {{
            padding: 12px 16px;
            border-top: 1px solid var(--border);
            font-size: 11px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .collapse-toggle-btn {{
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 11.5px;
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 4px 8px;
            border-radius: 4px;
        }}

        .collapse-toggle-btn:hover {{
            background: #f1f5f9;
            color: var(--text-dark);
        }}

        /* ========================================================= */
        /* MAIN WORKSPACE */
        /* ========================================================= */
        .portal-main {{
            flex: 1;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background: #ffffff;
            position: relative;
        }}

        .portal-topbar {{
            height: 44px;
            min-height: 44px;
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            z-index: 50;
        }}

        .topbar-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .sidebar-btn {{
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11.5px;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .sidebar-btn:hover {{
            background: #f1f5f9;
            color: var(--text-dark);
        }}

        .view-title {{
            font-size: 13px;
            font-weight: 600;
            color: var(--text-dark);
        }}

        .topbar-right {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .fullscreen-btn {{
            background: transparent;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11.5px;
            font-family: 'Poppins', sans-serif;
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .fullscreen-btn:hover {{
            background: #f8fafc;
            color: var(--text-dark);
        }}

        .portal-viewport {{
            flex: 1;
            position: relative;
            height: calc(100vh - 44px);
            overflow: hidden;
            background: #f1f5f9;
        }}

        .slides-view {{
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            display: block;
            background: #f1f5f9;
        }}

        .tech-notes-view {{
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            display: none;
            overflow-y: auto;
            background: #ffffff;
            padding: 24px 32px;
        }}

        .doc-frame {{
            width: 100%;
            height: 100%;
            border: none;
            position: absolute;
            top: 0;
            left: 0;
            display: none;
            background: #ffffff;
        }}

        /* ========================================================= */
        /* REVEAL.JS PRESENTATION STYLES - SLIDE TEMPLATE MATCH */
        /* ========================================================= */
        .reveal {{
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f1f5f9;
            color: var(--text-dark);
            height: 100% !important;
            width: 100% !important;
        }}

        .reveal .slides {{
            text-align: left;
        }}

        .reveal .slides section {{
            top: 0 !important;
            padding: 24px 40px 48px 40px !important;
            box-sizing: border-box;
            overflow: hidden !important;
            height: 100% !important;
            border-radius: 6px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: none !important;
        }}

        /* Permanent Base64 16:9 DSN Backgrounds */
        .reveal .slides section.dsn-cover-slide {{
            background: #ffffff url('{bg_cover_b64}') no-repeat center center / 100% 100% !important;
        }}

        .reveal .slides section.dsn-agenda-slide {{
            background: #ffffff url('{bg_agenda_b64}') no-repeat center center / 100% 100% !important;
            padding: 0 !important;
            position: relative !important;
        }}

        /* Agenda Slide Elements - Matching DSN New Presentation Slides PPTX */
        .agenda-items-wrap {{
            position: absolute;
            top: 13.5%;
            left: 43.6%;
            width: 52%;
            height: 73%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .agenda-item-row {{
            display: flex;
            align-items: center;
            gap: 24px;
        }}

        .agenda-num-box {{
            width: 64px;
            height: 60px;
            background: #ff0000;
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
            font-size: 0.60em;
            font-weight: 700;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            box-shadow: 0 4px 14px rgba(255, 0, 0, 0.28);
            letter-spacing: -0.01em;
        }}

        .agenda-text-box {{
            font-family: 'Poppins', sans-serif;
            font-size: 0.58em;
            font-weight: 500;
            color: #0f172a;
            line-height: 1.25;
            letter-spacing: -0.01em;
        }}

        .agenda-row-divider {{
            width: 96%;
            height: 1px;
            background: #e2e8f0;
            margin-left: 88px;
        }}

        .reveal .slides section.dsn-content-slide {{
            background: #ffffff url('{bg_content_b64}') no-repeat center center / 100% 100% !important;
        }}

        .reveal .slides section.dsn-ending-slide {{
            background: #ffffff url('{bg_ending_b64}') no-repeat center center / 100% 100% !important;
        }}

        /* Slide Container: 540px max height -> Leaves 75px+ whitespace above DSN footer! */
        .slide-container, .slide-body {{
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 6px;
            max-height: 540px;
            overflow: hidden;
            position: relative;
        }}

        /* DSN Header Logo - Top-Right */
        .dsn-header-logo {{
            position: absolute;
            top: 18px;
            right: 32px;
            width: 80px;
            height: auto;
            z-index: 50;
            pointer-events: none;
            display: block;
        }}

        /* Clean Slide Header - NO PILL TAGS / NO COLORED BACKGROUND BANNERS */
        .slide-header {{
            margin-bottom: 7px;
            padding-bottom: 2px;
            max-width: 950px;
        }}

        .reveal h1, .reveal h2, .reveal h3, .reveal h4 {{
            font-family: 'Poppins', sans-serif;
            color: var(--text-dark);
            text-transform: none;
        }}

        .reveal h1 {{
            font-size: 1.50em;
            line-height: 1.15;
            font-weight: 700;
        }}

        /* Smart, refined Title - NO WRAPPING OVERFLOW */
        .reveal h2 {{
            font-size: 0.95em !important;
            line-height: 1.25 !important;
            font-weight: 600 !important;
            color: #0f172a !important;
            margin: 0 !important;
            padding: 0 !important;
            text-align: left !important;
            border: none !important;
        }}

        .reveal h3 {{
            font-size: 0.68em !important;
            color: var(--primary) !important;
            font-weight: 600 !important;
            margin: 2px 0 4px 0 !important;
        }}

        .reveal h4 {{
            font-size: 0.54em !important;
            color: var(--text-dark) !important;
            font-weight: 600 !important;
            margin: 0 0 3px 0 !important;
        }}

        .reveal p, .reveal li {{
            font-size: 0.36em !important;
            line-height: 1.38 !important;
            color: var(--text-secondary) !important;
        }}

        .reveal ul {{
            margin-left: 16px;
            margin-bottom: 4px;
        }}

        .reveal li {{
            margin-bottom: 3px;
        }}

        /* Clean Smart Lead Box - NO COLORED VERTICAL BARS */
        .lead-callout {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 7px 11px;
            margin-bottom: 7px;
        }}

        .lead-callout p {{
            font-size: 0.37em !important;
            line-height: 1.38 !important;
            color: #1e293b !important;
        }}

        /* Clean Smart Cards - PURE WHITE, SOFT 1PX BORDER, ZERO COLORED BARS */
        .card {{
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 7px 11px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        }}

        .card-rose, .card-blue, .card-amber, .card-teal, .card-emerald, .card-purple, .card-cyan {{
            border: 1px solid #e2e8f0 !important;
        }}

        .callout, .concept-card {{
            background: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 6px 10px !important;
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
        }}

        .grid-4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
        }}

        /* Monospace diagram comparison strip */
        .diagram-strip {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 7px 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.42em;
            color: #1e293b;
            margin-bottom: 6px;
        }}

        .formula-box {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 6px 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.44em;
            line-height: 1.4;
            color: #1e293b;
            margin: 4px 0;
        }}

        .tech-note-ref {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 0.38em;
            color: #6d28d9;
            background: #f5f3ff;
            border: 1px solid #ddd6fe;
            border-radius: 4px;
            padding: 2px 7px;
            margin-top: 4px;
            cursor: pointer;
            text-decoration: none;
            font-weight: 500;
        }}

        .tech-note-ref:hover {{
            background: #ede9fe;
            color: #5b21b6;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.40em;
            margin-top: 4px;
        }}

        th {{
            background: #f8fafc;
            color: var(--text-dark);
            font-weight: 600;
            padding: 3px 5px;
            border-bottom: 1.5px solid var(--border);
            text-align: left;
        }}

        td {{
            padding: 2px 5px;
            border-bottom: 1px solid var(--border);
            color: var(--text-secondary);
        }}

        tr:nth-child(even) td {{
            background: #f8fafc;
        }}

        /* DSN Cover Slide */
        .dsn-cover-container {{
            max-width: 660px;
            padding-left: 20px;
            padding-top: 20px;
        }}

        .dsn-cover-logo {{
            height: 48px;
            width: auto;
            object-fit: contain;
            margin-bottom: 12px;
            display: block;
        }}

        .dsn-cover-title {{
            font-size: 1.30em !important;
            font-weight: 700 !important;
            line-height: 1.18 !important;
            color: #0f172a;
            margin-bottom: 6px !important;
        }}

        .dsn-cover-subtitle {{
            font-size: 0.65em !important;
            font-weight: 600 !important;
            color: var(--dsn-green) !important;
            margin-bottom: 14px !important;
        }}

        .dsn-cover-author {{
            display: flex;
            flex-direction: column;
            gap: 2px;
            margin-top: 10px;
        }}

        .author-name {{
            font-size: 0.48em !important;
            font-weight: 600 !important;
            color: #0f172a !important;
            letter-spacing: -0.01em;
        }}

        .author-org {{
            font-size: 0.38em !important;
            font-weight: 500 !important;
            color: #64748b !important;
        }}

        /* DSN Ending Slide */
        .dsn-ending-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 640px;
            text-align: center;
            position: relative;
        }}

        .dsn-ending-logo {{
            position: absolute;
            top: 24px;
            right: 32px;
            width: 120px;
            height: auto;
            display: block;
        }}

        .dsn-ending-title {{
            font-size: 2.6em !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            margin-bottom: 6px !important;
        }}

        .dsn-ending-subtitle {{
            font-size: 1.25em !important;
            font-weight: 600 !important;
            color: #86efac !important;
            margin-bottom: 24px !important;
        }}

        .dsn-ending-card {{
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
            padding: 20px 32px;
            max-width: 720px;
        }}

        .dsn-ending-links {{
            display: flex;
            gap: 16px;
            justify-content: center;
            font-size: 0.55em;
            color: #e2e8f0;
        }}

        /* ========================================================= */
        /* REVEAL NAVIGATION CONTROLS - SEPARATED (LEFT & RIGHT)     */
        /* ========================================================= */
        .reveal .controls {{
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            width: 100% !important;
            height: 100% !important;
            pointer-events: none !important;
            z-index: 999 !important;
            display: block !important;
        }}

        .reveal .controls button {{
            pointer-events: auto !important;
            opacity: 0.65 !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            background: rgba(255, 255, 255, 0.90) !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 6px !important;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        .reveal .controls button.enabled {{
            opacity: 0.95 !important;
        }}

        .reveal .controls button:hover {{
            opacity: 1 !important;
            background: #ffffff !important;
            border-color: #0284c7 !important;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25) !important;
        }}

        /* Left-facing arrow moved to bottom-left corner */
        .reveal .controls .navigate-left {{
            position: absolute !important;
            bottom: 14px !important;
            left: 24px !important;
            top: auto !important;
            right: auto !important;
            width: 36px !important;
            height: 36px !important;
            transform: none !important;
        }}

        /* Right-facing arrow in bottom-right corner */
        .reveal .controls .navigate-right {{
            position: absolute !important;
            bottom: 14px !important;
            right: 24px !important;
            top: auto !important;
            left: auto !important;
            width: 36px !important;
            height: 36px !important;
            transform: none !important;
        }}

        /* Hide vertical controls */
        .reveal .controls .navigate-up,
        .reveal .controls .navigate-down {{
            display: none !important;
        }}

        /* Slide Number placement: bottom-right, just inside right arrow */
        .reveal .slide-number {{
            right: 68px !important;
            left: auto !important;
            bottom: 18px !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            color: #475569 !important;
            background: rgba(255, 255, 255, 0.90) !important;
            padding: 2px 7px !important;
            border-radius: 4px !important;
            border: 1px solid #e2e8f0 !important;
            z-index: 998 !important;
        }}

        /* ========================================================= */
        /* SLIDE 2 ENHANCED CREATIVE ARRANGEMENT                     */
        /* ========================================================= */
        .trap-card {{
            display: flex !important;
            flex-direction: column !important;
            gap: 4px !important;
            padding: 8px 10px !important;
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        }}

        .trap-pill {{
            align-self: flex-start;
            font-size: 0.31em !important;
            font-weight: 700 !important;
            letter-spacing: 0.06em;
            color: #475569;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 1px 6px;
            border-radius: 4px;
            margin-bottom: 1px;
        }}

        .trap-title {{
            font-size: 0.48em !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            margin: 0 !important;
            line-height: 1.22 !important;
        }}

        .trap-subtitle {{
            font-size: 0.34em !important;
            font-weight: 600 !important;
            color: #0284c7 !important;
            margin-bottom: 2px !important;
        }}

        .trap-points {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .trap-point {{
            font-size: 0.31em !important;
            line-height: 1.34 !important;
            color: #334155 !important;
            background: #f8fafc;
            padding: 4px 6px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}

        .strategic-takeaway-banner {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 7px 12px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .banner-label {{
            font-size: 0.31em !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em;
            color: #0a7a0a;
            text-transform: uppercase;
        }}

        .banner-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 12px;
        }}

        .banner-step {{
            display: flex;
            align-items: flex-start;
            gap: 6px;
            font-size: 0.31em !important;
            line-height: 1.32 !important;
            color: #1e293b !important;
        }}

        .step-badge {{
            background: #0284c7;
            color: #ffffff;
            font-size: 0.85em;
            font-weight: 700;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 1px;
        }}

        .tech-notes-view .doc-container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
    </style>
</head>
<body>
    <div class="portal-layout">
        <!-- Sidebar Navigation -->
        <aside class="portal-sidebar" id="portalSidebar">
            <div class="sidebar-brand">
                <img src="{logo_b64}" alt="DSN Logo" class="brand-logo">
                <div class="brand-title-wrap">
                    <span class="brand-name">Spatial Statistics</span>
                    <span class="brand-badge">DSN Masterclass</span>
                </div>
            </div>

            <nav class="sidebar-menu">
                <div class="menu-heading">Course Presentation</div>
                <button class="nav-link-btn active" id="btn-slides" onclick="switchPortalView('slides')">
                    <span class="nav-icon">📊</span>
                    <span>Lecture Slides</span>
                </button>
                <button class="nav-link-btn" id="btn-technical_notes" onclick="switchPortalView('technical_notes')">
                    <span class="nav-icon">📜</span>
                    <span>Technical Note</span>
                </button>

                <div class="menu-heading">Curriculum Modules</div>
                <button class="nav-link-btn" id="btn-01_esda" onclick="switchPortalView('01_esda')">
                    <span class="nav-icon">🗺️</span>
                    <span>01: ESDA &amp; Autocorrelation</span>
                </button>
                <button class="nav-link-btn" id="btn-02_modeling" onclick="switchPortalView('02_modeling')">
                    <span class="nav-icon">📐</span>
                    <span>02: Spatial Econometrics</span>
                </button>
                <button class="nav-link-btn" id="btn-03_gwr" onclick="switchPortalView('03_gwr')">
                    <span class="nav-icon">🔬</span>
                    <span>03: Spatial Heterogeneity</span>
                </button>
                <button class="nav-link-btn" id="btn-04_sectoral" onclick="switchPortalView('04_sectoral')">
                    <span class="nav-icon">🎯</span>
                    <span>04: Spatial Synthesis</span>
                </button>

                <div class="menu-heading">Repository</div>
                <a href="https://github.com/SammyGIS/dsn_advanced_spatial_stats" target="_blank" rel="noopener noreferrer" class="nav-link-btn github-btn">
                    <svg class="nav-icon" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                    </svg>
                    <span>View on GitHub</span>
                </a>
            </nav>

            <div class="sidebar-footer">
                <span>Data Science Nigeria</span>
                <button class="collapse-toggle-btn" onclick="toggleSidebar()" title="Collapse sidebar">
                    <span id="collapseLabel">◀ Hide</span>
                </button>
            </div>
        </aside>

        <!-- Main Workspace -->
        <main class="portal-main">
            <!-- Top Bar -->
            <div class="portal-topbar">
                <div class="topbar-left">
                    <button class="sidebar-btn" onclick="toggleSidebar()" aria-label="Toggle Sidebar">
                        ☰ <span>Navigation</span>
                    </button>
                    <span class="view-title" id="currentViewTitle">Lecture Slides: Theory, Intuition &amp; Spatial Statistics Modeling</span>
                </div>
                <div class="topbar-right">
                    <button class="fullscreen-btn" onclick="toggleFullscreen()" title="Fullscreen Slides (F)">
                        ⛶ <span>Fullscreen</span>
                    </button>
                </div>
            </div>

            <!-- Viewport Container -->
            <div class="portal-viewport" id="portalViewport">
                <!-- 1. Reveal.js Slides View -->
                <div class="slides-view" id="slidesView">
                    <div class="reveal" id="revealDeck">
                        <div class="slides">
{all_slides_combined}
                        </div>
                    </div>
                </div>

                <!-- 2. Document Frame for Technical Note & Notebooks -->
                <iframe id="docFrame" class="doc-frame" title="Document Viewer"></iframe>
            </div>
        </main>
    </div>

    <!-- Reveal.js Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.js"></script>
    <script>
        // Initialize Reveal.js with 16:9 widescreen dimensions and generous gaps/margins
        let deck = new Reveal(document.getElementById('revealDeck'), {{
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
        }});
        deck.initialize();

        // Portal View Navigation Dictionary
        const portalViews = {{
            'slides': {{
                type: 'slides',
                title: 'Lecture Slides: Theory, Intuition & Spatial Statistics Modeling'
            }},
            'technical_notes': {{
                type: 'frame',
                url: 'technical_notes.html',
                title: 'Technical Note: Mathematical Formulations & Statistical Mechanics'
            }},
            '01_esda': {{
                type: 'frame',
                url: 'notebooks_html/01_exploratory_spatial_data_analysis.html',
                title: 'Module 01: Exploratory Spatial Data Analysis (ESDA)'
            }},
            '02_modeling': {{
                type: 'frame',
                url: 'notebooks_html/02_spatial_statistics_modeling.html',
                title: 'Module 02: Spatial Econometrics & Statistical Modeling'
            }},
            '03_gwr': {{
                type: 'frame',
                url: 'notebooks_html/03_spatial_heterogeneity_gwr_mgwr.html',
                title: 'Module 03: Spatial Heterogeneity (GWR & MGWR)'
            }},
            '04_sectoral': {{
                type: 'frame',
                url: 'notebooks_html/04_sectoral_decision_intelligence.html',
                title: 'Module 04: Sectoral Spatial Synthesis & Prioritization'
            }}
        }};

        function switchPortalView(key) {{
            const viewConfig = portalViews[key];
            if (!viewConfig) return;

            // Update Active Nav Button
            document.querySelectorAll('.nav-link-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById('btn-' + key);
            if (activeBtn) activeBtn.classList.add('active');

            // Update Topbar Title
            document.getElementById('currentViewTitle').innerText = viewConfig.title;

            const slidesView = document.getElementById('slidesView');
            const docFrame = document.getElementById('docFrame');

            if (viewConfig.type === 'slides') {{
                docFrame.style.display = 'none';
                slidesView.style.display = 'block';
                setTimeout(() => {{ deck.layout(); }}, 50);
            }} else {{
                slidesView.style.display = 'none';
                docFrame.style.display = 'block';
                if (docFrame.src !== viewConfig.url && !docFrame.src.endsWith('/' + viewConfig.url)) {{
                    docFrame.src = viewConfig.url;
                }}
            }}

            history.replaceState(null, null, '#' + key);
        }}

        function toggleSidebar() {{
            const sidebar = document.getElementById('portalSidebar');
            sidebar.classList.toggle('collapsed');
            const isCollapsed = sidebar.classList.contains('collapsed');
            document.getElementById('collapseLabel').innerText = isCollapsed ? '▶ Show' : '◀ Hide';
            setTimeout(() => {{ deck.layout(); }}, 280);
        }}

        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen().catch(err => {{
                    console.log('Fullscreen error:', err);
                }});
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }}
            }}
            setTimeout(() => {{ deck.layout(); }}, 300);
        }}

        window.addEventListener('resize', () => {{
            deck.layout();
        }});

        function triggerMathRender() {{
            if (typeof renderMathInElement === 'function') {{
                renderMathInElement(document.getElementById('slidesView'), {{
                    delimiters: [
                        {{ left: '$$', right: '$$', display: true }},
                        {{ left: '$', right: '$', display: false }}
                    ],
                    throwOnError: false
                }});
            }}
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            const hash = window.location.hash.replace('#', '');
            if (hash && portalViews[hash]) {{
                switchPortalView(hash);
            }} else {{
                switchPortalView('slides');
            }}
            setTimeout(triggerMathRender, 200);
        }});
        deck.on('ready', () => {{ setTimeout(triggerMathRender, 100); }});
    </script>
</body>
</html>
"""
    presentation_path = os.path.join(base_dir, "docs", "presentation.html")
    index_path = os.path.join(base_dir, "docs", "index.html")

    with open(presentation_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated clean DSN Masterclass Presentation at {presentation_path}")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Synchronized clean DSN Masterclass Portal at {index_path}")

if __name__ == "__main__":
    main()
