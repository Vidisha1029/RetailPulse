import streamlit as st
import pandas as pd
import plotly.express as px

st.title("👨‍💼 Executive Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_online_retail.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()
total_customers = df["Customer ID"].nunique()
total_products = df["Description"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Orders", f"{total_orders:,}")
col3.metric("👥 Customers", f"{total_customers:,}")
col4.metric("🛍 Products", f"{total_products:,}")

st.divider()
st.subheader("📈 Monthly Revenue")

monthly = (
    df.groupby("Month")["Revenue"]
      .sum()
      .reset_index()
)

month_names = {
1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"
}

monthly["Month"] = monthly["Month"].map(month_names)

fig = px.line(
    monthly,
    x="Month",
    y="Revenue",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

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
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🏆 Top Products")

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
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🎯 Customer Segmentation")

customer = (
    df.groupby("Customer ID")["Revenue"]
      .sum()
      .reset_index()
)

customer["Segment"] = pd.qcut(
    customer["Revenue"],
    q=3,
    labels=["Low","Medium","High"]
)

segment = (
    customer.groupby("Segment")
    .size()
    .reset_index(name="Customers")
)

fig = px.pie(
    segment,
    names="Segment",
    values="Customers",
    hole=0.4
)

st.plotly_chart(fig, use_container_width=True)

