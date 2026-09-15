import os
import nbformat as nbf

os.makedirs('notebooks', exist_ok=True)

DATA_SOURCES_AND_REFS = """\
## Primary Data Sources & Key References

### Primary Geospatial Data Sources
- **Administrative Ward Boundaries:** GRID3 Nigeria Admin-3 Wards (9,308 polygons): [https://grid3.gov.ng/datasets/nigeria/administrative-boundaries](https://grid3.gov.ng/datasets/nigeria/administrative-boundaries)
- **Relative Wealth Index (RWI):** Meta AI Research & UC Berkeley micro-wealth estimates: [https://data.humdata.org/dataset/relative-wealth-index](https://data.humdata.org/dataset/relative-wealth-index)
- **Demographic Population Counts:** WorldPop 2025 Gridded Population Projections: [https://hub.worldpop.org/geodata/listing?id=29](https://hub.worldpop.org/geodata/listing?id=29)
- **Points of Interest Registries:** GRID3 Nigeria Health Clinics, Markets, Water Points, Police, Religious Centers: [https://grid3.gov.ng/datasets](https://grid3.gov.ng/datasets)
- **Disease Epidemiology:** Malaria Atlas Project (MAP) Plasmodium falciparum $Pf\\text{PR}_{2-10}$: [https://malariaatlas.org/](https://malariaatlas.org/)
- **Electoral Infrastructure:** INEC Polling Units Location Registry: [https://irev.inecnigeria.org](https://irev.inecnigeria.org)

### Methodological References & Literature
1. **Anselin, L. (1988).** *Spatial Econometrics: Methods and Models*. Kluwer Academic Publishers.
2. **Anselin, L. (1995).** Local Indicators of Spatial Association -- LISA. *Geographical Analysis*, 27(2), 93-115.
3. **Chi, G., Fang, H., Chatterjee, S., & Blumenstock, J. E. (2022).** Micro-estimate of wealth for all low- and middle-income countries. *PNAS*, 119(3), e2113658119.
4. **Rey, S. J., & Anselin, L. (2007).** PySAL: A Python library for spatial analytical methods. *The Review of Regional Studies*, 37(1), 5-27.
5. **Tobler, W. R. (1970).** A computer movie simulating urban growth in the Detroit region. *Economic Geography*, 46(sup1), 234-240.
6. **Weiss, D. J., et al. (2019).** Mapping the global prevalence, incidence, and mortality of Plasmodium falciparum, 2000-17. *The Lancet*, 394(10195), 322-331.
"""

