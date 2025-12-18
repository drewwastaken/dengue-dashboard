# 🦟 Dengue Hotspot Heatmap Dashboard

**Spatiotemporal Analysis of Dengue Cases in Metro Manila to Predict Outbreaks**

---

## 📊 Project Overview

This interactive dashboard provides visualization and analysis of dengue fever cases across 11 cities in Metro Manila (NCR) from January 2019 to February 2020. The system enables health authorities and researchers to identify dengue hotspots, track temporal trends, and predict potential outbreaks.

### 🎯 Key Objectives

- **Early Outbreak Detection**: Visual identification of case spikes by location and time
- **Geographic Targeting**: Identify high-risk areas for focused health interventions
- **Seasonal Pattern Recognition**: Analyze temporal trends to predict high-risk periods
- **Data-Driven Decision Making**: Transform raw epidemiological data into actionable insights

---

## ✨ Features

### Interactive Filters
- 📅 **Year Selection**: Compare data across 2019-2020
- 📆 **Month Selection**: Analyze specific months or ranges
- 🏙️ **City Selection**: Focus on specific NCR cities
- 🔢 **Case Threshold**: Filter by minimum case counts

### Visualizations
1. **🗺️ Interactive Hotspot Map** - Geographic distribution of cases with bubble sizing
2. **📊 Top 5 Affected Cities** - Horizontal bar chart ranking
3. **📈 Monthly Trends** - Line chart showing temporal patterns by city
4. **🌡️ Seasonal Analysis** - Bar chart highlighting outbreak seasons
5. **⚖️ Cases vs Deaths** - Comparative analysis by city
6. **📅 Year-over-Year** - Grouped bar chart for trend comparison

### Key Metrics
- Total dengue cases
- Total deaths
- Average cases per city
- Case fatality rate (%)

---

### Data Dictionary

| Column | Type | Description |
|--------|------|-------------|
| `Month` | Text | Calendar month of reported cases |
| `Year` | Integer | Year of report (2019-2020) |
| `City` | Text | NCR city location |
| `Region` | Text | Administrative region (NCR) |
| `Dengue_Cases` | Integer | Total confirmed dengue cases |
| `Dengue_Deaths` | Integer | Number of dengue-related deaths |

---

## 📦 Project Structure

```
dengue-dashboard/
│
├── app.py                
├── dengue_data.csv      
├── requirements.txt     
└── README.md             
```

---

## 📸 Screenshots

### Dashboard Overview
*Interactive filters and key metrics at a glance*

### Hotspot Map
*Geographic visualization of dengue cases across Metro Manila*

### Temporal Analysis
*Monthly trends and seasonal patterns*

---

## 🎓 Academic Context

**Course**: Health Informatics (ITE3)  
**Instructor**: Engr. Val Patrick Fabregas, MTA  
**Institution**: Nicholas Andrew Alcantar
**Year**: BSIT-3A

This project demonstrates the application of data visualization and health informatics principles to real-world public health challenges.

---

## 🙏 Acknowledgments

- **Kaggle** - https://www.kaggle.com
- **Streamlit Community** - For the excellent visualization framework
- **Engr. Val Patrick Fabregas** - For guidance and instruction

---

## 📧 Contact

**Developer**: Nicholas Andrew Alcantara
**Email**: nicholasandrewalcantara0@gmail.com
**GitHub**: drewwastaken
