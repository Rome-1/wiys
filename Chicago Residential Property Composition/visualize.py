#!/usr/bin/env python3
"""
Visualize Chicago residential property compositions by community area.
Focuses on: Wall Material, Roof Material, Garage 2 Material, Repair Condition, Age.
"""
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec
import seaborn as sns
import numpy as np
from shapely.geometry import Point
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'figure.dpi': 150,
    'font.size': 9,
    'axes.titlesize': 11,
    'figure.facecolor': 'white',
})

OUTDIR = '/home/rome/gt/wiys/crew/alice/analysis/figures'
import os
os.makedirs(OUTDIR, exist_ok=True)

# --- Label maps ---
WALL_LABELS = {1: 'Wood', 2: 'Masonry', 3: 'Wood & Masonry', 4: 'Stucco'}
ROOF_LABELS = {1: 'Shingle/Asphalt', 2: 'Tar & Gravel', 3: 'Slate', 4: 'Shake', 5: 'Tile', 6: 'Other'}
GAR2_LABELS = {0: 'None', 1: 'Frame', 2: 'Masonry', 3: 'Frame/Masonry', 4: 'Stucco'}
REPAIR_LABELS = {1: 'Above Average', 2: 'Average', 3: 'Below Average'}

# --- Load data ---
print("Loading property data...")
df = pd.read_csv('/home/rome/gt/wiys/crew/alice/analysis/properties.csv')

# Filter to rows with characteristics (non-null ext_wall as proxy)
df_chars = df.dropna(subset=['ext_wall']).copy()
print(f"Properties with characteristics: {len(df_chars):,}")

# Filter to most recent tax year per PIN
df_chars = df_chars.sort_values('tax_year', ascending=False).drop_duplicates(subset='pin', keep='first')
print(f"After dedup to latest tax year: {len(df_chars):,}")

# --- Spatial join with community areas ---
print("Loading community areas...")
ca = gpd.read_file('/home/rome/gt/wiys/crew/alice/analysis/community_areas.geojson')
ca['community_area'] = ca['community'].str.title()
ca['area_num'] = ca['area_numbe'].astype(int)

# Filter to properties with coordinates
df_geo = df_chars.dropna(subset=['centroid_x', 'centroid_y']).copy()
df_geo['centroid_x'] = df_geo['centroid_x'].astype(float)
df_geo['centroid_y'] = df_geo['centroid_y'].astype(float)

# Only keep points roughly in Chicago area
df_geo = df_geo[
    (df_geo['centroid_x'] > -88.0) & (df_geo['centroid_x'] < -87.5) &
    (df_geo['centroid_y'] > 41.6) & (df_geo['centroid_y'] < 42.1)
]
print(f"Properties in Chicago bbox: {len(df_geo):,}")

# Create GeoDataFrame and spatial join
gdf = gpd.GeoDataFrame(
    df_geo,
    geometry=gpd.points_from_xy(df_geo.centroid_x, df_geo.centroid_y),
    crs="EPSG:4326"
)
ca = ca.to_crs("EPSG:4326")

print("Performing spatial join...")
joined = gpd.sjoin(gdf, ca[['geometry', 'community_area', 'area_num']], how='inner', predicate='within')
print(f"Properties matched to community areas: {len(joined):,}")
print(f"Community areas represented: {joined['community_area'].nunique()}")

