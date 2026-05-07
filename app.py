import pandas as pd
import streamlit as st

import charts
import db

st.title("BasketCraft Dashboard")

try:
    conn = db.get_connection()
    st.success("Connected to Snowflake")
except Exception as e:
    st.error(str(e))
    st.stop()

counts = db.get_table_row_counts(conn)
df_counts = pd.DataFrame(list(counts.items()), columns=["Table", "Row Count"])
st.dataframe(df_counts, use_container_width=True)

st.subheader("Sales Performance")
df_perf = db.get_sales_performance(conn)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(charts.revenue_chart(df_perf), use_container_width=True)
with col2:
    st.plotly_chart(charts.gross_profit_chart(df_perf), use_container_width=True)
st.plotly_chart(charts.order_count_chart(df_perf), use_container_width=True)
