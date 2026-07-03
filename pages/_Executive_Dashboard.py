import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    page_title="Executive Dashboard",
    page_icon="👔",
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

    "👔 Executive Dashboard",

    "Business Performance Overview",

    """
This dashboard provides a high-level overview of business performance,
highlighting revenue trends, customer activity, product performance and
strategic business KPIs that support executive decision making.
"""

)

spacer(2)

# =====================================================
# EXECUTIVE KPIs
# =====================================================

section(
    "📌 Executive KPIs",
    "Key performance indicators summarizing business performance."
)

total_revenue = df["Revenue"].sum()

orders = df["Invoice"].nunique()

customers = df["Customer ID"].nunique()

products = df["Description"].nunique()

avg_order_value = total_revenue / orders

revenue_per_customer = total_revenue / customers

kpi_row([

{
"title":"💰 Revenue",
"value":f"${total_revenue:,.0f}"
},

{
"title":"🧾 Orders",
"value":f"{orders:,}"
},

{
"title":"👥 Customers",
"value":f"{customers:,}"
},

{
"title":"🛍 Products",
"value":f"{products:,}"
},

{
"title":"🛒 Avg Order Value",
"value":f"${avg_order_value:,.2f}"
},

{
"title":"💳 Revenue / Customer",
"value":f"${revenue_per_customer:,.2f}"
}

])

insight_box(
"""
These KPIs provide an immediate overview of business health. Executives can quickly assess sales performance, customer reach and purchasing behaviour before exploring detailed analytics.
"""
)

spacer(1)

# =====================================================
# EXECUTIVE HIGHLIGHTS
# =====================================================

section(
    "⭐ Executive Highlights",
    "Automatically generated insights from the current business performance."
)
# =====================================================
# MONTHLY REVENUE TREND
# =====================================================

section(
    "📈 Revenue Performance",
    "Monitor monthly revenue to understand business growth and seasonal sales patterns."
)

# -----------------------------------------------------
# Monthly Revenue
# -----------------------------------------------------

monthly_revenue = (
    df.groupby(pd.Grouper(key="InvoiceDate", freq="ME"))
      .agg(
          Revenue=("Revenue", "sum"),
          Orders=("Invoice", "nunique")
      )
      .reset_index()
)

monthly_revenue["Period"] = (
    monthly_revenue["InvoiceDate"]
    .dt.strftime("%b %Y")
)

average_revenue = monthly_revenue["Revenue"].mean()

chart_title(
    "Monthly Revenue Trend",
    "Revenue generated each month with the average monthly revenue benchmark."
)

fig = px.line(
    monthly_revenue,
    x="InvoiceDate",
    y="Revenue",
    markers=True
)

fig.update_traces(
    line=dict(width=4),
    marker=dict(size=8),
    hovertemplate=
    "<b>%{x|%b %Y}</b><br>" +
    "Revenue: $%{y:,.0f}<extra></extra>"
)

fig.add_hline(
    y=average_revenue,
    line_dash="dash",
    line_color="red",
    annotation_text="Average Revenue",
    annotation_position="top left"
)

fig.update_layout(

    template="plotly_white",

    height=500,

    hovermode="x unified",

    xaxis_title="Month",

    yaxis_title="Revenue ($)",

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    )

)

st.plotly_chart(
    fig,
    use_container_width=True
)

insight_box(
f"""
The average monthly revenue is **${average_revenue:,.0f}**.

Months above the benchmark represent stronger-than-average business performance,
while months below the benchmark may indicate seasonality, reduced customer
activity or opportunities for targeted sales campaigns.
"""
)

recommendation_box(
"""
Use the monthly revenue trend to identify seasonal demand patterns.
Business planning, marketing campaigns and inventory allocation should be
scheduled ahead of historically high-performing months to maximize revenue.
"""
)

spacer(2)
# -----------------------------
# Best Revenue Month
# -----------------------------

