# 📊 SmartTech Orders Analysis & Sales Insights Dashboard

A comprehensive data analysis project focused on cleaning, exploring, and visualizing global sales order data. This repository features an interactive Streamlit dashboard and a detailed Jupyter Notebook for exploratory data analysis (EDA).

## 📁 Project Structure

- **`dashboard.py`**: The main interactive application built with Streamlit.
- **`Data_Analysis_notebook.ipynb`**: Exploratory Data Analysis (EDA) notebook detailing the cleaning and initial discovery process.
- **`Orders.csv`**: The raw dataset containing global sales information.

## 🚀 Interactive Dashboard Features

The Streamlit dashboard provides high-level insights into sales performance with real-time interactivity:

### 📈 Visualizations
- **Sales Trends**: Visualize monthly revenue growth and seasonal patterns.
- **Product Hierarchy (Treemap)**: Exploratory view of Categories and Sub-Categories performance.
- **Price vs. Quantity Scatter Plot**: Analyze the correlation between unit pricing and sales volume.
- **Salesperson Performance**: A deep dive into top sales representatives.
- **Geographic Mapping**: Interactive world map showing global order distribution.
- **City-level Analysis**: Top 10 cities by revenue contribution.

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

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- Pandas
- Plotly

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd "Data Analysis"
   ```
2. Install dependencies:
   ```bash
   pip install streamlit pandas plotly
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
*Created and maintained as part of the Data Analysis project.*
