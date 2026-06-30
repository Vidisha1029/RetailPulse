import streamlit as st
import pandas as pd
import plotly.express as px
st.title("📊 Sales Analytics")

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_online_retail.csv")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
    df["Hour"] = df["InvoiceDate"].dt.hour
    return df

df = load_data()
monthly_sales = (
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
    12: "Dec"
}

monthly_sales["Month"] = monthly_sales["Month"].map(month_names)
st.subheader("📈 Monthly Revenue Trend")

st.line_chart(
    monthly_sales,
    x="Month",
    y="Revenue"
)
st.divider()

st.subheader("🌍 Revenue by Country")

country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    country_sales,
    x="Revenue",
    y="Country",
    orientation="h",
    title="Top 10 Countries by Revenue"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🏆 Top 10 Products by Revenue")
top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig = px.bar(
    top_products,
    x="Revenue",
    y="Description",
    orientation="h"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("📅 Revenue by Quarter")
quarter_sales = (
    df.groupby("Quarter")["Revenue"]
    .sum()
    .reset_index()
)
quarter_names = {
    1: "Q1",
    2: "Q2",
    3: "Q3",
    4: "Q4"
}
quarter_sales["Quarter"] = quarter_sales["Quarter"].map(quarter_names)
fig = px.bar(
    quarter_sales,
    x="Quarter",
    y="Revenue"
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("📅 Revenue by Year")
year_sales = (
    df.groupby("Year")["Revenue"]
      .sum()
      .reset_index()
)
fig = px.bar(
    year_sales,
    x="Year",
    y="Revenue",
    title="Revenue by Year",
    text_auto=".2s"
)

fig.update_xaxes(type="category")
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("👥 Top 10 Customers by Revenue")

customer_sales = (
    df.groupby("Customer ID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)
fig = px.bar(
    customer_sales,
    x="Revenue",
    y="Customer ID",
    orientation="h",
    title="Top 10 Customers by Revenue",
    text_auto=".2s"
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("📅 Revenue by Day of Week")

day_sales = (
    df.groupby("DayOfWeek")["Revenue"]
    .sum()
    .reset_index()

)
day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]
fig = px.bar(
    day_sales,
    x="DayOfWeek",
    y="Revenue",
    title="Revenue by Day of Week",
    text_auto=".2s"
)
fig.update_xaxes(
    categoryorder="array",
    categoryarray=day_order
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🕒 Revenue by Hour")
hour_sales = (
    df.groupby("Hour")["Revenue"]
    .sum()
    .reset_index()
)
fig = px.line(
    hour_sales,
    x="Hour",
    y="Revenue",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("📦 Monthly Orders Trend")

monthly_orders = (
    df.groupby("Month")["Invoice"]
    .nunique()
    .reset_index(name="Orders")
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
    12: "Dec"
}

monthly_orders["Month"] = monthly_orders["Month"].map(month_names)

fig = px.line(
    monthly_orders,
    x="Month",
    y="Orders",
    title="Monthly Orders Trend",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)