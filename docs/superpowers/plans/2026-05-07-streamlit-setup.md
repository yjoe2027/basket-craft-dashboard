# Streamlit Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap a runnable Streamlit app with a title as the starting point for the BasketCraft analytics dashboard.

**Architecture:** Flat project root — `app.py` is the sole Streamlit entry point, `requirements.txt` pins dependencies, a `venv/` holds the isolated environment. No additional abstraction layers at this stage.

**Tech Stack:** Python 3.14, Streamlit, pytest, streamlit.testing.v1 (built into Streamlit)

---

### Task 1: Create venv and requirements.txt

**Files:**
- Create: `requirements.txt`
- Create: `venv/` (via shell, not tracked in git)

- [ ] **Step 1: Verify venv is in .gitignore**

Read `.gitignore` and confirm `venv/` is listed. If not, add it.

- [ ] **Step 2: Create the virtual environment**

```bash
python3 -m venv venv
```

Expected: `venv/` directory created at project root.

- [ ] **Step 3: Create requirements.txt**

```
streamlit
pytest
```

- [ ] **Step 4: Install dependencies**

```bash
venv/bin/pip install -r requirements.txt
```

Expected: Streamlit and pytest installed with no errors. Ends with `Successfully installed ...`.

- [ ] **Step 5: Verify streamlit is available**

```bash
venv/bin/streamlit --version
```

Expected output (version may differ):
```
Streamlit, version 1.x.x
```

- [ ] **Step 6: Commit**

```bash
git add requirements.txt
git commit -m "feat: add requirements.txt with streamlit and pytest"
```

---

### Task 2: Write the failing test for the app title

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_app.py`

- [ ] **Step 1: Create tests directory and init file**

```bash
mkdir -p tests && touch tests/__init__.py
```

- [ ] **Step 2: Write the failing test**

Create `tests/test_app.py`:

```python
from streamlit.testing.v1 import AppTest


def test_title_is_displayed():
    at = AppTest.from_file("app.py").run()
    assert at.title[0].value == "BasketCraft Dashboard"
```

- [ ] **Step 3: Run test to verify it fails**

```bash
venv/bin/pytest tests/test_app.py -v
```

Expected: FAIL with `FileNotFoundError` or `ModuleNotFoundError` because `app.py` does not exist yet.

- [ ] **Step 4: Commit the failing test**

```bash
git add tests/__init__.py tests/test_app.py
git commit -m "test: add failing test for app title"
```

---

### Task 3: Create app.py and make the test pass

**Files:**
- Create: `app.py`

- [ ] **Step 1: Create app.py**

```python
import streamlit as st

st.title("BasketCraft Dashboard")
```

- [ ] **Step 2: Run test to verify it passes**

```bash
venv/bin/pytest tests/test_app.py -v
```

Expected:
```
tests/test_app.py::test_title_is_displayed PASSED
```

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: add minimal Streamlit app with title"
```

---

### Task 4: Run the app in the browser

**Files:** none (verification only)

- [ ] **Step 1: Launch the app**

```bash
venv/bin/streamlit run app.py
```

Expected terminal output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://x.x.x.x:8501
```

- [ ] **Step 2: Verify in browser**

Open `http://localhost:8501`. Confirm the page displays the heading **"BasketCraft Dashboard"** and nothing else.

- [ ] **Step 3: Stop the server**

Press `Ctrl+C` in the terminal.
