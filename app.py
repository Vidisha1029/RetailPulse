import streamlit as st

from utils import (
    load_css,
    hero,
    section,
    info_card,
    spacer,
    two_columns,
    three_columns,
    footer
)

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide"
)

load_css()

# ======================================================
# HERO
# ======================================================

hero(

    "📊 RetailPulse",

    "AI-Powered Retail Decision Platform",

    """
RetailPulse is an end-to-end Business Intelligence platform developed to help
retail organizations transform transactional data into strategic business decisions.

The platform combines Exploratory Data Analysis (EDA), Executive Reporting,
Customer Intelligence, Inventory Optimization, Product Performance Analysis,
and Sales Forecasting to support data-driven decision making.

Built using Python, Pandas, Plotly and Streamlit, RetailPulse demonstrates
how modern analytics can improve operational efficiency, customer retention,
inventory planning and business growth.
"""

)

spacer(2)

# ======================================================
# BUSINESS PROBLEM
# ======================================================

section(
    "💼 Business Problem",
    "The challenges RetailPulse is designed to solve."
)

left, right = two_columns(2, 1)

with left:

    info_card(
        "Why RetailPulse?",
        """
Retail businesses generate large volumes of transactional data every day.

Without a centralized analytics platform, decision-makers struggle to:

• Monitor business performance

• Identify sales trends

• Understand customer purchasing behaviour

• Detect customer churn

• Optimize inventory levels

• Forecast future demand

RetailPulse integrates descriptive, diagnostic and predictive analytics
into one unified platform, enabling faster and more informed business decisions.
"""
    )

with right:

    info_card(
        "🎯 Project Objectives",
        """
✔ Executive Reporting

✔ Customer Intelligence

✔ Inventory Optimization

✔ Product Analytics

✔ Sales Forecasting

✔ Business Recommendations
"""
    )

spacer(2)


# ======================================================
# PLATFORM MODULES
# ======================================================

section(
    "🧩 Analytics Modules",
    "RetailPulse consists of six integrated analytics modules, each designed to answer a different business question."
)

modules = [

{
"title":"📊 Exploratory Data Analysis",
"text":"Assess data quality, understand distributions, detect outliers, evaluate correlations and prepare data for analytics."
},

{
"title":"👨‍💼 Executive Dashboard",
"text":"Monitor executive KPIs, revenue trends, geographic performance and high-level business health."
},

{
"title":"👥 Customer Intelligence",
"text":"Perform RFM segmentation, identify loyal customers, detect churn risk and evaluate customer lifetime value."
},

{
"title":"📦 Inventory Optimization",
"text":"Optimize stock levels using ABC analysis, Pareto analysis, reorder insights and demand trends."
},

{
"title":"🛍 Product Intelligence",
"text":"Analyze product profitability, demand patterns, top performers and revenue contribution."
},

{
"title":"🔮 Sales Forecasting",
"text":"Forecast future revenue using historical transaction patterns to support strategic planning."
}

]

row1 = st.columns(3)

for col, module in zip(row1, modules[:3]):

    with col:

        info_card(
            module["title"],
            module["text"]
        )

row2 = st.columns(3)

for col, module in zip(row2, modules[3:]):

    with col:

        info_card(
            module["title"],
            module["text"]
        )

spacer(2)

# ======================================================
# ANALYTICS WORKFLOW
# ======================================================

section(
    "🔄 Analytics Workflow",
    "RetailPulse follows a structured data analytics lifecycle."
)

workflow = st.columns(6)

steps = [

("📥","Data Collection"),
("🧹","Data Cleaning"),
("📊","EDA"),
("📈","Business Intelligence"),
("🤖","Forecasting"),
("💡","Business Decisions")

]

for col, (icon, label) in zip(workflow, steps):

    with col:

        st.markdown(f"""
<div class="card" style="text-align:center;min-height:170px;">

<div style="font-size:44px;">
{icon}
</div>

<h4 style="margin-top:15px;">
{label}
</h4>

</div>
""", unsafe_allow_html=True)

spacer(2)

# ======================================================
# TECHNOLOGY STACK
# ======================================================

section(
    "⚙️ Technology Stack",
    "RetailPulse combines data engineering, analytics, visualization and forecasting technologies."
)

tech1, tech2, tech3 = st.columns(3)

with tech1:

    info_card(
        "🐍 Data Processing",
        """
• Python

• Pandas

• NumPy

• Data Cleaning

• Feature Engineering
"""
    )

with tech2:

    info_card(
        "📊 Visualization",
        """
• Streamlit

• Plotly

• Interactive Dashboards

• Business Intelligence

• KPI Reporting
"""
    )

with tech3:

    info_card(
        "🤖 Analytics & Forecasting",
        """
• RFM Analysis

• Customer Segmentation

• Inventory Optimization

• Time Series Forecasting

• Business Recommendations
"""
    )

spacer(2)

# ======================================================
# BUSINESS IMPACT
# ======================================================

section(
    "📈 Business Impact",
    "How RetailPulse helps decision-makers transform data into business value."
)

impact1, impact2 = two_columns()

with impact1:

    info_card(
        "📌 Key Benefits",
        """
✔ Improve executive visibility

✔ Detect customer churn

✔ Optimize inventory levels

✔ Identify profitable products

✔ Forecast future revenue

✔ Support strategic planning
"""
    )

with impact2:

    info_card(
        "🎯 Business Outcomes",
        """
• Better decision-making

• Reduced stock-outs

• Improved customer retention

• Revenue optimization

• Operational efficiency

• Data-driven business strategy
"""
    )

spacer(2)

# ======================================================
# PROJECT OVERVIEW
# ======================================================

section(
    "📖 Project Overview",
    "RetailPulse was developed as an end-to-end retail analytics solution using the Online Retail II dataset."
)

st.markdown("""
<div class="card">

This project demonstrates the complete lifecycle of a modern analytics solution:

<ul style="line-height:2; color:#475569; font-size:16px;">

<li><b>Data Preparation</b> – Cleaning and transforming raw retail transactions.</li>

<li><b>Exploratory Data Analysis</b> – Understanding distributions, trends and relationships.</li>

<li><b>Business Intelligence</b> – Executive, customer, product and inventory dashboards.</li>

<li><b>Predictive Analytics</b> – Forecasting future sales trends.</li>

<li><b>Decision Support</b> – Delivering actionable recommendations through interactive dashboards.</li>

</ul>

</div>
""", unsafe_allow_html=True)

spacer(2)
footer()
