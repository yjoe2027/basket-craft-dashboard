import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def revenue_trend_chart(df: pd.DataFrame) -> go.Figure:
    return px.line(
        df,
        x="ORDER_MONTH",
        y="TOTAL_REVENUE",
        title="Revenue Trend",
        labels={"ORDER_MONTH": "Month", "TOTAL_REVENUE": "Revenue ($)"},
    )


def revenue_chart(df: pd.DataFrame) -> go.Figure:
    return px.line(
        df,
        x="ORDER_MONTH",
        y="TOTAL_REVENUE",
        color="PRODUCT_NAME",
        title="Total Revenue by Product",
        labels={
            "ORDER_MONTH": "Month",
            "TOTAL_REVENUE": "Revenue ($)",
            "PRODUCT_NAME": "Product",
        },
    )


def gross_profit_chart(df: pd.DataFrame) -> go.Figure:
    return px.line(
        df,
        x="ORDER_MONTH",
        y="GROSS_PROFIT",
        color="PRODUCT_NAME",
        title="Gross Profit by Product",
        labels={
            "ORDER_MONTH": "Month",
            "GROSS_PROFIT": "Gross Profit ($)",
            "PRODUCT_NAME": "Product",
        },
    )


def top_products_chart(df: pd.DataFrame) -> go.Figure:
    return px.bar(
        df,
        x="TOTAL_REVENUE",
        y="PRODUCT_NAME",
        orientation="h",
        title="Top Products by Revenue",
        labels={"TOTAL_REVENUE": "Revenue ($)", "PRODUCT_NAME": "Product"},
    )


def order_count_chart(df: pd.DataFrame) -> go.Figure:
    return px.line(
        df,
        x="ORDER_MONTH",
        y="ORDER_COUNT",
        color="PRODUCT_NAME",
        title="Order Count by Product",
        labels={
            "ORDER_MONTH": "Month",
            "ORDER_COUNT": "Orders",
            "PRODUCT_NAME": "Product",
        },
    )
