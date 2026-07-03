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
    page_title="Product Intelligence",
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
    st.warning("No data available.")
    st.stop()

# =====================================================
# HERO
# =====================================================

hero(

    "📦 Product Intelligence",

    "Understanding Product Performance and Demand",

    """
Product Intelligence helps identify the products that generate the highest
business value, understand demand patterns and support pricing, merchandising
and inventory decisions.

This dashboard evaluates product performance using revenue, sales quantity,
pricing behaviour and seasonal demand.
"""

)

spacer(2)

# =====================================================
# PRODUCT KPIs
# =====================================================

section(
    "📊 Product Overview",
    "Key performance indicators describing product performance."
)

total_products = df["Description"].nunique()

total_quantity = df["Quantity"].sum()

avg_product_price = df["Price"].mean()

avg_product_revenue = (
    df.groupby("Description")["Revenue"]
      .sum()
      .mean()
)

top_product = (
    df.groupby("Description")["Revenue"]
      .sum()
      .idxmax()
)

kpi_row([

{
"title":"📦 Products",
"value":f"{total_products:,}"
},

{
"title":"🛒 Units Sold",
"value":f"{total_quantity:,.0f}"
},

{
"title":"💲 Avg Price",
"value":f"${avg_product_price:.2f}"
},

{
"title":"💰 Avg Product Revenue",
"value":f"${avg_product_revenue:,.0f}"
},

{
"title":"🏆 Best Product",
"value":top_product[:18] + "..."
if len(top_product) > 18
else top_product
}

])

insight_box(
"""
These KPIs summarize the overall product portfolio, highlighting product count,
sales volume, pricing behaviour and the highest-performing product by revenue.
"""
)

spacer(2)

# =====================================================
# TOP REVENUE PRODUCTS
# =====================================================

section(
    "🏆 Top Revenue Products",
    "Identify the products generating the highest business revenue."
)

top_products = (
    df.groupby("ShortDescription", as_index=False)
      .agg(
          Revenue=("Revenue", "sum"),
          Quantity=("Quantity", "sum")
      )
      .sort_values("Revenue", ascending=False)
      .head(10)
)

# Percentage contribution
total_revenue = top_products["Revenue"].sum()
top_products["Contribution (%)"] = (
    top_products["Revenue"] / total_revenue * 100
)

chart_title(
    "Top 10 Products by Revenue",
    "Highest revenue-generating products and their contribution."
)

fig = px.bar(
    top_products,
    x="Revenue",
    y="ShortDescription",
    orientation="h",
    color="Revenue",
    text="Contribution (%)",
    color_continuous_scale="Blues"
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    coloraxis_showscale=False,
    yaxis=dict(autorange="reversed"),
    xaxis_title="Revenue ($)",
    yaxis_title="Product",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

top_product = top_products.iloc[0]

insight_box(
f"""
**{top_product['ShortDescription']}** is the highest revenue-generating product,
contributing **{top_product['Contribution (%)']:.1f}%** of the revenue among the top 10 products.

These products should receive priority in pricing strategy, merchandising and inventory planning.
"""
)

spacer(2)

# =====================================================
# PRODUCT PERFORMANCE MATRIX
# =====================================================

section(
    "📈 Product Performance Matrix",
    "Compare demand, revenue and pricing strategy across products."
)

product_matrix = (
    df.groupby("ShortDescription", as_index=False)
      .agg(
          Revenue=("Revenue", "sum"),
          Quantity=("Quantity", "sum"),
          AvgPrice=("Price", "mean")
      )
)

# Keep top 300 products by revenue for readability
product_matrix = (
    product_matrix
    .sort_values("Revenue", ascending=False)
    .head(300)
)

chart_title(
    "Revenue vs Quantity",
    "Color represents the average selling price."
)

fig = px.scatter(

    product_matrix,

    x="Quantity",

    y="Revenue",

    color="AvgPrice",

    hover_name="ShortDescription",

    hover_data={
        "Revenue":":,.0f",
        "Quantity":True,
        "AvgPrice":":.2f"
    },

    color_continuous_scale="Viridis"
)

# Median reference lines

fig.add_vline(
    x=product_matrix["Quantity"].median(),
    line_dash="dash",
    line_color="gray"
)

fig.add_hline(
    y=product_matrix["Revenue"].median(),
    line_dash="dash",
    line_color="gray"
)

fig.update_layout(

    template="plotly_white",

    height=600,

    xaxis_title="Units Sold",

    yaxis_title="Revenue ($)",

    coloraxis_colorbar_title="Average Price"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

insight_box(
"""
Products in the upper-right quadrant combine high demand with high revenue and should be prioritized for inventory planning and marketing. High-revenue products with lower sales volume may represent premium offerings that benefit from targeted promotion rather than broad discounting.
"""
)

recommendation_box(
"""
Develop differentiated strategies for each product group:

• Protect inventory for star products.

• Promote premium products through targeted campaigns.

• Increase basket size for high-volume, low-revenue products.

• Review low-demand, low-revenue products for optimization or discontinuation.
"""
)

spacer(2)