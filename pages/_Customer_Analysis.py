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
    page_title="Customer Intelligence",
    page_icon="👥",
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

    "👥 Customer Intelligence",

    "Understanding Customer Behaviour Through RFM Analysis",

    """
Customer Intelligence transforms transactional data into actionable customer insights.

This dashboard uses Recency, Frequency and Monetary (RFM) Analysis to identify
high-value customers, detect customers at risk of churn, understand purchasing
behaviour and support personalized marketing strategies.
"""

)

spacer(2)

# =====================================================
# CREATE RFM TABLE
# =====================================================

section(
    "📊 RFM Customer Analysis",
    "Calculate customer Recency, Frequency and Monetary values."
)

# -----------------------------------------------------
# Remove customers with missing Customer ID
# -----------------------------------------------------

rfm_df = df.dropna(subset=["Customer ID"]).copy()

rfm_df["Customer ID"] = (
    rfm_df["Customer ID"]
    .astype(int)
)

# -----------------------------------------------------
# Reference Date
# One day after the last transaction
# -----------------------------------------------------

snapshot_date = (
    rfm_df["InvoiceDate"].max() +
    pd.Timedelta(days=1)
)

# -----------------------------------------------------
# Create RFM Table
# -----------------------------------------------------

rfm = (
    rfm_df.groupby("Customer ID")
    .agg(

        Recency=(
            "InvoiceDate",
            lambda x: (snapshot_date - x.max()).days
        ),

        Frequency=(
            "Invoice",
            "nunique"
        ),

        Monetary=(
            "Revenue",
            "sum"
        )

    )
    .reset_index()
)

spacer(2)

# =====================================================
# CUSTOMER KPIs
# =====================================================

section(
    "👥 Customer Overview",
    "Key metrics describing customer behaviour."
)

total_customers = len(rfm)

avg_recency = rfm["Recency"].mean()

avg_frequency = rfm["Frequency"].mean()

avg_monetary = rfm["Monetary"].mean()

highest_customer = rfm["Monetary"].max()

kpi_row([

{
"title":"👥 Customers",
"value":f"{total_customers:,}"
},

{
"title":"📅 Avg Recency",
"value":f"{avg_recency:.0f} Days"
},

{
"title":"🔄 Avg Frequency",
"value":f"{avg_frequency:.1f}"
},

{
"title":"💰 Avg Monetary",
"value":f"${avg_monetary:,.0f}"
},

{
"title":"🏆 Highest Customer Value",
"value":f"${highest_customer:,.0f}"
}

])

insight_box(
"""
The RFM table summarizes customer purchasing behaviour into three dimensions:
how recently customers purchased, how frequently they buy and how much they spend.
These metrics form the foundation for customer segmentation and retention strategies.
"""
)

spacer(2)

# =====================================================
# RFM SCORING
# =====================================================

section(
    "🏆 RFM Scoring",
    "Rank customers based on Recency, Frequency and Monetary behaviour."
)

# -----------------------------------------------------
# R Score
# Lower Recency = Better
# -----------------------------------------------------

rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    q=5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# -----------------------------------------------------
# F Score
# Higher Frequency = Better
# -----------------------------------------------------

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# -----------------------------------------------------
# M Score
# Higher Monetary = Better
# -----------------------------------------------------

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# -----------------------------------------------------
# Overall RFM Score
# -----------------------------------------------------

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str) +
    rfm["F_Score"].astype(str) +
    rfm["M_Score"].astype(str)
)

insight_box(
"""
Customers are scored from **1 (lowest)** to **5 (highest)** for each RFM metric.
Using quintiles ensures customers are evaluated relative to the overall customer base,
making the segmentation robust and adaptable to different datasets.
"""
)

spacer(2)

# =====================================================
# CUSTOMER SEGMENTATION
# =====================================================

section(
    "🎯 Customer Segmentation",
    "Classify customers into actionable business segments."
)

def assign_segment(row):

    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4:
        return "Loyal Customers"

    elif r >= 4 and f <= 2:
        return "Potential Loyalists"

    elif r <= 2 and f >= 3:
        return "At Risk"

    else:
        return "Others"

rfm["Segment"] = rfm.apply(assign_segment, axis=1)

segment_summary = (
    rfm.groupby("Segment", as_index=False)
       .agg(
           Customers=("Customer ID", "count"),
           Revenue=("Monetary", "sum")
       )
       .sort_values("Revenue", ascending=False)
)

spacer(2)

# =====================================================
# CUSTOMER SEGMENT DISTRIBUTION
# =====================================================