month_summary = (
    df.groupby(["Month", "MonthName"])["Revenue"]
      .sum()
      .reset_index()
      .sort_values("Month")
)

best_month = month_summary.loc[
    month_summary["Revenue"].idxmax()
]

# -----------------------------
# Best Country
# -----------------------------

country_summary = (
    df.groupby("Country")["Revenue"]
      .sum()
)

best_country = country_summary.idxmax()

# -----------------------------
# Best Product
# -----------------------------

product_summary = (
    df.groupby("Description")["Revenue"]
      .sum()
)

best_product = product_summary.idxmax()

# -----------------------------
# Revenue Per Customer
# -----------------------------

avg_customer = total_revenue / customers

col1, col2 = st.columns(2)

with col1:

    recommendation_box(f"""

**🏆 Highest Revenue Month**

**{best_month['MonthName']}**

Revenue Generated

**${best_month['Revenue']:,.0f}**

""")

    recommendation_box(f"""

**🌍 Best Performing Country**

**{best_country}**

""")

with col2:

    recommendation_box(f"""

**🛍 Highest Revenue Product**

**{best_product}**

""")

    recommendation_box(f"""

**👤 Average Revenue Per Customer**

**${avg_customer:,.2f}**

""")

spacer(2)


# =====================================================
# REVENUE TREND
# =====================================================

section(
    "📈 Business Growth",
    "Monitor monthly revenue performance to identify business growth and seasonal trends."
)

monthly_revenue = (
    df.groupby(["Month", "MonthName"])["Revenue"]
      .sum()
      .reset_index()
      .sort_values("Month")
)

chart_title(
    "Monthly Revenue Trend",
    "Revenue performance over time."
)

fig = px.line(
    monthly_revenue,
    x="MonthName",
    y="Revenue",
    markers=True
)

fig.update_traces(
    line=dict(width=4),
    marker=dict(size=8)
)

fig.update_layout(
    template="plotly_white",
    height=450,
    xaxis_title="Month",
    yaxis_title="Revenue ($)",
    margin=dict(l=20,r=20,t=20,b=20)
)

st.plotly_chart(fig, use_container_width=True)

insight_box(
"""
This trend highlights the overall business growth pattern across the year.
Sudden peaks indicate seasonal demand, promotional campaigns or holiday purchasing behaviour.
"""
)

spacer(2)

# =====================================================
# COUNTRY PERFORMANCE
# =====================================================

section(
    "🌍 Country Performance",
    "Compare revenue contribution across the highest-performing markets."
)

country_revenue = (
    df.groupby("Country", as_index=False)
      .agg(
          Revenue=("Revenue", "sum"),
          Orders=("Invoice", "nunique"),
          Customers=("Customer ID", "nunique")
      )
      .sort_values("Revenue", ascending=False)
      .head(10)
)

chart_title(
    "Top 10 Countries by Revenue",
    "Markets generating the highest business revenue."
)

