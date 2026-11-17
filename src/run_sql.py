"""Load the star schema into SQLite and run the analytical SQL layer.

Usage (from the repository root):
    python -m src.run_sql
"""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
QUERIES = ROOT / "sql" / "analytics_queries.sql"
TABLES = ["dim_channel", "dim_product", "dim_date", "fact_sales"]


def build_database() -> sqlite3.Connection:
    """Create an in-memory SQLite warehouse from the processed star-schema CSVs."""
    if not (PROCESSED / "fact_sales.csv").exists():
        from src.etl_pipeline import run_pipeline
        run_pipeline()

    conn = sqlite3.connect(":memory:")
    for table in TABLES:
        pd.read_csv(PROCESSED / f"{table}.csv").to_sql(table, conn, index=False)
    return conn


def split_queries(sql_text: str) -> list[tuple[str, str]]:
    """Split the SQL file into (title, query) pairs using the numbered comment headers."""
    queries, title, buffer = [], "", []
    for line in sql_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("-- ") and stripped[3:4].isdigit():
            title = stripped[3:]
        elif stripped.startswith("--") or not stripped:
            continue
        else:
            buffer.append(line)
            if stripped.endswith(";"):
                queries.append((title, "\n".join(buffer)))
                buffer = []
    return queries


def main() -> None:
    conn = build_database()
    pd.set_option("display.width", 120)
    for title, query in split_queries(QUERIES.read_text()):
        print(f"\n=== {title} ===")
        print(pd.read_sql_query(query, conn).to_string(index=False))
    conn.close()


if __name__ == "__main__":
    main()
