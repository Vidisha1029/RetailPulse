import pandas as pd
import streamlit as st


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
def apply_filters(df):
    st.sidebar.header("🔎 Filters")

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