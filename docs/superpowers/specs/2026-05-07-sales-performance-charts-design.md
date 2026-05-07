# Sales Performance Charts — Design Spec

**Date:** 2026-05-07  
**Status:** Approved

## Goal

Add three Plotly line charts to the BasketCraft dashboard showing monthly `TOTAL_REVENUE`, `GROSS_PROFIT`, and `ORDER_COUNT` by product from `MART_SALES_PERFORMANCE`.

## Architecture

```
db.py            ← add get_sales_performance() → pd.DataFrame
charts.py        ← new: three chart functions returning go.Figure
app.py           ← add chart section below existing row-count table
requirements.txt ← add plotly
tests/
  test_charts.py ← new: assert each function returns go.Figure
```

## `db.py` Addition

```python
def get_sales_performance(conn) -> pd.DataFrame:
    # SELECT ORDER_MONTH, PRODUCT_NAME, TOTAL_REVENUE, GROSS_PROFIT, ORDER_COUNT
    # FROM MART_SALES_PERFORMANCE ORDER BY ORDER_MONTH
```

Returns a DataFrame with columns: `ORDER_MONTH`, `PRODUCT_NAME`, `TOTAL_REVENUE`, `GROSS_PROFIT`, `ORDER_COUNT`.

## `charts.py` Interface

Three functions, each accepting a `pd.DataFrame` (as returned by `get_sales_performance`) and returning a `plotly.graph_objects.Figure`. Each chart:
- X-axis: `ORDER_MONTH`
- Y-axis: the relevant metric
- One line per `PRODUCT_NAME`
- Hover tooltips showing month, product, and value

```python
def revenue_chart(df: pd.DataFrame) -> go.Figure
def gross_profit_chart(df: pd.DataFrame) -> go.Figure
def order_count_chart(df: pd.DataFrame) -> go.Figure
```

Implementation uses `plotly.express.line` with `x="ORDER_MONTH"`, `y=<metric>`, `color="PRODUCT_NAME"`.

## `app.py` Layout Addition

Below the existing row-count table, add:

```python
st.subheader("Sales Performance")
df = db.get_sales_performance(conn)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(charts.revenue_chart(df), use_container_width=True)
with col2:
    st.plotly_chart(charts.gross_profit_chart(df), use_container_width=True)
st.plotly_chart(charts.order_count_chart(df), use_container_width=True)
```

## Dependencies Added

```
plotly
```

## Testing

`tests/test_charts.py` — builds a minimal sample DataFrame with 2 products × 2 months, calls each chart function, asserts the return value is a `plotly.graph_objects.Figure`. No Snowflake connection needed.

## Out of Scope

- Date range filters or dropdowns
- Metric toggles
- Chart theming / custom colors
- Export to PNG/CSV
