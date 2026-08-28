import os
import plotly.express as px
import streamlit as st
from etl_pipeline import run_pipeline
import pandas as pd

st.set_page_config(page_title="FMCG Commercial Analytics", layout="wide")

st.title("📊 Omnichannel FMCG Sales & Commercial Insights")
st.markdown("Real-time revenue, promotional lift, and margin analytics dashboard.")

if not os.path.exists("data/processed/fact_sales.csv"):
    run_pipeline()

df = pd.read_csv("data/processed/fact_sales.csv")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_region = st.sidebar.multiselect(
    "Select Region", options=df["Region"].unique(), default=df["Region"].unique()
)
selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique(),
)

filtered_df = df[
    (df["Region"].isin(selected_region))
    & (df["Category"].isin(selected_category))
]

# Top KPI Cards
c1, c2, c3, c4 = st.columns(4)
total_rev = filtered_df["NetRevenue"].sum()
total_margin = filtered_df["GrossMargin"].sum()
total_units = filtered_df["UnitsSold"].sum()
avg_margin_pct = (total_margin / total_rev) * 100 if total_rev > 0 else 0

c1.metric("Total Net Revenue", f"€{total_rev:,.2f}")
c2.metric("Gross Profit Margin", f"€{total_margin:,.2f}")
c3.metric("Units Sold", f"{total_units:,}")
c4.metric("Avg Margin %", f"{avg_margin_pct:.1f}%")

# Visualizations
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue by Sales Channel")
    fig_channel = px.bar(
        filtered_df.groupby("Channel")["NetRevenue"].sum().reset_index(),
        x="Channel",
        y="NetRevenue",
        color="Channel",
        text_auto=".2s",
    )
    st.plotly_chart(fig_channel, use_container_width=True)

with col_right:
    st.subheader("Promotional Impact on Volume")
    promo_vol = (
        filtered_df.groupby(["Product", "IsPromo"])["UnitsSold"]
        .sum()
        .reset_index()
    )
    promo_vol["IsPromo"] = promo_vol["IsPromo"].map(
        {0: "Regular Price", 1: "On Promotion"}
    )
    fig_promo = px.bar(
        promo_vol,
        x="Product",
        y="UnitsSold",
        color="IsPromo",
        barmode="group",
    )
    st.plotly_chart(fig_promo, use_container_width=True)
