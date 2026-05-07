import os
from unittest.mock import MagicMock, patch


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
