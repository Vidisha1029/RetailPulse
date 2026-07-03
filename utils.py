import streamlit as st
import pandas as pd

# ======================================================
# LOAD DATA
# ======================================================
# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data(show_spinner=False)
def load_data():

    df = pd.read_csv(
        "data/cleaned_online_retail_small.csv",
        low_memory=False
    )

    # -----------------------------
    # Date Columns
    # -----------------------------

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    df["Year"] = df["InvoiceDate"].dt.year
    df["Quarter"] = df["InvoiceDate"].dt.quarter
    df["Month"] = df["InvoiceDate"].dt.month
    df["MonthName"] = df["InvoiceDate"].dt.strftime("%b")
    df["Day"] = df["InvoiceDate"].dt.day
    df["Hour"] = df["InvoiceDate"].dt.hour
    df["Week"] = df["InvoiceDate"].dt.isocalendar().week.astype(int)
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()

    # -----------------------------
    # Revenue
    # -----------------------------

    df["Revenue"] = df["Quantity"] * df["Price"]

    # -----------------------------
    # Product Description
    # -----------------------------

    df["Description"] = (
        df["Description"]
        .fillna("Unknown Product")
        .astype(str)
        .str.strip()
    )

    df["ShortDescription"] = (
        df["Description"]
        .apply(
            lambda x: x[:35] + "..."
            if len(x) > 35
            else x
        )
    )

    # -----------------------------
    # Data Quality
    # -----------------------------

    df = df[df["Quantity"] > 0]
    df = df[df["Price"] > 0]

    return df


# ======================================================
# SIDEBAR FILTERS
# ======================================================

def apply_filters(df):

    st.sidebar.image(
        "https://img.icons8.com/fluency/96/dashboard-layout.png",
        width=60
    )

    st.sidebar.title("RetailPulse")

    st.sidebar.markdown(
        "Configure the filters below to analyze different business segments."
    )

    st.sidebar.divider()

    # -----------------------------
    # Country Filter
    # -----------------------------

    countries = sorted(df["Country"].dropna().unique())

    selected_countries = st.sidebar.multiselect(
        "🌍 Country",
        options=countries,
        default=countries
    )

    # -----------------------------
    # Year Filter
    # -----------------------------

    years = sorted(df["Year"].unique())

    selected_years = st.sidebar.multiselect(
        "📅 Year",
        options=years,
        default=years
    )

    # -----------------------------
    # Month Filter
    # -----------------------------

    months = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    available_months = (
        df["MonthName"]
        .dropna()
        .unique()
        .tolist()
    )

    month_order = [m for m in months if m in available_months]

    selected_months = st.sidebar.multiselect(
        "🗓 Month",
        options=month_order,
        default=month_order
    )

    # -----------------------------
    # Apply Filters
    # -----------------------------

    filtered_df = df[
        (df["Country"].isin(selected_countries)) &
        (df["Year"].isin(selected_years)) &
        (df["MonthName"].isin(selected_months))
    ]

    st.sidebar.divider()

    st.sidebar.metric(
        "Filtered Records",
        f"{len(filtered_df):,}"
    )

    return filtered_df

# ======================================================
# GLOBAL CSS
# ======================================================

