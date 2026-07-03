import streamlit as st
import pandas as pd
import plotly.express as px

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
    footer,
    two_columns
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Inventory Optimization",
    page_icon="📦",
    layout="wide"
)

load_css()

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()
df = apply_filters(df)

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# =====================================================
# HERO
# =====================================================

hero(
    "📦 Inventory Optimization",
    "Optimizing Inventory Through Sales Behaviour",
    """
Inventory Optimization helps businesses maintain the right products in the right quantities.

This dashboard identifies fast-moving products, classifies inventory using the ABC method,
analyzes seasonal demand patterns and highlights products that require strategic inventory planning.
"""
)

spacer(2)

# =====================================================
# INVENTORY KPIs
# =====================================================

section(
    "📊 Inventory Overview",
    "Key inventory and demand indicators."
)

total_units = int(df["Quantity"].sum())

active_products = df["Description"].nunique()

monthly_demand = (
    df.groupby("MonthName")["Quantity"]
      .sum()
      .mean()
)

avg_velocity = (
    df.groupby("Description")["Quantity"]
      .sum()
      .mean()
)

fastest_product = (
    df.groupby("Description")["Quantity"]
      .sum()
      .idxmax()
)

kpi_row([

{
"title":"📦 Units Sold",
"value":f"{total_units:,}"
},

{
"title":"🛍 Active Products",
"value":f"{active_products:,}"
},

{
"title":"📈 Avg Monthly Demand",
"value":f"{monthly_demand:,.0f}"
},

{
"title":"⚡ Avg Product Velocity",
"value":f"{avg_velocity:,.0f}"
},

{
"title":"🏆 Fastest Moving Product",
"value":(
    fastest_product[:18] + "..."
    if len(fastest_product) > 18
    else fastest_product
)
}

])

insight_box(
"""
These KPIs summarize overall product movement and demand. Products with consistently high sales velocity should receive greater inventory attention to reduce the risk of stockouts.
"""
)

spacer(2)

# =====================================================
# ABC INVENTORY CLASSIFICATION
# =====================================================

section(
    "📦 ABC Inventory Classification",
    "Prioritize inventory using cumulative revenue contribution."
)

# -----------------------------------------------------
# Product Revenue
# -----------------------------------------------------

abc = (
    df.groupby("ShortDescription", as_index=False)
      .agg(
          Revenue=("Revenue", "sum")
      )
      .sort_values("Revenue", ascending=False)
)

# Revenue %

abc["Revenue %"] = (
    abc["Revenue"] /
    abc["Revenue"].sum()
)

abc["Cumulative %"] = abc["Revenue %"].cumsum()

# ABC Classification

def classify(value):

    if value <= 0.70:
        return "A"

    elif value <= 0.90:
        return "B"

    else:
        return "C"

abc["Category"] = abc["Cumulative %"].apply(classify)

abc_summary = (
    abc.groupby("Category", as_index=False)
       .agg(
           Products=("ShortDescription", "count"),
           Revenue=("Revenue", "sum")
       )
)

chart_title(
    "ABC Inventory Classification",
    "Products classified according to cumulative revenue contribution."
)

fig = px.bar(
    abc_summary,
    x="Category",
    y="Products",
    color="Category",
    text="Products",
    category_orders={"Category": ["A", "B", "C"]},
    color_discrete_map={
        "A": "#2563EB",
        "B": "#F59E0B",
        "C": "#94A3B8"
    }
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    height=450,
    xaxis_title="Inventory Category",
    yaxis_title="Number of Products",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

a_products = abc_summary.loc[
    abc_summary["Category"] == "A",
    "Products"
].iloc[0]

insight_box(
f"""
Category A contains **{a_products}** products that contribute the majority of business revenue. These products require the highest inventory control, frequent replenishment and close monitoring to prevent stockouts.
"""
)

recommendation_box(
"""
Focus forecasting and replenishment efforts on Category A products. Review Category C items periodically for slow movement, excess inventory or possible discontinuation to improve inventory efficiency.
"""
)

spacer(2)

# =====================================================
# MONTHLY PRODUCT DEMAND HEATMAP
# =====================================================

section(
    "🔥 Seasonal Product Demand",
    "Analyze monthly demand patterns for the highest-selling products."
)

# -----------------------------------------------------
# Top 15 Products by Quantity
# -----------------------------------------------------

top_products = (
    df.groupby("ShortDescription")["Quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(15)
      .index
)

heatmap_df = (
    df[df["ShortDescription"].isin(top_products)]
      .groupby(["ShortDescription", "MonthName"])["Quantity"]
      .sum()
      .reset_index()
)

# Keep months in calendar order
month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

heatmap_df["MonthName"] = pd.Categorical(
    heatmap_df["MonthName"],
    categories=month_order,
    ordered=True
)

heatmap_pivot = (
    heatmap_df
    .pivot(
        index="ShortDescription",
        columns="MonthName",
        values="Quantity"
    )
    .fillna(0)
)

chart_title(
    "Monthly Demand Heatmap",
    "Darker colors indicate higher sales volume."
)

fig = px.imshow(
    heatmap_pivot,
    aspect="auto",
    color_continuous_scale="Blues",
    labels=dict(
        color="Units Sold"
    )
)

fig.update_layout(
    template="plotly_white",
    height=650,
    xaxis_title="Month",
    yaxis_title="Product"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

insight_box(
"""
The heatmap reveals seasonal demand patterns across the highest-selling products.
Products with recurring peaks should be stocked proactively before high-demand months,
while consistently low-demand products require less aggressive inventory planning.
"""
)

recommendation_box(
"""
Align purchasing and replenishment schedules with seasonal demand.
Increase safety stock before peak periods for high-demand products and reduce excess inventory for products with consistently low demand.
"""
)

spacer(2)

