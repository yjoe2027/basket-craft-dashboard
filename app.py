import pandas as pd
import streamlit as st

import db

st.title("BasketCraft Dashboard")

try:
    conn = db.get_connection()
    st.success("Connected to Snowflake")
except Exception as e:
    st.error(str(e))
    st.stop()

counts = db.get_table_row_counts(conn)
df = pd.DataFrame(list(counts.items()), columns=["Table", "Row Count"])
st.dataframe(df, use_container_width=True)
