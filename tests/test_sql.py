import pandas as pd
import pytest

from src.run_sql import QUERIES, build_database, split_queries


@pytest.fixture(scope="module")
def results():
    conn = build_database()
    frames = [pd.read_sql_query(q, conn) for _, q in split_queries(QUERIES.read_text())]
    conn.close()
    return frames


def test_all_four_queries_run(results):
    assert [len(frame) for frame in results] == [4, 12, 3, 3]


def test_documented_figures(results):
    """These figures are quoted in the READMEs."""
    channels, months, promo, categories = results
    assert channels["total_orders"].sum() == 10_000
    assert channels["total_units_sold"].sum() == 82_485
    assert channels["net_revenue_eur"].sum() == pytest.approx(129_566.76)
    assert channels["gross_margin_eur"].sum() == pytest.approx(52_464.10)
    assert months.iloc[-1]["mom_growth_pct"] == pytest.approx(19.28)
    assert promo.iloc[0]["Category"] == "Snacks"
    assert promo.iloc[0]["promo_lift_pct"] == pytest.approx(105.93)
    assert categories.iloc[0]["Category"] == "Dairy"
    assert categories.iloc[0]["pct_of_total_revenue"] == pytest.approx(38.20)
