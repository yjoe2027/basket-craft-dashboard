from datetime import date

import pandas as pd
import plotly.graph_objects as go

SAMPLE_DF = pd.DataFrame([
    {
        "ORDER_MONTH": date(2023, 1, 1),
        "PRODUCT_NAME": "Gift Basket",
        "TOTAL_REVENUE": 1000.0,
        "GROSS_PROFIT": 600.0,
        "ORDER_COUNT": 20,
    },
    {
        "ORDER_MONTH": date(2023, 1, 1),
        "PRODUCT_NAME": "Deluxe Basket",
        "TOTAL_REVENUE": 500.0,
        "GROSS_PROFIT": 300.0,
        "ORDER_COUNT": 10,
    },
    {
        "ORDER_MONTH": date(2023, 2, 1),
        "PRODUCT_NAME": "Gift Basket",
        "TOTAL_REVENUE": 1500.0,
        "GROSS_PROFIT": 900.0,
        "ORDER_COUNT": 30,
    },
    {
        "ORDER_MONTH": date(2023, 2, 1),
        "PRODUCT_NAME": "Deluxe Basket",
        "TOTAL_REVENUE": 800.0,
        "GROSS_PROFIT": 480.0,
        "ORDER_COUNT": 16,
    },
])


TREND_DF = pd.DataFrame([
    {"ORDER_MONTH": date(2023, 1, 1), "TOTAL_REVENUE": 1500.0},
    {"ORDER_MONTH": date(2023, 2, 1), "TOTAL_REVENUE": 2300.0},
])


def test_revenue_trend_chart_returns_figure():
    import charts
    fig = charts.revenue_trend_chart(TREND_DF)
    assert isinstance(fig, go.Figure)


def test_revenue_chart_returns_figure():
    import charts
    fig = charts.revenue_chart(SAMPLE_DF)
    assert isinstance(fig, go.Figure)


def test_gross_profit_chart_returns_figure():
    import charts
    fig = charts.gross_profit_chart(SAMPLE_DF)
    assert isinstance(fig, go.Figure)


def test_order_count_chart_returns_figure():
    import charts
    fig = charts.order_count_chart(SAMPLE_DF)
    assert isinstance(fig, go.Figure)