fig = px.bar(
    country_revenue,
    x="Revenue",
    y="Country",
    orientation="h",
    color="Revenue",
    text="Revenue",
    color_continuous_scale="Blues"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    height=450,
    coloraxis_showscale=False,
    yaxis=dict(autorange="reversed"),
    xaxis_title="Revenue ($)",
    yaxis_title="Country",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------
# Business Insight
# -----------------------------------------------------

top_country = country_revenue.iloc[0]

country_share = (
    top_country["Revenue"] /
    country_revenue["Revenue"].sum()
) * 100

insight_box(
f"""
**{top_country['Country']}** is the highest-performing market among the top 10 countries,
contributing **{country_share:.1f}%** of the revenue shown in this chart.

This indicates a strong market presence while also highlighting opportunities
to strengthen sales performance in lower-performing regions.
"""
)

recommendation_box(
"""
Prioritize customer retention and inventory availability in the highest-performing
markets while designing targeted marketing campaigns for emerging markets to
reduce dependence on a single geographic region.
"""
)

spacer(2)

# =====================================================
# PRODUCT PARETO ANALYSIS
# =====================================================

section(
    "🛍 Product Revenue Concentration",
    "Identify whether a small number of products contribute the majority of business revenue."
)

# -----------------------------------------------------
# Aggregate Product Revenue
# -----------------------------------------------------

pareto = (
    df.groupby("Description", as_index=False)
      .agg(
          Revenue=("Revenue", "sum")
      )
      .sort_values("Revenue", ascending=False)
)

# Top 20 products for readability
pareto = pareto.head(20)

# Cumulative Revenue %

pareto["Cumulative Revenue"] = pareto["Revenue"].cumsum()

pareto["Cumulative %"] = (
    pareto["Cumulative Revenue"] /
    pareto["Revenue"].sum()
) * 100

chart_title(
    "Pareto Analysis of Product Revenue",
    "Identify products contributing most of the revenue."
)

# -----------------------------------------------------
# Figure
# -----------------------------------------------------

fig = go.Figure()

# Revenue Bars

fig.add_trace(

    go.Bar(

        x=pareto["Description"],

        y=pareto["Revenue"],

        name="Revenue"

    )

)

# Cumulative %

fig.add_trace(

    go.Scatter(

        x=pareto["Description"],

        y=pareto["Cumulative %"],

        mode="lines+markers",

        name="Cumulative %",

        yaxis="y2"

    )

)

# 80% Reference Line

fig.add_hline(

    y=80,

    yref="y2",

    line_dash="dash",

    annotation_text="80% Threshold"

)

fig.update_layout(

    template="plotly_white",

    height=520,

    xaxis=dict(
        tickangle=-45,
        title="Products"
    ),

    yaxis=dict(
        title="Revenue ($)"
    ),

    yaxis2=dict(

        title="Cumulative %",

        overlaying="y",

        side="right",

        range=[0,110]

    ),

    hovermode="x unified"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# Insight
# -----------------------------------------------------

products_for_80 = (
    pareto[pareto["Cumulative %"] <= 80]
    .shape[0]
)

insight_box(
f"""
The Pareto analysis shows that approximately **{products_for_80}** of the top-performing
products account for around **80% of the revenue** within this visualization.

This indicates that revenue is concentrated among a relatively small set of products,
making them strategically important for inventory planning, pricing, and promotional campaigns.
"""
)

recommendation_box(
"""
Prioritize inventory availability, supplier management and promotional activities
for the highest-contributing products. Products with lower revenue contribution
should be reviewed for optimization, bundling or discontinuation based on business objectives.
"""
)

spacer(2)

# =====================================================
# AVERAGE ORDER VALUE TREND
# =====================================================

section(
    "🛒 Average Order Value",
    "Monitor customer spending behaviour over time."
)

monthly_aov = (
    df.groupby(pd.Grouper(key="InvoiceDate", freq="ME"))
      .agg(
          Revenue=("Revenue", "sum"),
          Orders=("Invoice", "nunique")
      )
      .reset_index()
)

monthly_aov["AOV"] = (
    monthly_aov["Revenue"] /
    monthly_aov["Orders"]
)

chart_title(
    "Average Order Value by Month",
    "Average revenue generated from each order."
)

fig = px.line(
    monthly_aov,
    x="InvoiceDate",
    y="AOV",
    markers=True
)

fig.update_traces(
    line=dict(width=4),
    marker=dict(size=8)
)

fig.update_layout(
    template="plotly_white",
    height=420,
    xaxis_title="Month",
    yaxis_title="Average Order Value ($)",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

insight_box(
"""
Average Order Value (AOV) measures the average amount spent per transaction.
A rising AOV indicates customers are purchasing higher-value products or larger baskets, while a declining AOV may signal increased discounting or changes in purchasing behaviour.
"""
)

recommendation_box(
"""
Monitor AOV alongside revenue and order volume. If order counts remain stable but AOV declines, consider product bundling, upselling strategies and promotional adjustments to increase customer spend per transaction.
"""
)

spacer(2)


