# 🛒 FMCG Commercial Sales & Pricing Intelligence Dashboard

An end-to-end commercial analytics system designed for omnichannel retail environments. Features a normalized star schema data warehouse model, dimensional ETL pipeline, analytical SQL metric layers (CTEs, Window Functions), and an interactive Streamlit executive dashboard.

## 🏗️ Architecture & Data Model

The pipeline extracts synthetic multi-channel retail transaction logs and structures them into a dimensional star schema:

* **Fact Table (`fact_sales`)**: Grain at transaction line-item level (`TransactionID`, `date_id`, `product_id`, `channel_id`, `UnitsSold`, `NetRevenue`, `GrossMargin`, `MarginPct`, `IsPromo`).
* **Dimension Tables**:
  * `dim_channel`: Channel distribution (Supermarket, E-Commerce, Discounter, Convenience).
  * `dim_product`: Product hierarchy and categories (Beverages, Dairy, Snacks).
  * `dim_date`: Temporal calendar dimension for cohort analysis and billing period aggregation.

## 📊 Analytical SQL Metrics (`sql/analytics_queries.sql`)

The repository includes production SQL queries demonstrating:
* **Multi-table Joins**: Evaluating channel contribution and gross margin health.
* **Window Functions (`LAG`)**: Calculating Month-over-Month (MoM) revenue growth across sequential billing cycles.
* **Conditional Aggregations**: Evaluating category promotional uplift (`PromoLiftPct`) versus baseline sales.
* **CTEs & Window Partitions (`DENSE_RANK`, `SUM() OVER ()`)**: Quantifying category contribution shares to aggregate retail turnover.

## 🚀 Quickstart

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt