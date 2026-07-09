# NYC Taxi — Streamlit Reference

Reference Streamlit metrics app for **HYF Data Track Week 11 (Dashboarding)**. It reads the
Week 10 dbt mart `fct_trips` straight from Azure Postgres — no Airflow, no orchestration.

`main` is the finished app. Each exercise is a **branch** that starts from the finished project
with one function stubbed out; follow its `EXERCISE.md`, then diff against the matching
`-solution` branch.

## Exercises

| Exercise | Start branch | Solution branch |
| --- | --- | --- |
| KPI tiles from `fct_trips` | [`03-exercise-kpi-metrics`](../../tree/03-exercise-kpi-metrics) | [`03-exercise-kpi-metrics-solution`](../../tree/03-exercise-kpi-metrics-solution) |
| Daily trip-volume chart | [`04-exercise-daily-trend`](../../tree/04-exercise-daily-trend) | [`04-exercise-daily-trend-solution`](../../tree/04-exercise-daily-trend-solution) |

Each branch is independent (all start from the complete app), so you can do them in any order.

## Setup

```bash
git clone https://github.com/lassebenni/nyc-taxi-streamlit-reference.git
cd nyc-taxi-streamlit-reference

uv sync                                # creates .venv and installs from uv.lock
cp .env.example .env                   # set your Week 9/10 POSTGRES_URL + DB_SCHEMA
uv run streamlit run app.py
```

> New to `uv`? It replaces `python -m venv` + `pip install -r requirements.txt`: `uv sync` creates the virtual environment and installs the exact versions pinned in `uv.lock` in one step. `uv run` runs a command inside that environment without activating it manually.

## Prerequisites

- Your Week 10 `fct_trips` table populated in `dev_<name>` on the shared Azure Postgres.
- Your Postgres connection string (`POSTGRES_URL`) and schema name (`DB_SCHEMA`).
