"""
Build the DSN Themed Presentation & Unified Course Portal for Advanced Spatial Statistics.

Features:
- PPT Template Match from 'DSN New Presentation Slides .pptx':
  * Slide size: 16:9 Widescreen (1280x720 internal viewport).
  * Cover Slide (Slide 1): background figures/dsn_theme/image2.png with figures/dsn_theme/image3.png logo.
  * Content Slides (Slides 2-35): background figures/dsn_theme/image8.png with top-right DSN logo figures/dsn_theme/image7.png and bottom DSN green/red signature lines.
  * Ending Slide (Slide 36): background figures/dsn_theme/image11.png with figures/dsn_theme/image5.png white logo and 'Thank you / Q&A'.
  * Typography: Google Fonts 'Poppins' (300, 400, 500, 600, 700, 800) matching PPT master.
- Integrated Navigation Sidebar:
  * Sleek DSN Course Portal sidebar on the left.
  * Direct one-click switching between Lecture Slides, Technical Note, and Modules 01-04.
  * Collapsible sidebar toggle (☰ Navigation) and Fullscreen mode (⛶ Fullscreen).
  * Hash-based routing (#presentation, #technical_notes, #01_esda, etc.).
- Preserves all 35 pedagogical slides with complete explanations and formulas.
"""

import os
import re

