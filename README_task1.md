# Task 1: Web Scraping - IMDb Top 250 Movies

## 📌 Project Overview
This project demonstrates web scraping by collecting data from IMDb's Top 250 movies and creating custom datasets for analysis.

## ✅ Task Requirements Completed

### 1. **Used Python Libraries**
- BeautifulSoup4 for HTML parsing
- Requests for HTTP requests
- Pandas for data manipulation
- NumPy for numerical operations

### 2. **Collected Data from Public Web Pages**
- Source: https://www.imdb.com/chart/top/
- Data collected: Movie titles, years, ratings, IMDb IDs
- Total movies extracted: 250

### 3. **Handled HTML Structure and Navigation**
- Successfully extracted JSON-LD structured data
- Parsed complex HTML with multiple methods
- Implemented fallback strategies for data extraction

### 4. **Created Custom Dataset**
- **Basic Dataset** (`imdb_clean_basic.csv`): 6 columns, 250 movies
- **Custom Dataset** (`imdb_clean_custom.csv`): 10 columns with enhanced fields
- Added derived fields: rating categories, movie age, decade, quality score

### 5. **Analysis-Ready Dataset**
- Dataset structured for trend analysis
- Clean, organized data with no messy JSON
- Ready for Tasks 2, 3, and 4 of the internship

## 🛠️ Technical Implementation

### **Files Structure:**
- `imdb_scraper_final.py` - Main scraping script
- `requirements.txt` - Python dependencies
- `imdb_clean_basic.csv` - Basic scraped data (250 movies)
- `imdb_clean_custom.csv` - Enhanced dataset for analysis
- `README_task1.md` - This documentation file

### **Key Features:**
- Multiple data extraction methods (JSON-LD, HTML parsing)
- Error handling and data validation
- Realistic data generation for missing values
- Clean, organized CSV output

## 🚀 How to Run

### Prerequisites:
```bash
pip install -r requirements.txt