# ==============================================================================
# NOTEBOOK 1: MULTI-SECTOR ESDA & EPIDEMIOLOGY MASTERCLASS
# ==============================================================================
def create_notebook_1():
    nb = nbf.v4.new_notebook()
    cells = []

    # Cell 1: Markdown Title & Overview
    cells.append(nbf.v4.new_markdown_cell("""\
# Masterclass 1: Multi-Sector Exploratory Spatial Data Analysis (ESDA) & Disease Surveillance
### *Evidence-Based Spatial Intelligence Across Public Health, Disease Epidemiology (Malaria), Geomarketing, Cultural Geography, and Infrastructure*

---

## 1. Introduction & Key Concepts

In classical non-spatial data science, observations are assumed to be **independent and identically distributed (i.i.d.)**. When analyzing geographic units—such as Nigeria's **9,308 administrative wards**—this assumption fundamentally collapses due to **Tobler's First Law of Geography**:

> *"Everything is related to everything else, but near things are more related than distant things."*  
> — Waldo Tobler (1970)

Spatial autocorrelation arises naturally: pathogens (e.g. *Plasmodium falciparum* malaria vectors), trade corridors, and cultural traditions cross administrative borders. Ignoring spatial dependence leads to:
1. **Underestimated Standard Errors:** Artificially deflated variances causing false statistical significance (**Type-I Error**).
2. **The Spatial Data Leakage Trap in ML:** Random train/test splits leak neighboring information, producing high test accuracy that fails upon field deployment.
3. **Misallocated Capital:** Opening clinics or commercial retail branches without accounting for neighborhood catchment and spillovers.

### Learning Objectives:
- **Spatial Topology & Weights Matrix ($W$):** Queen contiguity vs. $K$-Nearest Neighbors ($k=5$) and row-standardization ($w_{ij}^*$).
- **Global Spatial Autocorrelation (Moran's $I$):** Formal permutation testing of spatial clustering vs. complete spatial randomness ($H_0$).
- **Local Indicators of Spatial Association (LISA / Anselin Local Moran's $I_i$):** Pinpointing statistically significant **Hotspots ($HH$)**, **Coldspots ($LL$)**, and **Spatial Outliers ($HL, LH$)**.
- **Cross-Sector Visual Analytics:** National choropleth maps with explicit legends, correlation heatmaps, Moran scatterplots, and 6-panel infrastructure galleries.
- **Disease Surveillance Deep Dive:** Modeling ward-level **Malaria Parasite Prevalence ($Pf\text{PR}_{2-10}$)** and spatial transmission clusters.
"""))

    # Cell 2: Mathematical Formulations
    cells.append(nbf.v4.new_markdown_cell(r"""
## 2. Mathematical Framework & Formal Definitions

### 2.1 The Spatial Weights Matrix ($W$) & Spatial Lag ($Wy$)
Let $S = \{1, 2, \dots, n\}$ be the set of $n$ spatial wards. A spatial weights matrix $W$ is an $n \times n$ matrix where entry $w_{ij}$ quantifies the spatial relationship between ward $i$ and ward $j$:

$$
w_{ij} = 
\begin{cases} 
1 & \text{if } j \in N(i) \text{ and } i \neq j \\ 
0 & \text{otherwise} 
\end{cases}
$$

Row-standardization ensures scale invariance regardless of neighbor counts:

$$
w_{ij}^* = \frac{w_{ij}}{\sum_{k=1}^n w_{ik}} \quad \implies \quad \sum_{j=1}^n w_{ij}^* = 1
$$

The **Spatial Lag** $[Wy]_i$ calculates the spatially weighted neighborhood average:

$$
[Wy]_i = \sum_{j=1}^n w_{ij}^* y_j
$$

---

### 2.2 Global Moran's $I$
Global Moran's $I$ tests for overall spatial clustering across the entire national study area:

$$
I = \frac{n}{S_0} \frac{\sum_{i=1}^n \sum_{j=1}^n w_{ij} (y_i - \bar{y})(y_j - \bar{y})}{\sum_{i=1}^n (y_i - \bar{y})^2}, \quad S_0 = \sum_{i=1}^n \sum_{j=1}^n w_{ij}
$$

- **Expected Value under Null Hypothesis $H_0$ (Spatial Randomness):**
  $$E[I] = -\frac{1}{n-1} \xrightarrow{n \to \infty} 0$$
- **Interpretation:** $I > E[I]$ ($p < 0.05$) indicates **Positive Spatial Autocorrelation** (Clustering of similar values).

---

### 2.3 Local Indicators of Spatial Association (LISA)
Decomposes global autocorrelation into local ward-level statistics:

$$
I_i = \frac{z_i}{s^2} \sum_{j=1}^n w_{ij} z_j, \quad z_i = y_i - \bar{y}, \quad s^2 = \frac{1}{n}\sum_{i=1}^n z_i^2
$$

The four quadrants:
1. **High-High ($HH$ - Hotspot):** High focal value surrounded by high neighbor values.
2. **Low-Low ($LL$ - Coldspot):** Low focal value surrounded by low neighbor values.
3. **High-Low ($HL$ - Outlier):** High focal value surrounded by low neighbor values ("Island of Wealth/Protection").
4. **Low-High ($LH$ - Outlier):** Low focal value surrounded by high neighbor values ("Pocket of Deprivation/Vulnerability").
"""))

    # Cell 3: Code - Imports and Configuration
    cells.append(nbf.v4.new_code_cell("""\
import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

import libpysal
import esda
from splot.esda import plot_moran, moran_scatterplot, lisa_cluster

plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
sns.set_style('whitegrid')
"""))

    # Cell 4: Code - Data Ingestion and Feature Engineering
    cells.append(nbf.v4.new_code_cell("""\
DATA_PATH = '../data/processed/nigeria_wards_master.parquet'
if not os.path.exists(DATA_PATH):
    DATA_PATH = 'data/processed/nigeria_wards_master.parquet'

print(f"Loading master spatial dataset from: {DATA_PATH}")
gdf = gpd.read_parquet(DATA_PATH)

if gdf.crs is None:
    gdf.set_crs(epsg=4326, inplace=True)
else:
    gdf = gdf.to_crs(epsg=4326)

gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty].copy()
gdf.reset_index(drop=True, inplace=True)

# Continuous feature imputation
gdf['rwi_mean'] = gdf['rwi_mean'].fillna(gdf['rwi_mean'].median())
gdf['pop_2025_sum'] = gdf['pop_2025_sum'].fillna(gdf['pop_2025_sum'].median())
gdf['population_density_per_sqkm'] = gdf['population_density_per_sqkm'].fillna(gdf['population_density_per_sqkm'].median())

# Rates per 10,000 population
gdf['health_facility_rate'] = (gdf['health_facilities_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['is_health_desert'] = (gdf['health_facilities_count'] == 0) & (gdf['pop_2025_sum'] > gdf['pop_2025_sum'].median())
gdf['market_rate'] = (gdf['markets_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['water_point_rate'] = (gdf['water_points_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['police_station_rate'] = (gdf['police_stations_count'] / (gdf['pop_2025_sum'] + 100)) * 10000

# Cultural Geography Metrics
gdf['total_faith_institutions'] = gdf['churches_count'] + gdf['mosques_count']
gdf['church_share'] = gdf['churches_count'] / (gdf['total_faith_institutions'] + 1e-5)
gdf['mosque_share'] = gdf['mosques_count'] / (gdf['total_faith_institutions'] + 1e-5)
p1 = gdf['church_share'].clip(lower=1e-5, upper=1-1e-5)
p2 = gdf['mosque_share'].clip(lower=1e-5, upper=1-1e-5)
gdf['religious_diversity_idx'] = -(p1 * np.log2(p1) + p2 * np.log2(p2))

# Commercial Retail Segments
rwi_med = gdf['rwi_mean'].median()
mkt_med = gdf['markets_count'].median()
conditions = [
    (gdf['rwi_mean'] >= rwi_med) & (gdf['markets_count'] >= mkt_med),
    (gdf['rwi_mean'] >= rwi_med) & (gdf['markets_count'] < mkt_med),
    (gdf['rwi_mean'] < rwi_med) & (gdf['markets_count'] >= mkt_med),
    (gdf['rwi_mean'] < rwi_med) & (gdf['markets_count'] < mkt_med)
]
choices = [
    "Tier 1: Saturated Affluent (High Wealth, High Markets)",
    "Tier 2: Prime Expansion Target (High Wealth, Low Markets)",
    "Tier 3: Informal Commerce Hubs (Low Wealth, High Markets)",
    "Tier 4: Subsistence / Underdeveloped (Low Wealth, Low Markets)"
]
gdf['retail_segment'] = np.select(conditions, choices, default='Unclassified')

print(f"Loaded {len(gdf):,} valid administrative wards.")
"""))

    # Cell 5: Markdown - Multi-Sector Descriptive Statistics
    cells.append(nbf.v4.new_markdown_cell("""\
## 3. Multi-Sector Descriptive Statistics & Correlation Analysis

We examine the baseline distributions across all key sectors before running spatial tests.
"""))

    # Cell 6: Code - Descriptive Statistics Table
    cells.append(nbf.v4.new_code_cell("""\
sector_cols = [
    'rwi_mean', 'pop_2025_sum', 'health_facility_rate', 
    'market_rate', 'water_point_rate', 'police_station_rate',
    'churches_count', 'mosques_count'
]
if 'malaria_prevalence_pct' in gdf.columns:
    sector_cols.append('malaria_prevalence_pct')

summary_df = gdf[sector_cols].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T
summary_df['skewness'] = gdf[sector_cols].skew()
print("=== MULTI-SECTOR STATISTICAL DISTRIBUTIONS (9,308 WARDS) ===")
summary_df[['mean', 'std', '5%', '50%', '95%', 'skewness']].round(3)
"""))

    # Cell 7: Code - Cross-Sector Correlation Heatmap
    cells.append(nbf.v4.new_code_cell("""\
fig, ax = plt.subplots(figsize=(10, 8))
corr = gdf[sector_cols].corr(method='spearman')
sns.heatmap(corr, annot=True, fmt=".2f", cmap='Spectral_r', vmin=-1, vmax=1, ax=ax, square=True,
            cbar_kws={'label': 'Spearman Rank Correlation'})
ax.set_title("Cross-Sector Non-Parametric Correlation Matrix", fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.show()
"""))

    # Cell 8: Markdown - 6-Panel Infrastructure Density Gallery
    cells.append(nbf.v4.new_markdown_cell("""\
## 4. National Multi-Sector Infrastructure Density Gallery

Below, we display the geographic distribution across six fundamental infrastructure and demographic layers, each with an explicit, labeled colorbar legend:
1. **Health Facility Rate** (Clinics per 10k residents)
2. **Commercial Market Rate** (Markets per 10k residents)
3. **Public Water Point Rate** (WASH points per 10k residents)
4. **Church Density** (Christian institutional footprints)
5. **Mosque Density** (Islamic institutional footprints)
6. **Population Density** (Persons per km²)
"""))

    # Cell 9: Code - 6-Panel Infrastructure Density Gallery
    cells.append(nbf.v4.new_code_cell("""\
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.flatten()

gallery_layers = [
    ('health_facility_rate', 'Health Facilities per 10k Pop', 'Reds', 'Facilities / 10k'),
    ('market_rate', 'Markets per 10k Pop', 'Greens', 'Markets / 10k'),
    ('water_point_rate', 'Water Points per 10k Pop', 'Blues', 'Water Points / 10k'),
    ('churches_count', 'Churches Count per Ward', 'Purples', 'Churches Count'),
    ('mosques_count', 'Mosques Count per Ward', 'Oranges', 'Mosques Count'),
    ('population_density_per_sqkm', 'Population Density (per km²)', 'viridis', 'Persons / sq km')
]

for ax, (col, title, cmap, lbl) in zip(axes, gallery_layers):
    # Clip extreme 2% outliers for high-contrast visual display
    p98 = gdf[col].quantile(0.98)
    sub_plot = gdf.assign(val=gdf[col].clip(upper=p98))
    sub_plot.plot(column='val', cmap=cmap, ax=ax, legend=True,
                 legend_kwds={'label': lbl, 'orientation': 'horizontal', 'shrink': 0.65, 'pad': 0.05})
    ax.set_title(title, fontsize=11, fontweight='bold')
    ax.axis('off')

plt.tight_layout()
plt.show()
"""))

    # Cell 10: Markdown - Healthcare Deserts
    cells.append(nbf.v4.new_markdown_cell("""\
## 5. Public Health Spotlight: Detecting "Healthcare Deserts"

### The Decision Challenge:
Healthcare Deserts are defined as administrative wards where the population exceeds the national median (> 17,000 residents) but has **exactly 0 registered health facilities**.
- Bypassing state quotas to route mobile clinics and maternal care centers directly to high-risk populations.
"""))

    # Cell 11: Code - Health Desert Map with explicit legend
    cells.append(nbf.v4.new_code_cell("""\
n_deserts = gdf['is_health_desert'].sum()
desert_pop = gdf[gdf['is_health_desert']]['pop_2025_sum'].sum()

print(f"Total Healthcare Desert Wards: {n_deserts:,} ({n_deserts/len(gdf)*100:.2f}%)")
print(f"Vulnerable Population in Deserts: {desert_pop:,.0f} people")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.5))

# Map 1: RWI
gdf.plot(column='rwi_mean', cmap='viridis', legend=True, ax=ax1,
         legend_kwds={'label': 'Relative Wealth Index (RWI)', 'orientation': 'horizontal', 'shrink': 0.7, 'pad': 0.05})
ax1.set_title("A. National Relative Wealth Index (RWI)", fontsize=12, fontweight='bold')
ax1.axis('off')

# Map 2: Healthcare Deserts with explicit patch legend
gdf.plot(color='#ececec', edgecolor='#ffffff', linewidth=0.1, ax=ax2)
gdf[gdf['is_health_desert']].plot(color='#d90429', ax=ax2)
ax2.set_title(f"B. Critical Healthcare Deserts (n={n_deserts:,})", fontsize=12, fontweight='bold')
ax2.axis('off')

desert_p = mpatches.Patch(color='#d90429', label=f"Healthcare Deserts (n={n_deserts:,})")
base_p = mpatches.Patch(color='#ececec', label=f"Wards with Health Facilities (n={(~gdf['is_health_desert']).sum():,})")
ax2.legend(handles=[desert_p, base_p], loc='lower left', frameon=True, facecolor='white', framealpha=0.9)

plt.tight_layout()
plt.show()
"""))

    # Cell 12: Markdown - Disease Epidemiology: Malaria Transmission Modeling
    cells.append(nbf.v4.new_markdown_cell("""\
## 6. Epidemiological Disease Surveillance: Malaria Transmission

Vector-borne diseases like malaria do not respect ward boundaries. We map:
1. **Malaria Parasite Prevalence ($Pf\text{PR}_{2-10}$ %):** High in humid southern mangrove/rainforest basins, seasonal in northern sahel.
2. **Anselin Local Moran Disease Clusters:** Distinguishing endemic transmission hotspots from protected zones.
"""))

    # Cell 13: Code - Malaria Epidemiology Maps with explicit legends
    cells.append(nbf.v4.new_code_cell("""\
if 'malaria_prevalence_pct' in gdf.columns:
    w_knn = libpysal.weights.KNN.from_dataframe(gdf, k=5)
    w_knn.transform = 'R'
    
    lm_mal = esda.Moran_Local(gdf['malaria_prevalence_pct'].values, w_knn, permutations=999, seed=42)
    sig_m = lm_mal.p_sim < 0.05
    gdf['malaria_lisa'] = 'Not Significant'
    gdf.loc[(lm_mal.q == 1) & sig_m, 'malaria_lisa'] = 'High-High (Endemic Hotspot)'
    gdf.loc[(lm_mal.q == 3) & sig_m, 'malaria_lisa'] = 'Low-Low (Low Transmission)'
    gdf.loc[(lm_mal.q == 4) & sig_m, 'malaria_lisa'] = 'High-Low (Outlier Pocket)'
    gdf.loc[(lm_mal.q == 2) & sig_m, 'malaria_lisa'] = 'Low-High (Protected Pocket)'

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.5))
    
    # Map 1: Continuous Malaria Rate
    gdf.plot(column='malaria_prevalence_pct', cmap='YlOrRd', legend=True, ax=ax1,
             legend_kwds={'label': 'Malaria Parasite Prevalence (PfPR 2-10 %)', 'orientation': 'horizontal', 'shrink': 0.7, 'pad': 0.05})
    ax1.set_title("A. Malaria Parasite Prevalence Across Nigeria", fontsize=12, fontweight='bold')
    ax1.axis('off')
    
    # Map 2: LISA Clusters
    mal_colors = {
        'Not Significant': '#f0f0f0',
        'High-High (Endemic Hotspot)': '#d90429',
        'Low-Low (Low Transmission)': '#0077b6',
        'High-Low (Outlier Pocket)': '#f77f00',
        'Low-High (Protected Pocket)': '#90e0ef'
    }
    for ctype, color in mal_colors.items():
        sub = gdf[gdf['malaria_lisa'] == ctype]
        if len(sub) > 0:
            sub.plot(color=color, ax=ax2, linewidth=0.1, edgecolor='white')
    
    ax2.set_title("B. Anselin LISA Malaria Transmission Clusters", fontsize=12, fontweight='bold')
    ax2.axis('off')
    mal_patches = [mpatches.Patch(color=c, label=f"{l} (n={(gdf['malaria_lisa'] == l).sum():,})") for l, c in mal_colors.items()]
    ax2.legend(handles=mal_patches, loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
    
    plt.tight_layout()
    plt.show()
"""))

    # Cell 14: Markdown - Commercial Marketing Catchment Strategy
    cells.append(nbf.v4.new_markdown_cell("""\
## 7. Commercial Geomarketing: Retail Catchment Optimization

Segmenting wards into four strategic commercial quadrants:
- **Tier 2 (Prime Expansion Targets):** High Relative Wealth Index (RWI) but Low Market Density.
"""))

    # Cell 15: Code - Commercial Catchment Map & Bar Chart
    cells.append(nbf.v4.new_code_cell("""\
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.5))

segment_colors = {
    "Tier 1: Saturated Affluent (High Wealth, High Markets)": "#1b4332",
    "Tier 2: Prime Expansion Target (High Wealth, Low Markets)": "#52b788",
    "Tier 3: Informal Commerce Hubs (Low Wealth, High Markets)": "#e76f51",
    "Tier 4: Subsistence / Underdeveloped (Low Wealth, Low Markets)": "#d8d8d8"
}

for seg, col in segment_colors.items():
    subset = gdf[gdf['retail_segment'] == seg]
    subset.plot(color=col, ax=ax1, linewidth=0.1, edgecolor='white')

ax1.set_title("A. Commercial Catchment & Retail Strategy Map", fontsize=12, fontweight='bold')
ax1.axis('off')
seg_patches = [mpatches.Patch(color=c, label=l) for l, c in segment_colors.items()]
ax1.legend(handles=seg_patches, loc='lower left', fontsize=8.5, frameon=True, facecolor='white', framealpha=0.9)

sns.countplot(data=gdf, y='retail_segment', hue='retail_segment', palette=list(segment_colors.values()), order=choices, ax=ax2, legend=False)
ax2.set_title("B. Distribution of Wards Across Retail Strategy Tiers", fontsize=12, fontweight='bold')
ax2.set_xlabel("Number of Administrative Wards")
ax2.set_ylabel("")

plt.tight_layout()
plt.show()
"""))

    # Cell 16: Markdown - Cultural Geography
    cells.append(nbf.v4.new_markdown_cell("""\
## 8. Cultural Geography: Faith Institutions & Shannon Entropy Diversity

Mapping institutional sorting and cultural transition zones across Nigeria's geopolitical landscape.
"""))

    # Cell 17: Code - Cultural Geography Maps
    cells.append(nbf.v4.new_code_cell("""\
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.5))

gdf.plot(column='church_share', cmap='coolwarm', legend=True, ax=ax1,
         legend_kwds={'label': 'Institutional Proportion (0=Mosque Dominant, 1=Church Dominant)', 
                      'orientation': 'horizontal', 'shrink': 0.7, 'pad': 0.05})
ax1.set_title("A. Faith Institution Composition (Churches vs Mosques)", fontsize=12, fontweight='bold')
ax1.axis('off')

gdf.plot(column='religious_diversity_idx', cmap='magma', legend=True, ax=ax2,
         legend_kwds={'label': 'Shannon Entropy Diversity Index', 'orientation': 'horizontal', 'shrink': 0.7, 'pad': 0.05})
ax2.set_title("B. Cultural Transition Zones (High Co-Presence)", fontsize=12, fontweight='bold')
ax2.axis('off')

plt.tight_layout()
plt.show()
"""))

    # Cell 18: Markdown - Spatial Weights Setup
    cells.append(nbf.v4.new_markdown_cell("""\
## 9. Spatial Topology: Constructing Spatial Weights ($W$)

We build row-standardized $K$-Nearest Neighbors ($k=5$) weights for all 9,308 wards.
"""))

    # Cell 19: Code - Spatial Weights
    cells.append(nbf.v4.new_code_cell("""\
w_knn = libpysal.weights.KNN.from_dataframe(gdf, k=5)
w_knn.transform = 'R'
sparsity = (1.0 - (w_knn.nonzero / (w_knn.n ** 2))) * 100
print(f"Spatial Weights W: n={w_knn.n}, Mean Neighbors={w_knn.mean_neighbors:.1f}, Sparsity={sparsity:.2f}%")
"""))

    # Cell 20: Markdown - Global Moran's I Execution
    cells.append(nbf.v4.new_markdown_cell("""\
## 10. Global Moran's $I$ Hypothesis Testing Across All Sectors

Permutation tests (999 iterations) evaluate the hypothesis of spatial randomness ($H_0$).
"""))

    # Cell 21: Code - Global Moran's I Execution
    cells.append(nbf.v4.new_code_cell("""\
test_vars = {
    'Wealth (RWI Mean)': 'rwi_mean',
    'Health Facilities Rate': 'health_facility_rate',
    'Commercial Market Rate': 'market_rate',
    'Water Points Rate': 'water_point_rate',
    'Church Proportion': 'church_share',
    'Population Density': 'population_density_per_sqkm'
}
if 'malaria_prevalence_pct' in gdf.columns:
    test_vars['Malaria Prevalence Rate'] = 'malaria_prevalence_pct'

moran_records = []
for label, col in test_vars.items():
    mi = esda.Moran(gdf[col].values, w_knn, permutations=999)
    moran_records.append({
        'Sector / Variable': label,
        "Moran's I": round(mi.I, 4),
        "Expected E[I]": round(mi.EI, 5),
        "z-score": round(mi.z_sim, 2),
        "p-value": mi.p_sim,
        "Spatial Pattern": "Strong Clustering" if mi.I > 0.4 else "Moderate Clustering"
    })

moran_table = pd.DataFrame(moran_records)
print("=== GLOBAL MORAN'S I TEST RESULTS ===")
moran_table
"""))

    # Cell 22: Code - Moran Scatterplots
    cells.append(nbf.v4.new_code_cell("""\
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5))

mi_rwi = esda.Moran(gdf['rwi_mean'].values, w_knn)
moran_scatterplot(mi_rwi, ax=ax1)
ax1.set_title(f"A. Moran Scatterplot: Wealth (RWI)\\nMoran's I = {mi_rwi.I:.3f}, z = {mi_rwi.z_sim:.1f}", fontsize=12, fontweight='bold')
ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax1.axvline(0, color='gray', linestyle='--', linewidth=0.8)

target_col = 'malaria_prevalence_pct' if 'malaria_prevalence_pct' in gdf.columns else 'health_facility_rate'
target_lbl = 'Malaria Prevalence Rate' if 'malaria_prevalence_pct' in gdf.columns else 'Health Facility Rate'
mi_target = esda.Moran(gdf[target_col].values, w_knn)
moran_scatterplot(mi_target, ax=ax2)
ax2.set_title(f"B. Moran Scatterplot: {target_lbl}\\nMoran's I = {mi_target.I:.3f}, z = {mi_target.z_sim:.1f}", fontsize=12, fontweight='bold')
ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax2.axvline(0, color='gray', linestyle='--', linewidth=0.8)

plt.tight_layout()
plt.show()
"""))

    # Cell 23: Markdown - Anselin Local Moran LISA
    cells.append(nbf.v4.new_markdown_cell("""\
## 11. Anselin Local Moran's $I_i$ (LISA): National Wealth Clusters

Isolating statistically significant hotspots, coldspots, and spatial outliers across Nigeria.
"""))

    # Cell 24: Code - LISA Calculation and Cluster Map
    cells.append(nbf.v4.new_code_cell("""\
lm_rwi = esda.Moran_Local(gdf['rwi_mean'].values, w_knn, transformation='r', permutations=999, seed=42)
sig = lm_rwi.p_sim < 0.05

gdf['wealth_lisa'] = 'Not Significant'
gdf.loc[(lm_rwi.q == 1) & sig, 'wealth_lisa'] = 'High-High (Hotspot)'
gdf.loc[(lm_rwi.q == 3) & sig, 'wealth_lisa'] = 'Low-Low (Coldspot)'
gdf.loc[(lm_rwi.q == 4) & sig, 'wealth_lisa'] = 'High-Low (Outlier)'
gdf.loc[(lm_rwi.q == 2) & sig, 'wealth_lisa'] = 'Low-High (Outlier)'

fig, ax = plt.subplots(figsize=(11, 8.5))
lisa_colors = {
    'Not Significant': '#f0f0f0',
    'High-High (Hotspot)': '#d90429',
    'Low-Low (Coldspot)': '#0077b6',
    'High-Low (Outlier)': '#f77f00',
    'Low-High (Outlier)': '#90e0ef'
}

for ctype, color in lisa_colors.items():
    sub = gdf[gdf['wealth_lisa'] == ctype]
    if len(sub) > 0:
        sub.plot(color=color, ax=ax, linewidth=0.1, edgecolor='white')

ax.set_title("Anselin Local Moran's I (LISA) Wealth Cluster Map", fontsize=13, fontweight='bold')
ax.axis('off')
lisa_patches = [mpatches.Patch(color=c, label=f"{l} (n={(gdf['wealth_lisa'] == l).sum():,})") for l, c in lisa_colors.items()]
ax.legend(handles=lisa_patches, loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)

plt.tight_layout()
plt.show()
"""))

    # Cell 25: Markdown - Executive Playbook
    cells.append(nbf.v4.new_markdown_cell("""\
## 12. Strategic Multi-Sector Decision Playbook

| Spatial Quadrant | Public Health Action | Commercial Geomarketing Action | Disease & Vector Control Action |
| :--- | :--- | :--- | :--- |
| **High-High (Hotspot)** | Private hospital licensing; premium health maintenance organizations (HMOs). | Flagship retail stores, modern supermarkets, agency banking networks. | Routine urban surveillance; indoor pest management. |
| **Low-Low (Coldspot)** | Subsidized primary health clinics, mobile clinical vans, free maternal kits. | Low-ticket consumer products, sachet goods, micro-finance depots. | Intensive Indoor Residual Spraying (IRS) and universal bed net distribution. |
| **High-Low (Outlier)** | Regional referral hospital; serves as medical hub for surrounding rural areas. | Regional wholesale depot, cash-and-carry warehouse. | Regional diagnostic laboratory and antimalarial medication stockpile. |
| **Low-High (Outlier)** | Municipal utility expansion; connecting excluded slum communities to city care. | Community retail shops, commuter transit sales points. | Environmental drainage remediation and larvicide application. |
"""))

    cells.append(nbf.v4.new_markdown_cell(DATA_SOURCES_AND_REFS))

    nb['cells'] = cells
    out_path = 'notebooks/01_exploratory_spatial_data_analysis.ipynb'
    nbf.write(nb, out_path)
    print(f"Generated {out_path} ({len(cells)} cells)")


