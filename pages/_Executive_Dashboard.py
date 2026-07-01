import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, apply_filters

st.title("👨‍💼 Executive Dashboard")
st.info("""
This dashboard provides an executive overview of business performance,
highlighting key metrics, revenue trends, and geographic sales performance
to support strategic decision-making.
""")

# ===========================
# Load Data
# ===========================

df = load_data()
df = apply_filters(df)

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ===========================
# KPI Cards
# ===========================

total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()
total_customers = df["Customer ID"].nunique()
total_products = df["Description"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Orders", f"{total_orders:,}")
col3.metric("👥 Customers", f"{total_customers:,}")
col4.metric("🛍 Products", f"{total_products:,}")

# ===========================
# Monthly Revenue
# ===========================

st.divider()
st.subheader("📈 Monthly Revenue")

monthly = (
    df.groupby("Month")["Revenue"]
      .sum()
      .reset_index()
)

month_names = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

monthly["Month"] = monthly["Month"].map(month_names)

fig = px.line(
    monthly,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig, width="stretch")

# ===========================
# Revenue by Country
# ===========================

st.divider()
st.subheader("🌍 Revenue by Country")

country = (
    df.groupby("Country")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    country,
    x="Revenue",
    y="Country",
    orientation="h",
    text="Revenue",
    title="Top 10 Countries by Revenue"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Revenue ($)",
    yaxis_title="Country",
    yaxis=dict(autorange="reversed"),   # Highest revenue at the top
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# Top Products
# ===========================

st.divider()

st.subheader("🏆 Top 10 Products")

products = (
    df.groupby("Description")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    products,
    x="Revenue",
    y="Description",
    orientation="h",
    text="Revenue",
    title="Top 10 Products by Revenue"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Revenue ($)",
    yaxis_title="Product",
    yaxis=dict(autorange="reversed"),   # Highest revenue appears at the top
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

