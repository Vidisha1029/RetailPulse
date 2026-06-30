import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📦 Product Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_online_retail.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()
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
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()
st.subheader("📦 Top 10 Products by Quantity Sold")

product_quantity = (
    df.groupby("Description")["Quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    product_quantity,
    x="Quantity",
    y="Description",
    orientation="h",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)
st.divider()
st.subheader("📈 Product Revenue Distribution")

product_distribution = (
    df.groupby("Description")["Revenue"]
      .sum()
      .reset_index()
)

fig = px.histogram(
    product_distribution,
    x="Revenue",
    nbins=40
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
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)