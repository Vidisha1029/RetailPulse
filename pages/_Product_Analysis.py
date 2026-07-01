import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, apply_filters

st.title("📦 Product Analysis")


st.info("""
This dashboard evaluates product performance by analyzing revenue generation,
sales volume, and product demand. These insights help businesses identify
best-selling products, optimize inventory planning, and support strategic
product decisions.
""")

df = load_data()
df = apply_filters(df)
total_products = df["Description"].nunique()
average_product_revenue = df.groupby("Description")["Revenue"].sum().mean()
average_quantity = df["Quantity"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("📦 Products", f"{total_products:,}")
col2.metric("💰 Avg Product Revenue", f"${average_product_revenue:,.2f}")
col3.metric("🛒 Avg Quantity Sold", f"{average_quantity:.2f}")
st.divider()

st.subheader("🏆 Top 10 Products by Revenue")

product_sales = (
    df.groupby("Description")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    product_sales,
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

# Highest revenue at the top
fig.update_yaxes(
    categoryorder="total ascending"
)

fig.update_layout(
    xaxis_title="Revenue ($)",
    yaxis_title="Product",
    showlegend=False,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📦 Top 10 Products by Quantity Sold")

top_quantity = (
    df.groupby("Description")["Quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    top_quantity,
    x="Quantity",
    y="Description",
    orientation="h",
    text="Quantity",
    title="Top 10 Products by Quantity Sold"
)

fig.update_traces(
    textposition="outside"
)

fig.update_yaxes(
    categoryorder="total ascending"
)

fig.update_layout(
    xaxis_title="Units Sold",
    yaxis_title="Product"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("📋 Most Frequently Ordered Products")

product_orders = (
    df.groupby("Description")["Invoice"]
      .nunique()
      .sort_values(ascending=False)
      .head(10)
      .reset_index(name="Orders")
)

fig = px.bar(
    product_orders,
    x="Orders",
    y="Description",
    orientation="h",
    text="Orders",
    title="Top 10 Most Frequently Ordered Products"
)

fig.update_traces(
    textposition="outside"
)

# Display highest value at the top
fig.update_yaxes(
    categoryorder="total ascending"
)

fig.update_layout(
    xaxis_title="Number of Orders",
    yaxis_title="Product",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)