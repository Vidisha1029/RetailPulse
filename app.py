import streamlit as st
from utils import load_css, load_data, footer

st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide"
)

load_css()

df = load_data()

# ============================
# HERO
# ============================

st.markdown("""
<div style="
background: linear-gradient(135deg,#2563EB,#3B82F6);
padding:70px;
border-radius:24px;
text-align:center;
color:white;
margin-bottom:40px;
">

<h1 style="
font-size:62px;
margin-bottom:10px;
color:white;
font-weight:800;
">
📊 RetailPulse
</h1>

<h3 style="
font-weight:400;
color:#DBEAFE;
margin-bottom:25px;
">
AI-Powered Retail Decision Platform
</h3>

<p style="
font-size:20px;
max-width:850px;
margin:auto;
line-height:1.8;
color:white;
">

Transform retail transaction data into
interactive business intelligence,
customer insights,
product analytics,
sales monitoring
and machine learning powered revenue forecasting.

</p>

</div>
""", unsafe_allow_html=True)
# ======================================================
# HERO
# ======================================================

st.markdown("---")

left,right=st.columns([1.3,1])

with left:

    st.markdown("""
# Why RetailPulse?

Every retail company generates enormous amounts of transactional data.

Without analytics, these numbers remain hidden inside spreadsheets.

RetailPulse converts raw data into interactive dashboards that help businesses:

• Understand customers

• Monitor revenue

• Discover top-performing products

• Forecast future sales

• Make confident business decisions

""")

with right:

    st.info("""
### 🚀 Platform Highlights

✔ Executive Dashboard

✔ Customer Analytics

✔ Product Intelligence

✔ Sales Monitoring

✔ Revenue Forecasting

✔ Interactive Visualizations
""")
    
    # ======================================================
# BUSINESS SNAPSHOT
# ======================================================

st.markdown("## 📊 Business Snapshot")

st.caption("A quick overview of the business before exploring detailed dashboards.")

c1,c2,c3,c4=st.columns(4)

with c1:
    st.metric(
        "💰 Revenue",
        "$2.0M",
        "+12.8%"
    )

with c2:
    st.metric(
        "📦 Orders",
        "27,631",
        "+8.4%"
    )

with c3:
    st.metric(
        "👥 Customers",
        "5,199",
        "+342"
    )

with c4:
    st.metric(
        "🌍 Countries",
        "43",
        "+4"
    )

    # ======================================================
# STORY
# ======================================================

st.markdown("---")

left,right=st.columns([1.5,1])

with left:

    st.markdown("""
## 📖 Why RetailPulse?

Every retail company generates thousands of invoices every day.

Unfortunately, raw spreadsheets cannot answer important business questions like:

- Why are sales increasing?

- Which customers generate the highest revenue?

- Which products should be restocked?

- Which countries drive most sales?

- What will next month's revenue look like?

RetailPulse transforms raw transactional data into powerful business intelligence dashboards that help organizations make faster and smarter decisions.
""")

with right:

    st.success("""

### 🚀 Platform Features

✔ Executive Dashboard

✔ Customer Intelligence

✔ Product Analytics

✔ Sales Performance

✔ Revenue Forecasting

✔ Interactive Dashboards

""")
    
    # ======================================================
# DASHBOARD SUITE
# ======================================================

st.markdown("---")

st.markdown("## 🚀 Explore RetailPulse")

st.caption(
    "Choose any dashboard below to begin exploring the analytics."
)

cards = [

("👨‍💼","Executive Dashboard",
"Business KPIs, revenue trends and executive insights"),

("👥","Customer Analysis",
"Customer segmentation, RFM analysis and lifetime value"),

("📈","Sales Analytics",
"Sales performance, monthly trends and country analysis"),

("📦","Product Analysis",
"Best-selling products and revenue contribution"),

("🔮","Revenue Forecasting",
"Predict future revenue using machine learning"),

("💡","Business Intelligence",
"Complete analytical overview for decision making")

]

col1,col2=st.columns(2)

for i,card in enumerate(cards):

    with (col1 if i%2==0 else col2):

        st.container(border=True)

        st.markdown(f"""
### {card[0]} {card[1]}

{card[2]}

➡️ **Open Dashboard**
""")
        
# ======================================================
# PIPELINE
# ======================================================

st.markdown("---")

st.markdown("## ⚙️ Analytics Workflow")

c1,c2,c3,c4,c5=st.columns(5)

c1.info("📥\n\nCollect\nData")
c2.info("🧹\n\nClean\nData")
c3.info("📊\n\nAnalyze")
c4.info("🤖\n\nForecast")
c5.info("💼\n\nBusiness\nDecision")

# ======================================================
# TECH STACK
# ======================================================

st.markdown("---")

col1,col2=st.columns(2)

with col1:

    st.markdown("""
### 💻 Technology Stack

- Python

- Pandas

- Plotly

- Streamlit

- Scikit-Learn

- Statsmodels
""")

with col2:

    st.markdown("""
### 📂 Dataset

- Online Retail II

- 1,067,371 Transactions

- 5,199 Customers

- 43 Countries

- 2009–2011
""")
    
st.markdown("---")

st.caption(
"""
Developed by **Vidisha More**

RetailPulse • Python • Pandas • Plotly • Streamlit
"""
)