# =============================================================================
# FIGURE 1: Overall distributions (4 panels)
# =============================================================================
print("\nGenerating Figure 1: Overall distributions...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Wall Material
ax = axes[0, 0]
wall_counts = joined['ext_wall'].map(WALL_LABELS).value_counts()
colors_wall = ['#8B4513', '#CD853F', '#D2691E', '#F5DEB3']
wall_counts.plot.bar(ax=ax, color=colors_wall[:len(wall_counts)], edgecolor='black', linewidth=0.5)
ax.set_title('Exterior Wall Material')
ax.set_ylabel('Number of Properties')
ax.set_xlabel('')
ax.tick_params(axis='x', rotation=30)
for i, v in enumerate(wall_counts.values):
    ax.text(i, v + 1000, f'{v:,}\n({v/len(joined)*100:.1f}%)', ha='center', va='bottom', fontsize=8)

# Roof Material
ax = axes[0, 1]
roof_counts = joined['roof_cnst'].map(ROOF_LABELS).value_counts()
colors_roof = ['#696969', '#A9A9A9', '#4682B4', '#8FBC8F', '#CD5C5C', '#DEB887']
roof_counts.plot.bar(ax=ax, color=colors_roof[:len(roof_counts)], edgecolor='black', linewidth=0.5)
ax.set_title('Roof Construction Material')
ax.set_ylabel('Number of Properties')
ax.set_xlabel('')
ax.tick_params(axis='x', rotation=30)
for i, v in enumerate(roof_counts.values):
    ax.text(i, v + 1000, f'{v:,}\n({v/len(joined)*100:.1f}%)', ha='center', va='bottom', fontsize=8)

# Repair Condition
ax = axes[1, 0]
repair_counts = joined['repair_cnd'].map(REPAIR_LABELS).value_counts()
colors_repair = ['#2E8B57', '#FFD700', '#DC143C']
bars = repair_counts.plot.bar(ax=ax, color=colors_repair[:len(repair_counts)], edgecolor='black', linewidth=0.5)
ax.set_title('Repair Condition')
ax.set_ylabel('Number of Properties')
ax.set_xlabel('')
ax.tick_params(axis='x', rotation=0)
for i, v in enumerate(repair_counts.values):
    ax.text(i, v + 1000, f'{v:,}\n({v/len(joined)*100:.1f}%)', ha='center', va='bottom', fontsize=8)

# Age Distribution
ax = axes[1, 1]
ax.hist(joined['age'].dropna(), bins=50, color='#4682B4', edgecolor='black', linewidth=0.3, alpha=0.8)
ax.axvline(joined['age'].median(), color='red', linestyle='--', linewidth=1.5, label=f'Median: {joined["age"].median():.0f} yrs')
ax.axvline(joined['age'].mean(), color='orange', linestyle='--', linewidth=1.5, label=f'Mean: {joined["age"].mean():.0f} yrs')
ax.set_title('Property Age Distribution')
ax.set_xlabel('Age (years)')
ax.set_ylabel('Number of Properties')
ax.legend(fontsize=8)

fig.suptitle('Chicago Residential Property Characteristics\n(Cook County Assessor Data, 2018-2019)', fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(f'{OUTDIR}/01_overall_distributions.png', bbox_inches='tight')
plt.close()
print("  Saved 01_overall_distributions.png")

# =============================================================================
# FIGURE 2: Wall Material composition by Community Area (choropleth)
# =============================================================================
print("Generating Figure 2: Wall material choropleth maps...")
fig, axes = plt.subplots(2, 2, figsize=(16, 20))

for idx, (wall_code, wall_name) in enumerate(WALL_LABELS.items()):
    ax = axes[idx // 2][idx % 2]
    # Compute fraction of each wall type per community area
    ca_wall = joined.groupby('area_num').apply(
        lambda g: (g['ext_wall'] == wall_code).mean(), include_groups=False
    ).reset_index()
    ca_wall.columns = ['area_num', 'fraction']

    ca_plot = ca.merge(ca_wall, on='area_num', how='left')
    ca_plot.plot(column='fraction', ax=ax, legend=True, cmap='YlOrRd',
                 edgecolor='black', linewidth=0.5, missing_kwds={'color': 'lightgray'},
                 legend_kwds={'shrink': 0.6, 'label': f'Fraction {wall_name}'})
    ax.set_title(f'{wall_name}', fontsize=12, fontweight='bold')
    ax.set_axis_off()

fig.suptitle('Fraction of Properties by Wall Material\nper Chicago Community Area', fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(f'{OUTDIR}/02_wall_material_choropleth.png', bbox_inches='tight')
plt.close()
print("  Saved 02_wall_material_choropleth.png")

# =============================================================================
# FIGURE 3: Roof Material composition by Community Area
# =============================================================================
print("Generating Figure 3: Roof material choropleth...")
fig, axes = plt.subplots(2, 3, figsize=(18, 20))

for idx, (roof_code, roof_name) in enumerate(ROOF_LABELS.items()):
    ax = axes[idx // 3][idx % 3]
    ca_roof = joined.groupby('area_num').apply(
        lambda g: (g['roof_cnst'] == roof_code).mean(), include_groups=False
    ).reset_index()
    ca_roof.columns = ['area_num', 'fraction']

    ca_plot = ca.merge(ca_roof, on='area_num', how='left')
    ca_plot.plot(column='fraction', ax=ax, legend=True, cmap='YlGnBu',
                 edgecolor='black', linewidth=0.5, missing_kwds={'color': 'lightgray'},
                 legend_kwds={'shrink': 0.6, 'label': f'Fraction'})
    ax.set_title(f'{roof_name}', fontsize=12, fontweight='bold')
    ax.set_axis_off()

fig.suptitle('Fraction of Properties by Roof Material\nper Chicago Community Area', fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(f'{OUTDIR}/03_roof_material_choropleth.png', bbox_inches='tight')
plt.close()
print("  Saved 03_roof_material_choropleth.png")

# =============================================================================
# FIGURE 4: Median Age by Community Area
# =============================================================================
print("Generating Figure 4: Median age choropleth...")
fig, ax = plt.subplots(1, 1, figsize=(10, 12))

ca_age = joined.groupby('area_num')['age'].median().reset_index()
ca_age.columns = ['area_num', 'median_age']
ca_plot = ca.merge(ca_age, on='area_num', how='left')

ca_plot.plot(column='median_age', ax=ax, legend=True, cmap='RdYlGn_r',
             edgecolor='black', linewidth=0.5, missing_kwds={'color': 'lightgray'},
             legend_kwds={'shrink': 0.6, 'label': 'Median Age (years)'})

# Label community areas
for _, row in ca_plot.iterrows():
    centroid = row.geometry.centroid
    ax.annotate(row['community_area'], xy=(centroid.x, centroid.y),
                fontsize=4.5, ha='center', va='center', fontweight='bold',
                color='black', alpha=0.8)

ax.set_title('Median Property Age by Community Area', fontsize=14, fontweight='bold')
ax.set_axis_off()
fig.savefig(f'{OUTDIR}/04_median_age_choropleth.png', bbox_inches='tight')
plt.close()
print("  Saved 04_median_age_choropleth.png")

# =============================================================================
# FIGURE 5: Repair Condition by Community Area
# =============================================================================
print("Generating Figure 5: Repair condition choropleth...")
fig, axes = plt.subplots(1, 3, figsize=(20, 10))

for idx, (rep_code, rep_name) in enumerate(REPAIR_LABELS.items()):
    ax = axes[idx]
    ca_rep = joined.groupby('area_num').apply(
        lambda g: (g['repair_cnd'] == rep_code).mean(), include_groups=False
    ).reset_index()
    ca_rep.columns = ['area_num', 'fraction']

    ca_plot = ca.merge(ca_rep, on='area_num', how='left')
    cmap = ['Greens', 'YlOrBr', 'Reds'][idx]
    ca_plot.plot(column='fraction', ax=ax, legend=True, cmap=cmap,
                 edgecolor='black', linewidth=0.5, missing_kwds={'color': 'lightgray'},
                 legend_kwds={'shrink': 0.6, 'label': f'Fraction'})
    ax.set_title(f'{rep_name}', fontsize=12, fontweight='bold')
    ax.set_axis_off()

fig.suptitle('Repair Condition Distribution\nper Chicago Community Area', fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(f'{OUTDIR}/05_repair_condition_choropleth.png', bbox_inches='tight')
plt.close()
print("  Saved 05_repair_condition_choropleth.png")

# =============================================================================
# FIGURE 6: Top/Bottom community areas stacked bar chart - Wall Material
# =============================================================================
print("Generating Figure 6: Wall material stacked bars by community area...")

# Compute wall composition per community area
wall_comp = pd.crosstab(joined['community_area'], joined['ext_wall'].map(WALL_LABELS), normalize='index')
# Sort by masonry fraction
wall_comp = wall_comp.sort_values('Masonry', ascending=True)

fig, ax = plt.subplots(figsize=(14, 18))
colors_wall = {'Wood': '#8B4513', 'Masonry': '#CD853F', 'Wood & Masonry': '#D2691E', 'Stucco': '#F5DEB3'}
wall_comp.plot.barh(stacked=True, ax=ax, color=[colors_wall.get(c, '#999') for c in wall_comp.columns],
                     edgecolor='white', linewidth=0.3)
ax.set_xlabel('Fraction of Properties')
ax.set_title('Wall Material Composition by Community Area\n(sorted by Masonry fraction)', fontsize=13, fontweight='bold')
ax.legend(title='Wall Material', bbox_to_anchor=(1.02, 1), loc='upper left')
ax.set_xlim(0, 1)
plt.tight_layout()
fig.savefig(f'{OUTDIR}/06_wall_material_stacked_bars.png', bbox_inches='tight')
plt.close()
print("  Saved 06_wall_material_stacked_bars.png")

# =============================================================================
# FIGURE 7: Age distribution violin plot by top community areas
# =============================================================================
print("Generating Figure 7: Age distribution by community area...")

# Pick top 20 most populous community areas
top_ca = joined['community_area'].value_counts().head(20).index.tolist()
df_top = joined[joined['community_area'].isin(top_ca)].copy()

# Sort by median age
ca_order = df_top.groupby('community_area')['age'].median().sort_values().index.tolist()

fig, ax = plt.subplots(figsize=(14, 8))
sns.boxplot(data=df_top, x='community_area', y='age', order=ca_order, ax=ax,
            fliersize=0.5, linewidth=0.8, palette='coolwarm')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
ax.set_xlabel('')
ax.set_ylabel('Property Age (years)')
ax.set_title('Property Age Distribution — Top 20 Most Populous Community Areas\n(sorted by median age)', fontsize=13, fontweight='bold')
plt.tight_layout()
fig.savefig(f'{OUTDIR}/07_age_boxplot_by_community.png', bbox_inches='tight')
plt.close()
print("  Saved 07_age_boxplot_by_community.png")

# =============================================================================
# FIGURE 8: Roof material stacked bars
# =============================================================================
print("Generating Figure 8: Roof material stacked bars...")

roof_comp = pd.crosstab(joined['community_area'], joined['roof_cnst'].map(ROOF_LABELS), normalize='index')
roof_comp = roof_comp.sort_values('Shingle/Asphalt', ascending=True)

fig, ax = plt.subplots(figsize=(14, 18))
colors_r = {'Shingle/Asphalt': '#696969', 'Tar & Gravel': '#A9A9A9', 'Slate': '#4682B4',
            'Shake': '#8FBC8F', 'Tile': '#CD5C5C', 'Other': '#DEB887'}
roof_comp.plot.barh(stacked=True, ax=ax, color=[colors_r.get(c, '#999') for c in roof_comp.columns],
                     edgecolor='white', linewidth=0.3)
ax.set_xlabel('Fraction of Properties')
ax.set_title('Roof Material Composition by Community Area\n(sorted by Shingle/Asphalt fraction)', fontsize=13, fontweight='bold')
ax.legend(title='Roof Material', bbox_to_anchor=(1.02, 1), loc='upper left')
ax.set_xlim(0, 1)
plt.tight_layout()
fig.savefig(f'{OUTDIR}/08_roof_material_stacked_bars.png', bbox_inches='tight')
plt.close()
print("  Saved 08_roof_material_stacked_bars.png")

# =============================================================================
# FIGURE 9: Correlation heatmap — Age vs Wall Material vs Repair
# =============================================================================
print("Generating Figure 9: Age vs Wall and Repair heatmap...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Age by wall material
ax = axes[0]
age_wall = joined.groupby(joined['ext_wall'].map(WALL_LABELS))['age'].describe()[['mean', '50%', 'count']]
age_wall.columns = ['Mean Age', 'Median Age', 'Count']
age_wall = age_wall.sort_values('Median Age', ascending=False)
bars = ax.barh(age_wall.index, age_wall['Median Age'], color=[colors_wall.get(n, '#999') for n in age_wall.index],
               edgecolor='black', linewidth=0.5)
for i, (idx, row) in enumerate(age_wall.iterrows()):
    ax.text(row['Median Age'] + 1, i, f'{row["Median Age"]:.0f} yrs (n={row["Count"]:,.0f})', va='center', fontsize=8)
ax.set_xlabel('Median Age (years)')
ax.set_title('Median Property Age by Wall Material')

# Age by repair condition
ax = axes[1]
age_rep = joined.groupby(joined['repair_cnd'].map(REPAIR_LABELS))['age'].describe()[['mean', '50%', 'count']]
age_rep.columns = ['Mean Age', 'Median Age', 'Count']
rep_colors = {'Above Average': '#2E8B57', 'Average': '#FFD700', 'Below Average': '#DC143C'}
bars = ax.barh(age_rep.index, age_rep['Median Age'],
               color=[rep_colors.get(n, '#999') for n in age_rep.index],
               edgecolor='black', linewidth=0.5)
for i, (idx, row) in enumerate(age_rep.iterrows()):
    ax.text(row['Median Age'] + 1, i, f'{row["Median Age"]:.0f} yrs (n={row["Count"]:,.0f})', va='center', fontsize=8)
ax.set_xlabel('Median Age (years)')
ax.set_title('Median Property Age by Repair Condition')

fig.suptitle('Property Age Relationships', fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(f'{OUTDIR}/09_age_relationships.png', bbox_inches='tight')
plt.close()
print("  Saved 09_age_relationships.png")

# =============================================================================
# FIGURE 10: Summary stats table by community area
# =============================================================================
print("Generating summary statistics...")

summary = joined.groupby('community_area').agg(
    n_properties=('pin', 'count'),
    median_age=('age', 'median'),
    mean_age=('age', 'mean'),
    pct_masonry=('ext_wall', lambda x: (x == 2).mean() * 100),
    pct_wood=('ext_wall', lambda x: (x == 1).mean() * 100),
    pct_shingle_roof=('roof_cnst', lambda x: (x == 1).mean() * 100),
    pct_above_avg_repair=('repair_cnd', lambda x: (x == 1).mean() * 100),
    pct_below_avg_repair=('repair_cnd', lambda x: (x == 3).mean() * 100),
    mean_bldg_sf=('bldg_sf', 'mean'),
).round(1)

summary = summary.sort_values('n_properties', ascending=False)
summary.to_csv(f'{OUTDIR}/community_area_summary.csv')
print(f"  Saved community_area_summary.csv")

# Print top/bottom highlights
print("\n=== KEY FINDINGS ===")
print(f"\nTotal Chicago properties analyzed: {len(joined):,}")
print(f"Community areas: {joined['community_area'].nunique()}")

print(f"\n--- Wall Material (overall) ---")
for code, name in WALL_LABELS.items():
    pct = (joined['ext_wall'] == code).mean() * 100
    print(f"  {name}: {pct:.1f}%")

print(f"\n--- Roof Material (overall) ---")
for code, name in ROOF_LABELS.items():
    pct = (joined['roof_cnst'] == code).mean() * 100
    print(f"  {name}: {pct:.1f}%")

print(f"\n--- Repair Condition (overall) ---")
for code, name in REPAIR_LABELS.items():
    pct = (joined['repair_cnd'] == code).mean() * 100
    print(f"  {name}: {pct:.1f}%")

print(f"\n--- Age ---")
print(f"  Median: {joined['age'].median():.0f} years")
print(f"  Mean: {joined['age'].mean():.1f} years")

print("\n--- Highest Masonry % (top 5 community areas) ---")
top_masonry = summary.nlargest(5, 'pct_masonry')[['pct_masonry', 'n_properties']]
for ca_name, row in top_masonry.iterrows():
    print(f"  {ca_name}: {row['pct_masonry']:.1f}% ({int(row['n_properties']):,} properties)")

print("\n--- Oldest Properties (top 5 by median age) ---")
top_old = summary.nlargest(5, 'median_age')[['median_age', 'n_properties']]
for ca_name, row in top_old.iterrows():
    print(f"  {ca_name}: median {row['median_age']:.0f} yrs ({int(row['n_properties']):,} properties)")

print("\n--- Highest Below-Average Repair (top 5) ---")
top_bad = summary.nlargest(5, 'pct_below_avg_repair')[['pct_below_avg_repair', 'n_properties']]
for ca_name, row in top_bad.iterrows():
    print(f"  {ca_name}: {row['pct_below_avg_repair']:.1f}% ({int(row['n_properties']):,} properties)")

print("\nDone! All figures saved to:", OUTDIR)
