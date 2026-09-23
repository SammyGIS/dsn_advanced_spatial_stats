"""
Build a comprehensive, beautifully typeset Technical Note document for 
Advanced Spatial Statistics: Theory, Formulations & Statistical Modeling.

Features:
- Long-form, continuous scrolling document with a sticky Table of Contents.
- Generous, large typography (17px body, 1.7 line height, elegant Inter & JetBrains Mono).
- Complete mathematical formulations, derivations, proofs, and matrix algebra.
- KaTeX auto-rendered mathematics.
- Covers:
  1. Spatial Topology & Weight Matrix Algebra
  2. Spatial Autocorrelation & Association Metrics
  3. Classical Regression Mechanics & Gauss-Markov Breakdown
  4. Spatial Model Specifications (SAR, SEM, SDM, Multipliers)
  5. Local Regression & Multiscale Spatial Heterogeneity (GWR, MGWR)
  6. Spatial Statistics vs. Machine Learning (GWR vs RF/XGBoost)
  7. Spatial Statistics Model Selection Protocol
"""

import os

TECHNICAL_NOTE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical Note, Advanced Spatial Statistics</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
    <style>
        :root {
            --text-main: #0f172a;
            --text-secondary: #334155;
            --text-muted: #64748b;
            --primary: #0284c7;
            --primary-dark: #0369a1;
            --teal: #0d9488;
            --crimson: #e11d48;
            --amber: #d97706;
            --purple: #7c3aed;
            --border: #e2e8f0;
            --bg-light: #f8fafc;
            --card-bg: #ffffff;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #ffffff;
            color: var(--text-main);
            line-height: 1.78;
            font-size: 18.5px;
            -webkit-font-smoothing: antialiased;
        }

        /* Wide Layout with Sticky TOC */
        .doc-container {
            display: flex;
            max-width: 1680px;
            width: 96%;
            margin: 0 auto;
            padding: 30px 20px;
            gap: 40px;
            background-color: #ffffff;
        }

        /* Sticky Sidebar Table of Contents */
        .toc-sidebar {
            width: 320px;
            flex-shrink: 0;
            position: sticky;
            top: 30px;
            height: calc(100vh - 60px);
            overflow-y: auto;
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 24px 18px;
        }

        .toc-sidebar::-webkit-scrollbar {
            width: 5px;
        }
        .toc-sidebar::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 3px;
        }

        .toc-title {
            font-size: 14.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 14px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
        }

        .toc-nav {
            list-style: none;
        }

        .toc-nav li {
            margin-bottom: 6px;
        }

        .toc-nav a {
            display: block;
            font-size: 15px;
            color: var(--text-secondary);
            text-decoration: none;
            padding: 7px 12px;
            border-radius: 6px;
            transition: all 0.15s ease;
            line-height: 1.4;
        }

        .toc-nav a:hover {
            background: #f8fafc;
            color: var(--primary);
        }

        .toc-nav a.active {
            background: #f1f5f9;
            color: var(--primary-dark);
            font-weight: 600;
        }

        /* Main Article Content */
        .doc-content {
            flex: 1;
            min-width: 0;
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 56px 72px;
        }

        /* Typography */
        h1.doc-header-title {
            font-size: 2.5em;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.03em;
            line-height: 1.20;
            margin-bottom: 12px;
        }

        .doc-subtitle {
            font-size: 1.22em;
            color: var(--text-muted);
            font-weight: 400;
            margin-bottom: 32px;
            line-height: 1.5;
            padding-bottom: 24px;
            border-bottom: 2px solid var(--border);
        }

        h2 {
            font-size: 1.80em;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.02em;
            margin-top: 54px;
            margin-bottom: 18px;
            padding-bottom: 8px;
            border-bottom: 1.5px solid var(--border);
        }

        h3 {
            font-size: 1.25em;
            font-weight: 600;
            color: var(--primary-dark);
            margin-top: 34px;
            margin-bottom: 14px;
        }

        h4 {
            font-size: 1.15em;
            font-weight: 600;
            color: var(--text-main);
            margin-top: 22px;
            margin-bottom: 10px;
        }

        p {
            margin-bottom: 18px;
            color: var(--text-secondary);
            font-size: 18px;
        }

        ul, ol {
            margin-left: 28px;
            margin-bottom: 22px;
            color: var(--text-secondary);
            font-size: 18px;
        }

        li {
            margin-bottom: 9px;
        }

        /* Clean Formula Display Boxes (No colored edge borders) */
        .formula-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px 24px;
            margin: 24px 0;
            overflow-x: auto;
        }

        .formula-card.blue, .formula-card.purple, .formula-card.teal, .formula-card.rose, .formula-card.amber {
            border: 1px solid #e2e8f0;
            background: #f8fafc;
        }

        .formula-title {
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            margin-bottom: 10px;
        }

        /* Clean Callout Boxes (No colored edge borders) */
        .callout {
            border-radius: 8px;
            padding: 20px 24px;
            margin: 24px 0;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
        }
        .callout.blue, .callout.teal, .callout.rose, .callout.amber, .callout.purple {
            border: 1px solid #e2e8f0;
            background: #f8fafc;
        }

        .callout h4 {
            margin-top: 0;
            margin-bottom: 8px;
        }

        /* Tables */
        table.ref-table {
            width: 100%;
            border-collapse: collapse;
            margin: 26px 0;
            font-size: 16px;
        }

        table.ref-table th, table.ref-table td {
            padding: 14px 18px;
            border: 1px solid var(--border);
            text-align: left;
            vertical-align: top;
        }

        table.ref-table th {
            background: #f1f5f9;
            font-weight: 700;
            color: var(--text-main);
        }

        table.ref-table tr:hover {
            background: #f8fafc;
        }

        code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.88em;
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            color: #0f172a;
        }

        @media (max-width: 1080px) {
            .doc-container {
                flex-direction: column;
                padding: 16px;
                width: 100%;
            }
            .toc-sidebar {
                width: 100%;
                height: auto;
                position: relative;
                top: 0;
            }
            .doc-content {
                padding: 32px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="doc-container">

        <!-- Sticky Table of Contents -->
        <aside class="toc-sidebar">
            <div class="toc-title">Technical Index</div>
            <ul class="toc-nav">
                <li><a href="#sec1">1. Foundations &amp; Spatial Axioms</a></li>
                <li><a href="#sec2">2. Spatial Weights Matrices ($W$)</a></li>
                <li><a href="#sec3">3. Spatial Autocorrelation &amp; LISA</a></li>
                <li><a href="#sec4">4. OLS Mechanics &amp; Gauss-Markov Breakdown</a></li>
                <li><a href="#sec5">5. Spatial Lag Model (SAR)</a></li>
                <li><a href="#sec6">6. Spatial Error Model (SEM)</a></li>
                <li><a href="#sec7">7. Spatial Durbin Model (SDM) &amp; Multipliers</a></li>
                <li><a href="#sec8">8. Geographically Weighted Regression (GWR)</a></li>
                <li><a href="#sec9">9. Multiscale GWR (MGWR)</a></li>
                <li><a href="#sec10">10. Spatial Statistics vs. Machine Learning</a></li>
                <li><a href="#sec11">11. Master Model Reference Table</a></li>
                <li><a href="#sec12">12. Statistical Selection Protocol</a></li>
            </ul>
        </aside>


        <!-- Main Document Body -->
        <main class="doc-content">
            <h1 class="doc-header-title">Technical Note: Advanced Spatial Statistics</h1>
            <p class="doc-subtitle">Intuitive explanations, worked examples, and complete formulations, a companion reference for the lecture series.</p>

            <!-- SECTION 1 -->
            <section id="sec1">
                <h2>1. Why Space Breaks Standard Statistics</h2>
                <p>Every statistics course begins with a deceptively simple assumption: your observations are <strong>independent</strong> of each other. The temperature measured in Lagos today has nothing to do with the temperature measured in Accra. The crop yield of one farmer's field tells you nothing about the field next door. This assumption is the engine that makes classical tests, t-tests, OLS regression, ANOVA, run cleanly.</p>
                <p>The moment your data has <strong>geographic coordinates</strong>, this assumption collapses. A child's nutritional status in one ward is tightly linked to the nutritional status of children in neighbouring wards. Property prices on one block bleed directly into prices on adjacent blocks. Disease incidence in one district ripples into adjacent districts through shared roads, markets, and social networks.</p>
                <p>This pervasive geographic interdependence was captured by Waldo Tobler in 1970 as the <strong>First Law of Geography</strong>: <em>"Everything is related to everything else, but near things are more related than distant things."</em></p>

                <div class="formula-card blue">
                    <div class="formula-title">Tobler's Law, Distance-Decay Covariance</div>
                    $$\text{Cov}(Z(s_i), Z(s_j)) = C(\|s_i - s_j\|) > 0, \quad \lim_{\|s_i - s_j\| \to \infty} C(\|s_i - s_j\|) = 0$$
                </div>

                <p>The covariance between any two geographic observations $Z(s_i)$ and $Z(s_j)$ is a <em>decreasing function of their separation distance</em>. Close neighbours share high covariance; distant units share near-zero covariance. The function $C(\cdot)$ is the <strong>covariance kernel</strong>, the mathematical shape of how influence decays with distance.</p>

                <h3>The Consequence: Phantom Precision</h3>
                <p>When observations are spatially correlated, each new geographic data point carries less <em>new</em> independent information than it appears to. Fifty census tracts that are all adjacent to each other do not give you fifty independent data points, they might effectively give you fifteen or twenty, because they are all echoing each other. Standard software, unaware of this, computes standard errors by dividing by $(n - k)$ when it should divide by a much smaller effective sample. The result: standard errors are <strong>far too small</strong>, t-statistics are <strong>too large</strong>, and p-values declare significance that does not actually exist, a phenomenon called Type I error inflation.</p>

                <div class="example-box">
                    <div class="example-label">Real-World Example, Maternal Mortality</div>
                    <p>A researcher fits an OLS model explaining maternal mortality across 200 health wards using poverty, distance to clinic, and education. The model reports $p &lt; 0.01$ for distance to clinic. She concludes the effect is highly significant.</p>
                    <p>However, a Moran's I test on the OLS residuals returns $I = 0.42$, $p &lt; 0.001$, the residuals are strongly clustered. The 200 wards carry the effective information of perhaps 80 independent observations. The standard errors are artificially small. The correct model, a Spatial Error Model, inflates the standard error for distance, and the $p$-value becomes $0.09$. The earlier conclusion was an artefact of spatial autocorrelation.</p>
                </div>
            </section>

            <!-- SECTION 2 -->
            <section id="sec2">
                <h2>2. Spatial Weights Matrices ($W$), Encoding Geography as Algebra</h2>
                <p>Before we can model space, we must <em>define</em> space. Who is a neighbour of whom? How much does each neighbour matter? The spatial weights matrix $W$ is an $n \times n$ matrix where entry $w_{ij}$ encodes the geographic relationship between unit $i$ and unit $j$. The diagonal is always zero ($w_{ii} = 0$), no unit is its own neighbour.</p>

                <h3>2.1 How to Define Neighbours</h3>

                <div class="example-box">
                    <div class="example-label">Queen Contiguity, Shared Borders &amp; Corners</div>
                    <p><strong>Analogy:</strong> Think of a chess queen, which can move in all eight directions. Unit $i$ and unit $j$ are neighbours if they share <em>any</em> boundary edge or even just touch at a corner point. This is the most common definition for administrative polygons like wards, LGAs, or counties.</p>
                    <p><strong>Applied use:</strong> Modelling disease spread between administrative health wards, where transmission can occur even where two districts share only a corner point.</p>
                </div>

                <div class="example-box">
                    <div class="example-label">k-Nearest Neighbours (k-NN), Distance-Based</div>
                    <p><strong>Analogy:</strong> Your $k$ nearest neighbours are simply the $k$ locations physically closest to you. Unit $i$ connects to the $k$ geographically nearest units, regardless of shared borders.</p>
                    <p><strong>Applied use:</strong> Point data (individual household survey locations, well positions, farm GPS coordinates) where polygons do not exist.</p>
                </div>

                <div class="example-box">
                    <div class="example-label">Distance-Decay Weights, Continuous Gravity</div>
                    <p><strong>Analogy:</strong> Gravity. The gravitational pull between two planets decreases with distance squared. Similarly, $w_{ij} = d_{ij}^{-\alpha}$ means influence decays as a power function of separation distance $d_{ij}$.</p>
                    <p><strong>Applied use:</strong> Economic market influence, radio signal propagation, agricultural input diffusion, any process where impact fades smoothly with distance.</p>
                </div>

                <h3>2.2 Row Standardisation, Making Comparisons Fair</h3>
                <p>Different units have different numbers of neighbours. A central LGA might share borders with eight others; a peripheral one at the state boundary might have only two. Raw binary weights would make central units dominate simply because they have more neighbours. Row standardisation rescales each row so all weights for unit $i$ sum to exactly 1, producing a weighted average of neighbours.</p>

                <div class="formula-card teal">
                    <div class="formula-title">Row-Standardisation</div>
                    $$w_{ij}^* = \frac{c_{ij}}{\sum_{j=1}^n c_{ij}} \quad \implies \quad \sum_{j=1}^n w_{ij}^* = 1 \quad \forall \; i$$
                </div>

                <h3>2.3 The Spatial Lag, A Neighbourhood Average</h3>
                <p>Multiplying row-standardised $W$ by a variable vector $y$ produces the <strong>spatial lag</strong>: for each unit $i$, the weighted average value of $y$ in its neighbours. If $y$ is malaria incidence, then $[Wy]_i$ is the average malaria incidence in the neighbours of unit $i$. This is the spatial context for every observation.</p>

                <div class="formula-card">
                    <div class="formula-title">Spatial Lag: Neighbourhood Average</div>
                    $$[Wy]_i = \sum_{j=1}^n w_{ij}^* y_j$$
                </div>
            </section>

            <!-- SECTION 3 -->
            <section id="sec3">
                <h2>3. Measuring Spatial Clustering, Is the Pattern Random?</h2>
                <p>Before fitting any spatial model, we need to ask: <em>is there actually a spatial pattern in the data?</em> Two families of statistics answer this: <strong>global</strong> tests (one number summarising the entire map) and <strong>local</strong> tests (a different number for every location, revealing where clusters are).</p>

                <h3>3.1 Global Moran's $I$, Is There Clustering Anywhere?</h3>
                <p>Moran's $I$ is the spatial analogue of a correlation coefficient. It asks: when I pick any unit $i$ and look at its value $y_i$, are its neighbours' values $y_j$ also high? Intuitively: plot each unit's value on the horizontal axis and its spatial lag (neighbourhood average) on the vertical axis. This is the <strong>Moran Scatter Plot</strong>. Moran's $I$ is essentially the slope of that scatter plot.</p>

                <div class="formula-card blue">
                    <div class="formula-title">Global Moran's $I$</div>
                    $$I = \frac{n}{S_0} \cdot \frac{\sum_i \sum_j w_{ij}(y_i - \bar{y})(y_j - \bar{y})}{\sum_i (y_i - \bar{y})^2}, \quad S_0 = \sum_i \sum_j w_{ij}$$
                </div>

                <ul>
                    <li>$I \approx +1$: Perfect positive clustering (high near high, low near low)</li>
                    <li>$I \approx 0$: No spatial pattern, purely random</li>
                    <li>$I \approx -1$: Perfect negative clustering, checkerboard pattern</li>
                </ul>

                <div class="example-box">
                    <div class="example-label">Real-World Example, Stunting Rates Across LGAs</div>
                    <p>A researcher maps child stunting rates across 774 LGAs in Nigeria. Moran's $I = 0.63$, $p &lt; 0.001$. High-stunting LGAs cluster geographically in the northwest, and low-stunting LGAs cluster in the south. Any regression model that ignores this is fundamentally broken.</p>
                </div>

                <h3>3.2 Local Moran's $I_i$ (LISA), <em>Where</em> are the Clusters?</h3>
                <p>LISA (Anselin, 1995) decomposes Global Moran's $I$ into one value per unit. Each unit gets its own $I_i$, measuring how its value correlates with its immediate neighbourhood. Each unit lands in one of four quadrants of the Moran Scatter Plot:</p>

                <div class="formula-card teal">
                    <div class="formula-title">Local Moran's $I_i$</div>
                    $$I_i = \frac{y_i - \bar{y}}{m_2} \sum_j w_{ij}(y_j - \bar{y}), \quad m_2 = \frac{1}{n}\sum_i (y_i - \bar{y})^2$$
                </div>

                <ul>
                    <li><strong>High-High (Hotspot):</strong> Unit $i$ has high value, neighbours also high. Example: a cluster of high-mortality wards in a conflict zone.</li>
                    <li><strong>Low-Low (Coldspot):</strong> Unit $i$ and neighbours both low. Example: a well-served cluster around a well-equipped regional hospital.</li>
                    <li><strong>High-Low (Spatial Outlier):</strong> Unit $i$ is unusually high surrounded by low-value neighbours. Example: an urban ward with high crime surrounded by quiet suburbs.</li>
                    <li><strong>Low-High (Spatial Outlier):</strong> Unit $i$ is unusually low surrounded by high-value neighbours. Example: a well-funded enclave clinic within a deprived region.</li>
                </ul>

                <h3>3.3 Getis-Ord $G_i^*$, Pure Hotspot Detection</h3>
                <p>The Getis-Ord $G_i^*$ statistic is purpose-built for hotspot and coldspot detection. It asks: is the sum of values in a neighbourhood significantly higher or lower than expected by chance? A high positive $z$-score ($> +1.96$) signals a hotspot; a strongly negative $z$-score ($< -1.96$) signals a coldspot. Unlike Local Moran, it does not identify High-Low outliers.</p>

                <div class="example-box">
                    <div class="example-label">Application, Food Insecurity Atlas</div>
                    <p>Using $G_i^*$ on food insecurity scores across sub-Saharan districts, analysts identify a statistically significant coldspot cluster ($z &lt; -2.5$) in the Ethiopian highlands, a region with high agricultural productivity, and a hotspot cluster ($z &gt; 3.1$) across the Sahel belt, guiding emergency food aid allocation.</p>
                </div>
            </section>

            <!-- SECTION 4 -->
            <section id="sec4">
                <h2>4. OLS Regression, How It Works and Why Space Breaks It</h2>
                <p>Ordinary Least Squares (OLS) finds the line that passes as close as possible to all data points, minimising the sum of squared vertical distances from each point to the fitted line. The Gauss-Markov theorem guarantees OLS is the Best Linear Unbiased Estimator (BLUE), under five assumptions. The most important for spatial analysis: residuals must be <em>uncorrelated</em> with each other.</p>

                <div class="formula-card blue">
                    <div class="formula-title">OLS, Closed-Form Estimator</div>
                    $$\hat{\beta} = (X'X)^{-1}X'y$$
                </div>

                <h3>4.1 What Happens When Space Violates This</h3>

                <div class="example-box">
                    <div class="example-label">Problem 1, Spatial Error: Biased Standard Errors</div>
                    <p>All LGAs in the northeast are jointly affected by a drought your model has no variable for. Their residuals are all positive and clustered. OLS treats these as independent errors, so it divides by $n - k$ when it should divide by a much smaller effective number. Result: standard errors are too small, t-statistics too large, and you declare effects as significant that are not.</p>
                    <p>This is like measuring the weight of 50 members of the same sports team, they train together, so their weights are correlated. Treating them as independent samples from the general population gives overconfident estimates.</p>
                </div>

                <div class="example-box">
                    <div class="example-label">Problem 2, Spatial Lag: Biased Coefficients</div>
                    <p>If the outcome in each unit is driven partly by outcomes in neighbouring units, omitting this effect is like omitting a critical predictor. OLS coefficients absorb this omitted spatial feedback and become biased, not just inefficient. Even with infinite data, OLS converges to the wrong answer.</p>
                    <p>A school district builds a new library. Neighbouring districts benefit too (students travel there, resources diffuse). Ignoring this means the coefficient on library investment is underestimated, because OLS attributes only local effects and misses neighbourhood spillovers.</p>
                </div>

                <h3>4.2 OLS Spatial Diagnostic Tests</h3>
                <ul>
                    <li><strong>Moran's I on residuals:</strong> The single most important test. If significant, OLS is invalidated.</li>
                    <li><strong>LM-Lag:</strong> Tests whether a spatial lag of the outcome ($\rho Wy$) should be added. Significant → consider SAR model.</li>
                    <li><strong>LM-Error:</strong> Tests whether the error process is spatially autocorrelated ($\lambda Wu$). Significant → consider SEM model.</li>
                    <li><strong>Robust LM statistics:</strong> When both LM-Lag and LM-Error are significant, Robust LM tests control for each other, pointing to the dominant process.</li>
                </ul>
            </section>

            <!-- SECTION 5 -->
            <section id="sec5">
                <h2>5. Spatial Lag Model (SAR), Modelling Contagion &amp; Peer Effects</h2>

                <h3>5.1 The Core Intuition</h3>
                <p>The SAR model is built for situations where outcomes are directly <strong>caused by outcomes in neighbouring units</strong>. Think of it as a social network effect: my decision about whether to vaccinate my child is influenced by whether my neighbours vaccinated theirs. Crime in one neighbourhood spills into adjacent neighbourhoods as criminals relocate.</p>

                <div class="formula-card blue">
                    <div class="formula-title">SAR Structural Equation</div>
                    $$y = \rho W y + X\beta + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, \sigma^2 I_n), \quad \rho \in (-1, 1)$$
                </div>

                <h3>5.2 The Multiplier Effect</h3>
                <p>Because I am affected by my neighbours, and my neighbours are affected by their neighbours (who may loop back to me), the system creates an infinite series of feedback loops. The total multiplier is $\frac{1}{1 - \rho}$, just like the Keynesian fiscal multiplier in macroeconomics.</p>

                <div class="example-box">
                    <div class="example-label">Real-World Example, Retail Geomarketing</div>
                    <p>A supermarket chain models weekly revenue across 400 store locations. The SAR coefficient $\hat{\rho} = 0.45$. The multiplier is $\frac{1}{1-0.45} = 1.82$. Every ₦1 million in marketing spend at a focal store generates an expected ₦1.82 million in total regional revenue, because elevated foot traffic in one location spills into nearby stores through customer discovery and brand awareness.</p>
                    <p>A naive OLS model would have estimated only the direct ₦1M effect, missing the ₦820,000 in neighbourhood spillovers.</p>
                </div>

                <h3>5.3 Interpreting $\hat{\rho}$</h3>
                <ul>
                    <li>$\hat{\rho} = 0.45$ means: 45% of the outcome in any location is driven by the weighted average outcome of its neighbours, before any predictor effects.</li>
                    <li>Every local intervention is amplified system-wide by the multiplier $\frac{1}{1-\hat{\rho}}$.</li>
                    <li>OLS reports only the direct local effect. SAR adds the entire indirect ripple chain through neighbours. Ignoring SAR when it is present biases all $\hat{\beta}$ estimates because $Wy$ becomes an omitted variable.</li>
                </ul>
            </section>

            <!-- SECTION 6 -->
            <section id="sec6">
                <h2>6. Spatial Error Model (SEM), Modelling Unmeasured Regional Shocks</h2>

                <h3>6.1 The Core Intuition</h3>
                <p>The SEM addresses a different problem. Here, the outcome does <em>not</em> directly cause itself in neighbours. Instead, there are <strong>unobserved forces</strong> that simultaneously affect geographically clustered groups of units, and the model has no variable for those forces. The residuals of the model cluster spatially because the omitted variable is itself spatially clustered.</p>

                <div class="formula-card teal">
                    <div class="formula-title">SEM Specification</div>
                    $$y = X\beta + u, \quad u = \lambda W u + \varepsilon \quad \implies \quad u = (I - \lambda W)^{-1}\varepsilon$$
                </div>

                <div class="example-box">
                    <div class="example-label">Real-World Example, Agricultural Yield Modelling</div>
                    <p>An economist models crop yields across 300 farming districts in West Africa using rainfall, temperature, and fertiliser access. The OLS residuals show Moran's $I = 0.51$, strong clustering remains. The clustered residuals represent shared soil quality gradients and correlated weather patterns not captured by the three predictors.</p>
                    <p>Fitting a SEM with $\hat{\lambda} = 0.48$ corrects the error correlation. The coefficient on fertiliser access grows from $\hat{\beta} = 0.31$ (OLS, underestimated) to $\hat{\beta} = 0.44$ (SEM, correctly estimated), because the inflated standard errors from spatial error correlation had been masking the true precision of the estimate.</p>
                </div>

                <h3>6.2 SAR vs. SEM, The Decision Rule</h3>
                <ul>
                    <li><strong>Is the outcome contagious?</strong> Does high disease in my district actually cause high disease in your district (through shared water sources, migration)? → <strong>SAR</strong></li>
                    <li><strong>Is the outcome driven by shared unobserved forces?</strong> Is disease high in neighbouring districts because they are all affected by the same drought or governance failure, not because of direct contagion? → <strong>SEM</strong></li>
                </ul>
                <p>$\hat{\lambda} = 0.6$ means: 60% of unexplained variation in each unit can be predicted from its neighbours' unexplained variation. OLS standard errors were severely underestimated, all significance tests were inflated.</p>
            </section>

            <!-- SECTION 7 -->
            <section id="sec7">
                <h2>7. Spatial Durbin Model (SDM), The Richer, Safer Specification</h2>

                <h3>7.1 When Both Channels Operate</h3>
                <p>The SDM is the most complete spatial specification. It simultaneously models <strong>outcome spillovers</strong> (like SAR) and <strong>predictor spillovers</strong>, the idea that neighbours' characteristics directly affect the focal unit's outcome. Building a new hospital in District A benefits District A directly, but Districts B, C, and D also benefit as residents cross boundaries to seek care. The SDM captures this by including $WX\gamma$: the spatially lagged predictors.</p>

                <div class="formula-card purple">
                    <div class="formula-title">Spatial Durbin Model</div>
                    $$y = \rho W y + X\beta + W X \gamma + \varepsilon, \quad \rho, \gamma \in (-1, 1)$$
                </div>

                <h3>7.2 Direct, Indirect, and Total Effects</h3>
                <p>In an SDM (or SAR) model, reading $\hat{\beta}$ as the marginal effect is <strong>wrong</strong>. Because outcomes ripple through the network, the true impact has three components:</p>

                <div class="example-box">
                    <div class="example-label">Real-World Example, School Funding Spillovers</div>
                    <p>An SDM of district-level literacy rates with school funding as a key predictor gives:<br>
                    <strong>Direct effect</strong> = 0.42, a 10% increase in school funding in District A directly raises its literacy rate by 4.2 percentage points.<br>
                    <strong>Indirect (spillover) effect</strong> = 0.31, it also raises literacy by 3.1 percentage points in surrounding districts (through teacher mobility, student sharing, demonstration effects).<br>
                    <strong>Total effect</strong> = 0.73 per 10% investment.<br><br>
                    A policymaker who read only $\hat{\beta} = 0.39$ would underestimate the true ROI of education investment by nearly 50%.</p>
                </div>

                <p>LeSage &amp; Pace (2009) proved that SDM produces unbiased coefficient estimates even when relevant spatially correlated variables are omitted, because the $WX\gamma$ term absorbs their influence. This makes SDM the <strong>safest default specification</strong> when uncertain about which spatial process is at work.</p>
            </section>

            <!-- SECTION 8 -->
            <section id="sec8">
                <h2>8. Geographically Weighted Regression (GWR), When Relationships Change Across Space</h2>

                <h3>8.1 The Problem: One Size Does Not Fit All</h3>
                <p>OLS, SAR, SEM, and SDM all assume the relationship between predictors and outcomes is the <strong>same everywhere</strong>. The effect of rainfall on yield may be strong in semi-arid regions and irrelevant in already-humid tropical zones. The effect of distance to clinic on child mortality may be critical in rural areas but negligible in dense urban areas with many competing facilities.</p>
                <p>GWR (Brunsdon, Fotheringham &amp; Charlton, 1996) dissolves this constraint. Instead of one global equation, it fits a <strong>separate local regression at every point in space</strong>. Each observation $i$ gets its own locally estimated coefficients $\hat{\beta}_k(u_i, v_i)$.</p>

                <div class="formula-card purple">
                    <div class="formula-title">GWR Local Equation</div>
                    $$y_i = \beta_0(u_i, v_i) + \sum_{k=1}^p \beta_k(u_i, v_i) x_{ik} + \varepsilon_i$$
                </div>

                <div class="example-box">
                    <div class="example-label">Applied Example, Child Mortality, Nigeria</div>
                    <p>A GWR model of child mortality on clinic access shows:<br>
                    <strong>Rural NE:</strong> $\hat{\beta}_{\text{distance}} = 0.74$, strong, significant ($t = 4.2$). Distance is a life-or-death predictor here.<br>
                    <strong>Urban Lagos:</strong> $\hat{\beta}_{\text{distance}} = 0.09$, non-significant ($t = 1.1$). Substitutes abound; distance barely matters.<br>
                    <strong>Global OLS:</strong> $\hat{\beta} = 0.38$, the average, which accurately describes no specific place.<br><br>
                    The GWR map tells planners exactly <em>where</em> to build new facilities for maximum impact.</p>
                </div>

                <h3>8.2 How to Interpret GWR Output</h3>
                <ul>
                    <li><strong>Parameter map:</strong> Each district coloured by its local $\hat{\beta}_k$, a continuous surface showing strength and direction of the relationship across geography. Blue-to-red diverging palette: blue = strong negative, red = strong positive.</li>
                    <li><strong>Significance masking:</strong> Only show coefficients where $|t| > 1.96$ ($p &lt; 0.05$). Greyed-out areas mean the relationship is not statistically detectable there. Never interpret or act on these areas.</li>
                    <li><strong>Residual Moran's $I$:</strong> After GWR, residuals should show $I \approx 0$, confirming the local model absorbed the spatial structure the global model missed.</li>
                    <li><strong>Sharp colour transitions:</strong> Rapid changes across adjacent districts signal a governance boundary, ecological threshold, or cultural border where the relationship regime changes.</li>
                </ul>

                <h3>8.3 Bandwidth &amp; Kernels</h3>
                <p>The bandwidth $b$ controls how many nearby observations influence each local regression. The optimal bandwidth is chosen by minimising the <strong>Corrected AIC (AICc)</strong>.</p>
                <ul>
                    <li><strong>Adaptive Bisquare (recommended):</strong> Adapts radius to local data density. In Lagos (dense), bandwidth shrinks to capture fine-grained variation. In Bornu (sparse), it expands to borrow information from farther away.</li>
                    <li><strong>Fixed Gaussian:</strong> Same physical radius everywhere. Use when the process itself is fixed-scale (e.g. disease transmission radius = 50km).</li>
                    <li>If optimal $bw^* = 40$ in a 774-LGA study, each local regression uses its 40 nearest neighbours as primary data, a hyper-local scale. If $bw^* = 600$, the process is essentially global.</li>
                </ul>
            </section>

            <!-- SECTION 9 -->
            <section id="sec9">
                <h2>9. Multiscale GWR (MGWR), Different Processes, Different Scales</h2>

                <h3>9.1 The Limitation of Standard GWR</h3>
                <p>Standard GWR forces all predictors to use the <em>same</em> bandwidth. But clinic access varies at the village level while national governance quality varies at the country level. Forcing both to share one bandwidth either over-smooths the local process or under-smooths the regional one. MGWR (Fotheringham, Yang &amp; Kang, 2017) assigns each predictor its own dedicated, separately optimised bandwidth $bw_k$.</p>

                <div class="formula-card purple">
                    <div class="formula-title">MGWR, Variable-Specific Bandwidths</div>
                    $$y_i = \beta_0(u_i, v_i) + \sum_{k=1}^p \beta_{bw_k}(u_i, v_i) x_{ik} + \varepsilon_i$$
                </div>

                <div class="example-box">
                    <div class="example-label">Applied Example, Child Stunting Analysis</div>
                    <p>An MGWR of child stunting across 30 countries reveals:<br>
                    <strong>Open defecation rate:</strong> $bw = 31$ (hyper-local, village sanitation norms change sharply between adjacent communities)<br>
                    <strong>Health facility density:</strong> $bw = 124$ (regional, facility catchments span multiple districts)<br>
                    <strong>Climate variability:</strong> $bw = 820$ (near-global, rainfall patterns are smooth across large zones)<br><br>
                    Standard GWR at $bw = 200$ would have over-smoothed defecation and under-smoothed climate, biasing all three estimates.</p>
                </div>

                <h3>9.2 Reading Bandwidth as a Scientific Finding</h3>
                <ul>
                    <li><strong>Small $bw_k$ (close to 1–20% of $n$):</strong> Predictor $k$ operates at a hyper-local scale. Target interventions at community level.</li>
                    <li><strong>Large $bw_k \approx n$:</strong> Predictor $k$ is essentially global, its coefficient barely changes across the map. Can be represented as a standard OLS term.</li>
                </ul>
                <p>Always compare AICc: if $\text{AICc}_{\text{MGWR}} &lt; \text{AICc}_{\text{GWR}} - 3$, the multi-scale structure is statistically meaningful and MGWR should be reported.</p>
            </section>

            <!-- SECTION 10 -->
            <section id="sec10">
                <h2>10. Spatial Statistics vs. Machine Learning, When to Use Which</h2>
                <p>Machine learning models are optimised for one thing: minimising prediction error on new data. They are powerful at this. But if the goal is to understand <em>why</em> something varies, to estimate the <em>magnitude and significance</em> of a specific effect, machine learning provides no reliable answers. "Feature importance" metrics tell you which variables the model used heavily, but say nothing about the direction of causality, the size of a policy-relevant effect, or whether the relationship is statistically significant.</p>

                <table class="ref-table">
                    <thead>
                        <tr>
                            <th>Dimension</th>
                            <th>Spatial Statistics &amp; GWR</th>
                            <th>Machine Learning (RF / XGBoost)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Primary Goal</strong></td>
                            <td>Causal inference: <em>why</em> does $y$ vary? How large is the effect of $x$?</td>
                            <td>Predictive accuracy: produce the most accurate $\hat{y}$ for new data.</td>
                        </tr>
                        <tr>
                            <td><strong>Coefficient Interpretation</strong></td>
                            <td>Direct marginal effects with confidence intervals, $p$-values, and significance maps.</td>
                            <td>No interpretable coefficients. SHAP values are post-hoc approximations, not causal estimates.</td>
                        </tr>
                        <tr>
                            <td><strong>Spatial Autocorrelation</strong></td>
                            <td>Explicitly modelled via $W$ matrices, spatial structure is a feature, not a problem.</td>
                            <td>Spatial autocorrelation causes catastrophic test-set leakage in standard k-fold cross-validation.</td>
                        </tr>
                        <tr>
                            <td><strong>Policy Transparency</strong></td>
                            <td>Results are fully auditable: every coefficient has a standard error, a $p$-value, and a clear interpretation.</td>
                            <td>Black box: cannot explain to a minister, court, or regulator why the model produced a given output.</td>
                        </tr>
                        <tr>
                            <td><strong>Small Sample Performance</strong></td>
                            <td>Reliable with small-to-medium $n$ (even $n = 50$ LGAs).</td>
                            <td>Needs large datasets; overfits badly on small geographic samples.</td>
                        </tr>
                    </tbody>
                </table>

                <div class="callout teal">
                    <h4>Decision Rule</h4>
                    <p><strong>Use Spatial Statistics / GWR when:</strong> You need to explain a geographic process, estimate the size of a specific effect, design a policy intervention, or publish findings in a peer-reviewed journal. You need coefficients with signs, magnitudes, and uncertainty bounds.</p>
                    <p style="margin-top:8px;"><strong>Use Machine Learning when:</strong> The problem is purely predictive, you need to map a variable everywhere using satellite features, and interpretation is not required. Always pair with spatial block cross-validation to avoid leakage.</p>
                    <p style="margin-top:8px;"><strong>Best practice:</strong> Use both. Fit GWR for structural understanding and hypothesis testing. Use ML for high-resolution prediction. The two approaches are complementary, not competing.</p>
                </div>
            </section>

            <!-- SECTION 11 -->
            <section id="sec11">
                <h2>11. Master Model Specification Reference</h2>
                <table class="ref-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Core Equation</th>
                            <th>The Problem It Solves</th>
                            <th>Real-Life Applied Use Case</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>OLS</strong></td>
                            <td>
    $$y = X\beta + \varepsilon$$
    <div style="margin-top:8px; font-size:0.85em; color:#475569; line-height:1.4;">
        <strong>Where:</strong> $y$ is the outcome vector, $X$ is the design matrix of explanatory variables, $\beta$ is the vector of fixed global coefficients, and $\varepsilon \sim N(0, \sigma^2 I)$ is independent random error noise.
    </div>
</td>
                            <td>Aspatial baseline. Valid only when residual Moran's $I \approx 0$ ($p > 0.05$).</td>
                            <td>Non-geographic data; or geographic data where spatial randomness is confirmed by diagnostics.</td>
                        </tr>
                        <tr>
                            <td><strong>Spatial Lag (SAR)</strong></td>
                            <td>
    $$y = \rho Wy + X\beta + \varepsilon$$
    <div style="margin-top:8px; font-size:0.85em; color:#475569; line-height:1.4;">
        <strong>Where:</strong> $\rho$ (rho) is the spatial autoregressive coefficient measuring direct outcome spillover strength, $W$ is the standardized spatial weight matrix, $Wy$ is the spatial lag of the outcome, $X\beta$ represents direct covariate effects, and $\varepsilon$ is random error.
    </div>
</td>
                            <td>Endogenous peer effects / contagion. Multiplier: $\frac{1}{1-\rho}$.</td>
                            <td>Retail competition; epidemic diffusion; crime displacement; school achievement peer effects.</td>
                        </tr>
                        <tr>
                            <td><strong>Spatial Error (SEM)</strong></td>
                            <td>
    $$y = X\beta + u, \; u = \lambda Wu + \varepsilon$$
    <div style="margin-top:8px; font-size:0.85em; color:#475569; line-height:1.4;">
        <strong>Where:</strong> $X\beta$ captures independent covariate effects, $u$ is spatially correlated structural noise, $\lambda$ (lambda) measures spatial error autoregression strength across neighbours, $W$ is spatial weight matrix, and $\varepsilon$ is spherical random noise.
    </div>
</td>
                            <td>Unobserved regional shocks inflate error correlation and shrink standard errors.</td>
                            <td>Agricultural yields (soil quality), disease rates (shared climate), welfare (governance quality).</td>
                        </tr>
                        <tr>
                            <td><strong>Spatial Durbin (SDM)</strong></td>
                            <td>
    $$y = \rho Wy + X\beta + WX\gamma + \varepsilon$$
    <div style="margin-top:8px; font-size:0.85em; color:#475569; line-height:1.4;">
        <strong>Where:</strong> $\rho Wy$ captures endogenous outcome spillovers, $X\beta$ measures direct local predictor effects, $WX\gamma$ measures exogenous predictor spillovers from neighbouring values, and $\varepsilon$ is random error.
    </div>
</td>
                            <td>Both outcome and predictor spillovers. Safest general specification. Decomposes Direct, Indirect, and Total effects.</td>
                            <td>Hospital/school investment spillovers; infrastructure impact analysis; multi-district policy evaluation.</td>
                        </tr>
                        <tr>
                            <td><strong>GWR</strong></td>
                            <td>
    $$y_i = \beta_0(u_i,v_i) + \sum \beta_k(u_i,v_i) x_{ik} + \varepsilon_i$$
    <div style="margin-top:8px; font-size:0.85em; color:#475569; line-height:1.4;">
        <strong>Where:</strong> $(u_i,v_i)$ are coordinates of location $i$, $\beta_0(u_i,v_i)$ is local intercept, $\beta_k(u_i,v_i)$ are continuous local regression coefficients estimated at point $i$ using spatial kernel weights, and $\varepsilon_i$ is local error.
    </div>
</td>
                            <td>Spatial heterogeneity, relationships differ by location. Produces local coefficient maps.</td>
                            <td>Clinic access effect on mortality (varies urban/rural); fertiliser response by agro-ecology zone.</td>
                        </tr>
                        <tr>
                            <td><strong>MGWR</strong></td>
                            <td>
    $$y_i = \sum_k \beta_{bw_k}(u_i,v_i) x_{ik} + \varepsilon_i$$
    <div style="margin-top:8px; font-size:0.85em; color:#475569; line-height:1.4;">
        <strong>Where:</strong> $bw_k$ is the specific optimal spatial bandwidth selected for predictor $k$, allowing different variables to operate at local, regional, or global spatial scales.
    </div>
</td>
                            <td>Multi-scale heterogeneity, each predictor operates at its own geographic scale.</td>
                            <td>Separating hyper-local sanitation effects ($bw$ = 31) from regional climate effects ($bw \approx n$).</td>
                        </tr>
                    </tbody>
                </table>
            </section>

            <!-- SECTION 12 -->
            <section id="sec12">
                <h2>12. Spatial Statistics Model Selection Protocol, A Step-by-Step Decision Framework</h2>

                <div class="callout blue">
                    <h4>Step 1, Fit OLS and Test for Spatial Problems</h4>
                    <p>Always start with OLS as the baseline. Then compute <strong>Moran's $I$ on the residuals</strong>. If $p \ge 0.05$: residuals are spatially random, OLS is valid, stop here. If $p &lt; 0.05$: OLS is invalidated. Proceed to Step 2.</p>
                </div>

                <div class="callout teal">
                    <h4>Step 2, Lagrange Multiplier Decision Rule</h4>
                    <ul>
                        <li>If <strong>LM-Lag</strong> is significant and LM-Error is not → Fit <strong>Spatial Lag Model (SAR)</strong>. The outcome has a contagion process.</li>
                        <li>If <strong>LM-Error</strong> is significant and LM-Lag is not → Fit <strong>Spatial Error Model (SEM)</strong>. Unobserved spatial shocks are distorting errors.</li>
                        <li>If <strong>both are significant</strong> → Compare Robust LM statistics. If both robust versions are also significant → Fit the <strong>Spatial Durbin Model (SDM)</strong>.</li>
                    </ul>
                </div>

                <div class="callout purple">
                    <h4>Step 3, Test for Spatial Non-Stationarity (GWR)</h4>
                    <p>Estimate GWR with adaptive bisquare kernel. If $\text{AICc}_{\text{GWR}} &lt; \text{AICc}_{\text{Global}} - 3$, local variation is statistically meaningful, the global model is masking important geographic heterogeneity.</p>
                </div>

                <div class="callout amber">
                    <h4>Step 4, Scale Discrimination via MGWR</h4>
                    <p>Run MGWR to establish the operating scale of each predictor. Report per-variable bandwidths. Predictors with $bw \approx n$ can be represented by their global estimates; predictors with small $bw$ require the full spatial flexibility of MGWR.</p>
                </div>

                <div class="example-box">
                    <div class="example-label">Complete Applied Example, Malaria Analysis Protocol</div>
                    <p><strong>Step 1:</strong> OLS of malaria incidence on health facility density, rainfall, and poverty. Moran's $I$ on residuals = 0.38, $p &lt; 0.001$. OLS invalid.</p>
                    <p><strong>Step 2:</strong> LM-Lag = 14.2 ($p &lt; 0.001$), LM-Error = 6.8 ($p &lt; 0.01$). Both significant. Robust LM-Lag = 8.9 ($p &lt; 0.001$), Robust LM-Error = 1.4 ($p = 0.24$). Lag dominates → fit SAR.</p>
                    <p><strong>Step 3:</strong> AICc_SAR = 1,842, AICc_GWR = 1,801. Difference = 41 >> 3. GWR improves substantially. Local heterogeneity confirmed.</p>
                    <p><strong>Step 4:</strong> MGWR shows: rainfall $bw = 18$ (hyper-local), health facility $bw = 142$ (regional), poverty $bw = 489$ (near-global).</p>
                    <p><strong>Conclusion:</strong> MGWR is the correct model. The SAR contagion multiplier $\frac{1}{1-0.31} = 1.45$ means malaria control in one district generates a 45% additional benefit in surrounding districts.</p>
                </div>
            </section>

        </main>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // KaTeX Auto-Render
            if (window.renderMathInElement) {
                renderMathInElement(document.body, {
                    delimiters: [
                        {left: "$$", right: "$$", display: true},
                        {left: "$", right: "$", display: false}
                    ],
                    throwOnError: false
                });
            }

            // Smooth Scroll for TOC
            document.querySelectorAll('.toc-nav a').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    const targetId = this.getAttribute('href');
                    const targetEl = document.querySelector(targetId);
                    if (targetEl) {
                        targetEl.scrollIntoView({ behavior: 'smooth' });
                    }
                });
            });
        });
    </script>
</body>
</html>
"""

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_dir, "docs", "technical_notes.html")
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(TECHNICAL_NOTE_HTML)
        
    print(f"Successfully generated Technical Note at {target_path}")

if __name__ == "__main__":
    main()