def generate_dsn_portal_html():
    # Read original slides from scripts/build_web_presentation.py
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_script = os.path.join(base_dir, "scripts", "build_web_presentation.py")
    with open(source_script, "r", encoding="utf-8") as f:
        src_content = f.read()

    # Extract all section blocks
    section_pattern = re.compile(r'<section.*?>([\s\S]*?)</section>', re.MULTILINE)
    raw_sections = section_pattern.findall(src_content)
    print(f"Extracted {len(raw_sections)} raw slide sections.")

    # Format Slide 1 (Cover Slide) with DSN image2.png and image3.png
    cover_slide_html = r"""
            <!-- SLIDE 1: DSN TITLE SLIDE -->
            <section class="dsn-cover-slide" data-background-image="figures/dsn_theme/image2.png" data-background-size="cover">
                <div class="dsn-cover-container">
                    <div class="dsn-cover-header">
                        <img src="figures/dsn_theme/image3.png" alt="Data Science Nigeria" class="dsn-cover-logo">
                        <div class="tag green" style="margin-left: 4px;">DSN Masterclass Series</div>
                    </div>
                    <h1 class="dsn-cover-title">Advanced Spatial Statistics</h1>
                    <h3 class="dsn-cover-subtitle">Theory, Intuition &amp; Spatial Statistics Modeling</h3>
                    <p class="dsn-cover-desc">
                        Direct conceptual explanations of spatial autocorrelation, topology networks, Gauss-Markov violations in geographic systems, spatial econometrics (SAR / SEM / SDM), and multiscale spatial heterogeneity (GWR / MGWR).
                    </p>
                    <div class="dsn-cover-meta">
                        <div class="meta-pill"><strong>Instructor:</strong> Adedoyin S. Ajeyomi</div>
                        <div class="meta-pill"><strong>Teaching Mode:</strong> Direct Intuition &amp; Visual Frameworks</div>
                        <div class="meta-pill"><strong>Accompanying Reference:</strong> Technical Note Document</div>
                    </div>
                </div>
            </section>
"""

    # Format Slides 2-35 (Content Slides) with DSN image8.png background and top-right image7.png logo
    content_slides = []
    for i, sec in enumerate(raw_sections[1:], start=2):
        # Inject DSN logo into header
        logo_html = '<img src="figures/dsn_theme/image7.png" class="dsn-header-logo" alt="DSN Logo">'
        
        # Replace slide header to include the logo
        if '<header class="slide-header">' in sec:
            modified_sec = sec.replace(
                '<header class="slide-header">',
                f'{logo_html}\n        <header class="slide-header">'
            )
        else:
            modified_sec = f'{logo_html}\n' + sec

        slide_html = f"""
            <!-- SLIDE {i} -->
            <section class="dsn-content-slide" data-background-image="figures/dsn_theme/image8.png" data-background-size="100% 100%">
{modified_sec}
            </section>
"""
        content_slides.append(slide_html)

    # Format Slide 36 (Ending Slide) with DSN image11.png and image5.png logo
    ending_slide_html = r"""
            <!-- SLIDE 36: DSN ENDING SLIDE -->
            <section class="dsn-ending-slide" data-background-image="figures/dsn_theme/image11.png" data-background-size="cover">
                <div class="dsn-ending-container">
                    <img src="figures/dsn_theme/image5.png" class="dsn-ending-logo" alt="DSN Logo">
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

    all_slides_html = cover_slide_html + "\n".join(content_slides) + ending_slide_html

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
    <style>
        :root {{
            --text-dark: #0f172a;
            --text-secondary: #334155;
            --text-muted: #64748b;
            --primary: #0284c7;
            --primary-dark: #0369a1;
            --dsn-green: #0a7a0a;
            --dsn-green-dark: #065406;
            --dsn-green-light: #e8f5e9;
            --dsn-red: #ff0000;
            --teal: #0d9488;
            --crimson: #e11d48;
            --amber: #d97706;
            --purple: #7c3aed;
            --border: #e2e8f0;
            --card-bg: #f8fafc;
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
            background-color: #f1f5f9;
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

        /* Sidebar Styling */
        .portal-sidebar {{
            width: var(--sidebar-width);
            min-width: var(--sidebar-width);
            height: 100vh;
            background: #ffffff;
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            z-index: 1000;
            transition: transform 0.25s ease, margin-left 0.25s ease;
            box-shadow: 2px 0 8px rgba(0, 0, 0, 0.03);
        }}

        .portal-sidebar.collapsed {{
            margin-left: calc(-1 * var(--sidebar-width));
        }}

        .sidebar-brand {{
            padding: 18px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid var(--border);
            background: #ffffff;
        }}

        .brand-logo {{
            height: 38px;
            width: auto;
            object-fit: contain;
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
            font-weight: 500;
            color: var(--dsn-green);
        }}

        .sidebar-menu {{
            flex: 1;
            padding: 14px 12px;
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
            padding: 9px 12px;
            border: 1px solid transparent;
            border-radius: 8px;
            background: transparent;
            color: var(--text-secondary);
            font-family: 'Poppins', sans-serif;
            font-size: 12.5px;
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
            width: 20px;
            text-align: center;
            flex-shrink: 0;
        }}

        .download-btn {{
            margin-top: 4px;
            color: var(--primary-dark);
            border: 1px dashed #cbd5e1;
            background: #f8fafc;
        }}

        .download-btn:hover {{
            background: #f1f5f9;
            border-color: var(--primary);
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
        /* MAIN VIEWPORT */
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

        /* Top Bar */
        .portal-topbar {{
            height: 48px;
            min-height: 48px;
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
            padding: 5px 10px;
            font-size: 12px;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: background 0.15s ease;
        }}

        .sidebar-btn:hover {{
            background: #f1f5f9;
            color: var(--text-dark);
        }}

        .view-title {{
            font-size: 13.5px;
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
            padding: 5px 10px;
            font-size: 12px;
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

        /* Viewport Workspace */
        .portal-viewport {{
            flex: 1;
            position: relative;
            height: calc(100vh - 48px);
            overflow: hidden;
            background: #ffffff;
        }}

        /* Slide View Container */
        .slides-view {{
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            display: block;
        }}

        /* Document / Notebook Iframe */
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
        /* REVEAL.JS PRESENTATION STYLES (DSN THEME) */
        /* ========================================================= */
        .reveal {{
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #ffffff;
            color: var(--text-dark);
            height: 100% !important;
            width: 100% !important;
        }}

        .reveal .slides {{
            text-align: left;
        }}

        .reveal .slides section {{
            top: 0 !important;
            padding: 10px 24px 20px 24px !important;
            box-sizing: border-box;
            overflow: hidden !important;
            height: 100% !important;
        }}

        /* Slide Container */
        .slide-container {{
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 4px;
            height: 680px;
            max-height: 680px;
            overflow-y: auto;
            padding-right: 4px;
            padding-top: 6px;
            position: relative;
        }}

        .slide-container::-webkit-scrollbar {{
            width: 5px;
        }}
        .slide-container::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 4px;
        }}

        /* DSN Header Logo on Content Slides */
        .dsn-header-logo {{
            position: absolute;
            top: 14px;
            right: 28px;
            width: 82px;
            height: auto;
            z-index: 50;
            pointer-events: none;
        }}

        /* Slide Headers */
        .slide-header {{
            display: flex;
            flex-direction: column;
            gap: 2px;
            margin-bottom: 6px;
            padding-bottom: 2px;
            max-width: 900px;
        }}

        .reveal h1, .reveal h2, .reveal h3, .reveal h4 {{
            font-family: 'Poppins', sans-serif;
            color: var(--text-dark);
            text-transform: none;
            font-weight: 700;
        }}

        .reveal h1 {{
            font-size: 1.85em;
            line-height: 1.15;
            margin-bottom: 0.05em;
        }}

        .reveal h2 {{
            font-size: 0.90em;
            line-height: 1.18;
            margin-bottom: 0.05em;
            padding-bottom: 0.02em;
            text-align: left;
            font-weight: 700;
        }}

        .reveal h3 {{
            font-size: 0.78em;
            color: var(--primary);
            margin-bottom: 0.05em;
            margin-top: 0.05em;
            font-weight: 600;
        }}

        .reveal h4 {{
            font-size: 0.65em;
            margin-bottom: 2px;
            margin-top: 0;
            color: var(--text-dark);
            font-weight: 600;
        }}

        .reveal p, .reveal li {{
            font-size: 0.46em;
            line-height: 1.25;
            color: var(--text-secondary);
        }}

        .reveal ul {{
            margin-left: 14px;
            margin-bottom: 4px;
        }}

        .reveal li {{
            margin-bottom: 2px;
        }}

        /* Tags / Badges */
        .tag {{
            display: inline-block;
            font-size: 0.38em;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            width: fit-content;
        }}

        .tag.blue {{ background: #e0f2fe; color: #0369a1; }}
        .tag.teal {{ background: #ccfbf1; color: #0f766e; }}
        .tag.rose {{ background: #ffe4e6; color: #be123c; }}
        .tag.amber {{ background: #fef3c7; color: #b45309; }}
        .tag.purple {{ background: #f3e8ff; color: #6b21a8; }}
        .tag.green {{ background: #e8f5e9; color: var(--dsn-green); }}

        /* Cards & Grids */
        .card {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 8px 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
        }}

        .grid-4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
        }}

        .callout {{
            border-left: 3px solid var(--primary);
            background: #f8fafc;
            padding: 6px 10px;
            border-radius: 0 6px 6px 0;
            margin: 4px 0;
        }}

        .callout.blue {{ border-color: var(--primary); background: #f0f9ff; }}
        .callout.teal {{ border-color: var(--teal); background: #f0fdfa; }}
        .callout.rose {{ border-color: var(--crimson); background: #fff1f2; }}
        .callout.amber {{ border-color: var(--amber); background: #fffbeb; }}
        .callout.purple {{ border-color: var(--purple); background: #faf5ff; }}
        .callout.green {{ border-color: var(--dsn-green); background: #f0fdf4; }}

        .concept-card {{
            background: #f8fafc;
            border-left: 3px solid var(--teal);
            border-radius: 0 6px 6px 0;
            padding: 6px 10px;
            margin-top: 4px;
        }}

        .stat-badge {{
            display: inline-flex;
            flex-direction: column;
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 4px 8px;
            text-align: center;
        }}

        .stat-num {{
            font-size: 0.85em;
            font-weight: 700;
            color: var(--primary-dark);
            line-height: 1.1;
        }}

        .stat-lbl {{
            font-size: 0.38em;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .formula-box {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-left: 3px solid var(--primary);
            border-radius: 6px;
            padding: 6px 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.45em;
            line-height: 1.35;
            color: #1e293b;
            margin: 4px 0;
        }}

        .formula-box strong {{
            color: var(--primary-dark);
        }}

        .tech-note-ref {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 0.40em;
            color: #6d28d9;
            background: #f5f3ff;
            border: 1px solid #ddd6fe;
            border-radius: 4px;
            padding: 2px 7px;
            margin-top: 4px;
            cursor: pointer;
            text-decoration: none;
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
            background: #f1f5f9;
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

        /* ========================================================= */
        /* DSN COVER SLIDE SPECIFICS */
        /* ========================================================= */
        .dsn-cover-container {{
            max-width: 660px;
            padding-left: 20px;
            padding-top: 30px;
        }}

        .dsn-cover-header {{
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 12px;
        }}

        .dsn-cover-logo {{
            height: 52px;
            width: auto;
            object-fit: contain;
        }}

        .dsn-cover-title {{
            font-size: 1.85em !important;
            font-weight: 800 !important;
            line-height: 1.15;
            color: #0f172a;
            margin-bottom: 8px !important;
        }}

        .dsn-cover-subtitle {{
            font-size: 0.95em !important;
            font-weight: 600 !important;
            color: var(--dsn-green) !important;
            margin-bottom: 12px !important;
        }}

        .dsn-cover-desc {{
            font-size: 0.52em !important;
            line-height: 1.55;
            color: #475569;
            max-width: 600px;
            margin-bottom: 20px;
        }}

        .dsn-cover-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }}

        .meta-pill {{
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 0.44em;
            color: #334155;
        }}

        /* ========================================================= */
        /* DSN ENDING SLIDE SPECIFICS */
        /* ========================================================= */
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
        }}

        .dsn-ending-title {{
            font-size: 2.6em !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            margin-bottom: 6px !important;
            letter-spacing: -0.02em;
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
            padding: 22px 36px;
            max-width: 720px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}

        .dsn-ending-links {{
            display: flex;
            gap: 16px;
            justify-content: center;
            font-size: 0.55em;
            color: #e2e8f0;
        }}

        /* Slide Number Placement matching PPT template */
        .reveal .slide-number {{
            right: 28px !important;
            left: auto !important;
            bottom: 12px !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            color: #475569 !important;
            background: rgba(255, 255, 255, 0.85) !important;
            padding: 3px 8px !important;
            border-radius: 4px !important;
            border: 1px solid #e2e8f0 !important;
        }}
    </style>
</head>
<body>
    <div class="portal-layout">
        <!-- Sidebar Navigation -->
        <aside class="portal-sidebar" id="portalSidebar">
            <div class="sidebar-brand">
                <img src="figures/dsn_theme/image7.png" alt="DSN Logo" class="brand-logo">
                <div class="brand-title-wrap">
                    <span class="brand-name">Spatial Statistics</span>
                    <span class="brand-badge">DSN Masterclass</span>
                </div>
            </div>

            <nav class="sidebar-menu">
                <div class="menu-heading">Course Presentation</div>
                <button class="nav-link-btn active" id="btn-slides" onclick="switchPortalView('slides')">
                    <span class="nav-icon">📊</span>
                    <span>Lecture Slides (35)</span>
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

                <div class="menu-heading">Resources</div>
                <a href="spatial_statistics_masterclass_presentation.pptx" class="nav-link-btn download-btn" download>
                    <span class="nav-icon">📥</span>
                    <span>Download PPTX Deck</span>
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
{all_slides_html}
                        </div>
                    </div>
                </div>

                <!-- 2. Document Frame for Technical Note & Modules -->
                <iframe id="docFrame" class="doc-frame" title="Document Viewer"></iframe>
            </div>
        </main>
    </div>

    <!-- Reveal.js Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.js"></script>
    <script>
        // Initialize Reveal.js with 16:9 widescreen dimensions matching PPT template
        let deck = new Reveal(document.getElementById('revealDeck'), {{
            width: 1280,
            height: 720,
            margin: 0.02,
            minScale: 0.2,
            maxScale: 2.0,
            controls: true,
            progress: true,
            center: false,
            hash: false, // Internal hash managed by portal
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
                // Trigger reveal layout reflow
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
            // Reflow presentation after transition
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

        // Listen for window resize to reflow Reveal layout smoothly
        window.addEventListener('resize', () => {{
            deck.layout();
        }});

        // Handle URL hash navigation on initial page load
        window.addEventListener('DOMContentLoaded', () => {{
            const hash = window.location.hash.replace('#', '');
            if (hash && portalViews[hash]) {{
                switchPortalView(hash);
            }} else {{
                switchPortalView('slides');
            }}
        }});
    </script>
</body>
</html>
"""
    return full_html

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    presentation_path = os.path.join(base_dir, "docs", "presentation.html")
    index_path = os.path.join(base_dir, "docs", "index.html")

    html = generate_dsn_portal_html()

    # Write to docs/presentation.html
    with open(presentation_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated DSN Themed Presentation at {presentation_path}")

    # Write identical unified portal to docs/index.html
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully synchronized DSN Course Portal at {index_path}")

if __name__ == "__main__":
    main()