section(
    "🍩 Customer Segment Distribution",
    "Understand how customers are distributed across RFM segments."
)

segment_count = (
    rfm["Segment"]
       .value_counts()
       .reset_index()
)

segment_count.columns = ["Segment", "Customers"]

chart_title(
    "Customer Distribution by Segment",
    "Proportion of customers in each RFM segment."
)

fig = px.pie(
    segment_count,
    names="Segment",
    values="Customers",
    hole=0.55
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

largest_segment = segment_count.iloc[0]

insight_box(
f"""
The largest customer segment is **{largest_segment['Segment']}**, representing
**{largest_segment['Customers']}** customers.

This distribution provides an overview of customer quality and highlights
where marketing and retention strategies should be focused.
"""
)

spacer(2)

# =====================================================
# REVENUE BY SEGMENT
# =====================================================

section(
    "💰 Revenue Contribution by Segment",
    "Compare the revenue generated by each customer segment."
)

segment_revenue = (
    rfm.groupby("Segment", as_index=False)
       .agg(
           Revenue=("Monetary", "sum")
       )
       .sort_values("Revenue", ascending=False)
)

chart_title(
    "Revenue by Customer Segment",
    "Identify the most valuable customer groups."
)

fig = px.bar(
    segment_revenue,
    x="Revenue",
    y="Segment",
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
    yaxis_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)

top_segment = segment_revenue.iloc[0]

recommendation_box(
f"""
The **{top_segment['Segment']}** segment generates the highest customer revenue.

Retention campaigns should prioritize this group, while personalized engagement
strategies should be developed to move lower-value customers into higher-value segments.
"""
)

spacer(2)


# =====================================================
# CUSTOMER VALUE MATRIX
# =====================================================

# =====================================================
# CUSTOMER VALUE MATRIX
# =====================================================

section(
    "🫧 Customer Value Matrix",
    "Identify high-value customers using Frequency and Monetary analysis."
)

# Top 500 customers by revenue for better readability
bubble_df = (
    rfm.sort_values("Monetary", ascending=False)
       .head(500)
)

chart_title(
    "Customer Value Matrix",
    "Higher-value customers appear as larger bubbles. Dashed lines show the median values."
)

fig = px.scatter(
    bubble_df,
    x="Frequency",
    y="Monetary",
    size="Monetary",
    color="Segment",
    hover_name="Customer ID",
    hover_data={
        "Recency": True,
        "Frequency": True,
        "Monetary": ":,.2f"
    },
    size_max=40,
    log_y=True
)

# Median reference lines
median_frequency = bubble_df["Frequency"].median()
median_monetary = bubble_df["Monetary"].median()

fig.add_vline(
    x=median_frequency,
    line_dash="dash",
    line_color="gray"
)

fig.add_hline(
    y=median_monetary,
    line_dash="dash",
    line_color="gray"
)

fig.update_layout(
    template="plotly_white",
    height=600,
    xaxis_title="Purchase Frequency",
    yaxis_title="Customer Monetary Value (Log Scale)",
    legend_title="Customer Segment"
)

st.plotly_chart(fig, use_container_width=True)

insight_box(
"""
Customers in the upper-right quadrant purchase frequently and generate high revenue, making them the most valuable customers. The dashed median lines divide customers into four behavioural groups, helping identify opportunities for retention, upselling and re-engagement.
"""
)

recommendation_box(
"""
Prioritize retention campaigns for customers in the upper-right quadrant. Develop upselling strategies for frequent buyers with lower spending and targeted win-back campaigns for valuable customers with declining purchase activity.
"""
)

spacer(2)

# =====================================================
# CUSTOMER INTELLIGENCE SUMMARY
# =====================================================

section(
    "📝 Customer Intelligence Summary",
    "Key business findings from customer behaviour analysis."
)

st.markdown("""
<div class="card">

### Key Findings

- RFM Analysis identifies customers based on purchasing behaviour rather than total revenue alone.

- Champions and Loyal Customers contribute a significant share of revenue and should be prioritized for retention.

- At Risk customers represent an opportunity for targeted win-back campaigns.

- Customer segmentation enables personalized marketing instead of treating all customers equally.

- Customer value varies considerably, highlighting the importance of tailored CRM strategies.

</div>
""", unsafe_allow_html=True)

recommendation_box(
"""
Implement personalized marketing campaigns based on customer segments.
Retention initiatives should focus on Champions and Loyal Customers,
while At Risk customers should receive targeted offers to encourage repeat purchases.
"""
)

footer()

