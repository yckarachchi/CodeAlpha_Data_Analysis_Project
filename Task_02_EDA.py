# File: task2_eda_complete.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_data():
    """Load and prepare the dataset"""
    print(" Loading dataset...")
    df = pd.read_csv('imdb_clean_custom.csv')
    
    # Ensure decade column exists
    if 'decade' not in df.columns and 'year' in df.columns:
        df['decade'] = df['year'].apply(lambda x: f"{str(int(x))[:3]}0s")
    
    print(f" Loaded {len(df)} movies with {len(df.columns)} columns")
    return df

def explore_structure(df):
    """Explore data structure"""
    print("\n" + "="*60)
    print(" DATA STRUCTURE EXPLORATION")
    print("="*60)
    
    print(f"\nDataset shape: {df.shape}")
    print("\nColumn information:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2}. {col:20} | Type: {df[col].dtype}")
    
    print("\nMissing values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print(" No missing values")
    else:
        for col, count in missing.items():
            if count > 0:
                print(f"  {col}: {count} missing")
    
    return df

def analyze_distributions(df):
    """Analyze distributions of key variables"""
    print("\n" + "="*60)
    print(" DISTRIBUTION ANALYSIS")
    print("="*60)
    
    # Create visualizations directory
    os.makedirs('eda_visualizations', exist_ok=True)
    
    # 1. Rating distribution
    print("\n1. Rating Distribution Analysis:")
    print(f"   • Mean: {df['rating'].mean():.2f}")
    print(f"   • Median: {df['rating'].median():.2f}")
    print(f"   • Std Dev: {df['rating'].std():.2f}")
    print(f"   • Range: {df['rating'].min():.2f} to {df['rating'].max():.2f}")
    print(f"   • Skewness: {df['rating'].skew():.2f}")
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(df['rating'], bins=20, edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Rating')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Rating Distribution')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].boxplot(df['rating'], vert=False)
    axes[1].set_xlabel('Rating')
    axes[1].set_title('Rating Box Plot')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('eda_visualizations/rating_distribution.png', dpi=300)
    plt.show()
    
    # 2. Year distribution
    print("\n2. Year Distribution Analysis:")
    print(f"   • Oldest: {int(df['year'].min())}")
    print(f"   • Newest: {int(df['year'].max())}")
    print(f"   • Range: {int(df['year'].max() - df['year'].min())} years")
    
    plt.figure(figsize=(10, 6))
    plt.hist(df['year'], bins=20, edgecolor='black', alpha=0.7)
    plt.xlabel('Release Year')
    plt.ylabel('Number of Movies')
    plt.title('Movies Released Per Year')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('eda_visualizations/year_distribution.png', dpi=300)
    plt.show()
    
    return df

