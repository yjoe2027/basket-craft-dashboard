from streamlit.testing.v1 import AppTest


def test_title_is_displayed():
    at = AppTest.from_file("app.py").run()
    assert at.title[0].value == "BasketCraft Dashboard"
