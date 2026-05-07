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


def test_title_is_displayed():
    mock_conn = MagicMock()
    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value={}), \
         patch("db.get_sales_performance", return_value=SAMPLE_PERF_DF):
        at = AppTest.from_file("app.py").run()
    assert at.title[0].value == "BasketCraft Dashboard"


def test_connection_success_shows_banner_and_data():
    mock_conn = MagicMock()
    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value={"ORDERS": 100, "PRODUCTS": 5}), \
         patch("db.get_sales_performance", return_value=SAMPLE_PERF_DF):
        at = AppTest.from_file("app.py").run()
    assert len(at.success) == 1
    assert "Connected to Snowflake" in at.success[0].value
    assert len(at.dataframe) == 1


def test_sales_performance_section_renders():
    mock_conn = MagicMock()
    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value={}), \
         patch("db.get_sales_performance", return_value=SAMPLE_PERF_DF):
        at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert any(s.value == "Sales Performance" for s in at.subheader)
