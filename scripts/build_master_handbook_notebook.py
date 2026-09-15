import os
import nbformat as nbf

os.makedirs('notebooks', exist_ok=True)
nb = nbf.v4.new_notebook()
cells = []

# Cell 1: Hero Markdown
cells.append(nbf.v4.new_markdown_cell("""\
# Multi-Sector Spatial Statistics & Econometric Decision Intelligence
### *An Interactive Master Handbook Across Nigeria's 9,308 Administrative Wards*

---

## 1. Executive Roadmap & Decision Science Framework

In public policy planning and corporate strategy across developing nations, decision-makers have historically relied on aggregate, aspatial indicators (e.g. national averages, state-wide gross allocations). However, spatial phenomena—ranging from disease epidemiology and maternal mortality to commercial retail catchment and clean water access—exhibit intense localized geographic clustering and cross-boundary spatial spillovers.

This master handbook synthesizes advanced geospatial analytics and spatial econometrics across **9,308 administrative wards in Nigeria**, unifying:
- **Meta Relative Wealth Index (RWI):** Micro-targeted asset poverty and wealth estimates.
- **WorldPop Demographic Projections:** High-resolution gridded population distributions.
- **GRID3 Infrastructure Registries:** Health facilities, commercial markets, churches, mosques, public water points, and police stations.

### Core Sectors Analyzed:
1. **Public Health & Healthcare Deserts:** Identifying wards with high population concentration and zero primary health facilities.
2. **Commercial Marketing & Retail Catchment:** Pinpointing high-wealth, market-sparse wards as prime commercial retail targets.
3. **Cultural & Religious Geography:** Measuring spatial institutional sorting and Shannon Entropy diversity across geopolitical transition zones.
4. **Public Utilities (WASH):** Diagnosing structural spatial inequality in clean water point access using Lorenz Curves and Gini coefficients.
5. **Spatial Econometrics & Multiplier Effects:** Quantifying direct vs. indirect spatial multiplier spillovers $(I - \rho W)^{-1}$.
"""))

# Cell 2: Imports & Environment
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
import esda
from spreg import OLS, ML_Lag, ML_Error

# Visual settings
plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
sns.set_style('whitegrid')
"""))

# Cell 3: Data Ingestion & Enrichment
cells.append(nbf.v4.new_code_cell("""\
DATA_PATH = '../data/processed/nigeria_wards_master.parquet'
if not os.path.exists(DATA_PATH):
    DATA_PATH = 'data/processed/nigeria_wards_master.parquet'

print(f"Loading master spatial dataset: {DATA_PATH}")
gdf = gpd.read_parquet(DATA_PATH)

if gdf.crs is None:
    gdf.set_crs(epsg=4326, inplace=True)
else:
    gdf = gdf.to_crs(epsg=4326)

gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty].copy()
gdf.reset_index(drop=True, inplace=True)

# Feature Engineering
gdf['rwi_mean'] = gdf['rwi_mean'].fillna(gdf['rwi_mean'].median())
gdf['pop_2025_sum'] = gdf['pop_2025_sum'].fillna(gdf['pop_2025_sum'].median())
gdf['population_density_per_sqkm'] = gdf['population_density_per_sqkm'].fillna(gdf['population_density_per_sqkm'].median())

