import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, apply_filters
st.title("Sales_Analytics")

st.info("""
This visualization tracks monthly revenue trends to identify seasonal patterns,
growth opportunities, and changes in business performance over time.
""")
df = load_data()
df = apply_filters(df)
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
    text="Revenue",
    title="Top 10 Countries by Revenue"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

# Display highest revenue at the top
fig.update_yaxes(
    categoryorder="array",
    categoryarray=country_sales["Country"][::-1]
)

fig.update_layout(
    xaxis_title="Revenue ($)",
    yaxis_title="Country",
    showlegend=False,
    template="plotly_white",
    margin=dict(l=20, r=20, t=50, b=20)
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
    orientation="h",
    text="Revenue"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_yaxes(
    categoryorder="total ascending"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.divider()

st.subheader("📅 Revenue by Quarter")

quarter_sales = (
    df.groupby("Quarter")["Revenue"]
      .sum()
      .reset_index()
      .sort_values("Revenue", ascending=False)
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
    x="Revenue",
    y="Quarter",
    orientation="h",
    text="Revenue",
    title="Revenue by Quarter"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_yaxes(
    categoryorder="array",
    categoryarray=quarter_sales["Quarter"][::-1]
)

fig.update_layout(
    xaxis_title="Revenue ($)",
    yaxis_title="Quarter",
    template="plotly_white"
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