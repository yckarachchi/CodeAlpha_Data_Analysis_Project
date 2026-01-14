import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec

# Load data
df = pd.read_csv('imdb_clean_custom.csv')

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 11

# ============================================
# 1. MULTI-PANEL ANALYSIS: DECADE DEEP DIVE
# ============================================
fig = plt.figure(figsize=(16, 12))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# 1A: Average Rating per Decade
ax1 = fig.add_subplot(gs[0, 0])
decade_avg_rating = df.groupby('decade')['rating'].mean().sort_values(ascending=False)
colors1 = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(decade_avg_rating)))
bars1 = ax1.bar(decade_avg_rating.index, decade_avg_rating.values, color=colors1, edgecolor='black')
ax1.set_title('Average IMDb Rating per Decade', fontsize=14, fontweight='bold')
ax1.set_ylabel('Average Rating', fontsize=12)
ax1.tick_params(axis='x', rotation=45)
# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height - 0.1,
             f'{height:.2f}', ha='center', va='top', color='white', fontweight='bold')

# 1B: Movies Count per Decade
ax2 = fig.add_subplot(gs[0, 1])
decade_counts = df['decade'].value_counts().sort_index()
colors2 = plt.cm.viridis(np.linspace(0.2, 0.8, len(decade_counts)))
bars2 = ax2.bar(decade_counts.index, decade_counts.values, color=colors2, edgecolor='black')
ax2.set_title('Number of Movies per Decade', fontsize=14, fontweight='bold')
ax2.set_ylabel('Count', fontsize=12)
ax2.tick_params(axis='x', rotation=45)
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom')

# 1C: Rating Distribution by Decade (Box Plot)
ax3 = fig.add_subplot(gs[1, :])
# Order decades chronologically
decade_order = ['1920s', '1930s', '1940s', '1950s', '1960s', 
                '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
df_decade_ordered = df[df['decade'].isin(decade_order)]
sns.boxplot(x='decade', y='rating', data=df_decade_ordered, 
            order=decade_order, ax=ax3, palette='Set3')
ax3.set_title('Rating Distribution Across Decades', fontsize=14, fontweight='bold')
ax3.set_xlabel('Decade', fontsize=12)
ax3.set_ylabel('IMDb Rating', fontsize=12)
ax3.tick_params(axis='x', rotation=45)

plt.suptitle('Decade-wise Analysis of IMDb Top 250 Movies', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('6_decade_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================
# 2. HEATMAP: RATING CATEGORY VS DECADE
# ============================================
plt.figure(figsize=(14, 8))
# Create pivot table
heatmap_data = pd.crosstab(df['decade'], df['rating_category'])
heatmap_data = heatmap_data.reindex(decade_order)

sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', 
            linewidths=1, linecolor='gray', cbar_kws={'label': 'Number of Movies'})
plt.title('Movies Count: Decade vs Rating Category', fontsize=16, fontweight='bold')
plt.xlabel('Rating Category', fontsize=12)
plt.ylabel('Decade', fontsize=12)
plt.tight_layout()
plt.savefig('7_heatmap_decade_vs_category.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================
# 3. TOP 20 MOVIES VISUALIZATION
# ============================================
plt.figure(figsize=(14, 10))
top_20 = df.nlargest(20, 'rating')[['title', 'rating', 'year', 'decade']].sort_values('rating')

# Create a color map for decades
decade_colors = {decade: plt.cm.tab20(i/len(df['decade'].unique())) 
                 for i, decade in enumerate(df['decade'].unique())}
colors = [decade_colors[decade] for decade in top_20['decade']]

bars = plt.barh(top_20['title'], top_20['rating'], color=colors, edgecolor='black')
plt.xlabel('IMDb Rating', fontsize=12)
plt.title('Top 20 Highest Rated Movies', fontsize=16, fontweight='bold')

# Add rating values and year on bars
for i, (bar, rating, year) in enumerate(zip(bars, top_20['rating'], top_20['year'])):
    width = bar.get_width()
    plt.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
             f'{rating:.1f} ({int(year)})', va='center', fontsize=10)

# Add legend for decades
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=decade_colors[d], edgecolor='black', label=d) 
                   for d in sorted(top_20['decade'].unique())]
plt.legend(handles=legend_elements, title='Decade', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('8_top_20_movies.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================
# 4. MOVIE AGE ANALYSIS
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 4A: Movie Age Distribution
axes[0].hist(df['movie_age'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
axes[0].axvline(df['movie_age'].mean(), color='red', linestyle='--', linewidth=2,
                label=f'Mean: {df["movie_age"].mean():.1f} years')
axes[0].set_title('Distribution of Movie Ages', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Years Since Release', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# 4B: Rating vs Movie Age with Regression
scatter = axes[1].scatter(df['movie_age'], df['rating'], 
                          c=df['quality_score'], cmap='plasma', 
                          s=50, alpha=0.7, edgecolors='black')
plt.colorbar(scatter, ax=axes[1], label='Quality Score')

# Add regression line
z = np.polyfit(df['movie_age'], df['rating'], 1)
p = np.poly1d(z)
sorted_age = np.sort(df['movie_age'])
axes[1].plot(sorted_age, p(sorted_age), "r--", linewidth=2, 
             label=f'Trend: Rating = {z[0]:.4f}*Age + {z[1]:.2f}')

axes[1].set_title('Rating vs. Movie Age (with Quality Score)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Movie Age (Years)', fontsize=12)
axes[1].set_ylabel('IMDb Rating', fontsize=12)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('Movie Age Analysis', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('9_movie_age_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================
# 5. CORRELATION HEATMAP
# ============================================
plt.figure(figsize=(10, 8))
# Select numeric columns for correlation
numeric_cols = ['position', 'year', 'rating', 'movie_age', 'quality_score']
corr_matrix = df[numeric_cols].corr()

# Create mask for upper triangle
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix of Numeric Features', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('10_correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