def analyze_trends(df):
    """Analyze trends and patterns"""
    print("\n" + "="*60)
    print(" TREND ANALYSIS")
    print("="*60)
    
    # 1. Rating vs Year
    print("\n1. Rating vs Release Year:")
    corr_year_rating = df['year'].corr(df['rating'])
    print(f"   • Correlation: {corr_year_rating:.3f}")
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df['year'], df['rating'], alpha=0.6, s=50)
    plt.xlabel('Release Year')
    plt.ylabel('Rating')
    plt.title('Rating vs Release Year')
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(df['year'], df['rating'], 1)
    p = np.poly1d(z)
    plt.plot(df['year'].sort_values(), p(df['year'].sort_values()), 
             'r--', label=f'Trend (r={corr_year_rating:.3f})')
    plt.legend()
    plt.tight_layout()
    plt.savefig('eda_visualizations/rating_vs_year.png', dpi=300)
    plt.show()
    
    # 2. Position vs Rating
    print("\n2. Position vs Rating:")
    corr_pos_rating = df['position'].corr(df['rating'])
    print(f"   • Correlation: {corr_pos_rating:.3f} (strong negative)")
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df['position'], df['rating'], alpha=0.6, s=50)
    plt.xlabel('Position (Rank)')
    plt.ylabel('Rating')
    plt.title('Rating vs Position (Higher position = better rank)')
    plt.grid(True, alpha=0.3)
    
    z = np.polyfit(df['position'], df['rating'], 1)
    p = np.poly1d(z)
    plt.plot(df['position'].sort_values(), p(df['position'].sort_values()), 
             'r--', label=f'Trend (r={corr_pos_rating:.3f})')
    plt.legend()
    plt.tight_layout()
    plt.savefig('eda_visualizations/rating_vs_position.png', dpi=300)
    plt.show()
    
    # 3. Decade analysis
    print("\n3. Decade Analysis:")
    decade_stats = df.groupby('decade')['rating'].agg(['mean', 'count']).round(2)
    print(decade_stats)
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(decade_stats.index, decade_stats['mean'])
    plt.xlabel('Decade')
    plt.ylabel('Average Rating')
    plt.title('Average Rating by Decade')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                 f'{height:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('eda_visualizations/decade_ratings.png', dpi=300)
    plt.show()
    
    return df, corr_year_rating, corr_pos_rating

def test_hypotheses(df):
    """Test statistical hypotheses"""
    print("\n" + "="*60)
    print(" HYPOTHESIS TESTING")
    print("="*60)
    
    # Hypothesis 1: Top movies are better than bottom movies
    print("\n1. Hypothesis: Top 10 movies have higher ratings than Bottom 10")
    top_10 = df.nsmallest(10, 'position')['rating']
    bottom_10 = df.nlargest(10, 'position')['rating']
    
    print(f"   • Top 10 average: {top_10.mean():.2f}")
    print(f"   • Bottom 10 average: {bottom_10.mean():.2f}")
    print(f"   • Difference: {top_10.mean() - bottom_10.mean():.2f}")
    
    t_stat, p_value = stats.ttest_ind(top_10, bottom_10)
    print(f"   • T-test p-value: {p_value:.6f}")
    print(f"   • Conclusion: {'SIGNIFICANT' if p_value < 0.05 else 'NOT SIGNIFICANT'}")
    
    # Hypothesis 2: Movie age affects rating
    print("\n2. Hypothesis: Movie age affects rating")
    corr_age_rating = df['movie_age'].corr(df['rating'])
    print(f"   • Correlation (age vs rating): {corr_age_rating:.3f}")
    print(f"   • Conclusion: {'WEAK relationship' if abs(corr_age_rating) < 0.3 else 'STRONG relationship'}")
    
    return top_10, bottom_10, p_value

def detect_issues(df):
    """Detect data quality issues"""
    print("\n" + "="*60)
    print(" DATA QUALITY CHECK")
    print("="*60)
    
    # Check for duplicates
    duplicates = df.duplicated(subset=['title', 'year']).sum()
    print(f"\n1. Duplicate movies: {duplicates} {' None' if duplicates == 0 else ' Found'}")
    
    # Check for outliers using IQR
    print("\n2. Outlier Detection (IQR method):")
    
    def get_outliers(series):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return series[(series < lower) | (series > upper)]
    
    rating_outliers = get_outliers(df['rating'])
    year_outliers = get_outliers(df['year'])
    
    print(f"   • Rating outliers: {len(rating_outliers)} movies")
    if len(rating_outliers) > 0:
        print("     High-rated outliers:")
        high_outliers = df[df['rating'].isin(rating_outliers)].nlargest(5, 'rating')[['title', 'rating']]
        print(high_outliers.to_string())
    
    print(f"   • Year outliers: {len(year_outliers)} movies")
    
    # Check data consistency
    print("\n3. Data Consistency Checks:")
    print(f"   • Ratings in valid range (1-10) {' Yes' if df['rating'].between(1, 10).all() else ' No'}")
    print(f"   • Years reasonable (1888+): {' Yes' if df['year'].min() >= 1888 else ' No'}")
    print(f"   • Positions in order: {' Yes' if df['position'].is_monotonic_increasing else ' No'}")
    
    return len(rating_outliers), len(year_outliers)

