import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet

from utils import (
    load_data,
    apply_filters,
    load_css,
    hero,
    section,
    chart_title,
    kpi_row,
    insight_box,
    recommendation_box,
    spacer,
    footer
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Revenue Forecasting",
    page_icon="📈",
    layout="wide"
)

load_css()

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()
df = apply_filters(df)

if df.empty:
    st.warning("No data available.")
    st.stop()

    # =====================================================
# HERO
# =====================================================

hero(
    "📈 Revenue Forecasting",
    "Predicting Future Business Performance",
    """
Revenue forecasting enables businesses to anticipate future sales trends,
optimize inventory planning, support budgeting and make proactive business
decisions using historical transaction data.

This dashboard uses Meta Prophet to forecast future monthly revenue and
identify expected business trends.
"""
)

spacer(2)

# =====================================================
# PREPARE FORECAST DATA
# =====================================================

section(
    "📊 Revenue Forecast",
    "Monthly revenue aggregated for time-series forecasting."
)

monthly_sales = (
    df.groupby(pd.Grouper(key="InvoiceDate", freq="ME"))
      .agg(
          Revenue=("Revenue", "sum")
      )
      .reset_index()
)

forecast_df = monthly_sales.rename(
    columns={
        "InvoiceDate": "ds",
        "Revenue": "y"
    }
)

# =====================================================
# TRAIN PROPHET MODEL
# =====================================================

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    interval_width=0.95
)

model.fit(forecast_df)

# Forecast next 6 months
future = model.make_future_dataframe(
    periods=6,
    freq="ME"
)

forecast = model.predict(future)

# =====================================================
# FORECAST KPIs
# =====================================================

section(
    "📈 Forecast Summary",
    "Key metrics generated from the forecasting model."
)

historical_revenue = forecast_df["y"].sum()

last_actual = forecast_df.iloc[-1]["y"]

next_month = forecast.iloc[len(forecast_df)]["yhat"]

forecast_growth = (
    (next_month - last_actual) / last_actual
) * 100

kpi_row([
    {
        "title": "💰 Historical Revenue",
        "value": f"${historical_revenue:,.0f}"
    },
    {
        "title": "📅 Last Actual Month",
        "value": f"${last_actual:,.0f}"
    },
    {
        "title": "🔮 Next Month Forecast",
        "value": f"${next_month:,.0f}"
    },
    {
        "title": "📈 Forecast Growth",
        "value": f"{forecast_growth:.1f}%"
    }
])

spacer(2)

# =====================================================
# REVENUE FORECAST
# =====================================================

section(
    "📊 Revenue Forecast",
    "Historical monthly revenue with six-month Prophet forecast."
)

chart_title(
    "Historical Revenue & Forecast",
    "The shaded area represents the 95% prediction interval."
)

fig = go.Figure()

# Historical Revenue
fig.add_trace(
    go.Scatter(
        x=forecast_df["ds"],
        y=forecast_df["y"],
        mode="lines+markers",
        name="Historical Revenue",
        line=dict(width=3)
    )
)

# Forecast
fig.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        mode="lines",
        name="Forecast",
        line=dict(width=3, dash="dash")
    )
)

# Confidence Interval
fig.add_trace(
    go.Scatter(
        x=list(forecast["ds"]) + list(forecast["ds"][::-1]),
        y=list(forecast["yhat_upper"]) + list(forecast["yhat_lower"][::-1]),
        fill="toself",
        fillcolor="rgba(37,99,235,0.15)",
        line=dict(color="rgba(255,255,255,0)"),
        hoverinfo="skip",
        showlegend=True,
        name="95% Confidence Interval"
    )
)

fig.update_layout(
    template="plotly_white",
    height=600,
    xaxis_title="Month",
    yaxis_title="Revenue ($)",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)