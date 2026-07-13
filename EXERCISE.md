# Exercise: KPI tiles from `fct_trips`

Build the headline KPI row of the metrics dashboard without looking back at the
Building a Metrics Dashboard chapter. The daily-trend and freshness panels are already
implemented — you only fill in `render_kpi_panel`.

## Task

Open `app.py` and implement `render_kpi_panel()`:

1. Call `run_query(sql)` (already defined above it) with:
   `SELECT COUNT(*) AS trip_count, AVG(fare_amount) AS avg_fare, SUM(fare_amount) AS total_fare FROM {DB_SCHEMA}.fct_trips`
2. Take the first row with `.iloc[0]`.
3. Render three `st.metric` tiles side by side with `st.columns(3)`: Total trips, Average fare, Total revenue.

## Run it

```bash
uv sync                   # creates .venv and installs from uv.lock
cp .env.example .env      # set POSTGRES_URL and DB_SCHEMA
uv run streamlit run app.py
```

Expected once done:

```text
┌───────────────┬───────────────┬─────────────────────┐
│ Total trips   │ Average fare  │ Total revenue       │
│ 57,000        │ $13.42        │ $765,000            │
└───────────────┴───────────────┴─────────────────────┘
```

## Success criteria

- The three tiles show non-zero values from your real `fct_trips`.
- The query goes through `run_query`, which is already wrapped in `@st.cache_data(ttl=300)`.
- No credentials hardcoded — everything comes from environment variables.

## Stretch

Add a `st.selectbox` in the sidebar to filter the KPIs by `pickup_borough`, the way the chapter's
Panel 4 does, and wire it into your query with an f-string `WHERE` clause.

## Compare

Check your work against the `practice-kpi-metrics-solution` branch.
