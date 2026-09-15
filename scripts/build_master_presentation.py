import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

os.makedirs("docs", exist_ok=True)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

NAVY    = RGBColor(0x1D, 0x35, 0x57)
TEAL    = RGBColor(0x2A, 0x9D, 0x8F)
CORAL   = RGBColor(0xE7, 0x6F, 0x51)
CRIMSON = RGBColor(0xD9, 0x04, 0x29)
DARK_TEXT = RGBColor(0x21, 0x25, 0x29)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_BG = RGBColor(0xF4, 0xF7, 0xFA)

def add_header(slide, title, category="SPATIAL STATISTICS"):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                 Inches(0), Inches(0), Inches(13.333), Inches(1.1))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    acc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                 Inches(0), Inches(1.1), Inches(13.333), Inches(0.05))
    acc.fill.solid(); acc.fill.fore_color.rgb = TEAL; acc.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.9))
    tf = tb.text_frame; tf.word_wrap = True
    p1 = tf.paragraphs[0]; p1.text = category.upper()
    p1.font.size = Pt(11); p1.font.bold = True; p1.font.color.rgb = TEAL
    p2 = tf.add_paragraph(); p2.text = title
    p2.font.size = Pt(20); p2.font.bold = True; p2.font.color.rgb = WHITE


def add_box(slide, left, top, width, height, title, lines, accent=None):
    if accent is None:
        accent = NAVY
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                  Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid(); card.fill.fore_color.rgb = LIGHT_BG
    card.line.color.rgb = accent; card.line.width = Pt(1.5)
    tb = slide.shapes.add_textbox(Inches(left+0.18), Inches(top+0.18),
                                  Inches(width-0.36), Inches(height-0.36))
    tf = tb.text_frame; tf.word_wrap = True
    ph = tf.paragraphs[0]; ph.text = title
    ph.font.size = Pt(13); ph.font.bold = True; ph.font.color.rgb = accent
    for line in lines:
        pl = tf.add_paragraph(); pl.text = line
        pl.font.size = Pt(10.5); pl.font.color.rgb = DARK_TEXT; pl.space_before = Pt(5)


