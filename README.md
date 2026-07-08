# NYC Taxi — Streamlit Reference

Reference Streamlit metrics app for **HYF Data Track Week 11 (Dashboarding)**. It reads the
Week 10 dbt mart `fct_trips` straight from Azure Postgres — no Airflow, no orchestration.

`main` is the finished app. Each exercise is a **branch** that starts from the finished project
with one function stubbed out; follow its `EXERCISE.md`, then diff against the matching
`-solution` branch.

## Exercises

| Exercise | Start branch | Solution branch |
| --- | --- | --- |
| KPI tiles from `fct_trips` | [`exercise-kpi-metrics`](../../tree/exercise-kpi-metrics) | [`exercise-kpi-metrics-solution`](../../tree/exercise-kpi-metrics-solution) |
| Daily trip-volume chart | [`exercise-daily-trend`](../../tree/exercise-daily-trend) | [`exercise-daily-trend-solution`](../../tree/exercise-daily-trend-solution) |

Each branch is independent (all start from the complete app), so you can do them in any order.

## Setup

```bash
git clone https://github.com/lassebenni/nyc-taxi-streamlit-reference.git
cd nyc-taxi-streamlit-reference
git switch exercise-kpi-metrics        # then read EXERCISE.md

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                   # set your Week 9/10 POSTGRES_URL + DB_SCHEMA
streamlit run app.py
```

## Prerequisites

- Your Week 10 `fct_trips` table populated in `dev_<name>` on the shared Azure Postgres.
- Your Postgres connection string (`POSTGRES_URL`) and schema name (`DB_SCHEMA`).
