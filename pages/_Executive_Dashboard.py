import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_data,
    apply_filters,
    load_css,
    page_header,
    section_header,
    insight_box,
    footer
)

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)

load_css()



# ======================================================
# LOAD DATA
# ======================================================

df = load_data()
df = apply_filters(df)

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ======================================================
# HERO
# ======================================================

st.markdown(
    """
<div style="
background:linear-gradient(135deg,#0F172A,#1E3A8A);
padding:45px;
border-radius:20px;
margin-bottom:30px;
color:white;
">

<h1 style="
margin:0;
font-size:42px;
font-weight:700;
color:white;
">
👨‍💼 Executive Dashboard
</h1>

<p style="
font-size:18px;
line-height:1.8;
margin-top:15px;
color:#E5E7EB;
">
Monitor business performance through executive KPIs, revenue trends,
customer insights, product performance and geographic sales analysis
from one unified dashboard.
</p>

</div>
""",
unsafe_allow_html=True,
)

# ======================================================
# EXECUTIVE SNAPSHOT
# ======================================================

# ======================================================
# EXECUTIVE SNAPSHOT
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style="
font-size:32px;
font-weight:700;
color:#0F172A;
margin-bottom:5px;
">
📊 Executive Snapshot
</h2>

<p style="
color:#64748B;
font-size:17px;
margin-bottom:25px;
">
Key business metrics for the selected period.
</p>
""", unsafe_allow_html=True)

# ======================================================
# KPI METRICS
# ======================================================

total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()
total_customers = df["Customer ID"].nunique()
total_products = df["Description"].nunique()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        label="💰 Revenue",
        value=f"${total_revenue:,.0f}"
    )

with c2:
    st.metric(
        label="📦 Orders",
        value=f"{total_orders:,}"
    )

with c3:
    st.metric(
        label="👥 Customers",
        value=f"{total_customers:,}"
    )

with c4:
    st.metric(
        label="🛍 Products",
        value=f"{total_products:,}"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# BUSINESS INSIGHT
# ======================================================

st.markdown("""
<div style="
background:#EEF4FF;
border-left:6px solid #2563EB;
padding:22px;
border-radius:16px;
margin-top:10px;
margin-bottom:30px;
">

<h4 style="margin-top:0;color:#1E3A8A;">
💡 Business Insight
</h4>

<p style="font-size:17px;color:#334155;line-height:1.8;margin-bottom:0;">

The Executive Dashboard provides a high-level summary of business performance.
Use these KPIs to evaluate revenue, customer growth, order volume and product
performance before exploring detailed analytics below.

</p>

</div>
""", unsafe_allow_html=True)

# ======================================================
# MONTHLY REVENUE
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
background:white;
padding:28px;
border-radius:20px;
box-shadow:0 8px 24px rgba(15,23,42,.08);
border:1px solid #E5E7EB;
">

<h3 style="margin-top:0;color:#0F172A;">
📈 Monthly Revenue Trend
</h3>

<p style="
color:#64748B;
margin-bottom:20px;
">
Track how revenue changes throughout the year and identify seasonal sales patterns.
</p>

</div>
""", unsafe_allow_html=True)

monthly = (
    df.groupby("Month")["Revenue"]
      .sum()
      .reset_index()
)

month_names = {
    1:"Jan",2:"Feb",3:"Mar",4:"Apr",
    5:"May",6:"Jun",7:"Jul",8:"Aug",
    9:"Sep",10:"Oct",11:"Nov",12:"Dec"
}

monthly["Month"] = monthly["Month"].map(month_names)

fig = px.line(
    monthly,
    x="Month",
    y="Revenue",
    markers=True
)

fig.update_traces(
    line=dict(color="#2563EB", width=4),
    marker=dict(size=9, color="#1D4ED8")
)

fig.update_layout(

    template="plotly_white",

    height=500,

    margin=dict(l=20,r=20,t=20,b=20),

    paper_bgcolor="white",

    plot_bgcolor="white",

    xaxis_title="",

    yaxis_title="Revenue ($)",

    font=dict(size=15),

    hovermode="x unified"
)

st.plotly_chart(fig, width="stretch")

# ======================================================
# REVENUE BY COUNTRY
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
background:white;
padding:28px;
border-radius:20px;
box-shadow:0 8px 24px rgba(15,23,42,.08);
border:1px solid #E5E7EB;
">

<h3 style="margin-top:0;color:#0F172A;">
🌍 Revenue by Country
</h3>

<p style="color:#64748B;">
Top performing markets based on total revenue.
</p>

</div>
""", unsafe_allow_html=True)

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
    text="Revenue",
    color="Revenue",
    color_continuous_scale="Blues"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    height=520,
    margin=dict(l=20,r=20,t=20,b=20),
    paper_bgcolor="white",
    plot_bgcolor="white",
    coloraxis_showscale=False,
    yaxis=dict(autorange="reversed"),
    xaxis_title="Revenue ($)",
    yaxis_title=""
)

st.plotly_chart(fig, width="stretch")

# ======================================================
# TOP PRODUCTS
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
background:white;
padding:28px;
border-radius:20px;
box-shadow:0 8px 24px rgba(15,23,42,.08);
border:1px solid #E5E7EB;
">

<h3 style="margin-top:0;color:#0F172A;">
🏆 Top 10 Products
</h3>

<p style="color:#64748B;">
Highest revenue generating products.
</p>

</div>
""", unsafe_allow_html=True)

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
    height=600,
    margin=dict(l=20,r=20,t=20,b=20),
    paper_bgcolor="white",
    plot_bgcolor="white",
    coloraxis_showscale=False,
    yaxis=dict(autorange="reversed"),
    xaxis_title="Revenue ($)",
    yaxis_title=""
)

st.plotly_chart(fig, width="stretch")