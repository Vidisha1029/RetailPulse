import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(
    "data/cleaned_online_retail_small.csv",
    low_memory=False
)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()

df = load_data()
# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📊 RetailPulse")

st.sidebar.markdown("""
### AI-Powered Retail Decision Platform

Navigate using the pages on the left.
""")

# -----------------------------
# HOME PAGE
# -----------------------------
st.title("📈 RetailPulse")

st.subheader("AI-Powered Retail Decision Platform")

st.write("""
RetailPulse is an end-to-end Retail Analytics solution built using Python,
Power BI concepts, Machine Learning, and Streamlit.

This platform helps businesses:

• Understand customer behaviour

• Monitor sales performance

• Identify top-performing products

• Forecast future revenue

• Make data-driven business decisions
""")

# -----------------------------
# KPI SECTION
# -----------------------------

total_revenue = df["Revenue"].sum()

total_orders = df["Invoice"].nunique()

total_customers = df["Customer ID"].nunique()

average_order_value = total_revenue / total_orders

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "📦 Orders",
    f"{total_orders:,}"
)

col3.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

col4.metric(
    "🛒 Avg Order Value",
    f"${average_order_value:,.2f}"
)

st.divider()

st.subheader("Dataset Preview")

st.dataframe(df.head())


st.divider()

st.subheader("📈 Monthly Revenue Trend")
monthly_sales = (
    df.groupby("Month")["Revenue"]
      .sum()
      .reset_index()
)
st.line_chart(
    monthly_sales,
    x="Month",
    y="Revenue"
)
st.divider()

st.subheader("🏆 Top 10 Products by Revenue")

top_products = (
    df.groupby("Description")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)
st.bar_chart(top_products)
