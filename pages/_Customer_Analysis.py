import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_data,
    apply_filters,
    load_css,
    insight_box,
    footer
)

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Customer Analysis",
    page_icon="👥",
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
# HERO SECTION
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

👥 Customer Analysis

</h1>

<p style="
font-size:18px;
line-height:1.8;
margin-top:15px;
color:#E5E7EB;
">

Understand customer purchasing behaviour using RFM analysis,
identify high-value customers,
measure customer value,
and discover opportunities to improve retention and long-term profitability.

</p>

</div>
""",
unsafe_allow_html=True,
)

# ======================================================
# CUSTOMER SNAPSHOT
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style="
font-size:32px;
font-weight:700;
color:#0F172A;
margin-bottom:5px;
">
📊 Customer Snapshot
</h2>

<p style="
color:#64748B;
font-size:17px;
margin-bottom:25px;
">
A quick overview of customer value and purchasing activity.
</p>
""", unsafe_allow_html=True)

# ======================================================
# KPI METRICS
# ======================================================

total_customers = df["Customer ID"].nunique()
total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()

avg_customer_value = (
    total_revenue / total_customers
    if total_customers else 0
)

avg_orders = (
    total_orders / total_customers
    if total_customers else 0
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

with c2:
    st.metric(
        "💰 Avg Revenue / Customer",
        f"${avg_customer_value:,.2f}"
    )

with c3:
    st.metric(
        "🛒 Avg Orders / Customer",
        f"{avg_orders:.2f}"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# BUSINESS INSIGHT
# ======================================================

insight_box(
"""
Customer analysis helps identify your most valuable customers,
understand purchasing behaviour, and recognize opportunities to improve
customer retention and long-term revenue growth through data-driven decisions.
"""
)

# ======================================================
# TOP CUSTOMERS BY REVENUE
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
🏆 Top Customers by Revenue
</h3>

<p style="color:#64748B;">
Identify the highest-value customers based on total revenue contribution.
</p>

</div>
""", unsafe_allow_html=True)

customer_sales = (
    df.groupby("Customer ID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

customer_sales["Customer ID"] = (
    customer_sales["Customer ID"]
    .astype(int)
    .astype(str)
)

fig = px.bar(
    customer_sales,
    x="Revenue",
    y="Customer ID",
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
    height=500,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=20,r=20,t=20,b=20),
    coloraxis_showscale=False,
    yaxis=dict(
        autorange="reversed",
        title=""
    ),
    xaxis_title="Revenue ($)"
)

st.plotly_chart(fig, width="stretch")

insight_box(
"""
A small group of customers contributes a significant portion of total revenue.
Protecting these relationships through loyalty programs and personalized offers can
have a substantial impact on long-term business performance.
"""
)


# ======================================================
# TOP CUSTOMERS BY ORDERS
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
📦 Top Customers by Number of Orders
</h3>

<p style="color:#64748B;">
Customers with the highest purchasing frequency across all transactions.
</p>

</div>
""", unsafe_allow_html=True)

customer_orders = (
    df.groupby("Customer ID")["Invoice"]
      .nunique()
      .sort_values(ascending=False)
      .head(10)
      .reset_index(name="Orders")
)

customer_orders["Customer ID"] = (
    customer_orders["Customer ID"]
    .astype(int)
    .astype(str)
)

fig = px.bar(
    customer_orders,
    x="Orders",
    y="Customer ID",
    orientation="h",
    text="Orders",
    color="Orders",
    color_continuous_scale="Blues"
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=20, r=20, t=20, b=20),
    coloraxis_showscale=False,
    yaxis=dict(
        autorange="reversed",
        title=""
    ),
    xaxis_title="Number of Orders"
)

st.plotly_chart(fig, width="stretch")

insight_box(
"""
Customers with a high purchase frequency represent strong loyalty and repeat engagement.
These customers are ideal candidates for loyalty programs, exclusive offers, and personalized marketing campaigns.
"""
)
# ======================================================
# RFM ANALYSIS
# ======================================================

# ======================================================
# RFM CUSTOMER ANALYSIS
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
background:linear-gradient(135deg,#0F172A,#1E3A8A);
padding:32px;
border-radius:22px;
color:white;
margin-bottom:30px;
">

<h2 style="
margin:0;
font-size:34px;
font-weight:700;
color:white;
">
⭐ RFM Customer Analysis
</h2>

<p style="
margin-top:18px;
font-size:17px;
line-height:1.8;
color:#E5E7EB;
">
RFM (Recency, Frequency and Monetary) analysis helps identify your most valuable customers,
understand purchasing behaviour and discover customers who are likely to churn.
</p>

</div>
""", unsafe_allow_html=True)

# ======================================================
# CREATE RFM TABLE
# ======================================================

latest_date = df["InvoiceDate"].max()

rfm = (
    df.groupby("Customer ID")
      .agg(
          Recency=("InvoiceDate", lambda x: (latest_date - x.max()).days),
          Frequency=("Invoice", "nunique"),
          Monetary=("Revenue", "sum")
      )
      .reset_index()
)

rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    q=5,
    labels=[5,4,3,2,1],
    duplicates="drop"
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1,2,3,4,5],
    duplicates="drop"
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    q=5,
    labels=[1,2,3,4,5],
    duplicates="drop"
).astype(int)


def segment_customer(row):

    if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
        return "Champions"

    elif row["R_Score"] >= 3 and row["F_Score"] >= 3:
        return "Loyal Customers"

    elif row["R_Score"] >= 3 and row["F_Score"] <= 2:
        return "Potential Loyalists"

    elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
        return "At Risk"

    else:
        return "Lost Customers"


rfm["Segment"] = rfm.apply(segment_customer, axis=1)

# ======================================================
# REVENUE BY SEGMENT
# ======================================================

st.markdown("""
<div style="
background:white;
padding:28px;
border-radius:20px;
box-shadow:0 8px 24px rgba(15,23,42,.08);
border:1px solid #E5E7EB;
margin-bottom:20px;
">

<h3 style="
margin-top:0;
font-size:28px;
font-weight:700;
color:#0F172A;
">
💰 Revenue by Customer Segment
</h3>

<p style="
font-size:16px;
color:#64748B;
margin-bottom:0;
">
Compare the revenue contribution of each customer segment and identify which groups drive the business.
</p>

</div>
""", unsafe_allow_html=True)

segment_revenue = (
    rfm.groupby("Segment")["Monetary"]
       .sum()
       .reset_index()
       .sort_values("Monetary", ascending=False)
)

fig = px.bar(
    segment_revenue,
    x="Monetary",
    y="Segment",
    orientation="h",
    text="Monetary",
    color="Monetary",
    color_continuous_scale="Blues"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=20, r=20, t=20, b=20),
    coloraxis_showscale=False,
    yaxis=dict(
        autorange="reversed",
        title=""
    ),
    xaxis_title="Revenue ($)"
)
st.plotly_chart(fig, width="stretch")
insight_box("""
**Business Insight**

Champions and Loyal Customers typically contribute the largest share of revenue.
Prioritizing retention campaigns for these segments while re-engaging At Risk and Lost Customers can significantly improve long-term profitability.
""")

