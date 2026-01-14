# Task 2: Exploratory Data Analysis (EDA) - IMDb Movies Dataset

##  Project Overview
This project performs comprehensive Exploratory Data Analysis on the IMDb Top 250 movies dataset extracted in Task 1.

##  Task Requirements Completed

### 1. **Asked Meaningful Questions**
Before analysis, I defined 8 key questions:
1. What is the distribution of movie ratings?
2. How have movie ratings changed over decades?
3. Is there a relationship between movie age and rating?
4. What is the distribution across different decades?
5. Are there any outliers in ratings or years?
6. What are the top 10 highest and lowest rated movies?
7. How is the quality_score distributed?
8. Is there correlation between numerical features?

### 2. **Explored Data Structure**
- Dataset: 250 movies, 11 columns
- Data types: Numerical (position, year, rating, movie_age, quality_score) and Categorical (title, rating_category, decade, imdb_id)
- Missing values: None found
- Basic statistics calculated for all numerical columns

### 3. **Identified Trends and Patterns**
- **Rating Distribution**: Most movies (77.2%) rated "Very Good" (8.0-8.4)
- **Decade Trends**: 2000s have highest average rating (8.43), 2020s lowest (8.12)
- **Position-Rating Relationship**: Strong negative correlation (-0.838)
- **Year-Rating Relationship**: Weak positive correlation (0.207)

### 4. **Tested Hypotheses**
1. **Hypothesis 1**: Movies from earlier decades have higher ratings
   - **Result**: NOT SUPPORTED (r=0.207, newer movies have slightly higher ratings)
   
2. **Hypothesis 2**: Top 10 movies are significantly better than bottom 10
   - **Result**: SUPPORTED (p < 0.05, significant difference)
   - Top 10 avg: 9.01, Bottom 10 avg: 8.15
   
3. **Hypothesis 3**: Older movies have higher ratings
   - **Result**: NOT SUPPORTED (r=-0.207, older movies have slightly lower ratings)

### 5. **Detected Data Issues**
- **Outliers**: 8 high-rated movies identified as outliers (all 9.0+ ratings)
- **Duplicates**: None found
- **Data Consistency**: All ratings valid, years reasonable, positions in order
- **Missing Values**: None found

##  Key Findings

### Statistical Summary:
- **Average Rating**: 8.31
- **Rating Range**: 8.00 - 9.30
- **Highest Rated**: The Shawshank Redemption (9.30)
- **Lowest Rated**: The Incredibles (8.00)
- **Most Common Decade**: 1990s

### Correlation Analysis:
- **Strong Negative**: Position ↔ Rating (-0.838)
- **Perfect Negative**: Year ↔ Movie Age (-1.000)
- **Weak Positive**: Year ↔ Rating (0.207)
- **Positive**: Rating ↔ Quality Score (0.540)

##  Technical Implementation

### **Files Structure:**
- `Task_02_EDA.py` - Main EDA script
- `eda_report.txt` - Complete analysis report
- `eda_visualizations/` - All generated charts
- `README_task2.md` - This documentation

### **Libraries Used:**
- Pandas: Data manipulation
- NumPy: Numerical operations
- Matplotlib & Seaborn: Data visualization
- SciPy: Statistical testing

### **Visualizations Created:**
1. Rating distribution histogram and box plot
2. Year distribution histogram
3. Rating vs Year scatter plot with trend line
4. Rating vs Position scatter plot
5. Average rating by decade bar chart
6. Correlation heatmap

##  How to Run

### Prerequisites:
```bash
pip install pandas numpy matplotlib seaborn scipy