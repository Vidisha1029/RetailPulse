import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, apply_filters
st.title("Revenue Forecasting")
st.info("""
This visualization tracks monthly revenue trends to identify seasonal patterns,
growth opportunities, and changes in business performance over time.
""")
df = load_data()
df = apply_filters(df)
monthly_sales = (
    df.groupby(pd.Grouper(key="InvoiceDate", freq="ME"))["Revenue"]
      .sum()
      .reset_index()
)
monthly_sales["Forecast"] = (
    monthly_sales["Revenue"]
    .rolling(3, min_periods=1)
    .mean()
)
fig = px.line(
    monthly_sales,
    x="InvoiceDate",
    y=["Revenue", "Forecast"],
    title="Actual Revenue vs Forecast"
)

st.plotly_chart(fig, use_container_width=True)
last_date = monthly_sales["InvoiceDate"].max()

future_dates = pd.date_range(
    start=last_date,
    periods=7,
    freq="ME"
)[1:]
future = pd.DataFrame({
    "InvoiceDate": future_dates
})

future["Forecast"] = monthly_sales["Forecast"].iloc[-1]
st.subheader("📅 Next 6 Months Forecast")

st.dataframe(future)
fig = px.line(
    future,
    x="InvoiceDate",
    y="Forecast",
    markers=True,
    title="Forecasted Revenue"
)

st.plotly_chart(fig, use_container_width=True)