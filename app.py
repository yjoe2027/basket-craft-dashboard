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

# ── Sales Performance Charts ──────────────────────────────────────────────────
st.subheader("Sales Performance")
df_perf = db.get_sales_performance(conn)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(charts.revenue_chart(df_perf), use_container_width=True)
with col2:
    st.plotly_chart(charts.gross_profit_chart(df_perf), use_container_width=True)
st.plotly_chart(charts.order_count_chart(df_perf), use_container_width=True)
