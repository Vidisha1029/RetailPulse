import streamlit as st
import pandas as pd

# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

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

# ======================================================
# CSS
# ======================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1200px;
}

.main-title{
    font-size:58px;
    font-weight:800;
    color:#0F172A;
    margin-bottom:0px;
}

.subtitle{
    font-size:22px;
    color:#2563EB;
    font-weight:600;
    margin-bottom:25px;
}

.description{
    font-size:18px;
    color:#475569;
    line-height:1.8;
}

.card{
    background:#F8FAFC;
    border-radius:15px;
    padding:22px;
    border:1px solid #E2E8F0;
    margin-bottom:15px;
}

.card-title{
    font-size:20px;
    font-weight:700;
    color:#1E293B;
}

.card-text{
    color:#475569;
    font-size:16px;
}

.metric-box{
    background:#F8FAFC;
    border-radius:12px;
    padding:15px;
    text-align:center;
    border:1px solid #E2E8F0;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("📊 RetailPulse")

st.sidebar.markdown("""
### AI-Powered Retail Decision Platform

Navigate through the dashboards:

- 👨‍💼 Executive Dashboard
- 👥 Customer Analysis
- 📈 Sales Analytics
- 📦 Product Analysis
- 🔮 Revenue Forecasting
""")

# ======================================================
# HERO SECTION
# ======================================================

st.markdown(
    '<div class="main-title">📊 RetailPulse</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Retail Decision Platform</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="description">

RetailPulse is an end-to-end Business Intelligence platform developed using
<b>Python</b>, <b>Pandas</b>, <b>Plotly</b>, and <b>Streamlit</b>.

The application transforms more than <b>one million retail transactions</b>
into meaningful business insights through interactive dashboards,
customer analytics, product performance analysis, sales monitoring,
and revenue forecasting.

</div>
""", unsafe_allow_html=True)

# ======================================================
# KPI CARDS
# ======================================================

st.divider()

total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()
total_customers = df["Customer ID"].nunique()
countries = df["Country"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Revenue",
    f"${total_revenue:,.0f}"
)

c2.metric(
    "📦 Orders",
    f"{total_orders:,}"
)

c3.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

c4.metric(
    "🌍 Countries",
    f"{countries}"
)

# ======================================================
# PROJECT OVERVIEW
# ======================================================

st.divider()

st.header("📌 Project Overview")

st.info("""
RetailPulse enables organizations to monitor business performance,
understand customer behaviour, evaluate product performance,
analyze sales trends, and forecast future revenue for better
decision-making.
""")

# ======================================================
# FEATURES
# ======================================================

st.divider()

st.header("🚀 Dashboard Modules")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
<div class="card">
<div class="card-title">👨‍💼 Executive Dashboard</div>

<div class="card-text">

• Business KPIs

• Revenue Trends

• Country Performance

• Business Overview

</div>

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
<div class="card-title">👥 Customer Analysis</div>

<div class="card-text">

• Customer Segmentation

• RFM Analysis

• Top Customers

• Customer Insights

</div>

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
<div class="card-title">📈 Sales Analytics</div>

<div class="card-text">

• Monthly Sales

• Sales Trends

• Order Analysis

• Seasonal Performance

</div>

</div>
""", unsafe_allow_html=True)

with col2:

    st.markdown("""
<div class="card">
<div class="card-title">📦 Product Analysis</div>

<div class="card-text">

• Best Selling Products

• Revenue Contribution

• Product Performance

• Product Insights

</div>

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
<div class="card-title">🔮 Revenue Forecasting</div>

<div class="card-text">

• Machine Learning

• Revenue Prediction

• Trend Forecast

• Business Planning

</div>

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
<div class="card-title">📊 Interactive Dashboards</div>

<div class="card-text">

• Dynamic Filters

• Interactive Charts

• Real-Time Insights

• Executive Reporting

</div>

</div>
""", unsafe_allow_html=True)

# ======================================================
# DATASET
# ======================================================

st.divider()

st.header("📂 Dataset Information")

left, right = st.columns(2)

with left:

    st.markdown("""
### Dataset

- Source: UCI Online Retail II Dataset
- Transactions: 1,067,371+
- Customers: 5,199
- Countries: 37
- Period: 2009–2011
""")

with right:

    st.markdown("""
### Technologies

- Python
- Pandas
- Plotly
- Streamlit
- Machine Learning
- Time Series Forecasting
""")

# ======================================================
# BUSINESS VALUE
# ======================================================

st.divider()

st.header("🎯 Business Value")

st.success("""
RetailPulse empowers organizations to:

✔ Improve customer retention

✔ Identify high-value customers

✔ Optimize product strategy

✔ Track sales performance

✔ Forecast future revenue

✔ Make data-driven business decisions
""")

# ======================================================
# FOOTER
# ======================================================

st.divider()

st.caption(
    "Developed by Vidisha More • Python • Pandas • Plotly • Streamlit"
)