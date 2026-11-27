import random
from pathlib import Path

import pandas as pd
import pytest

from data.generate_data import generate_fmcg_dataset
from src.etl_pipeline import check_data_quality, run_pipeline

PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLES = ["dim_channel", "dim_product", "dim_date", "fact_sales"]


def test_pipeline_reproduces_committed_star_schema(tmp_path, monkeypatch):
    """Generating and transforming from scratch must give the committed tables."""
    # The generator seeds its random numbers at import time, so seed again here.
    random.seed(42)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    generate_fmcg_dataset()
    run_pipeline()
    for table in TABLES:
        built = pd.read_csv(tmp_path / "data" / "processed" / f"{table}.csv")
        committed = pd.read_csv(PROCESSED / f"{table}.csv")
        pd.testing.assert_frame_equal(built, committed)


@pytest.mark.parametrize(
    "units, revenue, message",
    [(0, 1.0, "units sold"), (1, -0.01, "Negative revenue")],
)
def test_bad_rows_are_rejected(units, revenue, message):
    df = pd.DataFrame({"UnitsSold": [units], "NetRevenue": [revenue]})
    with pytest.raises(ValueError, match=message):
        check_data_quality(df)


def test_valid_rows_pass():
    check_data_quality(pd.DataFrame({"UnitsSold": [1], "NetRevenue": [0.0]}))
