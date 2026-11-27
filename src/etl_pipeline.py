import os
import pandas as pd

def check_data_quality(df: pd.DataFrame) -> None:
    """Raise ValueError if the raw transactions break a business rule."""
    if not (df["UnitsSold"] > 0).all():
        raise ValueError("Data Quality Error: Non-positive units sold detected!")
    if not (df["NetRevenue"] >= 0).all():
        raise ValueError("Data Quality Error: Negative revenue detected!")


def run_pipeline():
    raw_path = "data/raw_fmcg_data.csv"
    if not os.path.exists(raw_path):
        from data.generate_data import generate_fmcg_dataset
        generate_fmcg_dataset()

    df = pd.read_csv(raw_path)

    # 1. Automated Data Quality Checks
    check_data_quality(df)

    # 2. Date parsing & feature engineering
    df["Date"] = pd.to_datetime(df["Date"])
    df["MarginPct"] = ((df["GrossMargin"] / df["NetRevenue"]) * 100).round(2)

    os.makedirs("data/processed", exist_ok=True)

    # 3. Build Star Schema: Dimension Tables
    # dim_channel
    channels = df[["Channel"]].drop_duplicates().reset_index(drop=True)
    channels["channel_id"] = channels.index + 1
    channels.to_csv("data/processed/dim_channel.csv", index=False)

    # dim_product
    products = df[["Category"]].drop_duplicates().reset_index(drop=True)
    products["product_id"] = products.index + 1
    products.to_csv("data/processed/dim_product.csv", index=False)

    # dim_date
    dates = pd.DataFrame({"full_date": df["Date"].drop_duplicates()}).sort_values("full_date").reset_index(drop=True)
    dates["date_id"] = dates.index + 1
    dates["year"] = dates["full_date"].dt.year
    dates["month"] = dates["full_date"].dt.month
    dates["year_month"] = dates["full_date"].dt.to_period("M").astype(str)
    dates["day_of_week"] = dates["full_date"].dt.day_name()
    dates.to_csv("data/processed/dim_date.csv", index=False)

    # 4. Build Star Schema: Fact Table (normalized with foreign keys)
    fact = df.merge(channels, on="Channel") \
             .merge(products, on="Category") \
             .merge(dates, left_on="Date", right_on="full_date")

    fact_sales = fact[[
        "TransactionID", "date_id", "product_id", "channel_id",
        "UnitsSold", "NetRevenue", "GrossMargin", "MarginPct", "IsPromo"
    ]]
    fact_sales.to_csv("data/processed/fact_sales.csv", index=False)
    print("ETL complete: Star schema tables exported to data/processed/")

if __name__ == "__main__":
    run_pipeline()