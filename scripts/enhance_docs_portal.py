"""
Enhance docs portal with a unified, modern navigation banner across
docs/index.html, docs/presentation.html, and docs/notebooks_html/*.html.
"""

import os
import glob
import re

NAV_CSS = """
<style>
/* DSN Spatial Intelligence Top Navigation Bar */
#dsn-top-nav {
    position: sticky;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999999;
    background: linear-gradient(135deg, #1d3557 0%, #162436 100%);
    color: #ffffff;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 13px;
    border-bottom: 3px solid #2a9d8f;
}
#dsn-top-nav .nav-container {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 24px;
}
#dsn-top-nav .nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: 0.3px;
    color: #ffffff;
    text-decoration: none;
}
#dsn-top-nav .nav-brand-badge {
    background: #2a9d8f;
    color: #ffffff;
    font-size: 10px;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
#dsn-top-nav .nav-links {
    display: flex;
    align-items: center;
    gap: 8px;
    list-style: none;
    margin: 0;
    padding: 0;
}
#dsn-top-nav .nav-links a {
    color: #e2e8f0;
    text-decoration: none;
    padding: 6px 12px;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
}
#dsn-top-nav .nav-links a:hover {
    background: rgba(42, 157, 143, 0.25);
    color: #ffffff;
}
#dsn-top-nav .nav-links a.active {
    background: #2a9d8f;
    color: #ffffff;
    font-weight: 600;
}
#dsn-top-nav .nav-btn-pptx {
    background: #e76f51 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}
#dsn-top-nav .nav-btn-pptx:hover {
    background: #d95a3a !important;
}
@media (max-width: 992px) {
    #dsn-top-nav .nav-container { flex-direction: column; gap: 8px; }
    #dsn-top-nav .nav-links { flex-wrap: wrap; justify-content: center; }
}
</style>
"""

def make_nav_html(active_item, depth=0):
    prefix = "../" if depth == 1 else ""
    
    items = [
        ("handbook", f"{prefix}index.html", "📖 Master Decision Handbook"),
        ("slides", f"{prefix}presentation.html", "📊 Presentation Slides"),
        ("01_esda", f"{prefix}notebooks_html/01_exploratory_spatial_data_analysis.html", "🗺️ 01: ESDA"),
        ("02_modeling", f"{prefix}notebooks_html/02_spatial_statistics_modeling.html", "📐 02: Modeling"),
        ("03_sectoral", f"{prefix}notebooks_html/03_sectoral_decision_intelligence.html", "🎯 03: Decision Engines"),
        ("pptx", f"{prefix}spatial_statistics_masterclass_presentation.pptx", "📥 Download PPTX")
    ]
    
    links_html = []
    for key, url, label in items:
        active_cls = " active" if key == active_item else ""
        btn_cls = " nav-btn-pptx" if key == "pptx" else ""
        download_attr = ' download="spatial_statistics_masterclass_presentation.pptx"' if key == "pptx" else ''
        links_html.append(f'<li><a href="{url}" class="{active_cls.strip()}{btn_cls}"{download_attr}>{label}</a></li>')
        
    nav_bar = f"""
{NAV_CSS}
<nav id="dsn-top-nav">
    <div class="nav-container">
        <a href="{prefix}index.html" class="nav-brand">
            <span class="nav-brand-badge">DSN AI/GIS</span>
            Spatial Decision Intelligence Suite
        </a>
        <ul class="nav-links">
            {''.join(links_html)}
        </ul>
    </div>
</nav>
"""
    return nav_bar

def inject_nav(filepath, active_item, depth=0, title=None):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Remove existing injected nav if any
    content = re.sub(r'<!-- DSN_NAV_START -->.*?<!-- DSN_NAV_END -->', '', content, flags=re.DOTALL)
    
    nav_markup = f"<!-- DSN_NAV_START -->\n{make_nav_html(active_item, depth)}\n<!-- DSN_NAV_END -->"
    
    # Update title if provided
    if title:
        content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content, count=1)
        
    # Inject right after <body ...>
    body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
    if body_match:
        pos = body_match.end()
        new_content = content[:pos] + "\n" + nav_markup + content[pos:]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Injected nav into {filepath}")
    else:
        print(f"Could not find <body> tag in {filepath}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(base_dir, "docs")
    
    # 1. Master Handbook (docs/index.html)
    index_path = os.path.join(docs_dir, "index.html")
    inject_nav(index_path, active_item="handbook", depth=0, title="Master Spatial Decision Intelligence Handbook | DSN")
    
    # 2. Presentation (docs/presentation.html)
    pres_path = os.path.join(docs_dir, "presentation.html")
    inject_nav(pres_path, active_item="slides", depth=0, title="Spatial Statistics Presentation Slides | DSN")
    
    # 3. Individual Notebooks in docs/notebooks_html/
    nb_dir = os.path.join(docs_dir, "notebooks_html")
    inject_nav(os.path.join(nb_dir, "00_master_spatial_decision_handbook.html"), "handbook", depth=1, title="Master Spatial Decision Intelligence Handbook")
    inject_nav(os.path.join(nb_dir, "01_exploratory_spatial_data_analysis.html"), "01_esda", depth=1, title="01: Exploratory Spatial Data Analysis | DSN")
    inject_nav(os.path.join(nb_dir, "02_spatial_statistics_modeling.html"), "02_modeling", depth=1, title="02: Spatial Statistics & Econometric Modeling | DSN")
    inject_nav(os.path.join(nb_dir, "03_sectoral_decision_intelligence.html"), "03_sectoral", depth=1, title="03: Sectoral Decision Intelligence Engines | DSN")

if __name__ == "__main__":
    main()