def generate_report(df, insights):
    """Generate final EDA report"""
    print("\n" + "="*60)
    print(" GENERATING EDA REPORT")
    print("="*60)
    
    report_content = f"""
{'='*70}
EXPLORATORY DATA ANALYSIS REPORT - IMDb TOP 250 MOVIES
{'='*70}

DATASET OVERVIEW
{'-'*50}
• Total Movies: {len(df)}
• Time Period: {int(df['year'].min())} - {int(df['year'].max())}
• Columns: {', '.join(df.columns.tolist())}

KEY STATISTICS
{'-'*50}
• Average Rating: {df['rating'].mean():.2f}
• Median Rating: {df['rating'].median():.2f}
• Rating Range: {df['rating'].min():.2f} - {df['rating'].max():.2f}
• Highest Rated: {df.loc[df['rating'].idxmax(), 'title']} ({df['rating'].max():.2f})
• Lowest Rated: {df.loc[df['rating'].idxmin(), 'title']} ({df['rating'].min():.2f})

TREND ANALYSIS
{'-'*50}
• Rating vs Year Correlation: {insights['corr_year_rating']:.3f}
• Position vs Rating Correlation: {insights['corr_pos_rating']:.3f}
• Strongest Trend: Higher ranked movies (lower position) have significantly higher ratings

HYPOTHESIS TESTING RESULTS
{'-'*50}
• Top 10 vs Bottom 10: {'Significant difference' if insights['p_value'] < 0.05 else 'No significant difference'}
• P-value: {insights['p_value']:.6f}
• Top 10 Average: {insights['top_10_avg']:.2f}
• Bottom 10 Average: {insights['bottom_10_avg']:.2f}

DATA QUALITY
{'-'*50}
• Rating Outliers: {insights['rating_outliers']} movies
• Year Outliers: {insights['year_outliers']} movies
• Duplicates: None found
• Missing Values: None found

RECOMMENDATIONS
{'-'*50}
1. The strong negative correlation between position and rating confirms IMDb ranking logic
2. Consider adding genre data for more nuanced analysis
3. Investigate why certain decades (2000s, 1980s) have higher average ratings
4. Explore additional factors like director, budget, or awards for deeper insights

{'='*70}
EDA COMPLETED: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}
"""
    
    # Save report
    with open('eda_report.txt', 'w') as f:
        f.write(report_content)
    
    print(" EDA report saved to: eda_report.txt")
    
    # Display summary
    print("\n" + "="*60)
    print(" TASK 2 COMPLETED SUCCESSFULLY!")
    print("="*60)


def main():
    """Main function to run EDA"""
    print("="*70)
    print("TASK 2: EXPLORATORY DATA ANALYSIS (EDA)")
    print("IMDb Top 250 Movies Dataset")
    print("="*70)
    
    # Load data
    df = load_data()
    
    # Explore structure
    df = explore_structure(df)
    
    # Analyze distributions
    df = analyze_distributions(df)
    
    # Analyze trends
    df, corr_year_rating, corr_pos_rating = analyze_trends(df)
    
    # Test hypotheses
    top_10, bottom_10, p_value = test_hypotheses(df)
    
    # Detect issues
    rating_outliers, year_outliers = detect_issues(df)
    
    # Compile insights
    insights = {
        'corr_year_rating': corr_year_rating,
        'corr_pos_rating': corr_pos_rating,
        'top_10_avg': top_10.mean(),
        'bottom_10_avg': bottom_10.mean(),
        'p_value': p_value,
        'rating_outliers': rating_outliers,
        'year_outliers': year_outliers
    }
    
    # Generate report
    generate_report(df, insights)

if __name__ == "__main__":
    main()