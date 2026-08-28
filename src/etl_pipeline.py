import os
import pandas as pd


def run_pipeline():
    raw_path = "data/raw_fmcg_data.csv"
    if not os.path.exists(raw_path):
        from data.generate_data import generate_fmcg_dataset

        generate_fmcg_dataset()

    df = pd.read_csv(raw_path)

    # 1. Validation Checks
    assert (df["UnitsSold"] > 0).all(), "Error: Negative or zero units found!"
    assert (df["NetRevenue"] >= 0).all(), "Error: Negative revenue detected!"

    # 2. Transformations & Feature Engineering
    df["Date"] = pd.to_datetime(df["Date"])
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
    df["MarginPct"] = (df["GrossMargin"] / df["NetRevenue"]).round(4) * 100

    # 3. Export Clean Tables
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/fact_sales.csv", index=False)

    channel_summary = (
        df.groupby("Channel")
        .agg(
            TotalRevenue=("NetRevenue", "sum"),
            TotalMargin=("GrossMargin", "sum"),
            TotalUnits=("UnitsSold", "sum"),
            PromoLiftPct=("IsPromo", "mean"),
        )
        .reset_index()
    )
    channel_summary.to_csv("data/processed/dim_channel_kpis.csv", index=False)
    print("ETL Pipeline complete: Clean data exported to data/processed/")


if __name__ == "__main__":
    run_pipeline()
