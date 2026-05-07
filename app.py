import pandas as pd
import streamlit as st

import charts
import db

st.title("Basket Craft — Merchandising Dashboard")

try:
    conn = db.get_connection()
except Exception as e:
    st.error(str(e))
    st.stop()

# ── KPI Scorecards ────────────────────────────────────────────────────────────
kpi_df = db.get_kpi_data(conn)
if len(kpi_df) >= 2:
    cur_m = kpi_df.iloc[0]
    prev_m = kpi_df.iloc[1]

    def _delta(current, previous):
        if previous == 0:
            return None
        pct = (current - previous) / abs(previous)
        return f"{pct:+.1%}"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue",   f"${cur_m['TOTAL_REVENUE']:,.0f}",
              _delta(cur_m["TOTAL_REVENUE"],   prev_m["TOTAL_REVENUE"]))
    c2.metric("Total Orders",    f"{int(cur_m['TOTAL_ORDERS']):,}",
              _delta(cur_m["TOTAL_ORDERS"],    prev_m["TOTAL_ORDERS"]))
    c3.metric("Avg Order Value", f"${cur_m['AVG_ORDER_VALUE']:,.2f}",
              _delta(cur_m["AVG_ORDER_VALUE"], prev_m["AVG_ORDER_VALUE"]))
    c4.metric("Items Sold",      f"{int(cur_m['TOTAL_ITEMS_SOLD']):,}",
              _delta(cur_m["TOTAL_ITEMS_SOLD"], prev_m["TOTAL_ITEMS_SOLD"]))

# ── Revenue Trend ─────────────────────────────────────────────────────────────
df_trend = db.get_revenue_trend(conn)
df_trend["ORDER_MONTH"] = pd.to_datetime(df_trend["ORDER_MONTH"])
min_date = df_trend["ORDER_MONTH"].min().date()
max_date = df_trend["ORDER_MONTH"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if len(date_range) == 2:
    start, end = date_range
    df_trend_filtered = df_trend[
        (df_trend["ORDER_MONTH"] >= pd.Timestamp(start))
        & (df_trend["ORDER_MONTH"] <= pd.Timestamp(end))
    ]
else:
    df_trend_filtered = df_trend

st.subheader("Revenue Trend")
st.plotly_chart(charts.revenue_trend_chart(df_trend_filtered), use_container_width=True)

# ── Top Products ─────────────────────────────────────────────────────────────
df_perf = db.get_sales_performance(conn)
df_perf["ORDER_MONTH"] = pd.to_datetime(df_perf["ORDER_MONTH"])

if len(date_range) == 2:
    df_perf_filtered = df_perf[
        (df_perf["ORDER_MONTH"] >= pd.Timestamp(start))
        & (df_perf["ORDER_MONTH"] <= pd.Timestamp(end))
    ]
else:
    df_perf_filtered = df_perf

df_top = (
    df_perf_filtered.groupby("PRODUCT_NAME", as_index=False)["TOTAL_REVENUE"]
    .sum()
    .sort_values("TOTAL_REVENUE", ascending=True)
)

st.subheader("Top Products")
st.plotly_chart(charts.top_products_chart(df_top), use_container_width=True)

# ── Sales Performance Charts ──────────────────────────────────────────────────
st.subheader("Sales Performance")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(charts.revenue_chart(df_perf), use_container_width=True)
with col2:
    st.plotly_chart(charts.gross_profit_chart(df_perf), use_container_width=True)
st.plotly_chart(charts.order_count_chart(df_perf), use_container_width=True)
