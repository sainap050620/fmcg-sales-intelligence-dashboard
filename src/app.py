import os
import streamlit as st
import pandas as pd
import plotly.express as px
try:
    from src.etl_pipeline import run_pipeline
except ModuleNotFoundError:
    from etl_pipeline import run_pipeline
st.set_page_config(
    page_title="FMCG Commercial Sales Intelligence",
    page_icon="🛒",
    layout="wide"
)

# Ensure star schema tables exist
FACT_PATH = "data/processed/fact_sales.csv"
if not os.path.exists(FACT_PATH):
    run_pipeline()

@st.cache_data
def load_data():
    fact = pd.read_csv("data/processed/fact_sales.csv")
    dim_channel = pd.read_csv("data/processed/dim_channel.csv")
    dim_product = pd.read_csv("data/processed/dim_product.csv")
    dim_date = pd.read_csv("data/processed/dim_date.csv")
    
    # Reconstruct analytical view via star-schema joins
    df = fact.merge(dim_channel, on="channel_id") \
             .merge(dim_product, on="product_id") \
             .merge(dim_date, on="date_id")
    df["full_date"] = pd.to_datetime(df["full_date"])
    return df

df = load_data()

# Header & Overview
st.title("🛒 FMCG Commercial Sales & Pricing Intelligence")
st.markdown("Executive BI dashboard evaluating omnichannel revenue, promotional lift, and margin health.")

# Sidebar Filters
st.sidebar.header("Global Filters")
selected_channel = st.sidebar.multiselect(
    "Sales Channel",
    options=df["Channel"].unique(),
    default=df["Channel"].unique()
)

selected_category = st.sidebar.multiselect(
    "Product Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Channel"].isin(selected_channel)) & 
    (df["Category"].isin(selected_category))
]

if filtered_df.empty:
    st.warning("No sales match these filters. Select at least one channel and one category.")
    st.stop()

# Top-Level KPI Cards
col1, col2, col3, col4 = st.columns(4)
total_revenue = filtered_df["NetRevenue"].sum()
total_margin = filtered_df["GrossMargin"].sum()
overall_margin_pct = (total_margin / total_revenue * 100) if total_revenue > 0 else 0
total_units = filtered_df["UnitsSold"].sum()

col1.metric("Net Revenue", f"€{total_revenue:,.2f}")
col2.metric("Gross Margin", f"€{total_margin:,.2f}")
col3.metric("Gross Margin %", f"{overall_margin_pct:.1f}%")
col4.metric("Units Sold", f"{total_units:,}")

st.markdown("---")

# Visualizations Row 1: Revenue Trends & Category Breakdown
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Monthly Net Revenue Trend")
    monthly_rev = filtered_df.groupby("year_month")["NetRevenue"].sum().reset_index()
    fig_monthly = px.line(
        monthly_rev, 
        x="year_month", 
        y="NetRevenue", 
        markers=True,
        labels={"year_month": "Month", "NetRevenue": "Revenue (€)"},
        title="Revenue by Billing Period"
    )
    st.plotly_chart(fig_monthly, width="stretch")

with row1_col2:
    st.subheader("Revenue by Product Category")
    cat_rev = filtered_df.groupby("Category")["NetRevenue"].sum().reset_index()
    fig_cat = px.bar(
        cat_rev, 
        x="Category", 
        y="NetRevenue", 
        color="Category",
        labels={"NetRevenue": "Revenue (€)"},
        title="Category Contribution"
    )
    st.plotly_chart(fig_cat, width="stretch")

# Visualizations Row 2: Promotional Lift Analysis
st.subheader("Promotional Uplift Analysis")
promo_summary = filtered_df.groupby(["Category", "IsPromo"])["UnitsSold"].mean().unstack().reset_index()
promo_summary = promo_summary.rename(columns={0: "Base Units", 1: "Promo Units"})
if "Base Units" in promo_summary and "Promo Units" in promo_summary:
    promo_summary["Promo Lift %"] = (
        (promo_summary["Promo Units"] - promo_summary["Base Units"]) / promo_summary["Base Units"] * 100
    ).round(2)
    st.dataframe(promo_summary, width="stretch")