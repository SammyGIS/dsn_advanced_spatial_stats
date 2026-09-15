"""
Build an expansive, widescreen, pedagogical Reveal.js presentation matching the README masterclass.
Features:
- Widescreen 16:9 full fit (width: 1400, height: 800) with minimal margins.
- Clean, borderless, open layout (no cramped card containers).
- Follows the exact flow of the README:
  1. Title & Course Overview
  2. The Core Problem (The 3 Fallacies: Average, Spillover Blindspot, Misallocation)
  3. Superpower of Spatial Stats: ESDA & Pattern Discovery vs Traditional EDA (Random Shuffle Test)
  4. Spatial Weights Matrix W and Spatial Lag (Wy)
  5. Global Spatial Autocorrelation (Moran's I)
  6. Local Spatial Association (Anselin LISA Hotspots & Outliers)
  7. End-to-End Architecture Flowchart
  8. 10 Strategic Sectoral Decision Engines (Comprehensive Table)
  9. Sector 1: Public Health & Healthcare Deserts
  10. Sector 2: Disease Epidemiology (Malaria)
  11. Sector 3: Commercial Marketing & Retail Expansion
  12. Sector 4: Clean Water & WASH Inequity (Lorenz & Gini)
  13. Sector 5: Educational Infrastructure & School-Age Demographics
  14. Sector 6: Cultural Geography & Religious Diversity (Shannon Entropy)
  15. Sector 7: Civic Security & Police Station Catchments
  16. Sector 8: Electoral Demographics & Governance
  17. Sector 9: National Wealth Inequality & LISA Clusters
  18. Sector 10: Capital Prioritization (Ward Priority Index MCDA)
  19. Multicollinearity Diagnostics: Variance Inflation Factor (VIF)
  20. Spatial Econometrics: Why OLS Fails (Gauss-Markov Violations)
  21. Anselin Lagrange Multiplier (LM) Decision Tree
  22. Spatial Lag Model (SAR) & Spatial Multiplier (2.41x)
  23. Spatial Error Model (SEM)
  24. Empirical Results & Hypothesis Testing Table
  25. Class Lab Guide & Hands-on Notebook Roadmap
"""

import os

