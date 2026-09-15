"""
Generate a clean, professional pedagogical diagram comparing:
Traditional Non-Spatial EDA vs. Exploratory Spatial Data Analysis (ESDA).
Saves to docs/figures/08_traditional_vs_spatial_eda.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Set font and style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.2), dpi=300)
fig.patch.set_facecolor('#ffffff')

# ─────────────────────────────────────────────────────────────────────────────
# PANEL 1: TRADITIONAL EDA (NON-SPATIAL)
# ─────────────────────────────────────────────────────────────────────────────
ax1.set_facecolor('#fcfcfd')
ax1.set_title("1. Traditional Non-Spatial EDA\n(Operates Only in Feature Space)", 
              fontsize=14, fontweight='bold', color='#0f172a', pad=15)

# Draw simulated histogram
np.random.seed(42)
vals = np.random.normal(0, 1, 1000)
ax1.hist(vals, bins=25, color='#94a3b8', edgecolor='#64748b', alpha=0.7, density=True)
ax1.set_xlim(-3.5, 3.5)
ax1.set_ylim(0, 0.55)
ax1.set_xlabel("Feature Value Distribution", fontsize=11, fontweight='bold', color='#334155')
ax1.set_ylabel("Density", fontsize=11, fontweight='bold', color='#334155')

# Annotation box
ax1.text(0, 0.46, "Summary: Mean = 0.00 | Std Dev = 1.00", 
         ha='center', fontsize=10.5, fontweight='bold', color='#0f172a',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#cbd5e1', lw=1.2))

ax1.text(0, -0.15, "CRITICAL FLAW: The Random Shuffle Test\nIf you shuffle all 9,308 ward locations across the map,\nthis histogram and summary stats remain 100% IDENTICAL.\nTraditional EDA cannot tell if poverty is clustered or random!", 
         ha='center', va='top', transform=ax1.transAxes, fontsize=10, color='#e11d48', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fff1f2', edgecolor='#fecdd3', lw=1.2))

# ─────────────────────────────────────────────────────────────────────────────
# PANEL 2: SPATIAL EDA (ESDA)
# ─────────────────────────────────────────────────────────────────────────────
ax2.set_facecolor('#fcfcfd')
ax2.set_title("2. Exploratory Spatial Data Analysis (ESDA)\n(Couples Attributes with Geographic Topology W)", 
              fontsize=14, fontweight='bold', color='#0f172a', pad=15)

# Draw simulated Moran Scatterplot (z vs Wz)
z = np.random.normal(0, 1, 120)
wz = 0.72 * z + np.random.normal(0, 0.4, 120)

# Quadrant scatter
colors = []
for zi, wzi in zip(z, wz):
    if zi > 0 and wzi > 0: colors.append('#e11d48')      # High-High (Hotspot)
    elif zi < 0 and wzi < 0: colors.append('#2563eb')    # Low-Low (Coldspot)
    elif zi > 0 and wzi < 0: colors.append('#d97706')    # High-Low (Island of Wealth)
    else: colors.append('#0284c7')                       # Low-High (Opportunity Sink)

ax2.scatter(z, wz, c=colors, s=40, alpha=0.85, edgecolors='#ffffff', linewidths=0.5)
# Regression slope (Moran's I)
x_line = np.linspace(-3, 3, 50)
ax2.plot(x_line, 0.72 * x_line, color='#0f172a', lw=2.5, linestyle='-', label="Moran's I = 0.684 (p < 0.001)")

ax2.axhline(0, color='#94a3b8', linestyle='--', lw=1)
ax2.axvline(0, color='#94a3b8', linestyle='--', lw=1)
ax2.set_xlim(-3.2, 3.2)
ax2.set_ylim(-3.2, 3.2)
ax2.set_xlabel("Standardized Value (z)", fontsize=11, fontweight='bold', color='#334155')
ax2.set_ylabel("Spatial Lag: Neighbor Average (Wz)", fontsize=11, fontweight='bold', color='#334155')

# Quadrant labels
ax2.text(1.8, 2.5, "High-High\n(Hotspot)", color='#e11d48', fontweight='bold', fontsize=9.5, ha='center')
ax2.text(-1.8, -2.5, "Low-Low\n(Coldspot)", color='#2563eb', fontweight='bold', fontsize=9.5, ha='center')
ax2.text(1.8, -2.5, "High-Low\n(Wealth Island)", color='#d97706', fontweight='bold', fontsize=9.5, ha='center')
ax2.text(-1.8, 2.5, "Low-High\n(Poverty Pocket)", color='#0284c7', fontweight='bold', fontsize=9.5, ha='center')

ax2.text(0, -0.15, "WHAT ESDA UNLOCKS:\n1. Proves spatial clustering is real, not visual chance (p < 0.001)\n2. Pinpoints exact coordinates of hotspots and coldspots\n3. Discovers local spatial outliers invisible to standard EDA!", 
         ha='center', va='top', transform=ax2.transAxes, fontsize=10, color='#0f766e', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#f0fdf4', edgecolor='#bbf7d0', lw=1.2))

plt.tight_layout()

# Save
out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "figures")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "08_traditional_vs_spatial_eda.png")
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Generated comparison diagram at {out_path}")
