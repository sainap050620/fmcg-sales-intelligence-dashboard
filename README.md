# 📊 Omnichannel FMCG Sales Intelligence & Commercial Dashboard

An end-to-end commercial analytics pipeline and dashboard simulating syndicated retail transaction data to evaluate sales performance, trade promotion effectiveness, and margin profitability.

## 📌 Features
- **Synthetic Data Engine (`data/generate_data.py`)**: Generates 10,000+ realistic FMCG transactions across retail channels (Supermarket, Discounter, E-Commerce).
- **Automated ETL Pipeline (`src/etl_pipeline.py`)**: Data cleaning, automated assertions, and feature engineering (margin %, promotional lift).
- **Interactive Web App (`src/app.py`)**: Streamlit & Plotly interface for real-time KPI filtering by region and product category.
- **SQL Analytics (`sql/analytics_queries.sql`)**: Production-ready analytical queries for promotional lift and category margin analysis.

## 🛠️ Tech Stack
- **Python:** Pandas, NumPy, Plotly, Streamlit, Faker
- **Database / BI:** SQL (PostgreSQL), Power BI Ready
- **Data Engineering:** Automated Assertions, Data Pipelines