def load_css():

    st.markdown("""
<style>

/* ======================================================
   GOOGLE FONT
====================================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

/* ======================================================
   MAIN APP
====================================================== */

.stApp{
    background:#F8FAFC;
}

/* ======================================================
   PAGE WIDTH
====================================================== */

.block-container{
    max-width:1400px;
    padding-top:2rem;
    padding-bottom:2rem;
}

/* ======================================================
   SIDEBAR
====================================================== */

section[data-testid="stSidebar"]{
    background:white;
    border-right:1px solid #E5E7EB;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:#0F172A;
}

/* ======================================================
   HEADINGS
====================================================== */

h1{
    color:#0F172A;
    font-weight:800;
}

h2{
    color:#0F172A;
    font-weight:700;
}

h3{
    color:#1E293B;
    font-weight:600;
}

/* ======================================================
   KPI CARDS
====================================================== */

div[data-testid="metric-container"]{

    background:white;

    border:1px solid #E5E7EB;

    border-radius:18px;

    padding:18px;

    box-shadow:0 4px 14px rgba(15,23,42,.05);

}

/* ======================================================
   CUSTOM CARD
====================================================== */

.card{

    background:white;

    padding:24px;

    border-radius:20px;

    border:1px solid #E5E7EB;

    box-shadow:0 4px 18px rgba(15,23,42,.05);

    margin-bottom:22px;

}

/* ======================================================
   HERO
====================================================== */

.hero{

    background:linear-gradient(
        135deg,
        #0F172A,
        #1E3A8A
    );

    color:white;

    padding:45px;

    border-radius:24px;

    margin-bottom:30px;

}

/* ======================================================
   INSIGHT
====================================================== */

.insight{

    background:#EFF6FF;

    border-left:6px solid #2563EB;

    padding:18px;

    border-radius:12px;

    margin-top:15px;

}

/* ======================================================
   RECOMMENDATION
====================================================== */

.recommendation{

    background:#ECFDF5;

    border-left:6px solid #16A34A;

    padding:18px;

    border-radius:12px;

    margin-top:15px;

}

/* ======================================================
   DATAFRAME
====================================================== */

[data-testid="stDataFrame"]{

    border-radius:16px;

    overflow:hidden;

}

/* ======================================================
   PLOTLY
====================================================== */

.js-plotly-plot{

    border-radius:18px;

}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LAYOUT COMPONENTS
# ======================================================

def spacer(height=1):
    """Adds vertical spacing."""
    for _ in range(height):
        st.markdown("<br>", unsafe_allow_html=True)


def divider():
    """Displays a horizontal divider."""
    st.divider()


def two_columns(left=1, right=1):
    """Creates two responsive columns."""
    return st.columns([left, right])


def three_columns(a=1, b=1, c=1):
    """Creates three responsive columns."""
    return st.columns([a, b, c])


def four_columns():
    """Creates four equal-width columns."""
    return st.columns(4)


# ======================================================
# SECTION TITLE
# ======================================================
# ======================================================
# HERO COMPONENT
# ======================================================

def hero(title, subtitle, description):

    st.markdown(
        f"""
<div class="hero">

<p style="color:#BFDBFE;font-size:18px;font-weight:600;margin-bottom:10px;">
{subtitle}
</p>

<h1 style="color:white;font-size:52px;margin:0;font-weight:800;">
{title}
</h1>

<p style="color:#E2E8F0;font-size:18px;line-height:1.9;margin-top:25px;margin-bottom:0;">
{description}
</p>

</div>
""",
        unsafe_allow_html=True,
    )

def section(title, description=""):

    st.markdown(
        f"""
<div style="margin-top:10px;margin-bottom:20px;">

<h2 style="margin-bottom:8px;">
{title}
</h2>

<p style="
color:#64748B;
font-size:16px;
line-height:1.8;
margin-top:0;
">
{description}
</p>

</div>
""",
        unsafe_allow_html=True,
    )

# ======================================================
# CHART TITLE
# ======================================================

def chart_title(title, description=""):

    st.markdown(
        f"""
<div style="margin-bottom:12px;">

<h3 style="
color:#1E293B;
margin-bottom:5px;
">
{title}
</h3>

<p style="
color:#64748B;
font-size:15px;
margin-top:0;
">
{description}
</p>

</div>
""",
        unsafe_allow_html=True,
    )
# ======================================================
# KPI ROW
# ======================================================

def kpi_row(metrics):
    """
    Display KPI metrics in a single responsive row.

    metrics = [
        {"title":"Revenue","value":"$1.2M"},
        {"title":"Orders","value":"2,350"}
    ]
    """

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):

        with col:

            st.metric(
                label=metric["title"],
                value=metric["value"]
            )


# ======================================================
# BUSINESS INSIGHT
# ======================================================

def insight_box(text):

    st.markdown(f"""
<div class="insight">

<h4 style="
margin-top:0;
color:#1E3A8A;
">

💡 Business Insight

</h4>

<p style="
color:#334155;
font-size:16px;
line-height:1.8;
margin-bottom:0;
">

{text}

</p>

</div>
""", unsafe_allow_html=True)


# ======================================================
# RECOMMENDATION
# ======================================================

def recommendation_box(text):

    st.markdown(f"""
<div class="recommendation">

<h4 style="
margin-top:0;
color:#15803D;
">

✅ Recommendation

</h4>

<p style="
color:#166534;
font-size:16px;
line-height:1.8;
margin-bottom:0;
">

{text}

</p>

</div>
""", unsafe_allow_html=True)


# ======================================================
# FOOTER
# ======================================================

def footer():

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.markdown("""
<div style="
text-align:center;
padding:20px;
color:#64748B;
font-size:15px;
">

<b>RetailPulse – AI Powered Retail Decision Platform</b>

<br><br>

Developed using Python • Pandas • Plotly • Streamlit

<br>

© 2026 Vidisha More

</div>
""", unsafe_allow_html=True)
    
# ======================================================
# INFO CARD
# ======================================================

def info_card(title, text):

    st.markdown(f"""
<div class="card">

<h3 style="
margin-top:0;
color:#1E3A8A;
font-weight:700;
">

{title}

</h3>

<p style="
font-size:16px;
line-height:1.8;
color:#475569;
margin-bottom:0;
">

{text}

</p>

</div>
""", unsafe_allow_html=True)
    
# ======================================================
# METRIC CARD
# ======================================================

def metric_card(icon, title, value, color="#2563EB"):

    st.markdown(f"""
<div style="

background:white;

padding:22px;

border-radius:20px;

border-top:5px solid {color};

box-shadow:0 4px 14px rgba(0,0,0,.06);

text-align:center;

">

<div style="font-size:42px;">

{icon}

</div>

<h4 style="
margin-top:12px;
margin-bottom:8px;
color:#64748B;
">

{title}

</h4>

<h2 style="
margin:0;
color:#0F172A;
font-weight:800;
">

{value}

</h2>

</div>
""", unsafe_allow_html=True)
    
    