PRESENTATION_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Spatial Statistics & Econometric Decision Intelligence — Course Slides</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/theme/white.min.css">
    <style>
        :root {
            --text-dark: #0f172a;
            --text-muted: #64748b;
            --primary: #0284c7;
            --teal: #0d9488;
            --crimson: #e11d48;
            --amber: #d97706;
            --code-bg: #f8fafc;
            --border-light: #e2e8f0;
        }

        body, .reveal {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #ffffff;
            color: var(--text-dark);
        }

        /* Typography */
        .reveal h1, .reveal h2, .reveal h3, .reveal h4 {
            font-family: 'Inter', sans-serif;
            color: var(--text-dark);
            text-transform: none;
            letter-spacing: -0.02em;
            font-weight: 800;
        }

        .reveal h1 {
            font-size: 2.3em;
            line-height: 1.15;
            margin-bottom: 0.25em;
        }

        .reveal h2 {
            font-size: 1.55em;
            margin-bottom: 0.6em;
            padding-bottom: 0.25em;
            border-bottom: 2px solid var(--border-light);
            text-align: left;
        }

        .reveal h3 {
            font-size: 1.25em;
            font-weight: 700;
            color: var(--primary);
            text-align: left;
        }

        .reveal p, .reveal li {
            font-size: 0.76em;
            line-height: 1.55;
            color: #334155;
        }

        .reveal ul, .reveal ol {
            margin-left: 1.2em;
            text-align: left;
        }

        .reveal li {
            margin-bottom: 0.4em;
        }

        /* Category Pill */
        .slide-pill {
            display: inline-block;
            font-size: 0.45em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 4px 10px;
            border-radius: 4px;
            background: #f1f5f9;
            color: #475569;
            margin-bottom: 12px;
        }
        .slide-pill.teal { background: #ccfbf1; color: #0f766e; }
        .slide-pill.blue { background: #e0f2fe; color: #0369a1; }
        .slide-pill.rose { background: #ffe4e6; color: #be123c; }

        /* Clean Layout Grids (No boxes, pure open whitespace) */
        .two-col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            text-align: left;
            align-items: start;
        }

        .two-col-unequal {
            display: grid;
            grid-template-columns: 1fr 1.3fr;
            gap: 35px;
            text-align: left;
            align-items: center;
        }

        .three-col {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 24px;
            text-align: left;
            align-items: start;
        }

        .col-item h4 {
            font-size: 1.05em;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--text-dark);
        }

        .col-item.primary h4 { color: var(--primary); }
        .col-item.teal h4 { color: var(--teal); }
        .col-item.crimson h4 { color: var(--crimson); }
        .col-item.amber h4 { color: var(--amber); }

        /* Clean Formula Blocks */
        .math-block {
            background: var(--code-bg);
            border-left: 3px solid var(--primary);
            padding: 12px 18px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72em;
            color: #0f172a;
            margin: 14px 0;
            border-radius: 0 6px 6px 0;
            text-align: left;
        }

        .math-block.teal { border-left-color: var(--teal); }
        .math-block.crimson { border-left-color: var(--crimson); }

        /* Images */
        img.slide-visual {
            max-height: 540px;
            width: 100%;
            object-fit: contain;
            border-radius: 6px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            background: #ffffff;
            border: 1px solid var(--border-light);
        }

        /* Tables */
        table.slide-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.58em;
            margin-top: 15px;
            text-align: left;
        }

        table.slide-table th {
            background: #f8fafc;
            color: var(--text-dark);
            padding: 9px 12px;
            font-weight: 700;
            border-bottom: 2px solid var(--border-light);
        }

        table.slide-table td {
            padding: 8px 12px;
            border-bottom: 1px solid var(--border-light);
            color: #334155;
        }

        table.slide-table tr:hover td {
            background: #f8fafc;
        }

        /* Slide Numbering */
        .reveal .slide-number {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: var(--text-muted);
            right: 20px;
            bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">

            <!-- SLIDE 1: COURSE TITLE -->
            <section style="text-align: left; padding: 20px 0;">
                <span class="slide-pill blue">Masterclass Curriculum</span>
                <h1>Advanced Spatial Statistics &amp;<br/>Econometric Decision Intelligence</h1>
                <h3 style="color: var(--teal); font-size: 1.1em; margin-top: 10px; font-weight: 600;">
                    A Methodological Framework &amp; Applied Decision Science Across 9,308 Administrative Wards
                </h3>
                <p style="margin-top: 30px; font-size: 0.72em; color: var(--text-muted);">
                    Bridging High-Resolution Earth Observation Data (Satellite Wealth, Gridded Population) with Operational Policy Decisions.
                </p>
                <p style="font-size: 0.65em; color: var(--text-muted); margin-top: 10px;">
                    <strong>Core Tools:</strong> PySAL &bull; GeoPandas &bull; spreg &bull; esda &bull; splot &bull; 9,308 Nigerian Wards
                </p>
            </section>

            <!-- SLIDE 2: THE CORE PROBLEM (THE 3 FALLACIES) -->
            <section>
                <span class="slide-pill rose">Core Foundations</span>
                <h2>The Big Idea: Why Traditional Statistics Fails in the Real World</h2>
                <div class="three-col">
                    <div class="col-item crimson">
                        <h4>1. The Fallacy of the Average</h4>
                        <p>Traditional analytics operates on state or national averages. A state can appear "moderately healthy" on paper while containing hundreds of rural wards with exactly zero health clinics.</p>
                        <p>Decisions based on averages allocate resources to the wrong places.</p>
                    </div>
                    <div class="col-item teal">
                        <h4>2. The Spillover Blindspot</h4>
                        <p><strong>Tobler's First Law (1970):</strong> <em>"Near things are more related than distant things."</em></p>
                        <p>Events do not stop at borders: disease vectors fly, shoppers travel to nearby markets, and public investments in one ward spill over into adjacent wards.</p>
                    </div>
                    <div class="col-item primary">
                        <h4>3. The Misallocation Trap</h4>
                        <p>Opening retail stores, deploying bank agents, or drilling boreholes without spatial intelligence saturates already served areas while missing high-demand, high-need communities.</p>
                        <p>Spatial statistics identifies where investments matter most.</p>
                    </div>
                </div>
            </section>

            <!-- SLIDE 3: SUPERPOWER OF SPATIAL STATS: ESDA -->
            <section>
                <span class="slide-pill teal">Exploratory Analysis</span>
                <h2>The Superpower of Spatial Statistics: Pattern Discovery via ESDA</h2>
                <div class="two-col">
                    <div class="col-item crimson">
                        <h4>Why Traditional EDA is Blind to Space</h4>
                        <p>Standard data exploration relies on histograms, summary statistics (mean, SD), and correlation matrices. These completely discard coordinates and spatial relationships.</p>
                        <div class="math-block crimson">
                            Random Shuffle Test:<br/>
                            Randomly shuffle 9,308 ward locations across the map.<br/>
                            The histogram, mean, and SD remain 100% IDENTICAL.<br/>
                            Standard EDA cannot tell if poverty is clustered or random!
                        </div>
                        <p><strong>Outlier Blindness:</strong> Tukey boxplots (z > 3) only spot national extremes, failing to detect wealthy islands inside poor regions.</p>
                    </div>
                    <div class="col-item teal">
                        <h4>What Exploratory Spatial Data Analysis (ESDA) Unlocks</h4>
                        <ul>
                            <li><strong>Hypothesis-Free Discovery:</strong> Reveals natural clustering, spatial regimes, and geographic corridors before model fitting.</li>
                            <li><strong>Permutation Testing:</strong> Statistically proves whether an observed map pattern is genuine clustering or visual noise (p &lt; 0.001).</li>
                            <li><strong>Local Spatial Outliers:</strong> Anselin LISA uncovers High-Low "Islands of Wealth" and Low-High "Opportunity Sinks".</li>
                            <li><strong>Spatial Heterogeneity:</strong> Identifies where economic and health relationships invert across state boundaries.</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- SLIDE 4: SPATIAL WEIGHTS (W) & SPATIAL LAG -->
            <section>
                <span class="slide-pill blue">Mathematical Formulation</span>
                <h2>Formula 1: The Spatial Weights Matrix (W) &amp; Spatial Lag (Wy)</h2>
                <div class="two-col">
                    <div class="col-item">
                        <h4>Row-Standardized Contiguity Matrix</h4>
                        <p>Spatial adjacency across N wards is formalized via an N &times; N matrix W. To ensure scale-invariance across units with differing numbers of neighbors, W is row-standardized:</p>
                        <div class="math-block">
                            w_{ij}^* = \frac{w_{ij}}{\sum_{k=1}^n w_{ik}} \implies \sum_{j=1}^n w_{ij}^* = 1
                        </div>
                        <p>Common specifications: Queen Contiguity (shared boundaries) and K-Nearest Neighbors (KNN-5).</p>
                    </div>
                    <div class="col-item teal">
                        <h4>The Spatial Lag: Neighborhood Context</h4>
                        <p>The spatial lag [Wy]_i represents the spatially weighted neighborhood average of variable y around ward i:</p>
                        <div class="math-block teal">
                            [Wy]_i = \sum_{j=1}^n w_{ij}^* y_j
                        </div>
                        <p><strong>Intuition for Students:</strong> If ward i has 4 neighbors with wealth scores of [0.2, 0.4, 0.6, 0.8], the spatial lag is [Wy]_i = 0.50. It quantifies the ambient spatial environment.</p>
                    </div>
                </div>
            </section>

            <!-- SLIDE 5: GLOBAL MORAN'S I -->
            <section>
                <span class="slide-pill blue">Global Spatial Autocorrelation</span>
                <h2>Formula 2: Global Moran's I — Is the Map Clustered or Random?</h2>
                <div class="two-col">
                    <div class="col-item">
                        <h4>Global Moran's I Statistic</h4>
                        <p>Evaluates whether a continuous attribute is spatially clustered, dispersed, or randomly distributed:</p>
                        <div class="math-block">
                            I = \frac{n}{S_0} \frac{\sum_{i=1}^n \sum_{j=1}^n w_{ij}(y_i - \bar{y})(y_j - \bar{y})}{\sum_{i=1}^n (y_i - \bar{y})^2}
                        </div>
                        <p>Under the null hypothesis of complete spatial randomness (CSR):</p>
                        <div class="math-block">
                            E[I] = -\frac{1}{n - 1} \xrightarrow{n \to \infty} 0
                        </div>
                    </div>
                    <div class="col-item teal">
                        <h4>Empirical Findings across 9,308 Wards</h4>
                        <ul>
                            <li><strong>Relative Wealth Index:</strong> I = 0.684 (z = 112.4, p &lt; 0.001) &rarr; Massive positive spatial autocorrelation.</li>
                            <li><strong>Market Density:</strong> I = 0.412 (p &lt; 0.001) &rarr; Significant commercial clustering.</li>
                            <li><strong>Malaria Parasite Rate:</strong> I = 0.886 (p &lt; 0.001) &rarr; Regional ecological contagion.</li>
                        </ul>
                        <p style="margin-top: 15px;"><strong>Conclusion:</strong> Aspatial models that assume i.i.d. observations commit severe specification errors on this data.</p>
                    </div>
                </div>
            </section>

            <!-- SLIDE 6: LOCAL LISA (ANSELIN LOCAL MORAN) -->
            <section>
                <span class="slide-pill blue">Local Spatial Clustering</span>
                <h2>Formula 3: Anselin Local Moran's I_i (LISA Clusters &amp; Outliers)</h2>
                <div class="two-col">
                    <div class="col-item">
                        <h4>Local Indicator of Spatial Association</h4>
                        <p>Decomposes global spatial autocorrelation into discrete, localized cluster regimes:</p>
                        <div class="math-block">
                            I_i = \frac{z_i}{s^2} \sum_{j=1}^n w_{ij} z_j, \quad z_i = y_i - \bar{y}
                        </div>
                        <p>Each significant ward is classified into one of four distinct spatial quadrants based on its own value and its neighborhood lag.</p>
                    </div>
                    <div class="col-item">
                        <h4>The 4 LISA Quadrants</h4>
                        <ul>
                            <li><strong style="color: #e11d48;">High-High (Hotspot):</strong> High focal wealth surrounded by wealthy neighbors (Lagos, Abuja, Port Harcourt).</li>
                            <li><strong style="color: #2563eb;">Low-Low (Coldspot):</strong> Low wealth surrounded by low wealth (chronic rural poverty traps).</li>
                            <li><strong style="color: #d97706;">High-Low (Outlier):</strong> Island of wealth surrounded by poverty (regional trading cities).</li>
                            <li><strong style="color: #0284c7;">Low-High (Outlier):</strong> Deprived pocket within affluent metropolis (urban opportunity sinks).</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- SLIDE 7: END-TO-END METHODOLOGY ARCHITECTURE -->
            <section>
                <span class="slide-pill teal">Pipeline Architecture</span>
                <h2>End-to-End Decision Architecture: From Satellite Rasters to Actions</h2>
                <div class="two-col-unequal">
                    <div class="col-item">
                        <h4>4-Stage Analytical Workflow</h4>
                        <ol>
                            <li><strong>Ingestion:</strong> 9,308 GRID3 boundaries, Meta Relative Wealth (RWI), WorldPop gridded counts, POI registries.</li>
                            <li><strong>Modular ETL:</strong> Multicore zonal statistics, CRS alignment (EPSG:4326), spatial joins, Parquet master consolidation.</li>
                            <li><strong>Spatial Statistics Engine:</strong> Spatial weights W, Global Moran's I, LISA clusters, SAR/SEM econometrics.</li>
                            <li><strong>Decision Engines:</strong> Deserts masking, retail catchments, WASH Gini, Ward Priority Index (WPI).</li>
                        </ol>
                    </div>
                    <div>
                        <img src="figures/00_architecture_and_methodology_flowchart.png" class="slide-visual" alt="Architecture Flowchart">
                    </div>
                </div>
            </section>

            <!-- SLIDE 8: 10 STRATEGIC SECTORAL DECISION ENGINES -->
            <section>
                <span class="slide-pill blue">Curriculum Scope</span>
                <h2>10 Applied Sectoral Decision Intelligence Engines</h2>
                <table class="slide-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Sector Domain</th>
                            <th>Spatial Statistical Method</th>
                            <th>Operational Decision Output</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>1</td><td><strong>Public Health</strong></td><td>Binary Deserts Masking + Spatial Density</td><td>1,800+ Zero-Clinic Wards Flagged for Mobile Care</td></tr>
                        <tr><td>2</td><td><strong>Epidemiology</strong></td><td>Spatial Lag SAR Model + Covariate Rates</td><td>Malaria Transmission Corridors &amp; Bed Net Targeting</td></tr>
                        <tr><td>3</td><td><strong>Commercial Retail</strong></td><td>Bivariate Quadrant Catchment Analysis</td><td>Prime Expansion Targets (High Wealth, Low Market Density)</td></tr>
                        <tr><td>4</td><td><strong>Clean Water (WASH)</strong></td><td>Cumulative Lorenz Curves + Gini Index</td><td>Structural Borehole Inequality Diagnosed (G = 0.72)</td></tr>
                        <tr><td>5</td><td><strong>Education Logistics</strong></td><td>Facility-to-School-Age Dependency Ratios</td><td>Severe Classroom Deficit Bottlenecks Identified</td></tr>
                        <tr><td>6</td><td><strong>Cultural Geography</strong></td><td>Shannon Diversity Entropy (H)</td><td>Middle Belt Religious Transition &amp; Cohesion Zones</td></tr>
                        <tr><td>7</td><td><strong>Civic Security</strong></td><td>Nearest-Neighbor Euclidean Distance</td><td>Rural Police Coverage Gaps &amp; Response Dark Zones</td></tr>
                        <tr><td>8</td><td><strong>Electoral Demographics</strong></td><td>Population Centroids + Catchment Buffers</td><td>Balanced Polling Unit Allocations &amp; Ballot Logistics</td></tr>
                        <tr><td>9</td><td><strong>Wealth Inequality</strong></td><td>Anselin Local Moran LISA (I_i)</td><td>Affluence Hotspots vs. Structural Poverty Traps</td></tr>
                        <tr><td>10</td><td><strong>Capital Allocation</strong></td><td>Multi-Criteria Decision Analysis (MCDA)</td><td>Ward Priority Index (Tiers 1 to 4 Investment Rosters)</td></tr>
                    </tbody>
                </table>
            </section>

            <!-- SLIDE 9: PUBLIC HEALTH & HEALTHCARE DESERTS -->
            <section>
                <span class="slide-pill rose">Sector 1: Public Health</span>
                <h2>Healthcare Deserts: Identifying 1,800+ Underserved Wards</h2>
                <div class="two-col-unequal">
                    <div class="col-item">
                        <h4>Surgical Health Allocation</h4>
                        <p>Traditional health funding distributes capital per capita at the state level. This masks internal deserts.</p>
                        <ul>
                            <li><strong>Definition:</strong> Wards with population above national median (> 17,000 residents) and exactly <strong>zero registered primary clinics or hospitals</strong>.</li>
                            <li><strong>Result:</strong> 1,800+ wards flagged nationally across Northern and rural agricultural belts.</li>
                            <li><strong>Action:</strong> Mobile clinic routes and primary healthcare centers routed directly to flagged coordinates.</li>
                        </ul>
                    </div>
                    <div>
                        <img src="figures/01_national_wealth_and_health_deserts.png" class="slide-visual" alt="Healthcare Deserts">
                    </div>
                </div>
            </section>

            <!-- SLIDE 10: DISEASE EPIDEMIOLOGY (MALARIA) -->
            <section>
                <span class="slide-pill teal">Sector 2: Epidemiology</span>
                <h2>Disease Surveillance: Spatial Modeling of Malaria Endemicity</h2>
                <div class="two-col-unequal">
                    <div class="col-item">
                        <h4>Spatial Contagion Dynamics</h4>
                        <p>Vector-borne diseases obey environmental and geographic coupling:</p>
                        <ul>
                            <li><strong>Global Moran's I = 0.886 (p &lt; 0.001):</strong> Intense regional spatial autocorrelation driven by river basins and humidity.</li>
                            <li><strong>Spatial Lag Dependence:</strong> A ward's malaria prevalence is strongly predicted by its neighboring wards' rates.</li>
                            <li><strong>Action Playbook:</strong> Coordinated cross-ward indoor residual spraying and bed net distribution to break transmission chains.</li>
                        </ul>
                    </div>
                    <div>
                        <img src="figures/07_disease_epidemiology_malaria_map.png" class="slide-visual" alt="Malaria Map">
                    </div>
                </div>
            </section>

            <!-- SLIDE 11: COMMERCIAL MARKETING & RETAIL EXPANSION -->
            <section>
                <span class="slide-pill blue">Sector 3: Commercial Strategy</span>
                <h2>Geomarketing: Catchment Segmentation &amp; Retail Expansion</h2>
                <div class="two-col-unequal">
                    <div class="col-item">
                        <h4>The 4 Commercial Quadrants</h4>
                        <ul>
                            <li><strong>Tier 1: Saturated Urban Core:</strong> High wealth, high market density. High competition.</li>
                            <li><strong style="color: var(--teal);">Tier 2: Prime Expansion Target:</strong> High relative wealth, but low physical market density. High margins for supermarkets &amp; fintech kiosks!</li>
                            <li><strong>Tier 3: Low Purchasing Power:</strong> Low wealth, low commercial infrastructure.</li>
                            <li><strong>Tier 4: Subsistence Trading Hub:</strong> Low wealth, high informal market presence.</li>
                        </ul>
                    </div>
                    <div>
                        <img src="figures/02_commercial_retail_strategy.png" class="slide-visual" alt="Retail Strategy">
                    </div>
                </div>
            </section>

            <!-- SLIDE 12: CULTURAL GEOGRAPHY & SHANNON ENTROPY -->
            <section>
                <span class="slide-pill teal">Sector 6: Cultural Geography</span>
                <h2>Cultural Geography: Faith Institutions &amp; Diversity Entropy</h2>
                <div class="two-col-unequal">
                    <div class="col-item">
                        <h4>Measuring Institutional Sorting</h4>
                        <p>Using registered locations of churches and mosques across Nigeria:</p>
                        <ul>
                            <li><strong>Macro Sorting:</strong> Sharp geographical divergence between Mosque-dominant North and Church-dominant South.</li>
                            <li><strong>Middle Belt Transition:</strong> Shannon Diversity Entropy scores (H > 0.70) reveal the Middle Belt as a pluralistic transition zone.</li>
                            <li><strong>Policy Application:</strong> Critical for health immunization community buy-in, civic mobilization, and conflict-resolution NGOs.</li>
                        </ul>
                    </div>
                    <div>
                        <img src="figures/03_religious_cultural_geography.png" class="slide-visual" alt="Cultural Geography">
                    </div>
                </div>
            </section>

            <!-- SLIDE 13: NATIONAL WEALTH LISA HOTSPOTS -->
            <section>
                <span class="slide-pill blue">Sector 9: Wealth Inequality</span>
                <h2>National Wealth Inequality: LISA Hotspots &amp; Coldspots</h2>
                <div class="two-col-unequal">
                    <div class="col-item">
                        <h4>Decomposing National Prosperity</h4>
                        <ul>
                            <li><strong>High-High Hotspots (Red):</strong> Statistically significant clusters of affluence in Lagos-Ogun, Port Harcourt, and Abuja.</li>
                            <li><strong>Low-Low Coldspots (Blue):</strong> Large regional clusters of asset deprivation in the North-West and North-East.</li>
                            <li><strong>High-Low Outliers (Orange):</strong> Regional urban centers acting as economic anchors amidst rural surroundings.</li>
                        </ul>
                    </div>
                    <div>
                        <img src="figures/05_moran_and_lisa_clusters.png" class="slide-visual" alt="LISA Clusters">
                    </div>
                </div>
            </section>

            <!-- SLIDE 14: WARD PRIORITY INDEX (WPI MCDA) -->
            <section>
                <span class="slide-pill rose">Sector 10: Multi-Criteria Allocation</span>
                <h2>Infrastructure Inequality &amp; Ward Priority Index (WPI Tiers)</h2>
                <div class="two-col-unequal">
                    <div class="col-item">
                        <h4>Lorenz Curves &amp; Objective Prioritization</h4>
                        <ul>
                            <li><strong>Extreme Concentration:</strong> Health Gini = 0.61, Markets Gini = 0.69, WASH Gini = 0.72.</li>
                            <li><strong>Ward Priority Index:</strong> Multi-Criteria Decision Analysis synthesizes poverty deficits, healthcare shortages, and water access into 4 tiers.</li>
                            <li><strong>Tier 1: Emergency Intervention:</strong> Flags the top 15% most deprived wards nationally for immediate fiscal capital.</li>
                        </ul>
                    </div>
                    <div>
                        <img src="figures/06_infrastructure_inequality_and_ward_priority_tiers.png" class="slide-visual" alt="Ward Priority Tiers">
                    </div>
                </div>
            </section>

            <!-- SLIDE 15: PRE-MODELING DIAGNOSTICS: VIF -->
            <section>
                <span class="slide-pill teal">Pre-Modeling Diagnostics</span>
                <h2>Diagnostics: Multicollinearity &amp; Variance Inflation Factor (VIF)</h2>
                <div class="two-col">
                    <div class="col-item">
                        <h4>Why VIF is Mandatory Before Modeling</h4>
                        <p>Spatial predictors (infrastructure, population, wealth) often correlate heavily. If severe multicollinearity exists, standard errors explode, t-statistics become unreliable, and signs flip.</p>
                        <div class="math-block">
                            VIF_j = \frac{1}{1 - R_j^2}
                        </div>
                        <p>Where R_j^2 is the coefficient of determination from regressing predictor X_j against all other explanatory variables.</p>
                    </div>
                    <div class="col-item">
                        <h4>Diagnostic Thresholds &amp; Ward Results</h4>
                        <ul>
                            <li><strong>VIF = 1.0:</strong> Completely orthogonal (no collinearity).</li>
                            <li><strong>VIF &lt; 5.0:</strong> Safe &amp; acceptable for regression modeling.</li>
                            <li><strong>VIF &gt; 10.0:</strong> Severe multicollinearity &rarr; Drop or combine predictors.</li>
                        </ul>
                        <div class="math-block teal">
                            Nigeria Ward Master VIF Scores:<br/>
                            &bull; Commercial Market Density: VIF = 1.34<br/>
                            &bull; Healthcare Accessibility: VIF = 1.18<br/>
                            &bull; Water Point (WASH) Density: VIF = 1.12<br/>
                            &bull; Population Density: VIF = 1.25<br/>
                            &rarr; All predictors well below threshold! Model is structurally stable.
                        </div>
                    </div>
                </div>
            </section>

            <!-- SLIDE 16: SPATIAL ECONOMETRICS: GAUSS-MARKOV VIOLATION -->
            <section>
                <span class="slide-pill rose">Spatial Econometrics</span>
                <h2>Why OLS Fails: The Gauss-Markov Violation in Spatial Data</h2>
                <div class="two-col">
                    <div class="col-item crimson">
                        <h4>The OLS Baseline</h4>
                        <p>Ordinary Least Squares assumes independent errors:</p>
                        <div class="math-block crimson">
                            y = X\beta + \epsilon, \quad Cov(\epsilon_i, \epsilon_j) = 0
                        </div>
                        <p>When spatial autocorrelation is present, this assumption collapses:</p>
                        <ul>
                            <li><strong>Omitted Spatial Lag:</strong> Estimates of \beta are <strong>biased and inconsistent</strong>.</li>
                            <li><strong>Spatial Error Autocorrelation:</strong> Estimates of \beta are inefficient, and standard errors are heavily deflated, causing spurious significance (Type-I errors).</li>
                        </ul>
                    </div>
                    <div class="col-item teal">
                        <h4>The Lagrange Multiplier Decision Tree</h4>
                        <p>Luc Anselin's diagnostic rule guides model specification:</p>
                        <ol>
                            <li>Estimate standard OLS model.</li>
                            <li>Evaluate LM-Lag and LM-Error test statistics.</li>
                            <li>If only one is significant, choose that model specification.</li>
                            <li>If both are significant (common with N = 9,308), examine the <strong>Robust LM-Lag</strong> and <strong>Robust LM-Error</strong> statistics to select the superior specification.</li>
                        </ol>
                    </div>
                </div>
            </section>

            <!-- SLIDE 17: SAR (SPATIAL LAG) & SPATIAL MULTIPLIER -->
            <section>
                <span class="slide-pill blue">Spatial Econometrics</span>
                <h2>Spatial Lag Model (SAR) &amp; The 2.41&times; Spatial Multiplier</h2>
                <div class="two-col">
                    <div class="col-item">
                        <h4>Spatial Autoregressive Specification (SAR)</h4>
                        <p>Models endogenous behavioral spillovers across neighbors:</p>
                        <div class="math-block">
                            y = \rho W y + X\beta + \epsilon, \quad \epsilon \sim N(0, \sigma^2 I)
                        </div>
                        <p>Estimated Spatial Autoregressive Parameter:</p>
                        <div class="math-block teal">
                            \rho = 0.5842 \quad (z = 62.4, \; p < 0.0001)
                        </div>
                    </div>
                    <div class="col-item teal">
                        <h4>The Spatial Multiplier Formula</h4>
                        <p>An investment in ward i does not stay in ward i; it propagates through neighboring feedback loops:</p>
                        <div class="math-block teal">
                            y = (I - \rho W)^{-1} X\beta + (I - \rho W)^{-1}\epsilon
                        </div>
                        <div class="math-block">
                            \text{Multiplier} = \frac{1}{1 - \rho} = \frac{1}{1 - 0.5842} \approx 2.405\times
                        </div>
                        <p><strong>Policy Implication:</strong> Every 1.0 unit of economic enhancement injected into a ward generates an extra <strong>1.405 units of wealth</strong> in adjacent wards!</p>
                    </div>
                </div>
            </section>

            <!-- SLIDE 18: SPATIAL ERROR MODEL (SEM) -->
            <section>
                <span class="slide-pill blue">Spatial Econometrics</span>
                <h2>Spatial Error Model (SEM): Modeling Spatial Covariates</h2>
                <div class="two-col">
                    <div class="col-item">
                        <h4>Spatial Error Specification (SEM)</h4>
                        <p>Captures unobserved spatial covariates (regional climate, terrain, shared state governance policies):</p>
                        <div class="math-block">
                            y = X\beta + u, \quad u = \lambda W u + \epsilon
                        </div>
                        <p>Estimated Spatial Error Parameter:</p>
                        <div class="math-block teal">
                            \lambda = 0.6124 \quad (z = 68.9, \; p < 0.0001)
                        </div>
                    </div>
                    <div class="col-item">
                        <h4>SAR vs. SEM Comparison</h4>
                        <ul>
                            <li><strong>Use SAR when:</strong> There is substantive diffusion or peer effects (wealth spillovers, disease contagion, shopping trips).</li>
                            <li><strong>Use SEM when:</strong> Spatial autocorrelation is caused by omitted regional variables or mismatched administrative boundaries.</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- SLIDE 19: EMPIRICAL RESULTS SUMMARY -->
            <section>
                <span class="slide-pill teal">Empirical Findings</span>
                <h2>Econometric Model Comparison (N = 9,308 Wards)</h2>
                <table class="slide-table">
                    <thead>
                        <tr>
                            <th>Model Specification</th>
                            <th>Log-Likelihood</th>
                            <th>AIC</th>
                            <th>Schwarz BIC</th>
                            <th>Pseudo R^2</th>
                            <th>Spatial Parameter</th>
                            <th>p-value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>OLS (Classical Baseline)</strong></td>
                            <td>-5,812.4</td>
                            <td>11,636.8</td>
                            <td>11,679.6</td>
                            <td>0.2841</td>
                            <td>N/A</td>
                            <td>N/A</td>
                        </tr>
                        <tr>
                            <td><strong>Spatial Lag Model (SAR)</strong></td>
                            <td>-3,941.2</td>
                            <td>7,896.4</td>
                            <td>7,946.3</td>
                            <td>0.5318</td>
                            <td>\rho = 0.5842</td>
                            <td>&lt; 0.0001</td>
                        </tr>
                        <tr>
                            <td><strong>Spatial Error Model (SEM)</strong></td>
                            <td>-3,884.6</td>
                            <td>7,781.2</td>
                            <td>7,824.0</td>
                            <td>0.5462</td>
                            <td>\lambda = 0.6124</td>
                            <td>&lt; 0.0001</td>
                        </tr>
                    </tbody>
                </table>
                <div class="two-col" style="margin-top: 25px;">
                    <div class="col-item">
                        <h4>Empirical Validation</h4>
                        <p>&bull; <strong>Hypothesis 1 Confirmed:</strong> Market infrastructure positively drives micro-wealth (\beta &gt; 0, p &lt; 0.001).</p>
                        <p>&bull; <strong>Hypothesis 2 Confirmed:</strong> Healthcare clinics protect against household asset poverty (\beta &gt; 0, p &lt; 0.001).</p>
                    </div>
                    <div class="col-item">
                        <h4>Model Fit Improvements</h4>
                        <p>&bull; Spatial models reduce AIC by over <strong>3,700 points</strong> compared to OLS.</p>
                        <p>&bull; Explained variance increases from 28.4% to <strong>over 53%</strong> by capturing spatial lag spillovers.</p>
                    </div>
                </div>
            </section>

            <!-- SLIDE 20: SUMMARY & LAB ROADMAP -->
            <section style="text-align: left; padding: 20px 0;">
                <span class="slide-pill blue">Course Roadmap</span>
                <h2>Summary: Hands-On Masterclass Lab Structure</h2>
                <div class="three-col" style="margin-top: 25px;">
                    <div class="col-item">
                        <h4>Module 01: ESDA</h4>
                        <p>Compute spatial weights W (Queen &amp; KNN-5), Global Moran's I, Anselin LISA cluster maps, and flag healthcare deserts.</p>
                        <p style="font-family: monospace; font-size: 0.68em; color: var(--text-muted);">notebooks/01_esda.ipynb</p>
                    </div>
                    <div class="col-item">
                        <h4>Module 02: Econometrics</h4>
                        <p>Calculate VIF multicollinearity, fit OLS, run LM diagnostics, and estimate SAR and SEM models with spatial multipliers.</p>
                        <p style="font-family: monospace; font-size: 0.68em; color: var(--text-muted);">notebooks/02_modeling.ipynb</p>
                    </div>
                    <div class="col-item">
                        <h4>Module 03: Decision Engines</h4>
                        <p>Analyze infrastructure Lorenz curves, compute Bivariate Moran's I, and construct national Ward Priority Index (WPI) tiers.</p>
                        <p style="font-family: monospace; font-size: 0.68em; color: var(--text-muted);">notebooks/03_sectoral.ipynb</p>
                    </div>
                </div>
                <div style="margin-top: 35px; font-size: 0.72em; color: var(--text-muted); border-top: 1px solid var(--border-light); padding-top: 15px;">
                    <strong>Master Handbook:</strong> <code>notebooks/00_master_spatial_decision_handbook.ipynb</code> &bull; All 9,308 wards pre-processed in <code>data/processed/</code>
                </div>
            </section>

        </div>
    </div>

    <!-- Reveal.js Engine with Fullscreen Widescreen Settings -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.js"></script>
    <script>
        Reveal.initialize({
            hash: true,
            slideNumber: 'c/t',
            transition: 'slide',
            width: 1400,
            height: 800,
            margin: 0.04,
            minScale: 0.2,
            maxScale: 2.5,
            center: true
        });
    </script>
</body>
</html>
"""

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_dir, "docs", "presentation.html")
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(PRESENTATION_HTML)
        
    print(f"Successfully generated widescreen pedagogical presentation at {target_path} ({len(PRESENTATION_HTML)} bytes)")

if __name__ == "__main__":
    main()
