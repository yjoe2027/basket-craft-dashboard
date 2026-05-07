import os

import pandas as pd
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )


def get_table_row_counts(conn):
    schema = os.environ["SNOWFLAKE_SCHEMA"].upper()
    cur = conn.cursor()
    cur.execute(
        "SELECT TABLE_NAME, ROW_COUNT FROM INFORMATION_SCHEMA.TABLES "
        "WHERE TABLE_SCHEMA = %s ORDER BY TABLE_NAME",
        (schema,),
    )
    return {row[0]: row[1] for row in cur.fetchall()}


def get_sales_performance(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT ORDER_MONTH, PRODUCT_NAME, TOTAL_REVENUE, GROSS_PROFIT, ORDER_COUNT "
        "FROM MART_SALES_PERFORMANCE ORDER BY ORDER_MONTH"
    )
    rows = cur.fetchall()
    return pd.DataFrame(
        rows,
        columns=["ORDER_MONTH", "PRODUCT_NAME", "TOTAL_REVENUE", "GROSS_PROFIT", "ORDER_COUNT"],
    )


def get_revenue_trend(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT ORDER_MONTH, SUM(TOTAL_REVENUE) AS TOTAL_REVENUE "
        "FROM MART_SALES_PERFORMANCE "
        "GROUP BY ORDER_MONTH "
        "ORDER BY ORDER_MONTH"
    )
    rows = cur.fetchall()
    return pd.DataFrame(rows, columns=["ORDER_MONTH", "TOTAL_REVENUE"])


def get_kpi_data(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT ORDER_MONTH, "
        "SUM(TOTAL_REVENUE) AS TOTAL_REVENUE, "
        "SUM(ORDER_COUNT) AS TOTAL_ORDERS, "
        "SUM(TOTAL_REVENUE) / NULLIF(SUM(ORDER_COUNT), 0) AS AVG_ORDER_VALUE, "
        "SUM(ITEMS_SOLD) AS TOTAL_ITEMS_SOLD "
        "FROM MART_SALES_PERFORMANCE "
        "GROUP BY ORDER_MONTH "
        "ORDER BY ORDER_MONTH DESC "
        "LIMIT 2"
    )
    rows = cur.fetchall()
    return pd.DataFrame(
        rows,
        columns=["ORDER_MONTH", "TOTAL_REVENUE", "TOTAL_ORDERS", "AVG_ORDER_VALUE", "TOTAL_ITEMS_SOLD"],
    )
