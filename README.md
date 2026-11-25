# 🛒 FMCG Sales Intelligence: Star-Schema Warehouse & Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fmcg-sales-intelligence.streamlit.app/)  
**Live demo:** https://fmcg-sales-intelligence.streamlit.app/

An end-to-end analytics project for an omnichannel retail business: raw transaction logs → **ETL with data-quality checks** → **star-schema data model** → **analytical SQL layer** → interactive **Streamlit** dashboard.

> The dataset is **synthetic** (10,000 seeded transactions for 2025), generated so the project is fully reproducible.

## 🏗️ Architecture

```
data/generate_data.py      raw transaction log (CSV)
        │
        ▼
src/etl_pipeline.py        data-quality checks → dimension & fact tables
        │
        ▼
data/processed/            star schema (fact_sales + 3 dimensions)
        │
        ├──► sql/analytics_queries.sql   ◄── src/run_sql.py (SQLite)
        └──► src/app.py                  Streamlit dashboard
```

## 🧱 Data Model

| Table | Grain / Content | Key columns |
|---|---|---|
| `fact_sales` | One row per transaction line item | `TransactionID`, `date_id`, `product_id`, `channel_id`, `UnitsSold`, `NetRevenue`, `GrossMargin`, `MarginPct`, `IsPromo` |
| `dim_date` | One row per calendar day | `date_id`, `full_date`, `year`, `month`, `year_month`, `day_of_week` |
| `dim_product` | Product category | `product_id`, `Category` |
| `dim_channel` | Sales channel (Supermarket, Discounter, E-Commerce, Convenience) | `channel_id`, `Channel` |

## ✅ Data-Quality Checks

The ETL step stops with a clear error before loading if the raw data breaks a business rule:

- `UnitsSold` must be strictly positive
- `NetRevenue` must not be negative

## 📊 Analytical SQL Layer

[`sql/analytics_queries.sql`](sql/analytics_queries.sql) answers four business questions:

| # | Question | SQL techniques |
|---|---|---|
| 1 | Which channels drive revenue and margin? | Multi-table joins, aggregation |
| 2 | How does revenue develop month over month? | CTE, `LAG()` window function |
| 3 | How much do promotions lift unit sales per category? | Conditional aggregation |
| 4 | What share of revenue does each category contribute? | CTE, `SUM() OVER ()`, `DENSE_RANK()` |

`src/run_sql.py` loads the star schema into an in-memory SQLite database and runs every query. Sample output:

```
=== 3. Promotional Lift by Product Category ===
 Category  avg_units_promo  avg_units_base  promo_lift_pct
   Snacks            13.53            6.57          106.06
```

## 🚀 Quickstart

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 1. (optional) regenerate raw data and rebuild the star schema
python -c "from data.generate_data import generate_fmcg_dataset; generate_fmcg_dataset()"
python -m src.etl_pipeline

# 2. run the SQL analytics layer
python -m src.run_sql

# 3. launch the dashboard
streamlit run src/app.py
```

Run all commands from the repository root. The processed star-schema tables are committed, so steps 2 and 3 work right after cloning.

## 🛠️ Tech Stack

Python · SQL (SQLite) · Pandas · Streamlit · Plotly · Faker
