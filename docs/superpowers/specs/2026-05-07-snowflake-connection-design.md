# Snowflake Connection — Design Spec

**Date:** 2026-05-07  
**Status:** Approved

## Goal

Connect the BasketCraft Streamlit dashboard to Snowflake and display row counts for all tables in the `analytics` schema.

## Architecture

```
app.py           ← UI only: connection status banner + row-count dataframe
db.py            ← data layer: cached connection + query functions
.env             ← Snowflake credentials (already exists, git-ignored)
requirements.txt ← adds snowflake-connector-python, python-dotenv
tests/
  test_app.py    ← existing title test (unchanged)
  test_db.py     ← tests get_table_row_counts() with a mock connection
```

## `db.py` Interface

```python
@st.cache_resource
def get_connection() -> snowflake.connector.SnowflakeConnection:
    # Loads .env via python-dotenv
    # Connects using SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    # SNOWFLAKE_ROLE, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA

def get_table_row_counts(conn: snowflake.connector.SnowflakeConnection) -> dict[str, int]:
    # Queries INFORMATION_SCHEMA.TABLES for tables in the analytics schema
    # Returns {"TABLE_NAME": row_count, ...} sorted by table name
```

## `app.py` Behavior

1. Calls `get_connection()` inside a `try/except`
2. On success: `st.success("Connected to Snowflake")`
3. On failure: `st.error(str(e))` and stops rendering
4. On success: calls `get_table_row_counts(conn)` and renders result as `st.dataframe`

## Dependencies Added

```
snowflake-connector-python
python-dotenv
```

## Testing

`tests/test_db.py` monkeypatches `db.get_connection` with a mock cursor returning two fake rows. Verifies that `get_table_row_counts` returns the correct `dict`. No live Snowflake connection required.

## Out of Scope

- Authentication via Streamlit secrets (`st.secrets`)
- Snowpark / DataFrame API
- Any chart or visualization beyond the row-count table
- Connection retry logic
