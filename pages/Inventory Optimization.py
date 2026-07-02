import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_data,
    apply_filters,
    load_css,
    footer
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
# DARK THEME
# =====================================================

st.markdown("""
<style>

.stApp{
    background:#0F172A;
}

.block-container{
    max-width:1450px;
    padding-top:1.5rem;
}

h1,h2,h3,h4,label,p{
    color:white !important;
}

[data-testid="metric-container"]{
    background:transparent;
    border:none;
    box-shadow:none;
}

.chart-card{

    background:#16213E;

    padding:25px;

    border-radius:20px;

    margin-top:25px;

    margin-bottom:25px;

    border:1px solid #243B6B;

}

.hero{

    background:linear-gradient(135deg,#0F172A,#1E3A8A);

    padding:45px;

    border-radius:24px;

    color:white;

    margin-bottom:25px;

}

.kpi{

    background:#16213E;

    padding:22px;

    border-radius:18px;

    text-align:center;

    border:1px solid #243B6B;

}

.kpi:hover{

    border:1px solid #3B82F6;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()
df = apply_filters(df)

if df.empty:
    st.warning("No data available.")
    st.stop()

# =====================================================
# INVENTORY KPIs
# =====================================================

total_products = df["Description"].nunique()
units_sold = int(df["Quantity"].sum())
inventory_value = df["Revenue"].sum()
orders = df["Invoice"].nunique()

# Dummy inventory status (can later replace with calculations)
reorder_alerts = int(total_products * 0.18)
overstock = int(total_products * 0.10)
stock_ok = total_products - reorder_alerts - overstock

# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero">

<h1 style="
font-size:58px;
margin-bottom:15px;
font-weight:800;
color:white;
">

📦 Inventory Optimization

</h1>

<p style="
font-size:22px;
color:#E2E8F0;
margin-bottom:35px;
">

EOQ • Safety Stock • Reorder Point

</p>

<p style="
font-size:18px;
line-height:1.8;
color:#CBD5E1;
">

Identify inventory risks, optimize stock levels, prevent stock-outs
and improve warehouse efficiency using retail transaction analytics.

</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI ROW
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
<div class="kpi">

<h1>🔴</h1>

<h3 style="color:white;">Reorder Alerts</h3>

<h2 style="color:#F87171;">{reorder_alerts}</h2>

</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
<div class="kpi">

<h1>🟡</h1>

<h3 style="color:white;">Overstock</h3>

<h2 style="color:#FBBF24;">{overstock}</h2>

</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
<div class="kpi">

<h1>🟢</h1>

<h3 style="color:white;">Stock OK</h3>

<h2 style="color:#4ADE80;">{stock_ok}</h2>

</div>
""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
<div class="kpi">

<h1>📦</h1>

<h3 style="color:white;">Products</h3>

<h2 style="color:#60A5FA;">{total_products}</h2>

</div>
""", unsafe_allow_html=True)
    
# =====================================================
# DASHBOARD TABS
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

alerts_tab, analytics_tab, table_tab = st.tabs(
    [
        "🚨 Alerts",
        "📊 Analytics",
        "📋 Full Inventory"
    ]
)

with alerts_tab:

    st.markdown("""
    <div class="chart-card">

    <h2 style="color:white;margin-bottom:8px;">
    🔴 Reorder Alerts
    </h2>

    <p style="color:#CBD5E1;font-size:17px;">
    Products with the highest inventory demand that should be replenished soon.
    </p>

    </div>
    """, unsafe_allow_html=True)

    top_products = (
        df.groupby("Description")["Quantity"]
          .sum()
          .sort_values(ascending=False)
          .head(20)
          .reset_index()
    )

    fig = px.bar(
        top_products,
        x="Description",
        y="Quantity",
        color="Quantity",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#16213E",
        plot_bgcolor="#16213E",
        height=520,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_showscale=False,
        xaxis_title="Products",
        yaxis_title="Units Sold"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Products with the highest sales volume should maintain higher safety stock levels to avoid stock-outs."
    )
with analytics_tab:

    # =====================================================
    # PRODUCT PERFORMANCE
    # =====================================================

    st.markdown("""
    <div class="chart-card">

    <h2 style="color:white;">
    📊 Inventory Analytics
    </h2>

    <p style="color:#CBD5E1;">
    Analyze inventory movement, product demand and warehouse performance.
    </p>

    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # Top Revenue Products
    # -------------------------------------------------

    revenue_products = (
        df.groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        revenue_products,
        x="Revenue",
        y="Description",
        orientation="h",
        color="Revenue",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#16213E",
        plot_bgcolor="#16213E",
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(fig, width="stretch")

    st.success(
        "High revenue products should always receive priority during inventory replenishment."
    )

    st.divider()

    # -------------------------------------------------
    # Inventory by Country
    # -------------------------------------------------

    country = (
        df.groupby("Country")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        country,
        x="Quantity",
        y="Country",
        orientation="h",
        color="Quantity",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#16213E",
        plot_bgcolor="#16213E",
        height=450,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(fig, width="stretch")

    st.info(
        "Countries with consistently high demand require optimized warehouse allocation."
    )

    st.divider()

    # -------------------------------------------------
    # Monthly Demand
    # -------------------------------------------------

    monthly = (
        df.groupby("Month")["Quantity"]
        .sum()
        .reset_index()
    )

    month_map = {
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

    monthly["Month"] = monthly["Month"].map(month_map)

    fig = px.line(
        monthly,
        x="Month",
        y="Quantity",
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#16213E",
        plot_bgcolor="#16213E",
        height=420,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig, width="stretch")

    st.success(
        "Monthly demand trends help forecast future inventory requirements."
    )
# =====================================================
# FULL INVENTORY
# =====================================================

with table_tab:

    st.markdown("""
    <div class="chart-card">

    <h2 style="color:white;">
    📋 Inventory Details
    </h2>

    <p style="color:#CBD5E1;">
    Explore product-level inventory information, quantities sold and revenue contribution.
    </p>

    </div>
    """, unsafe_allow_html=True)

    inventory_table = (
        df.groupby("Description")
          .agg(
              Total_Quantity=("Quantity", "sum"),
              Revenue=("Revenue", "sum"),
              Orders=("Invoice", "nunique")
          )
          .reset_index()
          .sort_values("Revenue", ascending=False)
    )

    inventory_table["Revenue"] = inventory_table["Revenue"].map(
        lambda x: f"${x:,.2f}"
    )

    st.dataframe(
        inventory_table,
        use_container_width=True,
        hide_index=True,
        height=600
    )

    st.success(
        "Use this table to identify high-performing products and support inventory planning decisions."
    )

    footer()

