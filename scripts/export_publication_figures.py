import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

import libpysal
import esda
from splot.esda import moran_scatterplot

os.makedirs('docs/figures', exist_ok=True)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
sns.set_style('whitegrid')

DATA_PATH = 'data/processed/nigeria_wards_master.parquet'
if not os.path.exists(DATA_PATH):
    DATA_PATH = '../data/processed/nigeria_wards_master.parquet'

print(f"Loading data from {DATA_PATH}...")
gdf = gpd.read_parquet(DATA_PATH)
if gdf.crs is None:
    gdf.set_crs(epsg=4326, inplace=True)
else:
    gdf = gdf.to_crs(epsg=4326)

gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty].copy()
gdf.reset_index(drop=True, inplace=True)

# Feature engineering
gdf['rwi_mean'] = gdf['rwi_mean'].fillna(gdf['rwi_mean'].median())
gdf['pop_2025_sum'] = gdf['pop_2025_sum'].fillna(gdf['pop_2025_sum'].median())
gdf['population_density_per_sqkm'] = gdf['population_density_per_sqkm'].fillna(gdf['population_density_per_sqkm'].median())

gdf['health_facility_rate'] = (gdf['health_facilities_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['is_health_desert'] = (gdf['health_facilities_count'] == 0) & (gdf['pop_2025_sum'] > gdf['pop_2025_sum'].median())
gdf['market_rate'] = (gdf['markets_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['water_point_rate'] = (gdf['water_points_count'] / (gdf['pop_2025_sum'] + 100)) * 10000
gdf['police_station_rate'] = (gdf['police_stations_count'] / (gdf['pop_2025_sum'] + 100)) * 10000

gdf['total_faith'] = gdf['churches_count'] + gdf['mosques_count']
gdf['church_share'] = gdf['churches_count'] / (gdf['total_faith'] + 1e-5)
gdf['mosque_share'] = gdf['mosques_count'] / (gdf['total_faith'] + 1e-5)
p1 = gdf['church_share'].clip(lower=1e-5, upper=1-1e-5)
p2 = gdf['mosque_share'].clip(lower=1e-5, upper=1-1e-5)
gdf['religious_diversity_idx'] = -(p1 * np.log2(p1) + p2 * np.log2(p2))

# -----------------------------------------------------------------------------
# Figure 1: National Wealth & Healthcare Deserts Dual Map
# -----------------------------------------------------------------------------
print("Exporting Figure 1: National Wealth & Healthcare Deserts...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

gdf.plot(column='rwi_mean', cmap='viridis', legend=True, ax=ax1,
         legend_kwds={'label': "Relative Wealth Index (RWI Mean)", 'orientation': "horizontal", 'shrink': 0.7, 'pad': 0.05})
ax1.set_title("A. National Relative Wealth Index (RWI)")
ax1.axis('off')

import matplotlib.patches as mpatches

# Legend for map 2
desert_patch = mpatches.Patch(color='#d90429', label=f"Healthcare Deserts (n={gdf['is_health_desert'].sum():,})")
base_patch = mpatches.Patch(color='#ececec', label=f"Wards with Facilities (n={(~gdf['is_health_desert']).sum():,})")
ax2.legend(handles=[desert_patch, base_patch], loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
ax2.axis('off')

plt.tight_layout()
fig.savefig('docs/figures/01_national_wealth_and_health_deserts.png', bbox_inches='tight', dpi=300)
plt.close(fig)

# -----------------------------------------------------------------------------
# Figure 2: Commercial Marketing & Retail Expansion Matrix
# -----------------------------------------------------------------------------
print("Exporting Figure 2: Commercial Retail Strategy...")
rwi_med = gdf['rwi_mean'].median()
mkt_med = gdf['markets_count'].median()

conditions = [
    (gdf['rwi_mean'] >= rwi_med) & (gdf['markets_count'] >= mkt_med),
    (gdf['rwi_mean'] >= rwi_med) & (gdf['markets_count'] < mkt_med),
    (gdf['rwi_mean'] < rwi_med) & (gdf['markets_count'] >= mkt_med),
    (gdf['rwi_mean'] < rwi_med) & (gdf['markets_count'] < mkt_med)
]
choices = [
    "Tier 1: Saturated Affluent (High RWI, High Markets)",
    "Tier 2: Prime Expansion Target (High RWI, Low Markets)",
    "Tier 3: Informal Commerce Hubs (Low RWI, High Markets)",
    "Tier 4: Subsistence / Underdeveloped (Low RWI, Low Markets)"
]
gdf['retail_segment'] = np.select(conditions, choices, default='Unclassified')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

segment_colors = {
    "Tier 1: Saturated Affluent (High RWI, High Markets)": "#1b4332",
    "Tier 2: Prime Expansion Target (High RWI, Low Markets)": "#52b788",
    "Tier 3: Informal Commerce Hubs (Low RWI, High Markets)": "#e76f51",
    "Tier 4: Subsistence / Underdeveloped (Low RWI, Low Markets)": "#d8d8d8"
}

for seg, col in segment_colors.items():
    subset = gdf[gdf['retail_segment'] == seg]
    subset.plot(color=col, ax=ax1, label=seg, linewidth=0.1, edgecolor='white')

ax1.set_title("A. Commercial Catchment & Retail Strategy Map")
ax1.axis('off')
seg_patches = [mpatches.Patch(color=c, label=l) for l, c in segment_colors.items()]
ax1.legend(handles=seg_patches, loc='lower left', fontsize=9, frameon=True, facecolor='white', framealpha=0.9)

sns.countplot(data=gdf, y='retail_segment', hue='retail_segment', palette=list(segment_colors.values()), order=choices, ax=ax2, legend=False)
ax2.set_title("B. Ward Distribution by Commercial Sector Strategy")
ax2.set_xlabel("Number of Administrative Wards")
ax2.set_ylabel("")

plt.tight_layout()
fig.savefig('docs/figures/02_commercial_retail_strategy.png', bbox_inches='tight', dpi=300)
plt.close(fig)

# -----------------------------------------------------------------------------
# Figure 3: Cultural & Religious Geography
# -----------------------------------------------------------------------------
print("Exporting Figure 3: Religious Geography...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

gdf.plot(column='church_share', cmap='coolwarm', legend=True, ax=ax1,
         legend_kwds={'label': "Church vs Mosque Share (0 = Mosque Dominated, 1 = Church Dominated)", 
                      'orientation': "horizontal", 'shrink': 0.7, 'pad': 0.05})
ax1.set_title("A. Religious Institution Composition (9,308 Wards)")
ax1.axis('off')

gdf.plot(column='religious_diversity_idx', cmap='magma', legend=True, ax=ax2,
         legend_kwds={'label': "Religious Diversity Index (Shannon Entropy)", 
                      'orientation': "horizontal", 'shrink': 0.7, 'pad': 0.05})
ax2.set_title("B. Cultural Transition Zones (Coexistence & Social Diversity)")
ax2.axis('off')

plt.tight_layout()
fig.savefig('docs/figures/03_religious_cultural_geography.png', bbox_inches='tight', dpi=300)
plt.close(fig)

# -----------------------------------------------------------------------------
# Figure 4: Cross-Sector Non-Parametric Correlation Matrix
# -----------------------------------------------------------------------------
print("Exporting Figure 4: Correlation Matrix...")
sector_cols = [
    'rwi_mean', 'pop_2025_sum', 'health_facility_rate', 
    'market_rate', 'water_point_rate', 'police_station_rate',
    'churches_count', 'mosques_count'
]
corr = gdf[sector_cols].corr(method='spearman')

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='Spectral_r', vmin=-1, vmax=1, ax=ax, square=True,
            cbar_kws={'label': 'Spearman Rank Correlation Coefficient'})
ax.set_title("Cross-Sector Non-Parametric Correlation Matrix", fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
fig.savefig('docs/figures/04_cross_sector_correlation_matrix.png', bbox_inches='tight', dpi=300)
plt.close(fig)

# -----------------------------------------------------------------------------
# Figure 5: Spatial Autocorrelation & Anselin LISA Cluster Map
# -----------------------------------------------------------------------------
print("Exporting Figure 5: Moran & LISA Analysis...")
w_knn = libpysal.weights.KNN.from_dataframe(gdf, k=5)
w_knn.transform = 'R'

mi_rwi = esda.Moran(gdf['rwi_mean'].values, w_knn, permutations=999)
lm_rwi = esda.Moran_Local(gdf['rwi_mean'].values, w_knn, transformation='r', permutations=999, seed=42)

sig = lm_rwi.p_sim < 0.05
hotspots = (lm_rwi.q == 1) & sig
coldspots = (lm_rwi.q == 3) & sig
high_low = (lm_rwi.q == 4) & sig
low_high = (lm_rwi.q == 2) & sig

gdf['lisa_cluster'] = 'Not Significant'
gdf.loc[hotspots, 'lisa_cluster'] = 'High-High (Hotspot)'
gdf.loc[coldspots, 'lisa_cluster'] = 'Low-Low (Coldspot)'
gdf.loc[high_low, 'lisa_cluster'] = 'High-Low (Outlier)'
gdf.loc[low_high, 'lisa_cluster'] = 'Low-High (Outlier)'

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

moran_scatterplot(mi_rwi, ax=ax1)
ax1.set_title(f"A. Global Moran's I Scatterplot: Wealth (RWI)\\nI = {mi_rwi.I:.3f}, z = {mi_rwi.z_sim:.1f} (p < 0.001)")
ax1.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax1.axvline(0, color='gray', linestyle='--', linewidth=0.8)

lisa_colors = {
    'Not Significant': '#f0f0f0',
    'High-High (Hotspot)': '#d90429',
    'Low-Low (Coldspot)': '#0077b6',
    'High-Low (Outlier)': '#f77f00',
    'Low-High (Outlier)': '#90e0ef'
}

for ctype, color in lisa_colors.items():
    sub = gdf[gdf['lisa_cluster'] == ctype]
    if len(sub) > 0:
        sub.plot(color=color, ax=ax2, label=f"{ctype} (n={len(sub):,})", linewidth=0.1, edgecolor='white')

ax2.set_title("B. Anselin Local Moran's I (LISA) Wealth Clusters")
ax2.axis('off')
lisa_patches = [mpatches.Patch(color=c, label=f"{l} (n={(gdf['lisa_cluster'] == l).sum():,})") for l, c in lisa_colors.items()]
ax2.legend(handles=lisa_patches, loc='lower left', frameon=True, facecolor='white', framealpha=0.9)

plt.tight_layout()
fig.savefig('docs/figures/05_moran_and_lisa_clusters.png', bbox_inches='tight', dpi=300)
plt.close(fig)

# -----------------------------------------------------------------------------
# Figure 6: Infrastructure Inequality (Lorenz Curves) & Ward Priority Tiers
# -----------------------------------------------------------------------------
print("Exporting Figure 6: Lorenz Curves & Ward Priority Tiers...")
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

ax1.plot([0, 1], [0, 1], 'k--', label='Perfect Spatial Equality (G = 0.0)')
for col, lbl, color in [
    ('health_facilities_count', 'Health Clinics', '#e63946'),
    ('markets_count', 'Commercial Markets', '#2a9d8f'),
    ('water_points_count', 'Water Points (WASH)', '#457b9d')
]:
    g_val = gini_coefficient(gdf[col].values)
    px, py = lorenz_curve(gdf[col].values)
    ax1.plot(px, py, label=f"{lbl} (Gini = {g_val:.3f})", color=color, linewidth=2.5)

ax1.set_title("A. Spatial Allocation Inequality (Lorenz Curves)")
ax1.set_xlabel("Cumulative Proportion of Wards")
ax1.set_ylabel("Cumulative Proportion of Facilities")
ax1.legend(loc='upper left', frameon=True)

# Ward Priority Index
def min_max(s):
    return (s - s.min()) / (s.max() - s.min() + 1e-8)

poverty_def = min_max(-gdf['rwi_mean'])
health_def = min_max(1 / (gdf['health_facility_rate'] + 0.1))
water_def = min_max(1 / (gdf['water_point_rate'] + 0.1))
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

tier_colors = {
    'Tier 1: Critical Emergency Intervention': '#d90429',
    'Tier 2: High Investment Priority': '#f77f00',
    'Tier 3: Moderate Support Needed': '#fcbf49',
    'Tier 4: Mature / Self-Sustaining': '#2a9d8f'
}

for t, col in tier_colors.items():
    sub = gdf[gdf['action_tier'] == t]
    sub.plot(color=col, ax=ax2, label=f"{t} (n={len(sub):,})", linewidth=0.1, edgecolor='white')

ax2.set_title("B. National Ward Priority Action Tiers (MCDA)")
ax2.axis('off')
tier_patches = [mpatches.Patch(color=c, label=f"{l} (n={(gdf['action_tier'] == l).sum():,})") for l, c in tier_colors.items()]
ax2.legend(handles=tier_patches, loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)

plt.tight_layout()
fig.savefig('docs/figures/06_infrastructure_inequality_and_ward_priority_tiers.png', bbox_inches='tight', dpi=300)
plt.close(fig)

print("All 6 publication-quality figures successfully exported to docs/figures/!")
