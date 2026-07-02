import pandas as pd
import streamlit as st


# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/cleaned_online_retail_small.csv",
        low_memory=False
    )

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month
    df["MonthName"] = df["InvoiceDate"].dt.strftime("%b")
    df["Day"] = df["InvoiceDate"].dt.day
    df["Hour"] = df["InvoiceDate"].dt.hour
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()

    return df


# ======================================================
# SIDEBAR FILTERS
# ======================================================

def apply_filters(df):

    st.sidebar.markdown("## 🔎 Filters")

    countries = st.sidebar.multiselect(
        "Country",
        sorted(df["Country"].dropna().unique()),
        default=sorted(df["Country"].dropna().unique())
    )

    years = st.sidebar.multiselect(
        "Year",
        sorted(df["Year"].unique()),
        default=sorted(df["Year"].unique())
    )

    filtered_df = df[
        (df["Country"].isin(countries)) &
        (df["Year"].isin(years))
    ]

    return filtered_df


# ======================================================
# GLOBAL CSS
# ======================================================

def load_css():

    st.markdown(
        """
<style>

/* Background */

.stApp{
    background:#F8FAFC;
}

/* Main Container */

.block-container{
    max-width:1300px;
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

/* Headings */

h1{
    color:#0F172A;
    font-weight:800;
}

h2,h3{
    color:#1E293B;
}

/* Cards */

.card{

    background:white;

    padding:24px;

    border-radius:18px;

    border:1px solid #E5E7EB;

    box-shadow:0px 4px 18px rgba(0,0,0,0.05);

    margin-bottom:20px;

}

.card:hover{

    transform:translateY(-4px);

    transition:0.25s;

}

/* Insight Box */

.insight{

    background:#EEF6FF;

    border-left:6px solid #2563EB;

    padding:18px;

    border-radius:12px;

    margin-top:10px;

    margin-bottom:20px;

}

/* Footer */

.footer{

    text-align:center;

    color:#64748B;

    padding-top:25px;

    padding-bottom:15px;

}

/* Metric Cards */

div[data-testid="metric-container"]{

    background:white;

    border:1px solid #E5E7EB;

    padding:18px;

    border-radius:16px;

    box-shadow:0px 3px 10px rgba(0,0,0,0.04);

}

</style>
""",
        unsafe_allow_html=True,
    )


# ======================================================
# PAGE HEADER
# ======================================================

def page_header(title, description):

    st.title(title)

    st.markdown(
        f"""
<div style="font-size:18px;
color:#64748B;
line-height:1.8;
margin-bottom:25px;">

{description}

</div>
""",
        unsafe_allow_html=True,
    )


# ======================================================
# SECTION HEADER
# ======================================================

def section_header(title, description=""):

    st.markdown("---")

    st.subheader(title)

    if description != "":

        st.caption(description)


# ======================================================
# INSIGHT BOX
# ======================================================

def insight_box(text):

    st.markdown(
        f"""
<div class="insight">

<b>💡 Business Insight</b>

<br><br>

{text}

</div>
""",
        unsafe_allow_html=True,
    )


# ======================================================
# FOOTER
# ======================================================

def footer():

    st.markdown("---")

    st.markdown(
        """
<div class="footer">

<b>RetailPulse</b><br>

AI-Powered Retail Decision Platform<br><br>

Developed by <b>Vidisha More</b>

</div>
""",
        unsafe_allow_html=True,
    )