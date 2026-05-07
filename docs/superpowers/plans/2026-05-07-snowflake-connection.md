# Snowflake Connection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Connect the BasketCraft Streamlit dashboard to Snowflake and display row counts for all tables in the `analytics` schema.

**Architecture:** `db.py` owns the data layer — cached Snowflake connection and query functions. `app.py` owns the UI — connection status banner and row-count dataframe. Credentials come from `.env` via `python-dotenv`.

**Tech Stack:** Python 3.14, Streamlit 1.57, snowflake-connector-python, python-dotenv, pytest, unittest.mock

---

### Task 1: Add snowflake-connector-python and python-dotenv to requirements

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Update requirements.txt**

Replace the entire contents of `requirements.txt` with:

```
streamlit
pytest
snowflake-connector-python
python-dotenv
```

- [ ] **Step 2: Install the new dependencies**

```bash
venv/bin/pip install -r requirements.txt
```

Expected: ends with a line like `Successfully installed ...` with no errors.

- [ ] **Step 3: Verify imports resolve**

```bash
venv/bin/python -c "import snowflake.connector; from dotenv import load_dotenv; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "feat: add snowflake-connector-python and python-dotenv"
```

---

### Task 2: Create db.py with tests (TDD)

**Files:**
- Create: `tests/test_db.py`
- Create: `db.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_db.py`:

```python
import os
from unittest.mock import MagicMock, patch


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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
venv/bin/pytest tests/test_db.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'db'`

- [ ] **Step 3: Create db.py**

Create `db.py` at the project root:

```python
import os

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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
venv/bin/pytest tests/test_db.py -v
```

Expected:

```
tests/test_db.py::test_get_table_row_counts_returns_dict PASSED
```

- [ ] **Step 5: Commit**

```bash
git add db.py tests/test_db.py
git commit -m "feat: add db.py with Snowflake connection and row count query"
```

---

### Task 3: Update app.py to show connection status and row counts (TDD)

**Files:**
- Modify: `tests/test_app.py`
- Modify: `app.py`

- [ ] **Step 1: Add the failing test to tests/test_app.py**

Open `tests/test_app.py`. It currently contains only `test_title_is_displayed`. Add this import at the top and this new test at the bottom:

```python
from streamlit.testing.v1 import AppTest
from unittest.mock import MagicMock, patch


def test_title_is_displayed():
    at = AppTest.from_file("app.py").run()
    assert at.title[0].value == "BasketCraft Dashboard"


def test_connection_success_shows_banner_and_data():
    mock_conn = MagicMock()

    with patch("db.get_connection", return_value=mock_conn), \
         patch("db.get_table_row_counts", return_value={"ORDERS": 100, "PRODUCTS": 5}):
        at = AppTest.from_file("app.py").run()

    assert len(at.success) == 1
    assert "Connected to Snowflake" in at.success[0].value
    assert len(at.dataframe) == 1
```

- [ ] **Step 2: Run the new test to verify it fails**

```bash
venv/bin/pytest tests/test_app.py::test_connection_success_shows_banner_and_data -v
```

Expected: FAIL — app.py doesn't import `db` yet.

- [ ] **Step 3: Replace app.py**

Replace the entire contents of `app.py` with:

```python
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
```

- [ ] **Step 4: Run the full test suite**

```bash
venv/bin/pytest tests/ -v
```

Expected:

```
tests/test_app.py::test_title_is_displayed PASSED
tests/test_app.py::test_connection_success_shows_banner_and_data PASSED
tests/test_db.py::test_get_table_row_counts_returns_dict PASSED

3 passed
```

- [ ] **Step 5: Commit**

```bash
git add app.py tests/test_app.py
git commit -m "feat: show Snowflake connection status and table row counts"
```

---

### Task 4: Verify live in the browser

**Files:** none (manual verification)

- [ ] **Step 1: Launch the app**

```bash
venv/bin/streamlit run app.py
```

Expected terminal output:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:8501`. Confirm:
- "BasketCraft Dashboard" heading is displayed
- A green "Connected to Snowflake" banner appears below the title
- A dataframe with columns **Table** and **Row Count** is rendered, listing tables from the `analytics` schema

- [ ] **Step 3: Stop the server**

Press `Ctrl+C` in the terminal.
