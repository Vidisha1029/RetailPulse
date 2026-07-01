import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, apply_filters

# ======================================================
# PAGE TITLE
# ======================================================

st.title("👥 Customer Analysis")
st.info("""
This dashboard analyzes customer purchasing behaviour using RFM analysis
to identify high-value customers, customer segments, and opportunities
to improve customer retention.
""")
st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1{
    color:#1E3A8A;
}

h2,h3{
    color:#374151;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================

df = load_data()
df = apply_filters(df)

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ======================================================
# KPIs
# ======================================================

total_customers = df["Customer ID"].nunique()
total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()

avg_customer_value = total_revenue / total_customers if total_customers else 0
avg_orders = total_orders / total_customers if total_customers else 0

c1, c2, c3 = st.columns(3)

c1.metric("👥 Total Customers", f"{total_customers:,}")
c2.metric("💰 Avg Revenue / Customer", f"${avg_customer_value:,.2f}")
c3.metric("🛒 Avg Orders / Customer", f"{avg_orders:.2f}")

# ======================================================
# TOP CUSTOMERS BY REVENUE
# ======================================================

st.divider()

st.subheader("🏆 Top 10 Customers by Revenue")

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
    text="Revenue"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_yaxes(type="category")

fig.update_layout(
    xaxis_title="Revenue ($)",
    yaxis_title="Customer ID"
)

st.plotly_chart(fig, use_container_width=True)

# ======================================================
# TOP CUSTOMERS BY ORDERS
# ======================================================

st.divider()

st.subheader("📦 Top Customers by Number of Orders")

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
    text="Orders"
)

fig.update_traces(
    textposition="outside"
)

fig.update_yaxes(type="category")

st.plotly_chart(fig, use_container_width=True)

# ======================================================
# RFM ANALYSIS
# ======================================================

st.divider()

st.subheader("⭐ RFM Analysis")

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

c1, c2, c3 = st.columns(3)

c1.metric("Average Recency", f"{rfm['Recency'].mean():.0f} Days")
c2.metric("Average Frequency", f"{rfm['Frequency'].mean():.1f}")
c3.metric("Average Monetary", f"${rfm['Monetary'].mean():,.2f}")

# ======================================================
# CUSTOMER SEGMENTATION
# ======================================================

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
# CUSTOMER SEGMENT PIE
# ======================================================

st.divider()

st.subheader("🥧 Customer Segments")

segment_count = (
    rfm.groupby("Segment")
    .size()
    .reset_index(name="Customers")
)

fig = px.pie(
    segment_count,
    names="Segment",
    values="Customers",
    hole=0.45
)

st.plotly_chart(fig, use_container_width=True)

# ======================================================
# REVENUE BY SEGMENT
# ======================================================

st.divider()

st.subheader("💵 Revenue by Customer Segment")

segment_revenue = (
    rfm.groupby("Segment")["Monetary"]
    .sum()
    .reset_index()
)

fig = px.bar(
    segment_revenue,
    x="Segment",
    y="Monetary",
    text="Monetary",
    color="Segment"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="Revenue ($)",
    xaxis_title="Customer Segment"
)

st.plotly_chart(fig, use_container_width=True)

# ======================================================
# CHAMPIONS
# ======================================================

st.divider()

st.subheader("🥇 Top 10 Champions")

champions = (
    rfm[rfm["Segment"] == "Champions"]
    .sort_values("Monetary", ascending=False)
    .head(10)
)

champions_display = champions.copy()

champions_display["Customer ID"] = (
    champions_display["Customer ID"]
    .astype(int)
    .astype(str)
)

champions_display["Monetary"] = champions_display["Monetary"].map(
    lambda x: f"${x:,.2f}"
)

st.dataframe(
    champions_display,
    hide_index=True,
    use_container_width=True
)