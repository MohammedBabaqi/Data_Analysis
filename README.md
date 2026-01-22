# 📊 SmartTech Orders Analysis & Sales Insights

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-red.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-v1.5+-green.svg)](https://pandas.pydata.org/)

An end-to-end data engineering and analytics pipeline designed to transform raw global sales data into actionable business intelligence. This project features a robust data cleaning pipeline, deep exploratory analysis, and a high-performance interactive dashboard.

![Dashboard Screenshothttps://raw.githubusercontent.com/MohammedBabaqi/Data_Analysis/main/Images/1.png)

## 📁 Project Architecture

- **`dashboard.py`**: The main interactive application built with Streamlit and Plotly for real-time data exploration.
- **`Data_Analysis_notebook.ipynb`**: A comprehensive end-to-end pipeline covering ingestion, cleaning, and advanced EDA.
- **`Data/Raw_Data/`**: Contains the source `Orders.csv` with multi-row metadata and unstructured headers.
- **`Data/Cleaned_Data/`**: Storage for the production-ready `Cleaned_Orders.csv` used by the dashboard.

## 📓 Technical Deep Dive (Notebook Insights)

The data transformation layer (detailed in the Jupyter Notebook) handles several critical data integrity steps:

- **Metadata Striping**: Programmatically removing the top 3 metadata rows and identifying the correct header row at index 3.
- **Null Value Logic**: Strategic handling of `NaN` values in `Discount` (filled with 0) and `Status` (normalized to readable strings).
- **Type Correction**: Converting `Order Date` with robust datetime parsing and ensuring numeric precision for `Total Price` calculations.
- **Feature Engineering**: Deriving geographic coordinates and formatting currency for reliable visualization.

## 🚀 Interactive Dashboard Features

The Streamlit dashboard provides high-level insights into sales performance with real-time interactivity:

### 📈 Advanced Visuals

- **Sales Trend Analysis**: Monthly revenue flow with seasonality detection.
- **Product Treemap**: Comprehensive hierarchy view from Category down to Sub-Category.
- **Value Efficiency**: Price vs. Quantity correlation using dynamic scatter plots.
- **Geographic Order Density**: Interactive map highlighting global market penetration.

### ⚙️ Smart Filters

- **Date Range**: Customize the timeframe for all metrics and visuals.
- **Multi-select Filters**: Filter by Country, Category, and Order Status.
- **Select All Functionality**: Quickly toggle all options for faster exploration.

### 💎 Key Metrics (KPIs)

- **Total Revenue**: At-a-glance formatted revenue (e.g., $22M).
- **Total Orders**: Total volume of transaction.
- **Total Quantity**: Units sold across all regions.
- **Avg Order Value**: Average revenue generated per unique Order ID.

## 📓 Data Analysis Notebook

The Jupyter Notebook serves as the foundation for the project, covering:

- **Data Ingestion**: Handling metadata rows and initial loading.
- **Data Cleaning**: Fixing column headers, handling missing values (NaNs in Discount/Status), and data type conversion.
- **Exploration**: Initial insights and data quality checks using `pandas` and `matplotlib`.

## 🛠️ Installation & Execution

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd "Data Analysis"
   ```
2. Install dependencies:
   ```bash
   pip install -r requiremetns.txt
   ```

### Running the Dashboard

Execute the following command in your terminal:

```bash
streamlit run dashboard.py
```

## 🛠 Built With

- **Streamlit**: Application framework.
- **Plotly**: Dynamic and interactive charts.
- **Pandas**: Data manipulation and processing.
- **Jupyter**: Exploratory analysis.

---

_Created and maintained as part of the Data Analysis project._
