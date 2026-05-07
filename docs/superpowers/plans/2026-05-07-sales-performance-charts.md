# Sales Performance Charts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three Plotly line charts (Total Revenue, Gross Profit, Order Count by product) to the BasketCraft dashboard below the existing row-count table.

**Architecture:** `db.py` gains `get_sales_performance()` returning a DataFrame; `charts.py` (new) owns the three chart functions; `app.py` wires them together in a 2-column + full-width layout. All chart logic is pure-function and tested without Streamlit or Snowflake.

**Tech Stack:** Python 3.14, Streamlit 1.57, Plotly Express, pandas, pytest, unittest.mock

---

### Task 1: Add plotly to requirements

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Add plotly to requirements.txt**

Replace the entire contents of `requirements.txt` with:

```
streamlit
pytest
snowflake-connector-python
python-dotenv
plotly
```

- [ ] **Step 2: Install the new dependency**

```bash
venv/bin/pip install -r requirements.txt
```

Expected: ends with `Successfully installed ...` or `Requirement already satisfied` — no errors.

- [ ] **Step 3: Verify import**

```bash
venv/bin/python -c "import plotly.express as px; import plotly.graph_objects as go; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "feat: add plotly dependency"
```

---

### Task 2: Add get_sales_performance to db.py (TDD)

**Files:**
- Modify: `tests/test_db.py`
- Modify: `db.py`

- [ ] **Step 1: Add the failing test to tests/test_db.py**

Open `tests/test_db.py`. Keep the existing `test_get_table_row_counts_returns_dict` test. Add this import at the top and this new test at the bottom:

```python
import os
from datetime import date
from unittest.mock import MagicMock, patch

import pandas as pd


def test_get_table_row_counts_returns_dict():
    import db

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchall.return_value = [
        ("ORDERS", 1000),
        ("PRODUCTS", 50),
    ]

    with patch.dict(os.environ, {"SNOWFLAKE_SCHEMA": "ANALYTICS"}):
        result = db.get_table_row_counts(mock_conn)

    assert result == {"ORDERS": 1000, "PRODUCTS": 50}


def test_get_sales_performance_returns_dataframe():
    import db

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.fetchall.return_value = [
        (date(2023, 3, 1), "Gift Basket", 2949.41, 1799.50, 59),
        (date(2023, 4, 1), "Gift Basket", 4999.00, 3050.00, 100),
    ]

    result = db.get_sales_performance(mock_conn)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == [
        "ORDER_MONTH", "PRODUCT_NAME", "TOTAL_REVENUE", "GROSS_PROFIT", "ORDER_COUNT"
    ]
    assert len(result) == 2
    assert result.iloc[0]["PRODUCT_NAME"] == "Gift Basket"
```

- [ ] **Step 2: Run the new test to verify it fails**

```bash
venv/bin/pytest tests/test_db.py::test_get_sales_performance_returns_dataframe -v
```

Expected: FAIL with `AttributeError` — `db` has no `get_sales_performance`.

- [ ] **Step 3: Add get_sales_performance to db.py**

Open `db.py`. Add this import at the top (after the existing imports):

```python
import pandas as pd
```

Then append this function at the bottom of `db.py`:

```python
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
```

- [ ] **Step 4: Run all db tests to verify they pass**

```bash
venv/bin/pytest tests/test_db.py -v
```

Expected:

```
tests/test_db.py::test_get_table_row_counts_returns_dict PASSED
tests/test_db.py::test_get_sales_performance_returns_dataframe PASSED
```

- [ ] **Step 5: Commit**

```bash
git add db.py tests/test_db.py
git commit -m "feat: add get_sales_performance to db.py"
```

---

### Task 3: Create charts.py (TDD)

**Files:**
- Create: `tests/test_charts.py`
- Create: `charts.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_charts.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
venv/bin/pytest tests/test_charts.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'charts'`

- [ ] **Step 3: Create charts.py**

Create `charts.py` at the project root:

```python
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
venv/bin/pytest tests/test_charts.py -v
```

Expected:

