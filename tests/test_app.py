from datetime import date
from unittest.mock import MagicMock, patch

import pandas as pd
from streamlit.testing.v1 import AppTest

SAMPLE_PERF_DF = pd.DataFrame([
    {
        "ORDER_MONTH": date(2023, 1, 1),
        "PRODUCT_NAME": "Gift Basket",
        "TOTAL_REVENUE": 1000.0,
        "GROSS_PROFIT": 600.0,
        "ORDER_COUNT": 20,
    },
])

SAMPLE_KPI_DF = pd.DataFrame([
    {"ORDER_MONTH": date(2026, 3, 1), "TOTAL_REVENUE": 79482.95,  "TOTAL_ORDERS": 1705, "AVG_ORDER_VALUE": 46.62, "TOTAL_ITEMS_SOLD": 1705},
    {"ORDER_MONTH": date(2026, 2, 1), "TOTAL_REVENUE": 129010.99, "TOTAL_ORDERS": 2701, "AVG_ORDER_VALUE": 47.76, "TOTAL_ITEMS_SOLD": 2701},
])

COMMON_PATCHES = dict(
    get_connection=MagicMock(),
    get_table_row_counts={},
    get_sales_performance=SAMPLE_PERF_DF,
    get_kpi_data=SAMPLE_KPI_DF,
)


def _run_app(**overrides):
    kwargs = {**COMMON_PATCHES, **overrides}
    mock_conn = kwargs.pop("get_connection")
    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value=kwargs["get_table_row_counts"]), \
         patch("db.get_sales_performance", return_value=kwargs["get_sales_performance"]), \
         patch("db.get_kpi_data", return_value=kwargs["get_kpi_data"]):
        return AppTest.from_file("app.py").run()


def test_title_is_displayed():
    at = _run_app()
    assert at.title[0].value == "Basket Craft — Merchandising Dashboard"


def test_connection_success_shows_charts():
    at = _run_app()
    assert not at.exception


def test_kpi_metrics_render():
    at = _run_app()
    assert not at.exception
    metric_labels = [m.label for m in at.metric]
    assert "Total Revenue" in metric_labels
    assert "Total Orders" in metric_labels
    assert "Avg Order Value" in metric_labels
    assert "Items Sold" in metric_labels


def test_sales_performance_section_renders():
    at = _run_app()
    assert not at.exception
    assert any(s.value == "Sales Performance" for s in at.subheader)
