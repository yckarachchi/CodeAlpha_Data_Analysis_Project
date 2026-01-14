import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the custom dataset (has more columns for visualization)
df = pd.read_csv('imdb_clean_custom.csv')

# Set visual style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# ===========================
# 1. RATING DISTRIBUTION HISTOGRAM
# ===========================
plt.figure(figsize=(10, 6))
sns.histplot(df['rating'], bins=20, kde=True, color='teal', edgecolor='black')
plt.title('Distribution of IMDb Ratings (Top 250 Movies)', fontsize=16, fontweight='bold')
plt.xlabel('Rating (0-10 scale)', fontsize=14)
plt.ylabel('Number of Movies', fontsize=14)
plt.axvline(df['rating'].mean(), color='red', linestyle='--', linewidth=2, 
            label=f'Mean: {df["rating"].mean():.2f}')
plt.legend()
plt.tight_layout()
plt.savefig('1_rating_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# ===========================
# 2. MOVIES PER DECADE (BAR CHART)
# ===========================
plt.figure(figsize=(12, 6))
# Count movies per decade
decade_counts = df['decade'].value_counts().sort_index()
# Create a nice color palette
colors = plt.cm.viridis(np.linspace(0, 1, len(decade_counts)))

bars = plt.bar(decade_counts.index, decade_counts.values, color=colors, edgecolor='black')
plt.title('Number of Top 250 Movies per Decade', fontsize=16, fontweight='bold')
plt.xlabel('Decade', fontsize=14)
plt.ylabel('Number of Movies', fontsize=14)
plt.xticks(rotation=45)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.savefig('2_movies_per_decade.png', dpi=300, bbox_inches='tight')
plt.show()

# ===========================
# 3. RATING VS. RELEASE YEAR (SCATTER PLOT)
# ===========================
plt.figure(figsize=(12, 7))
scatter = plt.scatter(df['year'], df['rating'], 
                     c=df['movie_age'], cmap='plasma', 
                     s=80, alpha=0.7, edgecolors='black')

plt.colorbar(scatter, label='Movie Age (Years)')
plt.title('IMDb Rating vs. Release Year', fontsize=16, fontweight='bold')
plt.xlabel('Release Year', fontsize=14)
plt.ylabel('IMDb Rating', fontsize=14)

# Add trend line
z = np.polyfit(df['year'], df['rating'], 1)
p = np.poly1d(z)
plt.plot(df['year'], p(df['year']), "r--", alpha=0.8, linewidth=2, 
         label=f'Trend line (slope: {z[0]:.4f})')

plt.legend()
plt.tight_layout()
plt.savefig('3_rating_vs_year.png', dpi=300, bbox_inches='tight')
plt.show()

# ===========================
# 4. RATING CATEGORIES (PIE CHART)
# ===========================
plt.figure(figsize=(10, 8))
rating_counts = df['rating_category'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Red, teal, blue
explode = (0.1, 0, 0)  # Explode the largest slice

plt.pie(rating_counts.values, labels=rating_counts.index, 
        autopct='%1.1f%%', startangle=90, colors=colors, 
        explode=explode, shadow=True, textprops={'fontsize': 12})

plt.title('Distribution of Rating Categories', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('4_rating_categories.png', dpi=300, bbox_inches='tight')
plt.show()

# ===========================
# 5. QUALITY SCORE VS RATING (SCATTER WITH REGRESSION)
# ===========================
plt.figure(figsize=(12, 7))
sns.regplot(x='quality_score', y='rating', data=df, 
            scatter_kws={'s': 60, 'alpha': 0.6, 'edgecolors': 'black'},
            line_kws={'color': 'red', 'linewidth': 3, 'alpha': 0.8},
            color='purple')

plt.title('Quality Score vs. IMDb Rating', fontsize=16, fontweight='bold')
plt.xlabel('Quality Score', fontsize=14)
plt.ylabel('IMDb Rating', fontsize=14)

# Calculate correlation
correlation = df['quality_score'].corr(df['rating'])
plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
         transform=plt.gca().transAxes, fontsize=12, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

plt.tight_layout()
plt.savefig('5_quality_vs_rating.png', dpi=300, bbox_inches='tight')
plt.show()
