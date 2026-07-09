# NYC Taxi — Streamlit Reference

Reference Streamlit metrics app for **HYF Data Track Week 11 (Dashboarding)**. It reads the
Week 10 dbt mart `fct_trips` straight from Azure Postgres — no Airflow, no orchestration.

Branches are grouped by which chapter or practice exercise they support:

| Branch | Purpose |
| --- | --- |
| [`chapter-4-start`](../../tree/chapter-4-start) | Starter for **Streamlit Fundamentals**: imports, credentials, `st.title` only. Add the chapter's primitives and Postgres/caching examples directly to `app.py`. |
| [`chapter-5-start`](../../tree/chapter-5-start) | Starter for **Building a Metrics Dashboard**: adds the `run_query` caching helper and page config. Build the four panels and the borough filter from the chapter into `app.py`. |
| [`chapter-5-solution`](../../tree/chapter-5-solution) | The finished dashboard from Building a Metrics Dashboard: all four panels plus the sidebar borough filter. Compare your work against it, or clone it directly as your Week 11 assignment starting point. |
| [`practice-kpi-metrics`](../../tree/practice-kpi-metrics) / [`-solution`](../../tree/practice-kpi-metrics-solution) | Practice exercise: rebuild the headline-KPI panel from Building a Metrics Dashboard without looking at the chapter. |
| [`practice-daily-trend`](../../tree/practice-daily-trend) / [`-solution`](../../tree/practice-daily-trend-solution) | Practice exercise: rebuild the daily trip-volume panel from Building a Metrics Dashboard without looking at the chapter. |

Each `-solution` branch has a matching non-solution branch: attempt the exercise yourself
first, then `git switch` to the solution branch to compare.

## Setup

```bash
git clone https://github.com/lassebenni/nyc-taxi-streamlit-reference.git
cd nyc-taxi-streamlit-reference
git switch chapter-4-start             # or any other branch from the table above

uv sync                                # creates .venv and installs from uv.lock
cp .env.example .env                   # set your Week 9/10 POSTGRES_URL + DB_SCHEMA
uv run streamlit run app.py
```

> New to `uv`? It replaces `python -m venv` + `pip install -r requirements.txt`: `uv sync` creates the virtual environment and installs the exact versions pinned in `uv.lock` in one step. `uv run` runs a command inside that environment without activating it manually.

## Prerequisites

- Your Week 10 `fct_trips` table populated in `dev_<name>` on the shared Azure Postgres.
- Your Postgres connection string (`POSTGRES_URL`) and schema name (`DB_SCHEMA`).
