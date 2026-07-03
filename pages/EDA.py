import streamlit as st
import plotly.express as px

from utils import (
    load_data,
    apply_filters,
    load_css,
    hero,
    section,
    chart_title,
    spacer,
    two_columns,
    kpi_row,
    insight_box,
    recommendation_box,
    footer
)

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Exploratory Data Analysis",
    page_icon="📊",
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

hero(

    "📊 Exploratory Data Analysis",

    "Understanding the Dataset Before Business Analytics",

    """
Exploratory Data Analysis (EDA) is the first phase of every analytics project.

This dashboard evaluates data quality, explores customer purchasing behaviour,
identifies statistical patterns, detects outliers and uncovers relationships
between variables before building business intelligence dashboards and predictive models.
"""

)

spacer(2)

# ======================================================
# ABOUT DATASET
# ======================================================

section(
    "📁 About the Dataset",
    "Project dataset and business context."
)

left, right = two_columns(2,1)

with left:

    st.markdown("""
<div class="card">

### 🛒 Online Retail II Dataset

RetailPulse uses the **Online Retail II** dataset containing transactional
sales data from a UK-based online retailer.

The dataset includes customer purchases, invoices, products,
countries, quantities and pricing information, making it suitable
for customer analytics, inventory optimization,
sales reporting and forecasting.

</div>
""", unsafe_allow_html=True)

with right:

    st.markdown(f"""
<div class="card">

### 📌 Dataset Summary

📄 Records: **{len(df):,}**

🌍 Countries: **{df['Country'].nunique()}**

👥 Customers: **{df['Customer ID'].nunique():,}**

🛍 Products: **{df['Description'].nunique():,}**

📅 Years: **{df['Year'].min()} - {df['Year'].max()}**

</div>
""", unsafe_allow_html=True)

spacer(2)

# ======================================================
# DATASET OVERVIEW
# ======================================================

section(
    "📊 Dataset Overview",
    "High-level summary of the retail transaction dataset."
)

total_transactions = len(df)
total_revenue = df["Revenue"].sum()
total_customers = df["Customer ID"].nunique()
total_products = df["Description"].nunique()
total_countries = df["Country"].nunique()
avg_order_value = total_revenue / df["Invoice"].nunique()

kpi_row([
    {
        "title": "🧾 Transactions",
        "value": f"{total_transactions:,}"
    },
    {
        "title": "💰 Revenue",
        "value": f"${total_revenue:,.0f}"
    },
    {
        "title": "👥 Customers",
        "value": f"{total_customers:,}"
    },
    {
        "title": "🛍 Products",
        "value": f"{total_products:,}"
    },
    {
        "title": "🌍 Countries",
        "value": f"{total_countries}"
    },
    {
        "title": "🛒 Avg Order Value",
        "value": f"${avg_order_value:,.2f}"
    }
])

insight_box(
"""
The dataset contains over one million retail transactions spanning multiple countries.
These KPIs provide a quick understanding of the business scale before performing deeper statistical analysis.
"""
)

spacer(2)

# ======================================================
# DATA QUALITY ASSESSMENT
# ======================================================

section(
    "🛡️ Data Quality Assessment",
    "Evaluate completeness and reliability before analysis."
)

missing_values = int(df.isnull().sum().sum())
duplicate_rows = int(df.duplicated().sum())
memory_usage = df.memory_usage(deep=True).sum() / (1024**2)

left, right = two_columns(2, 1)

