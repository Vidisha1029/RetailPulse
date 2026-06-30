import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, apply_filters

st.title("👥 Customer Analysis")

# ===========================
# Load & Filter Data
# ===========================

df = load_data()
df = apply_filters(df)

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ===========================
# KPIs
# ===========================

total_customers = df["Customer ID"].nunique()
total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()

average_customer_value = (
    total_revenue / total_customers
    if total_customers > 0 else 0
)

average_orders = (
    total_orders / total_customers
    if total_customers > 0 else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "👥 Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "💰 Avg Revenue / Customer",
    f"${average_customer_value:,.2f}"
)

col3.metric(
    "🛒 Avg Orders / Customer",
    f"{average_orders:.2f}"
)

# ===========================
# Top Customers
# ===========================

customer_sales = (
    df.groupby("Customer ID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    customer_sales,
    x="Customer ID",
    y="Revenue",
    title="Top 10 Customers by Revenue",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# Customer Spend Distribution
# ===========================

st.divider()

st.subheader("💰 Customer Spend Distribution")

customer_spend = (
    df.groupby("Customer ID")["Revenue"]
      .sum()
      .reset_index()
)

fig = px.histogram(
    customer_spend,
    x="Revenue",
    nbins=50,
    title="Customer Spend Distribution"
)

fig.update_xaxes(range=[0, 50000])

st.plotly_chart(fig, use_container_width=True)

# ===========================
# Customer Segmentation
# ===========================

st.divider()

st.subheader("🎯 Customer Segmentation")

customer_spend["Segment"] = pd.qcut(
    customer_spend["Revenue"],
    q=3,
    labels=["Low Value", "Medium Value", "High Value"],
    duplicates="drop"
)

segment_count = (
    customer_spend.groupby("Segment")
    .size()
    .reset_index(name="Customers")
)

fig = px.pie(
    segment_count,
    names="Segment",
    values="Customers",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# Revenue by Segment
# ===========================

st.divider()

st.subheader("💵 Revenue by Customer Segment")

segment_revenue = (
    customer_spend.groupby("Segment")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.bar(
    segment_revenue,
    x="Segment",
    y="Revenue",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# Top Customers by Orders
# ===========================

st.divider()

st.subheader("📦 Top Customers by Number of Orders")

customer_orders = (
    df.groupby("Customer ID")["Invoice"]
      .nunique()
      .sort_values(ascending=False)
      .head(10)
      .reset_index(name="Orders")
)

fig = px.bar(
    customer_orders,
    x="Orders",
    y="Customer ID",
    orientation="h",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# RFM Analysis
# ===========================

st.divider()

st.subheader("⭐ RFM Analysis")

latest_date = df["InvoiceDate"].max()

rfm = (
    df.groupby("Customer ID")
      .agg(
          Recency=("InvoiceDate", lambda x: (latest_date - x.max()).days),
          Frequency=("Invoice", "nunique"),
          Monetary=("Revenue", "sum")
      )
      .reset_index()
)

rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    q=5,
    labels=[5,4,3,2,1],
    duplicates="drop"
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1,2,3,4,5],
    duplicates="drop"
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    q=5,
    labels=[1,2,3,4,5],
    duplicates="drop"
).astype(int)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Recency",
    f"{rfm['Recency'].mean():.0f} Days"
)

col2.metric(
    "Average Frequency",
    f"{rfm['Frequency'].mean():.1f}"
)

col3.metric(
    "Average Monetary",
    f"${rfm['Monetary'].mean():,.2f}"
)

def segment_customer(row):
    if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
        return "Champions"

    elif row["R_Score"] >= 3 and row["F_Score"] >= 3:
        return "Loyal Customers"

    elif row["R_Score"] >= 3 and row["F_Score"] <= 2:
        return "Potential Loyalists"

    elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
        return "At Risk"

    else:
        return "Lost Customers"

rfm["Segment"] = rfm.apply(segment_customer, axis=1)

# ===========================
# Segment Pie Chart
# ===========================

st.divider()

st.subheader("🏆 Customer Segments")

segment_count = (
    rfm.groupby("Segment")
       .size()
       .reset_index(name="Customers")
)

fig = px.pie(
    segment_count,
    names="Segment",
    values="Customers",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

# ===========================
# Champions
# ===========================

st.divider()

st.subheader("🥇 Top 10 Champions")

champions = (
    rfm[rfm["Segment"] == "Champions"]
       .sort_values("Monetary", ascending=False)
       .head(10)
)

st.dataframe(champions, use_container_width=True)