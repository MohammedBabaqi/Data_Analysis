import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Orders Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Data Loading function
@st.cache_data
def load_data():
    try:
        file_path = r"./Data/Cleaned_Data/Cleaned_Orders.csv"
        # Load the cleaned data
        df = pd.read_csv(file_path)
        
        # Strip any whitespace from column names just in case
        df.columns = [col.strip() for col in df.columns]
        
        # Convert Order Date to datetime
        df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['Order Date'])
        
        # Handle Column Mapping (Cleaned data uses 'Total Price')
        if 'Total Price' in df.columns:
            df['Total Sales'] = pd.to_numeric(df['Total Price'], errors='coerce')
        
        # Robustly convert all numeric columns
        numeric_cols = ['Quantity', 'Unit Price', 'Discount', 'Total Sales', 'Lat', 'Lng']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Prevent crashes in visualizations by ensuring size values are non-negative
        if 'Total Sales' in df.columns:
            df['Total Sales'] = df['Total Sales'].abs()
        if 'Quantity' in df.columns:
            df['Quantity'] = df['Quantity'].abs()
        
        # Ensure Status is handled as string to match filter logic
        if 'Status' in df.columns:
            df['Status'] = df['Status'].astype(str)
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

if not df.empty:
    try:
        # --- Sidebar ---
        st.sidebar.title("📊 Filter Dashboard")
        st.sidebar.markdown("---")

        # Date Filter
        min_date = df['Order Date'].min().to_pydatetime()
        max_date = df['Order Date'].max().to_pydatetime()
        
        if min_date and max_date:
            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        else:
            st.sidebar.warning("Invalid date range in data.")
            date_range = [datetime(2023,1,1), datetime(2023,12,31)]

        # Helper for "Select All"
        def create_multiselect(label, options, key):
            container = st.sidebar.container()
            select_all = container.checkbox(f"Select All {label}", value=True, key=f"all_{key}")
            if select_all:
                selected = container.multiselect(f"Choose {label}", options, default=options, key=key)
            else:
                selected = container.multiselect(f"Choose {label}", options, key=key)
            return selected

        # Filters with Select All
        selected_countries = create_multiselect("Countries", sorted(df['Country'].unique()), "country_filter")
        selected_categories = create_multiselect("Categories", sorted(df['Category'].unique()), "category_filter")
        selected_status = create_multiselect("Status", sorted(df['Status'].unique()), "status_filter")

        # Filter the dataframe
        mask = (
            (df['Order Date'] >= pd.to_datetime(date_range[0])) & (df['Order Date'] <= pd.to_datetime(date_range[1])) &
            (df['Country'].isin(selected_countries)) &
            (df['Category'].isin(selected_categories)) &
            (df['Status'].isin(selected_status))
        )
        filtered_df = df.loc[mask]

        # Helper to format KPI numbers (e.g., 22M, 10K)
        def format_number(num):
            if num >= 1_000_000:
                return f"${num/1_000_000:.1f}M"
            elif num >= 1_000:
                return f"${num/1_000:.1f}K"
            else:
                return f"${num:.2f}"

        def format_count(num):
            if num >= 1_000_000:
                return f"{num/1_000_000:.1f}M"
            elif num >= 1_000:
                return f"{num/1_000:.1f}K"
            else:
                return f"{int(num)}"

        # --- Main Dashboard ---
        st.title("🚀 Sales Performance Insights")
        st.markdown(f"**Data Overview:** Showing {len(filtered_df):,} orders from {date_range[0]} to {date_range[1]}")

        # KPI Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_revenue = filtered_df['Total Sales'].sum() if not filtered_df.empty else 0
            st.metric("Total Revenue", format_number(total_revenue))
        with col2:
            total_orders = filtered_df['Order ID'].nunique() if not filtered_df.empty else 0
            st.metric("Total Orders", format_count(total_orders))
        with col3:
            total_quantity = filtered_df['Quantity'].sum() if not filtered_df.empty else 0
            st.metric("Total Quantity", format_count(total_quantity))
        with col4:
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            st.metric("Avg Order Value", format_number(avg_order_value))

        st.markdown("---")

        # Row 1: Trends and Category Bar
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.subheader("📈 Sales Trend Over Time")
            if not filtered_df.empty:
                trend_df = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Total Sales'].sum().reset_index()
                trend_df['Order Date'] = trend_df['Order Date'].astype(str)
                fig_trend = px.line(trend_df, x='Order Date', y='Total Sales', markers=True, 
                                    template="plotly_white", color_discrete_sequence=['#007bff'])
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("No data available for the selected filters.")

        with chart_col2:
            st.subheader("🏷️ Sales by Category")
            if not filtered_df.empty:
                category_df = filtered_df.groupby('Category')['Total Sales'].sum().sort_values(ascending=False).reset_index()
                fig_cat = px.bar(category_df, x='Category', y='Total Sales', text_auto='.2s',
                                 template="plotly_white", color='Total Sales', color_continuous_scale='Blues')
                st.plotly_chart(fig_cat, use_container_width=True)

        st.markdown("---")

        # Row 2: Treemap and Scatter Plot
        chart_col3, chart_col4 = st.columns([1, 1.5])

        with chart_col3:
            st.subheader("🌳 Product Hierarchy (Treemap)")
            if not filtered_df.empty:
                fig_tree = px.treemap(filtered_df, path=['Category', 'Sub Category'], values='Total Sales',
                                    color='Total Sales', color_continuous_scale='RdBu')
                st.plotly_chart(fig_tree, use_container_width=True)

        with chart_col4:
            st.subheader("🎯 Price vs Quantity Scatter Plot")
            if not filtered_df.empty:
                fig_scatter = px.scatter(filtered_df, x='Unit Price', y='Quantity', 
                                        size='Total Sales', color='Category', 
                                        hover_name='Item', template="plotly_white",
                                        title="Higher Price vs Volume Correlation")
                st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("---")

        # Row 3: Top Salespersons and Top Cities
        chart_col5, chart_col6 = st.columns(2)

        with chart_col5:
            st.subheader("👤 Top 10 Salespersons")
            if not filtered_df.empty:
                sales_rep_df = filtered_df.groupby('SalesPerson ID')['Total Sales'].sum().sort_values(ascending=False).head(10).reset_index()
                fig_rep = px.pie(sales_rep_df, values='Total Sales', names='SalesPerson ID', hole=0.4,
                                template="plotly_white", color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_rep, use_container_width=True)

        with chart_col6:
            st.subheader("🏙️ Top 10 Cities by Revenue")
            if not filtered_df.empty:
                city_df = filtered_df.groupby('City')['Total Sales'].sum().sort_values(ascending=False).head(10).reset_index()
                fig_city = px.bar(city_df, x='Total Sales', y='City', orientation='h', 
                                template="plotly_white", color='Total Sales', color_continuous_scale='Greens')
                st.plotly_chart(fig_city, use_container_width=True)

        st.markdown("---")

        # Row 4: Map (Full Width)
        st.subheader("🌍 Order Distribution Map")
        if not filtered_df.empty:
            map_df = filtered_df.dropna(subset=['Lat', 'Lng'])
            if not map_df.empty:
                st.map(map_df, latitude='Lat', longitude='Lng', size='Quantity', color='#ff4b4b')
            else:
                st.info("No valid latitude/longitude coordinates available.")
        else:
            st.info("No location data available.")

        # Data Table
        st.subheader("📄 Raw Data View")
        if not filtered_df.empty:
            # Drop columns that might not exist or are sensitive
            cols_to_drop = [c for c in ['Lat', 'Lng', 'Email', 'Phone Number'] if c in filtered_df.columns]
            st.dataframe(filtered_df.drop(columns=cols_to_drop).head(100), use_container_width=True)

        st.markdown("---")
        st.markdown("Dashboard refined by Antigravity AI")
    except Exception as e:
        st.error(f"Dashboard Runtime Error: {e}")
        st.exception(e)
else:
    st.warning("The dataset is empty. Please check the data loading process.")