with left:

    chart_title(
        "Missing Values by Column",
        "Identify columns requiring attention before analysis."
    )

    missing_df = (
        df.isnull()
          .sum()
          .reset_index()
    )

    missing_df.columns = ["Column", "Missing Values"]

    fig = px.bar(
        missing_df,
        x="Missing Values",
        y="Column",
        orientation="h",
        color="Missing Values",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed"),
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    chart_title(
        "Dataset Statistics",
        "Technical characteristics of the dataset."
    )

    st.markdown(f"""
<div class="card">

**Rows:** {len(df):,}

**Columns:** {len(df.columns)}

**Missing Values:** {missing_values:,}

**Duplicate Rows:** {duplicate_rows:,}

**Memory Usage:** {memory_usage:.2f} MB

**Date Range:** {df['InvoiceDate'].min().date()} → {df['InvoiceDate'].max().date()}

</div>
""", unsafe_allow_html=True)

recommendation_box(
"""
Customer ID contains missing values because not every transaction was linked to a registered customer. This is expected for the Online Retail II dataset and should be considered during customer-level analyses.
"""
)

spacer(2)

# ======================================================
# REVENUE & PRICE DISTRIBUTION
# ======================================================

section(
    "💰 Revenue & Price Distribution",
    "Understand transaction values and pricing patterns."
)

left, right = two_columns()

# ------------------------------------------------------
# Revenue Distribution
# ------------------------------------------------------

with left:

    chart_title(
        "📈 Revenue Distribution",
        "Most retail datasets contain many low-value transactions and a few very high-value purchases."
    )

    fig = px.histogram(
        df,
        x="Revenue",
        nbins=50,
        color_discrete_sequence=["#2563EB"]
    )

    fig.update_layout(
        template="plotly_white",
        height=430,
        xaxis_title="Revenue ($)",
        yaxis_title="Transactions",
        margin=dict(l=20,r=20,t=20,b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# Price Distribution
# ------------------------------------------------------

with right:

    chart_title(
        "💲 Price Distribution",
        "Analyze how product prices are distributed."
    )

    fig = px.histogram(
        df,
        x="Price",
        nbins=40,
        color_discrete_sequence=["#0EA5E9"]
    )

    fig.update_layout(
        template="plotly_white",
        height=430,
        xaxis_title="Price ($)",
        yaxis_title="Products",
        margin=dict(l=20,r=20,t=20,b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

insight_box(
"""
Both Revenue and Price are highly right-skewed. Most transactions involve lower-priced products, while a small number of premium products contribute disproportionately to revenue. This indicates the presence of high-value outliers that are important for business analysis.
"""
)

spacer(2)

# ======================================================
# QUANTITY ANALYSIS
# ======================================================

section(
    "📦 Quantity Analysis",
    "Evaluate purchasing behaviour and the relationship between sales volume and revenue."
)

left, right = two_columns()

# ------------------------------------------------------
# Quantity Box Plot
# ------------------------------------------------------

with left:

    chart_title(
        "📦 Quantity Distribution",
        "Detect bulk purchases and unusual order quantities."
    )

    fig = px.box(
        df,
        y="Quantity",
        color_discrete_sequence=["#2563EB"]
    )

    fig.update_layout(
        template="plotly_white",
        height=430,
        yaxis_title="Quantity",
        margin=dict(l=20,r=20,t=20,b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# Quantity vs Revenue
# ------------------------------------------------------

with right:

    chart_title(
        "🎯 Quantity vs Revenue",
        "Relationship between purchase quantity and generated revenue."
    )

    sample_df = df.sample(min(5000, len(df)), random_state=42)

    fig = px.scatter(
        sample_df,
        x="Quantity",
        y="Revenue",
        opacity=0.6,
        color="Country",
        hover_data=["Description"]
    )

    fig.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=20,r=20,t=20,b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

recommendation_box(
"""
The strong positive relationship between Quantity and Revenue suggests that increasing sales volume has a direct impact on business performance. Products with unusually high quantities should be reviewed for inventory planning and demand forecasting.
"""
)

spacer(2)

# ======================================================
# OUTLIER ANALYSIS
# ======================================================

section(
    "🚨 Outlier Analysis",
    "Identify unusually large transactions using the Interquartile Range (IQR) method."
)

def calculate_outliers(series):

    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = series[(series < lower) | (series > upper)]

    return len(outliers), len(outliers) / len(series) * 100

revenue_outliers, revenue_pct = calculate_outliers(df["Revenue"])
price_outliers, price_pct = calculate_outliers(df["Price"])
quantity_outliers, quantity_pct = calculate_outliers(df["Quantity"])

kpi_row([
    {
        "title":"💰 Revenue",
        "value":f"{revenue_outliers:,} ({revenue_pct:.1f}%)"
    },
    {
        "title":"💲 Price",
        "value":f"{price_outliers:,} ({price_pct:.1f}%)"
    },
    {
        "title":"📦 Quantity",
        "value":f"{quantity_outliers:,} ({quantity_pct:.1f}%)"
    }
])

insight_box(
"""
The IQR method identifies transactions that fall significantly outside the normal range. These outliers are not necessarily errors—they often represent bulk purchases, premium products, or high-value business customers. Such transactions should be analyzed separately because they can strongly influence summary statistics and business decisions.
"""
)

spacer(2)

# ======================================================
# CORRELATION ANALYSIS
# ======================================================

section(
    "🔥 Correlation Analysis",
    "Evaluate relationships between numerical business variables."
)

chart_title(
    "Correlation Heatmap",
    "Pearson correlation coefficients between numerical variables."
)

corr = df[
    ["Quantity","Price","Revenue","Month","Day"]
].corr(numeric_only=True)

fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    aspect="auto"
)

fig.update_layout(
    template="plotly_white",
    height=550,
    margin=dict(l=20,r=20,t=20,b=20)
)

st.plotly_chart(fig, use_container_width=True)

recommendation_box(
"""
Correlation analysis confirms a strong positive relationship between Quantity and Revenue, indicating that sales volume is a primary driver of revenue. Price has a weaker relationship, suggesting that increasing unit sales has a greater impact than simply selling higher-priced products.
"""
)

spacer(2)

# ======================================================
# MONTHLY TRANSACTION TREND
# ======================================================

section(
    "📈 Monthly Transaction Trend",
    "Analyze how customer purchasing activity changes over time."
)

chart_title(
    "Monthly Transactions",
    "Track the number of unique invoices generated each month."
)

monthly = (
    df.groupby(["Month", "MonthName"])["Invoice"]
      .nunique()
      .reset_index(name="Transactions")
      .sort_values("Month")
)

fig = px.line(
    monthly,
    x="MonthName",
    y="Transactions",
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
    yaxis_title="Transactions",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

insight_box(
"""
Transaction volume helps identify seasonal demand patterns and customer purchasing behaviour. Unlike revenue, transaction counts reveal how frequently customers are buying throughout the year.
"""
)

spacer(2)

# ======================================================
# COUNTRY ANALYSIS
# ======================================================

section(
    "🌍 Geographic Revenue Analysis",
    "Compare revenue contribution across countries."
)

country_sales = (
    df.groupby("Country")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

chart_title(
    "Top 10 Countries by Revenue",
    "Revenue is highly concentrated among a few countries."
)

fig = px.bar(
    country_sales,
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
    height=500,
    coloraxis_showscale=False,
    yaxis=dict(autorange="reversed"),
    xaxis_title="Revenue ($)",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

recommendation_box(
"""
Revenue is heavily concentrated in a small number of countries. Geographic expansion opportunities should focus on underperforming markets while maintaining strong customer engagement in high-revenue regions.
"""
)

spacer(2)

# ======================================================
# WEEKDAY ANALYSIS
# ======================================================

section(
    "📅 Weekday Sales Analysis",
    "Identify the busiest purchasing days."
)

weekday = (
    df.groupby("DayOfWeek")["Revenue"]
      .sum()
      .reindex([
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
          "Sunday"
      ])
      .reset_index()
)

fig = px.bar(
    weekday,
    x="DayOfWeek",
    y="Revenue",
    color="Revenue",
    color_continuous_scale="Teal"
)

fig.update_layout(
    template="plotly_white",
    height=450,
    coloraxis_showscale=False,
    xaxis_title="Day of Week",
    yaxis_title="Revenue ($)"
)

st.plotly_chart(fig, use_container_width=True)

insight_box(
"""
Weekly purchasing patterns help businesses optimize staffing, marketing campaigns and inventory replenishment schedules during peak demand periods.
"""
)

spacer(2)

# ======================================================
# EDA SUMMARY
# ======================================================

section(
    "📝 Key Findings from Exploratory Data Analysis",
    "Summary of the most important observations."
)

st.markdown("""
<div class="card">

### 🔍 Key Insights

- Revenue, Price and Quantity are highly right-skewed, indicating many low-value transactions and a few very large purchases.
- Quantity shows a strong positive relationship with Revenue, making sales volume a key business driver.
- Several statistically significant outliers represent bulk purchases or premium orders.
- Revenue is concentrated in a small number of countries, with the United Kingdom dominating sales.
- Transaction activity varies across months and weekdays, highlighting seasonal purchasing patterns.

</div>
""", unsafe_allow_html=True)

recommendation_box(
"""
The statistical analysis confirms that the dataset is suitable for customer segmentation, inventory optimization and sales forecasting. The next step is to translate these findings into business intelligence dashboards and predictive analytics.
"""
)

footer()