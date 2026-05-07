from unittest.mock import MagicMock, patch

from streamlit.testing.v1 import AppTest


def test_title_is_displayed():
    mock_conn = MagicMock()
    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value={}):
        at = AppTest.from_file("app.py").run()
    assert at.title[0].value == "BasketCraft Dashboard"


def test_connection_success_shows_banner_and_data():
    mock_conn = MagicMock()

    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value={"ORDERS": 100, "PRODUCTS": 5}):
        at = AppTest.from_file("app.py").run()

    assert len(at.success) == 1
    assert "Connected to Snowflake" in at.success[0].value
    assert len(at.dataframe) == 1