gdf['health_rate'] = (gdf['health_facilities_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['is_health_desert'] = (gdf['health_facilities_count'] == 0) & (gdf['pop_2025_sum'] > gdf['pop_2025_sum'].median())

gdf['market_rate'] = (gdf['markets_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['water_rate'] = (gdf['water_points_count'] / (gdf['pop_2025_sum'] + 100)) * 10000

# Cultural Geography
gdf['total_faith'] = gdf['churches_count'] + gdf['mosques_count']
gdf['church_share'] = gdf['churches_count'] / (gdf['total_faith'] + 1e-5)
gdf['mosque_share'] = gdf['mosques_count'] / (gdf['total_faith'] + 1e-5)
p1 = gdf['church_share'].clip(lower=1e-5, upper=1-1e-5)
p2 = gdf['mosque_share'].clip(lower=1e-5, upper=1-1e-5)
gdf['religious_diversity_idx'] = -(p1 * np.log2(p1) + p2 * np.log2(p2))

# Commercial Segmentation
rwi_med = gdf['rwi_mean'].median()
mkt_med = gdf['markets_count'].median()
conditions = [
    (gdf['rwi_mean'] >= rwi_med) & (gdf['markets_count'] >= mkt_med),
    (gdf['rwi_mean'] >= rwi_med) & (gdf['markets_count'] < mkt_med),
    (gdf['rwi_mean'] < rwi_med) & (gdf['markets_count'] >= mkt_med),
    (gdf['rwi_mean'] < rwi_med) & (gdf['markets_count'] < mkt_med)
]
choices = [
    "Tier 1: Saturated Affluent",
    "Tier 2: Prime Retail Target",
    "Tier 3: Informal Commerce Hubs",
    "Tier 4: Subsistence Wards"
]
gdf['retail_segment'] = np.select(conditions, choices, default='Unclassified')

print(f"Master dataset successfully prepared: {len(gdf):,} wards across {gdf['statename'].nunique()} states.")
"""))

# Cell 4: Markdown - Multi-Sector Visual Dashboard
cells.append(nbf.v4.new_markdown_cell("""\
## 2. Multi-Sector National Spatial Dashboard

Below, we display the comparative spatial distributions across four strategic dimensions:
1. **Wealth Distribution (RWI):** Demonstrating the stark macro-geographic economic divide.
2. **Healthcare Deserts:** Highlighting acute health infrastructure deficits in high-population wards.
3. **Commercial Strategy Segments:** Mapping expansion targets for commercial retail and agency banking.
4. **Religious Diversity Index:** Identifying cultural transition corridors in the Middle Belt.
"""))

# Cell 5: Code - Multi-Sector Dashboard Plot
cells.append(nbf.v4.new_code_cell("""\
fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# 1. RWI Map
gdf.plot(column='rwi_mean', cmap='viridis', legend=True, ax=axes[0, 0],
         legend_kwds={'label': "Relative Wealth Index", 'orientation': "horizontal", 'shrink': 0.6, 'pad': 0.05})
axes[0, 0].set_title("A. Wealth Distribution (RWI Mean)", fontsize=12, fontweight='bold')
axes[0, 0].axis('off')

# 2. Healthcare Deserts
gdf.plot(color='#eeeeee', edgecolor='#ffffff', linewidth=0.1, ax=axes[0, 1])
gdf[gdf['is_health_desert']].plot(color='#d90429', ax=axes[0, 1])
axes[0, 1].set_title(f"B. Critical Healthcare Deserts (n={gdf['is_health_desert'].sum():,})", fontsize=12, fontweight='bold')
axes[0, 1].axis('off')

# 3. Commercial Strategy
cat_colors = {'Tier 1: Saturated Affluent': '#1b4332', 'Tier 2: Prime Retail Target': '#52b788', 
              'Tier 3: Informal Commerce Hubs': '#e76f51', 'Tier 4: Subsistence Wards': '#d8d8d8'}
for cat, col in cat_colors.items():
    sub = gdf[gdf['retail_segment'] == cat]
    sub.plot(color=col, ax=axes[1, 0], linewidth=0.1, edgecolor='white')
axes[1, 0].set_title("C. Commercial Retail Catchment Segments", fontsize=12, fontweight='bold')
axes[1, 0].axis('off')

# 4. Religious Diversity
gdf.plot(column='religious_diversity_idx', cmap='magma', legend=True, ax=axes[1, 1],
         legend_kwds={'label': "Shannon Entropy Index", 'orientation': "horizontal", 'shrink': 0.6, 'pad': 0.05})
axes[1, 1].set_title("D. Cultural Diversity & Transition Zones", fontsize=12, fontweight='bold')
axes[1, 1].axis('off')

plt.tight_layout()
plt.show()
"""))

# Cell 6: Markdown - Interactive State & LGA Query Tool
cells.append(nbf.v4.new_markdown_cell("""\
## 3. Executive Decision Drilldown: State & LGA Spatial Inspector

Use the inspection function below to query any state in Nigeria to instantly retrieve summary statistics, total population living in healthcare deserts, retail expansion wards, and cultural diversity metrics.
"""))

# Cell 7: Code - Query Tool
cells.append(nbf.v4.new_code_cell("""\
def inspect_state_profile(state_name):
    sub = gdf[gdf['statename'].str.lower() == state_name.lower()].copy()
    if len(sub) == 0:
        print(f"State '{state_name}' not found. Available states: {sorted(gdf['statename'].unique())}")
        return
    
    total_pop = sub['pop_2025_sum'].sum()
    n_deserts = sub['is_health_desert'].sum()
    desert_pop = sub[sub['is_health_desert']]['pop_2025_sum'].sum()
    prime_retail_wards = (sub['retail_segment'] == 'Tier 2: Prime Retail Target').sum()
    avg_rwi = sub['rwi_mean'].mean()
    
    print(f"=== STRATEGIC EXECUTIVE PROFILE: {state_name.upper()} STATE ===")
    print(f"Total Wards: {len(sub):,} | Total Projected Population: {total_pop:,.0f}")
    print(f"Mean Relative Wealth Index (RWI): {avg_rwi:.3f}")
    print(f"Healthcare Desert Wards: {n_deserts:,} (Affecting {desert_pop:,.0f} residents)")
    print(f"Prime Commercial Retail Target Wards: {prime_retail_wards:,}")
    print("-----------------------------------------------------------------")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sub.plot(column='rwi_mean', cmap='viridis', legend=True, ax=ax,
             legend_kwds={'label': 'Relative Wealth Index (RWI)'})
    ax.set_title(f"{state_name.title()} State: Ward Wealth Distribution", fontsize=12, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.show()

# Example: Inspect Kano and Lagos States
inspect_state_profile('Kano')
inspect_state_profile('Lagos')
"""))

# Cell 8: Markdown - Econometrics & Policy Multipliers
cells.append(nbf.v4.new_markdown_cell(r"""
## 4. Spatial Econometrics & The Spatial Multiplier

In our spatial econometric regressions (detailed in Masterclass 2), we estimated the **Spatial Lag Model (SAR)**:

$$
y = \rho W y + X\beta + \epsilon \quad \implies \quad y = (I - \rho W)^{-1} X\beta + (I - \rho W)^{-1}\epsilon
$$

Our empirical findings across all 9,308 wards revealed:
- **Spatial Autoregressive Coefficient:** $\rho = 0.5842$ ($p < 0.0001$).
- **Calculated Spatial Multiplier:**
  $$\text{Multiplier} = \frac{1}{1 - \rho} \approx \frac{1}{1 - 0.5842} \approx 2.405$$

### The Strategic Policy Rule:
For every **1.0 unit of direct economic enhancement** generated in a focal ward (e.g. through a new central market or primary health clinic), an additional **1.405 units of wealth** are generated in contiguous neighboring wards via trade, labor, and service diffusion.
"""))

# Cell 9: Markdown - Multi-Criteria Ward Priority Index (WPI)
cells.append(nbf.v4.new_markdown_cell("""\
## 5. Multi-Criteria Ward Priority Index (WPI) Engine

Decision-makers can adjust sectoral weights to compute customized priority rosters for any state.
"""))

# Cell 10: Code - Custom WPI Calculator
cells.append(nbf.v4.new_code_cell("""\
def compute_custom_ward_priority(state_name, w_poverty=0.35, w_health=0.35, w_water=0.15, w_pop=0.15, top_n=5):
    sub = gdf[gdf['statename'].str.lower() == state_name.lower()].copy()
    if len(sub) == 0:
        return None
    
    def min_max(s):
        return (s - s.min()) / (s.max() - s.min() + 1e-8)
    
    poverty_def = min_max(-sub['rwi_mean'])
    health_def = min_max(1 / (sub['health_rate'] + 0.1))
    water_def = min_max(1 / (sub['water_rate'] + 0.1))
    pop_wt = min_max(np.log1p(sub['pop_2025_sum']))
    
    sub['custom_wpi'] = (
        w_poverty * poverty_def + 
        w_health * health_def + 
        w_water * water_def + 
        w_pop * pop_wt
    )
    
    top_wards = sub.sort_values(by='custom_wpi', ascending=False).head(top_n)
    return top_wards[['statename', 'lganame', 'wardname', 'custom_wpi', 'rwi_mean', 'pop_2025_sum', 'health_facilities_count', 'water_points_count']]

# Run for Rivers and Plateau States
print("=== TOP 5 PRIORITY INTERVENTION WARDS: RIVERS STATE ===")
display_cols = compute_custom_ward_priority('Rivers', top_n=5)
print(display_cols.round(3))

print("\\n=== TOP 5 PRIORITY INTERVENTION WARDS: PLATEAU STATE ===")
display_cols2 = compute_custom_ward_priority('Plateau', top_n=5)
print(display_cols2.round(3))
"""))

# Cell 11: Markdown - Navigation & Curriculum Sitemap
cells.append(nbf.v4.new_markdown_cell("""\
## 6. Curriculum Navigation & Specialized Masterclasses

To explore each mathematical and methodological domain in comprehensive depth:

| Masterclass Notebook | Pedagogical Domain & Topics |
| :--- | :--- |
| **[01_exploratory_spatial_data_analysis.ipynb](01_exploratory_spatial_data_analysis.ipynb)** | Complete ESDA theory, Queen/KNN spatial topology, Global Moran's $I$, Moran Scatterplots, Anselin Local Moran LISA cluster maps, Healthcare Deserts, and Cultural Diversity. |
| **[02_spatial_statistics_modeling.ipynb](02_spatial_statistics_modeling.ipynb)** | Econometric theory, Gauss-Markov spatial failure, Multicollinearity VIF, OLS residual spatial diagnostics, Lagrange Multiplier decision rules, Maximum Likelihood SAR/SEM estimation, and Spatial Multipliers. |
| **[03_sectoral_decision_intelligence.ipynb](03_sectoral_decision_intelligence.ipynb)** | Spatial infrastructure inequality, Lorenz Curves, Gini coefficients, Bivariate Moran's $I$, Ward Priority Index (WPI), and Executive State Action Rosters. |
"""))

nb['cells'] = cells
out_path = 'notebooks/00_master_spatial_decision_handbook.ipynb'
nbf.write(nb, out_path)
print(f"Generated {out_path} ({len(cells)} cells)")