```
tests/test_charts.py::test_revenue_chart_returns_figure PASSED
tests/test_charts.py::test_gross_profit_chart_returns_figure PASSED
tests/test_charts.py::test_order_count_chart_returns_figure PASSED
```

- [ ] **Step 5: Commit**

```bash
git add charts.py tests/test_charts.py
git commit -m "feat: add charts.py with revenue, gross profit, and order count line charts"
```

---

### Task 4: Update app.py with chart section (TDD)

**Files:**
- Modify: `tests/test_app.py`
- Modify: `app.py`

- [ ] **Step 1: Add the failing test to tests/test_app.py**

Replace the entire contents of `tests/test_app.py` with:

```python
from unittest.mock import MagicMock, patch
from datetime import date

import pandas as pd
from streamlit.testing.v1 import AppTest


SAMPLE_PERF_DF = pd.DataFrame([
    {
        "ORDER_MONTH": date(2023, 1, 1),
        "PRODUCT_NAME": "Gift Basket",
        "TOTAL_REVENUE": 1000.0,
        "GROSS_PROFIT": 600.0,
        "ORDER_COUNT": 20,
    },
])


def test_title_is_displayed():
    mock_conn = MagicMock()
    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value={}), \
         patch("db.get_sales_performance", return_value=SAMPLE_PERF_DF):
        at = AppTest.from_file("app.py").run()
    assert at.title[0].value == "BasketCraft Dashboard"


def test_connection_success_shows_banner_and_data():
    mock_conn = MagicMock()
    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value={"ORDERS": 100, "PRODUCTS": 5}), \
         patch("db.get_sales_performance", return_value=SAMPLE_PERF_DF):
        at = AppTest.from_file("app.py").run()
    assert len(at.success) == 1
    assert "Connected to Snowflake" in at.success[0].value
    assert len(at.dataframe) == 1


def test_sales_performance_section_renders():
    mock_conn = MagicMock()
    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value={}), \
         patch("db.get_sales_performance", return_value=SAMPLE_PERF_DF):
        at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert any(s.value == "Sales Performance" for s in at.subheader)
```

- [ ] **Step 2: Run the new test to verify it fails**

```bash
venv/bin/pytest tests/test_app.py::test_sales_performance_section_renders -v
```

Expected: FAIL — app.py doesn't import `charts` or call `get_sales_performance` yet.

- [ ] **Step 3: Replace app.py**

Replace the entire contents of `app.py` with:

```python
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
```

- [ ] **Step 4: Run the full test suite**

```bash
venv/bin/pytest tests/ -v
```

Expected — all 6 tests pass:

```
tests/test_app.py::test_title_is_displayed PASSED
tests/test_app.py::test_connection_success_shows_banner_and_data PASSED
tests/test_app.py::test_sales_performance_section_renders PASSED
tests/test_charts.py::test_revenue_chart_returns_figure PASSED
tests/test_charts.py::test_gross_profit_chart_returns_figure PASSED
tests/test_charts.py::test_order_count_chart_returns_figure PASSED
tests/test_db.py::test_get_table_row_counts_returns_dict PASSED
tests/test_db.py::test_get_sales_performance_returns_dataframe PASSED
```

- [ ] **Step 5: Commit**

```bash
git add app.py tests/test_app.py
git commit -m "feat: add sales performance charts to dashboard"
```

---

### Task 5: Verify live in browser

**Files:** none (manual verification)

- [ ] **Step 1: Restart the app**

Kill any running Streamlit instance and relaunch:

```bash
pkill -f "streamlit run"; sleep 1; venv/bin/streamlit run app.py
```

Expected:

```
  Local URL: http://localhost:8501
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:8501`. Confirm:
- Green "Connected to Snowflake" banner
- Row-count table
- "Sales Performance" subheader
- Two side-by-side line charts: **Total Revenue by Product** and **Gross Profit by Product**
- Full-width line chart: **Order Count by Product**
- Each chart has one line per product with hover tooltips

- [ ] **Step 3: Stop the server**

Press `Ctrl+C`.
