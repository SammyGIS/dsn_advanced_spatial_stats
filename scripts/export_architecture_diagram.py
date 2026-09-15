import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('docs/figures', exist_ok=True)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

fig, ax = plt.subplots(figsize=(15, 7.5), facecolor='#f8f9fa')
ax.set_facecolor('#f8f9fa')

# Stages with punchy, concise text
stages = [
    {
        "num": "01",
        "title": "DATA INGESTION",
        "color": "#1d3557",
        "accent": "#457b9d",
        "x": 0.04,
        "items": [
            "GRID3 Ward Boundaries (9,308)",
            "Meta Relative Wealth Index",
            "WorldPop Gridded Demographics",
            "Infrastructure POI Registries:\n  • Clinics & Hospitals\n  • Commercial Markets\n  • Churches & Mosques\n  • Public Water Points"
        ]
    },
    {
        "num": "02",
        "title": "SPATIAL HARMONIZATION",
        "color": "#2a9d8f",
        "accent": "#52b788",
        "x": 0.28,
        "items": [
            "CRS Standardization (EPSG:4326)",
            "Multi-Core Zonal Statistics\n(Ward Mean Wealth & Density)",
            "Point-in-Polygon Spatial Joins\n(Facility counts & per-capita rates)",
            "Parquet Master Consolidation\n(Fast, compressed, single file)"
        ]
    },
    {
        "num": "03",
        "title": "SPATIAL ANALYTICS",
        "color": "#e76f51",
        "accent": "#f4a261",
        "x": 0.52,
        "items": [
            "Spatial Topology (Weights W)",
            "Global Moran's I Test\n(Proves spatial clustering)",
            "Anselin LISA Cluster Mapping\n(Hotspots, Coldspots, Outliers)",
            "Spatial Econometrics\n(OLS, LM Tests, SAR & SEM)"
        ]
    },
    {
        "num": "04",
        "title": "DECISION INTELLIGENCE",
        "color": "#e63946",
        "accent": "#d90429",
        "x": 0.76,
        "items": [
            "Healthcare Deserts Identified\n(1,800+ acute shortage wards)",
            "Retail Commercial Siting\n(Prime expansion catchments)",
            "Cultural Transition Zones\n(Middle Belt diversity index)",
            "Spatial Multiplier (2.4x)\n(Cross-boundary policy returns)"
        ]
    }
]

box_width = 0.20
box_height = 0.42   # compact cards tightly wrapping the content without dead space
box_y = 0.28        # balanced vertical centering

for i, s in enumerate(stages):
    # Shadow
    shadow = patches.FancyBboxPatch(
        (s["x"] + 0.004, box_y - 0.008), box_width, box_height,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        facecolor='#dcdcdc', edgecolor='none', zorder=1
    )
    ax.add_patch(shadow)

    # Main Card
    card = patches.FancyBboxPatch(
        (s["x"], box_y), box_width, box_height,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        facecolor='#ffffff', edgecolor=s["color"], linewidth=2.0, zorder=2
    )
    ax.add_patch(card)

    # Header Ribbon
    ribbon = patches.FancyBboxPatch(
        (s["x"], box_y + box_height - 0.10), box_width, 0.10,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        facecolor=s["color"], edgecolor='none', zorder=3
    )
    ax.add_patch(ribbon)

    # Header Step Number & Title
    ax.text(
        s["x"] + 0.015, box_y + box_height - 0.05,
        s["num"],
        color='#a8dadc', fontsize=16, fontweight='black', va='center', zorder=4
    )
    ax.text(
        s["x"] + 0.055, box_y + box_height - 0.05,
        s["title"],
        color='#ffffff', fontsize=10, fontweight='bold', va='center', zorder=4
    )

    # Content bullets
    content = "\n\n".join(s["items"])
    ax.text(
        s["x"] + 0.015, box_y + box_height - 0.14,
        content,
        color='#2b2d42', fontsize=8.8, va='top', ha='left', zorder=4, linespacing=1.25
    )

    # Connecting Flow Arrow
    if i < len(stages) - 1:
        start_x = s["x"] + box_width + 0.008
        end_x = stages[i+1]["x"] - 0.008
        arrow_y = box_y + box_height / 2
        
        ax.annotate(
            '', xy=(end_x, arrow_y), xytext=(start_x, arrow_y),
            arrowprops=dict(
                arrowstyle="-|>", color='#6c757d', lw=2.5, mutation_scale=18
            ),
            zorder=5
        )

# Header Title & Subtitle
ax.text(0.5, 0.94, "SPATIAL DATA SCIENCE & DECISION INTELLIGENCE PIPELINE", 
        fontsize=16, fontweight='bold', ha='center', color='#1d3557')
ax.text(0.5, 0.89, "A 4-Stage End-to-End Framework Transforming Geographic Data into Strategic Actions", 
        fontsize=11, style='italic', ha='center', color='#457b9d')

ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.0)
ax.axis('off')

plt.tight_layout()
fig.savefig('docs/figures/00_architecture_and_methodology_flowchart.png', bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
plt.close(fig)
print("Updated docs/figures/00_architecture_and_methodology_flowchart.png with cleaner, concise flow!")