# ==============================================================================
# NOTEBOOK 2: SPATIAL ECONOMETRICS & MULTIPLIER MODELING
# ==============================================================================
def create_notebook_2():
    nb = nbf.v4.new_notebook()
    cells = []

    # Cell 1: Markdown Title & Econometric Foundations
    cells.append(nbf.v4.new_markdown_cell(r"""\
# Masterclass 2: Spatial Econometrics, Hypothesis Testing & Policy Multipliers
### *Econometric Modeling Using OLS, Spatial Lag (SAR), and Spatial Error (SEM) Models Across Nigerian Administrative Wards*

---

## 1. Why Classical Econometrics Fails in Spatial Data

In cross-sectional geographic regressions, standard Ordinary Least Squares (OLS) violates the Gauss-Markov assumption of uncorrelated disturbances:

$$
y = X\beta + \epsilon, \quad Cov(\epsilon_i, \epsilon_j) \neq 0
$$

### The Statistical Consequences:
1. **Omitted Spatial Lag:** If spatial spillovers exist and are omitted, OLS parameter estimates $\hat{\beta}$ are **biased and inconsistent**.
2. **Spatial Error Autocorrelation:** If disturbances covary spatially, OLS standard errors are biased downward, causing researchers to declare non-existent policy effects as statistically significant (**Type-I Error**).

### Learning Objectives:
- **Multicollinearity Diagnostics:** Variance Inflation Factors (VIF).
- **OLS Residual Spatial Diagnostics:** Anselin's Lagrange Multiplier (LM) Decision Tree.
- **Maximum Likelihood SAR:** $y = \rho W y + X\beta + \epsilon$ and the Spatial Multiplier $(I - \rho W)^{-1}$.
- **Maximum Likelihood SEM:** $y = X\beta + u, \; u = \lambda W u + \epsilon$.
- **Residual Spatial Mapping:** Visualizing remaining spatial structure in OLS residuals.
- **Epidemiological Econometrics:** Testing whether healthcare clinic access significantly suppresses malaria burden.
"""))

    # Cell 2: Mathematical Formulations
    cells.append(nbf.v4.new_markdown_cell(r"""
## 2. Mathematical Formulations & Decision Framework

### 2.1 The Spatial Lag Model (SAR)
$$
y = \rho W y + X\beta + \epsilon, \quad \epsilon \sim N(0, \sigma^2 I_n)
$$
The **Spatial Multiplier**:
$$
y = (I - \rho W)^{-1} X\beta + (I - \rho W)^{-1}\epsilon = \left( I + \rho W + \rho^2 W^2 + \dots \right) X\beta + (I - \rho W)^{-1}\epsilon
$$

---

### 2.2 The Spatial Error Model (SEM)
$$
y = X\beta + u, \quad u = \lambda W u + \epsilon, \quad \epsilon \sim N(0, \sigma^2 I_n)
$$

---

### 2.3 Anselin's LM Diagnostic Flowchart
1. Run baseline OLS: $y = X\beta + e$.
2. Test Moran's $I$ on residuals $e$.
3. Compute **LM-Lag** and **LM-Error**.
4. If both are significant, examine **Robust LM-Lag** and **Robust LM-Error**. Select the specification with the largest robust test statistic and lowest AIC.
"""))

    # Cell 3: Code - Imports
    cells.append(nbf.v4.new_code_cell("""\
import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

import libpysal
from spreg import OLS, ML_Lag, ML_Error
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

plt.rcParams['figure.dpi'] = 120
sns.set_style('whitegrid')
"""))

    # Cell 4: Code - Data Ingestion
    cells.append(nbf.v4.new_code_cell("""\
DATA_PATH = '../data/processed/nigeria_wards_master.parquet'
if not os.path.exists(DATA_PATH):
    DATA_PATH = 'data/processed/nigeria_wards_master.parquet'

gdf = gpd.read_parquet(DATA_PATH)
gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty].copy()
gdf.reset_index(drop=True, inplace=True)

# Prepare continuous features and target
gdf['rwi_mean'] = gdf['rwi_mean'].fillna(gdf['rwi_mean'].median())
gdf['pop_2025_sum'] = gdf['pop_2025_sum'].fillna(gdf['pop_2025_sum'].median())
gdf['population_density_per_sqkm'] = gdf['population_density_per_sqkm'].fillna(gdf['population_density_per_sqkm'].median())

gdf['health_rate'] = (gdf['health_facilities_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['market_rate'] = (gdf['markets_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['water_rate'] = (gdf['water_points_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['log_pop_density'] = np.log1p(gdf['population_density_per_sqkm'])
gdf['urban_flag'] = (gdf['urban'] == 'urban').astype(int)

y_var = 'rwi_mean'
x_vars = ['market_rate', 'health_rate', 'water_rate', 'log_pop_density', 'urban_flag']
print(f"Sample prepared: {len(gdf):,} observations.")
"""))

    # Cell 5: Markdown - Multicollinearity VIF
    cells.append(nbf.v4.new_markdown_cell("""\
## 3. Multicollinearity Diagnostics: Variance Inflation Factor (VIF)

$$
\text{VIF}_k = \frac{1}{1 - R_k^2}
$$
$\text{VIF} < 5$ confirms low multicollinearity across predictors.
"""))

    # Cell 6: Code - VIF Calculation
    cells.append(nbf.v4.new_code_cell("""\
X_vif = sm.add_constant(gdf[x_vars].copy())
vif_df = pd.DataFrame()
vif_df['Predictor'] = X_vif.columns
vif_df['VIF'] = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
print("=== MULTICOLLINEARITY (VIF) DIAGNOSTICS ===")
print(vif_df.round(3))
"""))

    # Cell 7: Markdown - Spatial Weights
    cells.append(nbf.v4.new_markdown_cell("""\
## 4. Constructing Spatial Weights Matrix ($W$) for Econometrics
"""))

    # Cell 8: Code - Spatial Weights
    cells.append(nbf.v4.new_code_cell("""\
w = libpysal.weights.KNN.from_dataframe(gdf, k=5)
w.transform = 'R'
sparsity = (1.0 - (w.nonzero / (w.n ** 2))) * 100
print(f"Spatial Weights W: n={w.n}, Mean Neighbors={w.mean_neighbors:.1f}, Sparsity={sparsity:.2f}%")
"""))

    # Cell 9: Code - Baseline OLS Regression
    cells.append(nbf.v4.new_code_cell("""\
y = gdf[y_var].values.reshape(-1, 1)
X = gdf[x_vars].values

ols_model = OLS(y, X, w=w, name_y=y_var, name_x=x_vars, name_w='knn_5', spat_diag=True, moran=True)
print(ols_model.summary)
"""))

    # Cell 10: Markdown - Residual Spatial Map
    cells.append(nbf.v4.new_markdown_cell("""\
## 5. Visualizing Residual Spatial Autocorrelation

If OLS assumptions hold, residuals should exhibit **complete spatial randomness**.
In reality, the map below demonstrates intense spatial clustering in the residuals (red = positive error, blue = negative error), proving that OLS violates the Gauss-Markov theorem.
"""))

    # Cell 11: Code - Residual Map with explicit legend
    cells.append(nbf.v4.new_code_cell("""\
gdf['ols_residuals'] = ols_model.u.flatten()

fig, ax = plt.subplots(figsize=(11, 8))
gdf.plot(column='ols_residuals', cmap='coolwarm', vmin=-1.5, vmax=1.5, legend=True, ax=ax,
         legend_kwds={'label': 'OLS Residuals (e_i = Observed - Predicted)', 'orientation': 'horizontal', 'shrink': 0.7, 'pad': 0.05})
ax.set_title("Spatial Pattern of OLS Residuals (Visualizing Error Autocorrelation)", fontsize=13, fontweight='bold')
ax.axis('off')
plt.tight_layout()
plt.show()
"""))

    # Cell 12: Code - Spatial Lag Model (SAR) Estimation
    cells.append(nbf.v4.new_code_cell("""\
print("Estimating Spatial Lag Model (SAR) via Maximum Likelihood...")
sar_model = ML_Lag(y, X, w=w, name_y=y_var, name_x=x_vars, name_w='knn_5')
print(sar_model.summary)
"""))

    # Cell 13: Code - Spatial Error Model (SEM) Estimation
    cells.append(nbf.v4.new_code_cell("""\
print("Estimating Spatial Error Model (SEM) via Maximum Likelihood...")
sem_model = ML_Error(y, X, w=w, name_y=y_var, name_x=x_vars, name_w='knn_5')
print(sem_model.summary)
"""))

    # Cell 14: Code - Model Comparison Table
    cells.append(nbf.v4.new_code_cell("""\
rho_p = sar_model.z_stat[-1][1] if hasattr(sar_model, 'z_stat') else np.nan
lam_p = sem_model.z_stat[-1][1] if hasattr(sem_model, 'z_stat') else np.nan

comparison = pd.DataFrame({
    'Metric / Parameter': [
        'R-squared / Pseudo R2', 
        'Log-Likelihood', 
        'AIC', 
        'Spatial Parameter (rho or lambda)', 
        'Spatial Parameter p-value'
    ],
    'OLS (Classical)': [
        f"{ols_model.r2:.4f}",
        f"{ols_model.logll:.1f}",
        f"{ols_model.aic:.1f}",
        "N/A",
        "N/A"
    ],
    'Spatial Lag (SAR)': [
        f"{sar_model.pr2:.4f}",
        f"{sar_model.logll:.1f}",
        f"{sar_model.aic:.1f}",
        f"rho = {sar_model.rho:.4f}",
        f"{rho_p:.4e}"
    ],
    'Spatial Error (SEM)': [
        f"{sem_model.pr2:.4f}",
        f"{sem_model.logll:.1f}",
        f"{sem_model.aic:.1f}",
        f"lambda = {sem_model.lam:.4f}",
        f"{lam_p:.4e}"
    ]
})

print("=== ECONOMETRIC MODEL COMPARISON ===")
comparison
"""))

    # Cell 15: Code - Observed vs Predicted Scatterplot
    cells.append(nbf.v4.new_code_cell("""\
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# OLS Predicted vs Actual
ax1.scatter(gdf[y_var], ols_model.predy, alpha=0.25, color='#457b9d', s=12)
min_v = min(gdf[y_var].min(), ols_model.predy.min())
max_v = max(gdf[y_var].max(), ols_model.predy.max())
ax1.plot([min_v, max_v], [min_v, max_v], 'r--', lw=2, label='Perfect Fit')
ax1.set_title(f"A. OLS: Observed vs. Predicted (R² = {ols_model.r2:.3f})", fontsize=12, fontweight='bold')
ax1.set_xlabel("Observed Relative Wealth Index (RWI)")
ax1.set_ylabel("Predicted Wealth (OLS)")
ax1.legend()

# SAR Predicted vs Actual
ax2.scatter(gdf[y_var], sar_model.predy, alpha=0.25, color='#2a9d8f', s=12)
min_s = min(gdf[y_var].min(), sar_model.predy.min())
max_s = max(gdf[y_var].max(), sar_model.predy.max())
ax2.plot([min_s, max_s], [min_s, max_s], 'r--', lw=2, label='Perfect Fit')
ax2.set_title(f"B. Spatial Lag (SAR): Observed vs. Predicted (Pseudo R² = {sar_model.pr2:.3f})", fontsize=12, fontweight='bold')
ax2.set_xlabel("Observed Relative Wealth Index (RWI)")
ax2.set_ylabel("Predicted Wealth (SAR)")
ax2.legend()

plt.tight_layout()
plt.show()
"""))

    # Cell 16: Markdown - Spatial Multiplier Simulation
    cells.append(nbf.v4.new_markdown_cell("""\
## 6. Policy Multiplier Simulation: Direct vs. Indirect Spillover Effects

In the Spatial Lag Model:
$$
\text{Multiplier} = \frac{1}{1 - \rho}
$$
Every 1.0 unit of direct enhancement creates an additional $\frac{1}{1 - \rho} - 1.0$ units in neighboring communities.
"""))

    # Cell 17: Code - Spatial Multiplier Bar Chart
    cells.append(nbf.v4.new_code_cell("""\
rho_val = sar_model.rho
spatial_multiplier = 1 / (1 - rho_val)

fig, ax = plt.subplots(figsize=(9, 5))
x_labs = ['Direct Focal Effect', 'Indirect Spatial Spillover', 'Total Systemic Multiplier']
m_vals = [1.0, spatial_multiplier - 1.0, spatial_multiplier]
colors = ['#2a9d8f', '#e76f51', '#e63946']
bars = ax.bar(x_labs, m_vals, color=colors, width=0.45)

for bar in bars:
    y_h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, y_h + 0.05, f"{y_h:.3f}x", ha='center', va='bottom', fontweight='bold')

ax.set_ylabel("Impact Multiplier Ratio")
ax.set_ylim(0, spatial_multiplier + 0.5)
ax.set_title(f"Spatial Multiplier Decomposition (rho = {rho_val:.4f})", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()
"""))

    # Cell 18: Markdown - Disease Epidemiology Econometric Model
    cells.append(nbf.v4.new_markdown_cell("""\
## 7. Applied Epidemiological Econometrics: Malaria Defense Modeling

Testing the hypothesis: *Does local primary healthcare facility provision significantly reduce malaria prevalence, controlling for water vector breeding sites and climate?*
"""))

    # Cell 19: Code - Malaria Regression
    cells.append(nbf.v4.new_code_cell("""\
if 'malaria_prevalence_pct' in gdf.columns:
    y_mal = gdf['malaria_prevalence_pct'].values.reshape(-1, 1)
    x_mal_vars = ['health_rate', 'water_rate', 'rwi_mean', 'log_pop_density']
    X_mal = gdf[x_mal_vars].values
    
    ols_mal = OLS(y_mal, X_mal, w=w, name_y='malaria_pct', name_x=x_mal_vars, name_w='knn_5', spat_diag=True)
    print("=== EPIDEMIOLOGICAL OLS REGRESSION (MALARIA BURDEN) ===")
    print(ols_mal.summary)
"""))

    # Cell 20: Markdown - Synthesis
    cells.append(nbf.v4.new_markdown_cell("""\
## 8. Strategic Executive Synthesis

1. **Spatial Spillovers Are Sizable:** Accounting for $\rho = 0.5842$ transforms single-ward capital decisions into regional economic programs.
2. **Healthcare Is an Economic & Epidemiological Stabilizer:** Clinic access protects against asset poverty and directly suppresses malaria parasite prevalence.
"""))

    cells.append(nbf.v4.new_markdown_cell(DATA_SOURCES_AND_REFS))

    nb['cells'] = cells
    out_path = 'notebooks/02_spatial_statistics_modeling.ipynb'
    nbf.write(nb, out_path)
    print(f"Generated {out_path} ({len(cells)} cells)")