def add_img(slide, path, left, top, width, height):
    if os.path.exists(path):
        slide.shapes.add_picture(path, Inches(left), Inches(top),
                                 Inches(width), Inches(height))


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 1 — TITLE
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
tb = s.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(5.0))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "ADVANCED SPATIAL STATISTICS & DECISION SCIENCE"
p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = WHITE
p2 = tf.add_paragraph()
p2.text = "How Location Data and Spatial Models Drive Smarter Decisions Across Every Sector"
p2.font.size = Pt(18); p2.font.color.rgb = TEAL; p2.space_before = Pt(14)
p3 = tf.add_paragraph()
p3.text = (
    "Disease Epidemiology | Health Deserts | Geomarketing | Cultural Geography "
    "| WASH | Electoral Logistics | Econometrics\n"
    "9,308 Nigerian Wards  |  PySAL | GeoPandas | spreg | esda | splot"
)
p3.font.size = Pt(13); p3.font.color.rgb = RGBColor(0xCD, 0xD3, 0xD8); p3.space_before = Pt(20)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 2 — TOBLER / WHY WHERE MATTERS
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "The Big Idea: Why Traditional Statistics Fails in the Real World", "CORE FOUNDATIONS")
add_box(s, 0.8, 1.3, 5.7, 5.7, "The Fallacy of the Average", [
    "Traditional analytics uses state or national averages.",
    "A state can look healthy on paper while having hundreds",
    "  of wards with ZERO clinics.",
    "Decisions based on averages waste money.",
    "Location dictates who has access and who is left behind.",
], CRIMSON)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Tobler's First Law of Geography (1970)", [
    "'Near things are more related than distant things.'",
    "",
    "Events in one ward do not stay in that ward.",
    "  Malaria mosquitoes fly across borders.",
    "  Shoppers travel to neighbouring markets.",
    "  Invest in Ward A -> Wards B, C, D also benefit.",
    "",
    "This cross-ward effect is called a SPATIAL SPILLOVER.",
], TEAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 2B — SPATIAL STATS vs TRADITIONAL STATS
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Spatial Statistics vs. Traditional Statistics — Head-to-Head", "CORE COMPARISON")
add_box(s, 0.8, 1.3, 5.7, 5.7, "Traditional Statistics — What It Misses", [
    "Assumes obs. are Independent & Identically Distributed (i.i.d.).",
    "Correlation: Pearson/Spearman — treats each ward as an isolated island.",
    "Regression (OLS): y = XB + e — assumes Cov(ei,ej) = 0.",
    "Outlier: Global z-score only (> 3 std devs from national mean).",
    "Multiplier: 1.0x — investment impacts only the targeted area.",
    "BLIND to: clustering, spillovers, and boundary effects.",
], CRIMSON)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Advanced Spatial Statistics — What It Adds", [
    "Foundation: Tobler's Law — neighbouring units are coupled.",
    "Correlation: Moran's I accounts for geographic distance & contiguity.",
    "Regression: Spatial Lag (SAR) and Spatial Error (SEM) models.",
    "Outlier: Anselin LISA — finds local High-Low and Low-High pockets.",
    "Multiplier: 2.4x — explicitly measures cross-ward investment returns.",
    "UNLOCKS: unbiased estimates, real significance, surgical targeting.",
], TEAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 2C — SPATIAL STATISTICS vs SPATIAL DATA SCIENCE
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Spatial Statistics vs. Spatial Data Science — They Are NOT the Same", "CLARIFICATION")
add_box(s, 0.8, 1.3, 5.7, 5.7, "Spatial Statistics (Mathematics + Inference)", [
    "A branch of MATHEMATICS and INFERENTIAL STATISTICS.",
    "The question it answers: Is this pattern REAL or due to chance?",
    "Core tools: Moran's I, LISA, SAR, SEM, Lagrange Multiplier tests.",
    "Output: p-values, confidence intervals, causal multipliers.",
    "Use when: You need to TEST a hypothesis and PROVE a result.",
    "Example: Prove malaria clusters in riverine wards (I=0.886, p<0.001).",
], NAVY)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Spatial Data Science (Engineering + Analytics)", [
    "A broader ENGINEERING and ANALYTICS field.",
    "The question it answers: How do we store, process, visualise, predict?",
    "Core tools: GeoPandas, PostGIS, QGIS, Kepler.gl, Folium, Deck.gl.",
    "Output: Maps, dashboards, ML predictions, ETL pipelines.",
    "Use when: You need to PROCESS and DISPLAY spatial info at scale.",
    "Example: Build an interactive ward-level map for 9,308 wards.",
    "",
    "-> Spatial statistics POWERS spatial data science from the inside.",
], TEAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 2D — 4 STRATEGIC ADVANTAGES
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "The 4 Strategic Advantages of Spatial Statistics", "CORE ADVANTAGES")
add_box(s, 0.8, 1.3, 2.75, 5.7, "1. Bias Elimination", [
    "Prevents Omitted Variable Bias.",
    "Spatial spillovers hide in OLS",
    "error terms — distorting B.",
    "Spatial models isolate genuine",
    "policy effects from geography.",
], NAVY)
add_box(s, 3.8, 1.3, 2.75, 5.7, "2. True Significance", [
    "Stops Type-I Errors.",
    "Non-spatial models produce",
    "deflated standard errors and",
    "inflated t-statistics.",
    "Spatial models prove whether",
    "an effect is real.",
], TEAL)
add_box(s, 6.8, 1.3, 2.75, 5.7, "3. Surgical Targeting", [
    "Bypasses crude quotas.",
    "LISA isolates the exact",
    "1,800+ desert wards instead",
    "of splitting budgets equally",
    "across 774 LGAs.",
    "Zero wasted capital.",
], CORAL)
add_box(s, 9.8, 1.3, 2.75, 5.7, "4. Quantified Spillovers", [
    "Unlocks the 2.4x Multiplier.",
    "$1M in Ward A creates",
    "$1.4M of indirect activity",
    "in contiguous wards.",
    "Justifies regional joint",
    "funding between LGAs.",
], CRIMSON)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 3 — SPATIAL STATS BEFORE ML
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Why Spatial Statistics Must Come BEFORE Machine Learning", "METHODOLOGY")
add_box(s, 0.8, 1.3, 5.7, 5.7, "The Trap: Spatial Data Leakage in ML", [
    "XGBoost/Random Forest with random train/test splits on spatial data CHEATS.",
    "Test points neighbour training points -> 95% accuracy in tests,",
    "  total failure when deployed in a new region.",
    "Tree models cannot model continuous distance decay.",
    "Off-the-shelf ML cannot give causal policy multipliers.",
], CRIMSON)
add_box(s, 6.8, 1.3, 5.7, 5.7, "The Solution: Spatial Stats First", [
    "1. Feature Engineering: Compute spatial lags [Wy] before training ML.",
    "2. Block Cross-Validation: Split by geographic clusters to prevent leakage.",
    "3. LM Tests: Confirm whether spatial dependence exists first.",
    "4. SAR/SEM: Give causal multipliers that ML cannot produce.",
    "",
    "Spatial statistics is the FOUNDATION that makes ML valid and honest.",
], TEAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 4 — PIPELINE FLOWCHART
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "The End-to-End Decision Pipeline: From Raw Data to Actions", "PIPELINE ARCHITECTURE")
add_img(s, "docs/figures/00_architecture_and_methodology_flowchart.png", 0.8, 1.3, 11.7, 5.7)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 5 — PYTHON LIBRARIES
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "The Full Python Toolkit for Spatial Statistics", "LIBRARIES REFERENCE")
add_box(s, 0.8, 1.3, 3.8, 5.7, "Core Spatial Statistics — PySAL Family", [
    "libpysal — Build spatial weights W (Queen, Rook, KNN, distance bands).",
    "esda     — Global Moran's I, LISA, Join-Count, Geary's C.",
    "spreg    — OLS, SAR (GM_Lag), SEM (GM_Error), LM diagnostic tests.",
    "giddy    — Spatial Markov chains; regional convergence analysis.",
    "splot    — Moran scatter plots & LISA cluster maps.",
    "segregation — Spatial segregation indices for cities.",
    "mgwr     — Multi-scale Geographically Weighted Regression.",
    "inequality  — Theil & spatial inequality decomposition.",
], NAVY)
add_box(s, 4.8, 1.3, 3.8, 5.7, "Geometry, I/O & Visualisation", [
    "GeoPandas  — Shapefiles, GeoJSON, Parquet I/O; spatial joins.",
    "Shapely    — Geometry ops: buffer, intersect, union, centroid.",
    "Fiona      — Low-level vector I/O (used inside GeoPandas).",
    "PyProj     — CRS transformations between EPSG projections.",
    "Folium     — Interactive Leaflet maps in Jupyter notebooks.",
    "Kepler.gl  — GPU-accelerated large-scale maps in browser.",
    "Contextily — Automatic basemap tiles (OpenStreetMap, CARTO).",
    "mapclassify — Natural Breaks, Quantile, Fisher class schemes.",
], TEAL)
add_box(s, 8.8, 1.3, 3.7, 5.7, "Raster, ETL & Network Analysis", [
    "Rasterio     — Read/write GeoTIFF rasters; window reads.",
    "rasterstats  — Fast zonal_stats for ward-level raster aggregation.",
    "xarray       — N-dimensional labelled raster arrays.",
    "rioxarray    — CRS-aware xarray extension for rasters.",
    "spatialpandas — Dask-scalable spatial partitioning.",
    "OSMnx        — Download & analyse OpenStreetMap road networks.",
    "NetworkX     — Graph algorithms for transport connectivity.",
    "scikit-mobility — Human mobility and flow modelling.",
], CORAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 6 — FORMULA 1: WEIGHTS MATRIX
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Formula 1: The Spatial Weights Matrix (W)", "MATHEMATICAL TOOLS")
add_box(s, 0.8, 1.3, 5.7, 5.7, "How We Connect Geography Mathematically", [
    "Adjacency:  wij = 1  if Ward i and Ward j share a boundary",
    "            wij = 0  otherwise",
    "",
    "Row-Standardisation:  w*ij = wij / sum_k(wik)",
    "",
    "This makes each row sum to 1.0.",
    "A ward with 10 neighbours is on the same scale as one with 3.",
    "Result: a weighted local average — the SPATIAL LAG.",
], DARK_TEXT)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Types of Adjacency in Practice", [
    "Queen Contiguity (Default):",
    "  Neighbours share an edge OR a corner point.",
    "Rook Contiguity:",
    "  Neighbours must share a full linear boundary edge.",
    "K-Nearest Neighbours (KNN-5):",
    "  Connects each ward to its 5 closest centroids.",
    "  Ensures every isolated island still has valid neighbours.",
    "Distance-Decay:  wij = d^(-alpha)  (weight drops with distance).",
], TEAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 7 — FORMULA 2: SPATIAL LAG
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Formula 2: The Spatial Lag Operator [Wy]", "MATHEMATICAL TOOLS")
add_box(s, 0.8, 1.3, 5.7, 5.7, "The Formula & Definition", [
    "[Wy]_i = sum_j ( w*_ij * y_j )",
    "",
    "Plain words: [Wy]_i = the AVERAGE VALUE of y in the neighbourhood around Ward i.",
    "",
    "If y = clinics per 10,000 people:",
    "  [Wy]_i tells you if SURROUNDING wards have clinics.",
    "If y = household wealth:",
    "  [Wy]_i tells you if the broader trade area has purchasing power.",
], NAVY)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Real-World Examples", [
    "Health Desert Diagnosis:",
    "  Ward i: 0 clinics, [W*Clinics]=6.0 -> Patients can walk to a neighbour.",
    "  Ward i: 0 clinics, [W*Clinics]=0.0 -> Severe isolated desert. Emergency.",
    "",
    "Retail Trade Catchment:",
    "  [W*Wealth]_i is high -> the entire surrounding area is affluent.",
    "  A supermarket here draws from a wealthy catchment even if the ward",
    "  itself has mixed incomes.",
], TEAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 8 — FORMULA 3: GLOBAL MORAN'S I
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Formula 3: Global Moran's I — Is There Clustering?", "MATHEMATICAL TOOLS")
add_box(s, 0.8, 1.3, 5.7, 5.7, "The Mathematical Formula", [
    "I = (n/S0) * [sum_i sum_j wij(yi-ybar)(yj-ybar)] / sum_i(yi-ybar)^2",
    "",
    "H0 (Null): Values are scattered randomly across the country.",
    "E[I] if random = -1/(n-1)  approx 0",
    "",
    "Interpretation:",
    "  I > 0 and p < 0.05 -> Clustering (High near High, Low near Low).",
    "  I < 0 and p < 0.05 -> Dispersion (checkerboard pattern).",
    "  p >= 0.05          -> Pure random noise.",
], DARK_TEXT)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Results Across 9,308 Nigerian Wards", [
    "Wealth Index (RWI):",
    "  I = 0.684, z = 112.4, p = 0.001 -> Extreme wealth clustering.",
    "Malaria Prevalence (PfPR):",
    "  I = 0.886, z = 140.5, p = 0.001 -> Intense transmission corridors.",
    "Religious Institutions (Churches):",
    "  I = 0.812, z = 138.2, p = 0.001 -> Sharp North-South cultural divide.",
    "",
    "CONCLUSION: Random models are completely wrong for Nigeria.",
], CORAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 9 — FORMULA 4: LISA
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Formula 4: Local Moran's I (LISA) — WHERE Is the Cluster?", "MATHEMATICAL TOOLS")
add_box(s, 0.8, 1.3, 5.7, 5.7, "The Local Formula", [
    "Global Moran tells us clustering EXISTS.",
    "LISA tells us WHERE — per ward.",
    "",
    "I_i = (z_i / s^2) * sum_j ( w_ij * z_j )",
    "where z_i = y_i - y_bar  (deviation from national mean).",
    "",
    "Each ward gets its own score and its own p-value.",
    "Wards are classified into 4 quadrants.",
], NAVY)
add_box(s, 6.8, 1.3, 5.7, 5.7, "The 4 LISA Quadrants", [
    "High-High (HH) — Red HOTSPOT:",
    "  High value surrounded by high neighbours.",
    "  Action: Deepen the advantage; build on existing momentum.",
    "Low-Low (LL) — Blue COLDSPOT:",
    "  Low value surrounded by low neighbours. Hardest-to-reach.",
    "  Action: Emergency intervention; prioritise in WPI Tier 1.",
    "High-Low (HL) — Orange ISLAND:",
    "  High value surrounded by low neighbours ('Island of Wealth').",
    "Low-High (LH) — Light Blue POCKET:",
    "  Low value surrounded by high neighbours ('Pocket of Poverty').",
], CRIMSON)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 10 — LISA MAP
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "National Wealth Clusters: Anselin LISA Map", "EMPIRICAL FINDINGS")
add_img(s, "docs/figures/05_moran_and_lisa_clusters.png", 0.8, 1.3, 11.7, 5.7)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 11 — SECTOR 1: HEALTHCARE DESERTS
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Sector 1: Public Health & Healthcare Deserts", "SECTOR ANALYSIS")
add_box(s, 0.8, 1.3, 4.5, 5.7, "Question, Method & Answer", [
    "THE QUESTION:",
    "  Where are populations trapped with zero primary healthcare?",
    "SPATIAL METHOD:",
    "  Spatial Join (population raster x facility points)",
    "  + Anselin LISA to classify wards into HH / LL clusters.",
    "WHAT THE METHOD DOES:",
    "  Cross-references 35,000+ health facilities against 9,308 ward",
    "  populations. Flags every ward where clinics_per_10k = 0",
    "  AND population > 17,000 people.",
    "THE ANSWER:",
    "  1,800+ Healthcare Desert wards found.",
    "  Over 30 million Nigerians live in these wards.",
], CRIMSON)
add_img(s, "docs/figures/01_national_wealth_and_health_deserts.png", 5.5, 1.3, 7.0, 5.7)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 12 — SECTOR 2: MALARIA
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Sector 2: Disease Epidemiology & Malaria Surveillance", "SECTOR ANALYSIS")
add_box(s, 0.8, 1.3, 4.5, 5.7, "Question, Method & Answer", [
    "THE QUESTION:",
    "  Does malaria cluster in environmental corridors?",
    "  Do local clinics protect against transmission?",
    "SPATIAL METHOD:",
    "  Global Moran's I + LISA hotspot mapping",
    "  + SAR regression with clinic_rate as a regressor.",
    "WHAT THE METHOD DOES:",
    "  Tests whether malaria in a ward correlates with malaria in",
    "  its neighbours. SAR quantifies how strongly the spatial",
    "  neighbourhood — not just local conditions — drives transmission.",
    "THE ANSWER:",
    "  I = 0.886, p = 0.001. Riverine wards: PfPR > 40%.",
    "  Higher clinic rates show significantly lower parasite rates.",
], NAVY)
add_img(s, "docs/figures/07_disease_epidemiology_malaria_map.png", 5.5, 1.3, 7.0, 5.7)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 13 — SECTOR 3: GEOMARKETING
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Sector 3: Geomarketing & Retail Expansion Strategy", "SECTOR ANALYSIS")
add_box(s, 0.8, 1.3, 4.5, 5.7, "Question, Method & Answer", [
    "THE QUESTION:",
    "  Where can supermarkets, retail chains, and fintechs expand",
    "  without facing crowded competition?",
    "SPATIAL METHOD:",
    "  Bivariate Moran's I (Wealth vs Market Density)",
    "  + LISA quadrant classification.",
    "WHAT THE METHOD DOES:",
    "  Compares each ward's RWI (wealth) with its neighbours' market",
    "  density. LH quadrant = affluent ward with low-market surrounding",
    "  -> PRIME EXPANSION TARGET (Tier 2).",
    "THE ANSWER:",
    "  Tier 2 wards: high consumer purchasing power, no formal retail.",
], CORAL)
add_img(s, "docs/figures/02_commercial_retail_strategy.png", 5.5, 1.3, 7.0, 5.7)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 14 — SECTOR 4: CULTURAL GEOGRAPHY
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Sector 4: Cultural Geography & Community Cohesion", "SECTOR ANALYSIS")
add_box(s, 0.8, 1.3, 4.5, 5.7, "Question, Method & Answer", [
    "THE QUESTION:",
    "  How are faith institutions distributed? Where are the cultural",
    "  transition zones of high co-presence?",
    "SPATIAL METHOD:",
    "  Global Moran's I per faith type",
    "  + Shannon Entropy Index (ward-level diversity score).",
    "WHAT THE METHOD DOES:",
    "  Moran's I proves churches and mosques sort spatially.",
    "  Shannon Entropy scores each ward: H=1.0 (equal mix) to H=0 (one faith).",
    "THE ANSWER:",
    "  Sharp North-South divide (I = 0.812).",
    "  Middle Belt = high-entropy zones needing inter-faith programs.",
], TEAL)
add_img(s, "docs/figures/03_religious_cultural_geography.png", 5.5, 1.3, 7.0, 5.7)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 15 — SECTOR 5: WASH
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Sector 5: WASH & Clean Water Infrastructure Equity", "SECTOR ANALYSIS")
add_box(s, 0.8, 1.3, 4.5, 5.7, "Question, Method & Answer", [
    "THE QUESTION:",
    "  How unequal is clean water distribution?",
    "  Which wards urgently need solar boreholes?",
    "SPATIAL METHOD:",
    "  Spatial Lorenz Curve + Gini Coefficient",
    "  + Ward Priority Index (WPI) composite scoring.",
    "WHAT THE METHOD DOES:",
    "  The Lorenz Curve ranks all 9,308 wards by borehole count.",
    "  WPI = weighted sum of (water deficit + health deficit + poverty).",
    "  Creates 4 Action Tiers so water boards drill highest-need first.",
    "THE ANSWER:",
    "  Gini = 0.72. WPI Tier 1 = emergency solar borehole intervention.",
], NAVY)
add_img(s, "docs/figures/06_infrastructure_inequality_and_ward_priority_tiers.png", 5.5, 1.3, 7.0, 5.7)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 16 — OLS FAILURE
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Spatial Econometrics: Why OLS Fails on Geographic Data", "ECONOMETRIC THEORY")
add_box(s, 0.8, 1.3, 5.7, 5.7, "The Classical OLS Regression", [
    "Standard Equation:  y = XB + e",
    "OLS assumes:  Cov(ei, ej) = 0  for i != j",
    "",
    "When geographic units are used, this breaks down.",
    "Poor wards border poor wards; wealthy wards border wealthy wards.",
    "The error term e absorbs spatial spillovers -> B is BIASED.",
    "",
    "Moran's I on OLS residuals = 0.421 (p < 0.001)",
    "-> Proof OLS violates its own assumptions on Nigerian ward data.",
], CRIMSON)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Real-Life Consequences & The Fix", [
    "If Spatial Lag is omitted:",
    "  B estimates are BIASED — policy inferences are wrong.",
    "If Spatial Error is present:",
    "  Standard errors shrink -> false positives multiply.",
    "  You believe a policy works when it actually does not.",
    "",
    "The Fix — Run Anselin's LM Diagnostic Tests:",
    "  LM-Lag > LM-Error -> use SAR (spreg.GM_Lag)",
    "  LM-Error > LM-Lag -> use SEM (spreg.GM_Error)",
], NAVY)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 17 — SAR MODEL
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "The Spatial Lag Model (SAR) & The 2.4x Investment Multiplier", "ECONOMETRIC THEORY")
add_box(s, 0.8, 1.3, 5.7, 5.7, "The SAR Equation", [
    "y = rho * Wy + XB + e",
    "",
    "rho = spatial autoregressive coefficient (how contagious the outcome is).",
    "Wy  = spatial lag (average outcome in neighbouring wards).",
    "",
    "Reduced Form:",
    "  y = (I - rho*W)^(-1) * XB + (I - rho*W)^(-1) * e",
    "",
    "The matrix (I - rho*W)^(-1) is the SPATIAL MULTIPLIER.",
    "It captures ALL rounds of cross-boundary feedback.",
], NAVY)
add_box(s, 6.8, 1.3, 5.7, 5.7, "The 2.4x Result on 9,308 Wards", [
    "Empirical regression found:",
    "  rho = 0.5842  (p < 0.0001)",
    "",
    "Spatial Multiplier:  1 / (1 - 0.5842) = 2.405x",
    "",
    "Plain words:",
    "For every 1.0 unit of wealth created in a focal ward",
    "(opening a market, clinic, or school), an additional 1.405 units",
    "SPILL OVER into surrounding wards automatically.",
    "",
    "This justifies JOINT regional funding between neighbouring LGAs.",
], CORAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 18 — SEM MODEL
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "The Spatial Error Model (SEM): Shared Geography, Not Spillovers", "ECONOMETRIC THEORY")
add_box(s, 0.8, 1.3, 5.7, 5.7, "The SEM Equation", [
    "y = XB + u",
    "u = lambda * Wu + e",
    "",
    "lambda = spatial error coefficient.",
    "e      = classical independent white noise.",
    "",
    "SEM says: the SAME hidden geographic factors hit neighbouring wards",
    "simultaneously — rainfall, soil type, colonial infrastructure legacy.",
    "This is NOT a behavioural spillover. It is shared environment.",
], NAVY)
add_box(s, 6.8, 1.3, 5.7, 5.7, "When to Use SEM vs SAR", [
    "Use SEM when dependence is UNOBSERVED GEOGRAPHY:",
    "  Regional climate and rainfall patterns.",
    "  Soil fertility and topography.",
    "  Historical state-level investment policies.",
    "",
    "Use SAR when dependence is BEHAVIOURAL SPILLOVER:",
    "  Markets, trade, and consumer travel.",
    "  Disease cross-border transmission.",
    "  Investment generating secondary economic activity.",
    "",
    "Nigeria: lambda = 0.6124 (p < 0.0001). AIC improves 3,740 pts.",
], TEAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 19 — MODEL COMPARISON TABLE
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Comparing OLS vs. SAR vs. SEM Across 9,308 Wards", "EMPIRICAL RESULTS")
add_box(s, 0.8, 1.3, 11.7, 5.7, "Model Performance Summary", [
    "MODEL 1 — Classical OLS:  y = XB + e",
    "  Pseudo R2 = 0.2841 | Log-Likelihood = -5,812.4 | AIC = 11,636.8",
    "  Moran's I on Residuals = 0.421 (p < 0.001) -> Severe autocorrelation.",
    "",
    "MODEL 2 — Spatial Lag Model (SAR):  y = rho*Wy + XB + e",
    "  Pseudo R2 = 0.5318 | Log-Likelihood = -3,941.2 | AIC = 7,896.4",
    "  rho = 0.5842 (p < 0.0001). AIC drops 3,740 points vs OLS.",
    "",
    "MODEL 3 — Spatial Error Model (SEM):  y = XB + lambda*Wu + e",
    "  Pseudo R2 = 0.5462 | Log-Likelihood = -3,884.6 | AIC = 7,781.2",
    "  lambda = 0.6124 (p < 0.0001). Best fit for structural geographic shocks.",
    "",
    "KEY TAKEAWAY: Spatial models explain TWICE the variance of classical OLS.",
], NAVY)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 20 — USE CASES PART 1
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "15 Enterprise Use Cases — Part 1: Health & Commercial (UC 1-8)", "TAXONOMY")
add_box(s, 0.8, 1.3, 5.7, 5.7, "Public Health & Human Capital (UC 1-4)", [
    "UC1 — Disease Surveillance",
    "  Method: Moran's I + LISA.",
    "  Example: Flag 312 high-malaria wards in Niger Delta for bed-net campaigns.",
    "UC2 — Healthcare Facility Siting",
    "  Method: Spatial Join + LISA LL coldspot classification.",
    "  Example: LISA flags 1,800 wards with 0 clinics and 17k+ people.",
    "UC3 — WASH Borehole Targeting",
    "  Method: Lorenz Curve + Ward Priority Index (WPI).",
    "  Example: Tier 1 wards receive solar boreholes based on WPI composite score.",
    "UC4 — School Dropout Risk Mapping",
    "  Method: SAR regression (school proximity x poverty spatial lag).",
    "  Example: Ward-level dropout risk score used by UBEC for planning.",
], NAVY)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Commercial Retail & Fintech (UC 5-8)", [
    "UC5 — Supermarket Siting",
    "  Method: Bivariate LISA (Wealth HH x Market Density LL).",
    "  Example: Tier 2 LH wards = affluent area with no formal retail.",
    "UC6 — Fintech POS Agent Network",
    "  Method: KDE + service-area gap analysis.",
    "  Example: Place cash-in/cash-out kiosks in unbanked corridors.",
    "UC7 — Telecoms 4G/5G Tower Siting",
    "  Method: Distance-decay weights + population density ranking.",
    "  Example: Balance signal coverage radius against population demand.",
    "UC8 — Off-Grid Solar Mini-Grid",
    "  Method: Spatial filter (wealth > threshold AND grid_access = 0).",
    "  Example: Identify affluent un-electrified settlements for private solar.",
], TEAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 21 — USE CASES PART 2
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "15 Enterprise Use Cases — Part 2: Civic, Urban & Governance (UC 9-15)", "TAXONOMY")
add_box(s, 0.8, 1.3, 5.7, 5.7, "Civic, Safety & Environment (UC 9-12)", [
    "UC9 — Cultural Peacebuilding",
    "  Method: Shannon Entropy Index + spatial smoothing.",
    "  Example: High-entropy wards in Plateau State targeted for NIPSS programs.",
    "UC10 — Emergency Response Stations",
    "  Method: Network analysis + p-median location model (OSMnx).",
    "  Example: Minimise average ambulance response time across all wards.",
    "UC11 — Urban Heat Island Detection",
    "  Method: SAR regression (LST raster x tree canopy deficit).",
    "  Example: Identify wards needing urgent urban forestry programs.",
    "UC12 — Agricultural Supply Chains",
    "  Method: Spatial flow analysis (farm-to-market travel cost surface).",
    "  Example: Locate grain silos to minimise aggregate transport cost.",
], CORAL)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Urban Infrastructure & Governance (UC 13-15)", [
    "UC13 — Real Estate Hedonic Valuation",
    "  Method: SAR regression with infrastructure variables.",
    "  Example: Clinic proximity adds N2.3M to ward median house price.",
    "UC14 — Road & Transport Investment ROI",
    "  Method: SAR Spatial Multiplier (2.4x).",
    "  Example: N5B road in Ogun creates N12B regional economic value.",
    "UC15 — Electoral Logistics (Polling Units)",
    "  Method: K-means clustering + 2km Euclidean buffer + LISA.",
    "  Example: Re-cluster 176,846 INEC polling units; flag wards where",
    "    voter travel > 2km as ACCESS GAPS needing new polling units.",
], NAVY)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 22 — ELECTORAL USE CASE DEEP DIVE
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Use Case 15 Deep Dive: Electoral Logistics & Polling Unit Optimisation", "SECTOR ANALYSIS")
add_box(s, 0.8, 1.3, 5.7, 5.7, "The Question & Data Sources", [
    "THE QUESTION:",
    "  Are all Nigerian voters within walking distance (<=2km) of a",
    "  polling unit? Which wards have unacceptable access gaps?",
    "DATA SOURCES:",
    "  INEC Polling Units (176,846 locations):",
    "  -> https://irev.inecnigeria.org",
    "  -> https://africaopendata.org",
    "  GRID3 Nigeria Ward Boundaries:",
    "  -> https://grid3.gov.ng/datasets/nigeria/administrative-boundaries",
    "  WorldPop population raster for voter density weighting:",
    "  -> https://hub.worldpop.org/geodata/listing?id=29",
], CRIMSON)
add_box(s, 6.8, 1.3, 5.7, 5.7, "The Spatial Method & Decision Output", [
    "SPATIAL METHOD (Step by Step):",
    "  1. Point-in-polygon join: assign each polling unit to its ward.",
    "  2. Compute PU density per ward (PUs per 10,000 registered voters).",
    "  3. Compute 2km Euclidean buffer around each polling unit.",
    "  4. Overlay population raster: count uncovered residents per ward.",
    "  5. Moran's I on PU density: test for spatial access inequality.",
    "  6. LISA LL coldspots: most geographically isolated wards.",
    "ACTIONABLE DECISION:",
    "  1. Open new polling units in access-gap wards.",
    "  2. Re-assign existing PUs to reduce travel time.",
    "  3. Prioritise mobile-polling trucks in LL coldspot wards.",
], NAVY)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 23 — DATA SOURCES & REFERENCES
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Data Sources & Key References", "REFERENCES")
add_box(s, 0.8, 1.3, 5.7, 5.7, "Primary Data Sources (with URLs)", [
    "Ward Boundaries (GRID3 Nigeria):",
    "  https://grid3.gov.ng/datasets/nigeria/administrative-boundaries",
    "Relative Wealth Index (Meta AI Research):",
    "  https://data.humdata.org/dataset/relative-wealth-index",
    "WorldPop Gridded Population (100m):",
    "  https://hub.worldpop.org/geodata/listing?id=29",
    "Malaria Atlas Project (PfPR rasters):",
    "  https://malariaatlas.org/explorer/",
    "GRID3 POI Registries (Clinics, Schools, Markets):",
    "  https://grid3.gov.ng/datasets/nigeria/health-facilities",
    "INEC Polling Units:",
    "  https://irev.inecnigeria.org  |  https://africaopendata.org",
    "OpenStreetMap Nigeria road network:",
    "  https://download.geofabrik.de/africa/nigeria.html",
], NAVY)
add_box(s, 6.8, 1.3, 5.7, 5.7, "Key Academic & Library References", [
    "Anselin, L. (1988). Spatial Econometrics. Kluwer Academic.",
    "Tobler, W. (1970). A computer movie. Economic Geography.",
    "",
    "PySAL:          https://pysal.org",
    "esda:           https://pysal.org/esda",
    "spreg:          https://pysal.org/spreg",
    "libpysal:       https://pysal.org/libpysal",
    "GeoPandas:      https://geopandas.org",
    "Rasterio:       https://rasterio.readthedocs.io",
    "OSMnx:          https://osmnx.readthedocs.io",
    "Folium:         https://python-visualization.github.io/folium",
    "Contextily:     https://contextily.readthedocs.io",
    "This project:   https://github.com/SammyGIS/dsn_advanced_spatial_stats",
], TEAL)

# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 24 — CONCLUSION & ACTION ROADMAP
# ──────────────────────────────────────────────────────────────────────────────
s = prs.slides.add_slide(blank_layout)
add_header(s, "Strategic Summary: How to Use This in Your Organisation", "ACTION PLAN")
add_box(s, 0.8, 1.3, 5.7, 5.7, "Key Rules for Decision-Makers", [
    "1. Stop Using Flat Averages — look at ward-level spatial distributions.",
    "2. Account for Spillovers — true return on capital is 2.4x due to",
    "   neighbouring gains.",
    "3. Start with a Question — formulate a clear hypothesis before running",
    "   any spatial model.",
    "4. Spatial Stats First — compute spatial lags and spatial CV before ML.",
    "5. Right Library for the Job:",
    "   PySAL/esda for stats, spreg for econometrics, GeoPandas for I/O.",
], NAVY)
add_box(s, 6.8, 1.3, 5.7, 5.7, "How to Access & Run This Project", [
    "Fast Track (5 seconds):",
    "  Unpack data/processed_data_bundle.zip and open any notebook.",
    "",
    "Notebooks in notebooks/:",
    "  00 — Master Executive Handbook & Inspector",
    "  01 — Multi-Sector ESDA & Malaria Surveillance",
    "  02 — Spatial Econometrics, SAR/SEM & Multipliers",
    "  03 — Decision Intelligence Across 15 Use Cases",
    "",
    "GitHub: https://github.com/SammyGIS/dsn_advanced_spatial_stats",
    "Slides: docs/spatial_statistics_masterclass_presentation.pptx",
], TEAL)

# ── Save ───────────────────────────────────────────────────────────────────────
out = "docs/spatial_statistics_masterclass_presentation.pptx"
prs.save(out)
print(f"Saved {out} — {len(prs.slides)} slides total.")
