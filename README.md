# Basket Craft — Merchandising Dashboard

**Live app:** https://basket-craft-dashboard-gcyfgkvkowyybu3vnxsjvc.streamlit.app/

A Streamlit dashboard for the Basket Craft merchandising team, powered by Snowflake.

## Features

- **KPI Scorecards** — Total Revenue, Orders, Avg Order Value, Items Sold with month-over-month deltas
- **Revenue Trend** — Line chart filterable by sidebar date range
- **Top Products** — Horizontal bar chart of products ranked by revenue within the selected date range
- **Bundle Finder** — Select a product to see what customers most frequently buy alongside it, with CSV export
- **Sales Performance** — Revenue, gross profit, and order count line charts by product

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your Snowflake credentials:

```
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_ROLE=...
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=...
SNOWFLAKE_SCHEMA=...
```

```bash
streamlit run app.py
```

## Tests

```bash
pytest tests/ -v
```