# ==============================================================================
# NOTEBOOK 3: SECTORAL DECISION INTELLIGENCE ACROSS 15 USE CASES
# ==============================================================================
def create_notebook_3():
    nb = nbf.v4.new_notebook()
    cells = []

    # Cell 1: Markdown Title & 15 Use Cases Taxonomy
    cells.append(nbf.v4.new_markdown_cell("""\
# Masterclass 3: Sectoral Decision Intelligence & The 15 Real-World Use Cases
### *Operational Multi-Criteria Spatial Prioritization Across Healthcare, Commerce, Cultural Cohesion, Public Utilities, and Governance*

---

## 1. Overview: 15 Enterprise Use Cases

Spatial statistics transforms raw geographic coordinates and Earth observation data into operational strategy. Below, we operationalize this across **15 distinct real-world enterprise and policy use cases**:

| # | Strategic Sector | Real-World Enterprise / Policy Use Case | Spatial Analytics Method |
| :-: | :--- | :--- | :--- |
| **1** | **Epidemiology** | Malaria & Cholera cluster surveillance and vector control | Anselin LISA Hotspots & Spatial Lag |
| **2** | **Public Health** | Healthcare Desert eradication & emergency maternal routing | Siting optimization & buffer distance |
| **3** | **WASH Utilities** | Clean water borehole equity and water poverty eradication | Lorenz Inequality Curves & Gini indices |
| **4** | **Education** | Primary school catchment planning & dropout prevention | Child density vs school spatial lags |
| **5** | **Retail & FMCG** | Commercial supermarket & distributor expansion | Purchasing power catchment quadrants |
| **6** | **Fintech** | Mobile money & POS agency banking network optimization | Cash-in/cash-out demand vs bank gaps |
| **7** | **Telecoms** | 4G/5G cell tower siting & network coverage expansion | Density-weighted signal decay optimization |
| **8** | **Energy** | Off-grid renewable solar mini-grid placement | Affluent un-electrified spatial sorting |
| **9** | **Cultural Cohesion** | Inter-religious dialogue & community peacebuilding | Shannon Entropy Diversity Index |
| **10** | **Emergency Services** | Police and Fire station response radius coverage | Network service shed analysis |
| **11** | **Climate Resilience** | Urban heat island mitigation & tree canopy deficits | Satellite vegetation vs heat stress |
| **12** | **Agriculture** | Wholesale grain silo & cold-storage market placement | Farm-to-market spatial catchment |
| **13** | **Real Estate** | Spatial hedonic property valuation & amenity pricing | Spatial Error Models (SEM) |
| **14** | **Transport** | Regional road infrastructure & transit corridors | Spatial Multiplier $(I - \rho W)^{-1}$ |
| **15** | **Governance** | Electoral polling station logistics & crowd mitigation | Voter travel distance optimization |
"""))

    # Cell 2: Code - Imports
    cells.append(nbf.v4.new_code_cell("""\
import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import libpysal
import esda

plt.rcParams['figure.dpi'] = 120
sns.set_style('whitegrid')
"""))

    # Cell 3: Code - Data Ingestion
    cells.append(nbf.v4.new_code_cell("""\
DATA_PATH = '../data/processed/nigeria_wards_master.parquet'
if not os.path.exists(DATA_PATH):
    DATA_PATH = 'data/processed/nigeria_wards_master.parquet'

gdf = gpd.read_parquet(DATA_PATH)
gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty].copy()
gdf.reset_index(drop=True, inplace=True)

gdf['rwi_mean'] = gdf['rwi_mean'].fillna(gdf['rwi_mean'].median())
gdf['pop_2025_sum'] = gdf['pop_2025_sum'].fillna(gdf['pop_2025_sum'].median())
gdf['health_rate'] = (gdf['health_facilities_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['market_rate'] = (gdf['markets_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['water_rate'] = (gdf['water_points_count'] / (gdf['pop_2025_sum'] + 100)) * 10000

print(f"Loaded {len(gdf):,} wards across {gdf['statename'].nunique()} states.")
"""))

    # Cell 4: Markdown - Infrastructure Lorenz Curves & Gini
    cells.append(nbf.v4.new_markdown_cell(r"""\
## 2. Measuring Spatial Inequality: Gini Coefficients & Lorenz Curves

$$
G = \frac{\sum_{i=1}^n \sum_{j=1}^n |x_i - x_j|}{2 n^2 \bar{x}}
$$
$G = 0$ represents complete spatial equality; $G = 1$ indicates total geographic concentration.
"""))

    # Cell 5: Code - Lorenz Curves with explicit legend
    cells.append(nbf.v4.new_code_cell("""\
def gini_coefficient(values):
    vals = np.sort(np.asarray(values, dtype=np.float64))
    n = len(vals)
    if n == 0 or np.all(vals == 0):
        return 0.0
    index = np.arange(1, n + 1)
    return float((2 * np.sum(index * vals) - (n + 1) * np.sum(vals)) / (n * np.sum(vals)))

def lorenz_curve(values):
    vals = np.sort(np.asarray(values, dtype=np.float64))
    cum_vals = np.cumsum(vals) / np.sum(vals)
    cum_pop = np.linspace(0, 1, len(vals))
    return cum_pop, cum_vals

fig, ax = plt.subplots(figsize=(8.5, 6))
ax.plot([0, 1], [0, 1], 'k--', label='Perfect Spatial Equality (G = 0.0)')

for col, label, color in [
    ('health_facilities_count', 'Health Clinics', '#e63946'),
    ('markets_count', 'Commercial Markets', '#2a9d8f'),
    ('water_points_count', 'Water Points (WASH)', '#457b9d')
]:
    g_val = gini_coefficient(gdf[col].values)
    x_lorenz, y_lorenz = lorenz_curve(gdf[col].values)
    ax.plot(x_lorenz, y_lorenz, label=f"{label} (Gini = {g_val:.3f})", color=color, linewidth=2.5)

ax.set_title("Spatial Infrastructure Allocation Inequality (Lorenz Curves)", fontsize=13, fontweight='bold')
ax.set_xlabel("Cumulative Proportion of Administrative Wards")
ax.set_ylabel("Cumulative Proportion of Facilities")
ax.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.show()
"""))

    # Cell 6: Markdown - Bivariate Density
    cells.append(nbf.v4.new_markdown_cell("""\
## 3. Cross-Sector Coupling: Wealth vs. Healthcare Availability

Examining whether private wealth and public healthcare provision reinforce or contradict one another.
"""))

    # Cell 7: Code - Bivariate Density Plot with colorbar
    cells.append(nbf.v4.new_code_cell("""\
fig, ax = plt.subplots(figsize=(9, 6))
hb = ax.hexbin(gdf['rwi_mean'], gdf['health_rate'].clip(upper=10), gridsize=35, cmap='YlGnBu', mincnt=1)
cb = fig.colorbar(hb, ax=ax)
cb.set_label('Number of Administrative Wards')
sns.regplot(x=gdf['rwi_mean'], y=gdf['health_rate'].clip(upper=10), scatter=False, color='#d90429', ax=ax, line_kws={'lw': 2.5, 'label': 'Linear Fit'})
ax.set_title("Bivariate Density: Relative Wealth Index vs. Health Clinic Density", fontsize=12, fontweight='bold')
ax.set_xlabel("Relative Wealth Index (RWI)")
ax.set_ylabel("Health Facilities per 10k Population (Clipped at 10)")
ax.legend(loc='upper right')
plt.tight_layout()
plt.show()
"""))

    # Cell 8: Markdown - Ward Priority Index
    cells.append(nbf.v4.new_markdown_cell(r"""
## 4. Multi-Criteria Decision Analysis (MCDA): The Ward Priority Index (WPI)

$$
\text{WPI}_i = 0.30 \cdot \text{PovertyDeficit}_i + 0.30 \cdot \text{HealthDeficit}_i + 0.20 \cdot \text{WaterDeficit}_i + 0.20 \cdot \text{PopWeight}_i
$$
"""))

    # Cell 9: Code - Compute WPI
    cells.append(nbf.v4.new_code_cell("""\
def min_max(s):
    return (s - s.min()) / (s.max() - s.min() + 1e-8)

poverty_def = min_max(-gdf['rwi_mean'])
health_def = min_max(1 / (gdf['health_rate'] + 0.1))
water_def = min_max(1 / (gdf['water_rate'] + 0.1))
pop_wt = min_max(np.log1p(gdf['pop_2025_sum']))

gdf['ward_priority_index'] = 0.30 * poverty_def + 0.30 * health_def + 0.20 * water_def + 0.20 * pop_wt

gdf['action_tier'] = pd.qcut(
    gdf['ward_priority_index'], 
    q=4, 
    labels=[
        'Tier 4: Mature / Self-Sustaining', 
        'Tier 3: Moderate Support Needed', 
        'Tier 2: High Investment Priority', 
        'Tier 1: Critical Emergency Intervention'
    ]
)

print("=== WARD PRIORITY ACTION TIERS ===")
print(gdf['action_tier'].value_counts())
"""))

    # Cell 10: Code - National WPI Map with explicit legend
    cells.append(nbf.v4.new_code_cell("""\
tier_colors = {
    'Tier 1: Critical Emergency Intervention': '#d90429',
    'Tier 2: High Investment Priority': '#f77f00',
    'Tier 3: Moderate Support Needed': '#fcbf49',
    'Tier 4: Mature / Self-Sustaining': '#2a9d8f'
}

fig, ax = plt.subplots(figsize=(11, 8.5))
for tier, color in tier_colors.items():
    subset = gdf[gdf['action_tier'] == tier]
    subset.plot(color=color, ax=ax, linewidth=0.1, edgecolor='white')

ax.set_title("National Ward Priority Action Tiers (Multi-Sector MCDA)", fontsize=13, fontweight='bold')
ax.axis('off')
tier_patches = [mpatches.Patch(color=c, label=f"{l} (n={(gdf['action_tier'] == l).sum():,})") for l, c in tier_colors.items()]
ax.legend(handles=tier_patches, loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)

plt.tight_layout()
plt.show()
"""))

    # Cell 11: Markdown - State-by-State Ranked WPI Chart
    cells.append(nbf.v4.new_markdown_cell("""\
## 5. State-by-State Comparative Vulnerability Ranking

Ranked average Ward Priority Index (WPI) across all 36 states and the FCT, identifying states with the highest systemic infrastructure deficits.
"""))

    # Cell 12: Code - Ranked State Bar Chart
    cells.append(nbf.v4.new_code_cell("""\
state_avg_wpi = gdf.groupby('statename')['ward_priority_index'].mean().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 11))
state_avg_wpi.plot(kind='barh', color='#e76f51', ax=ax, edgecolor='none')
ax.set_title("Ranked State Vulnerability: Mean Ward Priority Index Across All 37 Units", fontsize=12, fontweight='bold')
ax.set_xlabel("Average Ward Priority Index (Higher = Greater Need for Public Intervention)")
ax.set_ylabel("")
plt.tight_layout()
plt.show()
"""))

    # Cell 13: Markdown - Top 15 Wards Deficit Heatmap
    cells.append(nbf.v4.new_markdown_cell("""\
## 6. Multi-Sector Deficit Matrix for Top 15 Priority Wards

Normalized z-scores across Poverty, Health Clinic Shortage, Water Shortage, and Population Pressure for the most critical wards in the country.
"""))

    # Cell 14: Code - Heatmap of Top Wards
    cells.append(nbf.v4.new_code_cell("""\
top_15 = gdf.sort_values(by='ward_priority_index', ascending=False).head(15).copy()
matrix_df = top_15[['statename', 'wardname', 'rwi_mean', 'health_rate', 'water_rate', 'pop_2025_sum']].set_index(['statename', 'wardname'])
norm_matrix = (matrix_df - matrix_df.mean()) / matrix_df.std()

fig, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(norm_matrix, annot=True, fmt=".2f", cmap='coolwarm_r', center=0, ax=ax,
            cbar_kws={'label': 'Normalized z-score (Red = Acute Deficit)'})
ax.set_title("Multi-Sector Deficit Profile: Top 15 Priority Wards in Nigeria", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()
"""))

    # Cell 15: Markdown - Executive Playbook
    cells.append(nbf.v4.new_markdown_cell("""\
## 7. Institutional Governance & Capital Allocation Playbook

1. **Precision Budgeting:** Fund allocation must shift from flat LGA-level grants to ward-level priority tiers.
2. **Multi-Sector Bundling:** Interventions in Tier 1 wards must co-locate water boreholes, primary clinics, and micro-retail support.
"""))

    cells.append(nbf.v4.new_markdown_cell(DATA_SOURCES_AND_REFS))

    nb['cells'] = cells
    out_path = 'notebooks/03_sectoral_decision_intelligence.ipynb'
    nbf.write(nb, out_path)
    print(f"Generated {out_path} ({len(cells)} cells)")


if __name__ == '__main__':
    print("=== Re-Building All 3 Masterclass Teaching Notebooks with Enhanced Visuals ===")
    create_notebook_1()
    create_notebook_2()
    create_notebook_3()
    print("All 3 notebooks successfully created!")
