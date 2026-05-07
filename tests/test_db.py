import os
from datetime import date
from unittest.mock import MagicMock, patch

import pandas as pd


def test_get_table_row_counts_returns_dict():
    import db

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchall.return_value = [
        ("ORDERS", 1000),
        ("PRODUCTS", 50),
    ]

    with patch.dict(os.environ, {"SNOWFLAKE_SCHEMA": "ANALYTICS"}):
        result = db.get_table_row_counts(mock_conn)

    assert result == {"ORDERS": 1000, "PRODUCTS": 50}


def test_get_kpi_data_returns_dataframe():
    import db

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchall.return_value = [
        (date(2026, 3, 1), 79482.95, 1705, 46.62, 1705),
        (date(2026, 2, 1), 129010.99, 2701, 47.76, 2701),
    ]

    result = db.get_kpi_data(mock_conn)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == [
        "ORDER_MONTH", "TOTAL_REVENUE", "TOTAL_ORDERS", "AVG_ORDER_VALUE", "TOTAL_ITEMS_SOLD"
    ]
    assert len(result) == 2
    assert result.iloc[0]["TOTAL_REVENUE"] == 79482.95


def test_get_sales_performance_returns_dataframe():
    import db

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchall.return_value = [
        (date(2023, 3, 1), "Gift Basket", 2949.41, 1799.50, 59),
        (date(2023, 4, 1), "Gift Basket", 4999.00, 3050.00, 100),
    ]

    result = db.get_sales_performance(mock_conn)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == [
        "ORDER_MONTH", "PRODUCT_NAME", "TOTAL_REVENUE", "GROSS_PROFIT", "ORDER_COUNT"
    ]
    assert len(result) == 2
    assert result.iloc[0]["PRODUCT_NAME"] == "Gift Basket"


def test_get_bundle_data_returns_dataframe():
    import db

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchall.return_value = [
        ("Deluxe Basket", 42),
        ("Mini Basket",   18),
    ]

    result = db.get_bundle_data(mock_conn, "Gift Basket")

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["PRODUCT_NAME", "CO_PURCHASE_COUNT"]
    assert len(result) == 2
    assert result.iloc[0]["CO_PURCHASE_COUNT"] == 42
