# Streamlit Setup — Design Spec

**Date:** 2026-05-07  
**Status:** Approved

## Goal

Bootstrap a runnable Streamlit app as the starting point for the BasketCraft analytics dashboard.

## Layout

Flat structure at the project root:

```
basket-craft-dashboard/
├── app.py              # Streamlit entry point
├── requirements.txt    # Python dependencies
├── venv/               # Local virtual environment (git-ignored)
├── .env                # Snowflake credentials (git-ignored)
└── .gitignore
```

## app.py

Single file. One line: `st.title("BasketCraft Dashboard")`. No other content at this stage.

## requirements.txt

```
streamlit
```

## Environment

- Python 3.14 venv created at `venv/`
- Activated with `source venv/bin/activate`
- Dependencies installed with `pip install -r requirements.txt`
- App launched with `streamlit run app.py`

## Out of Scope

Snowflake connection, charts, data loading — all deferred to future iterations.
