# Exercise: Daily trip-volume chart

Add the daily trend line chart to the metrics dashboard without looking back at the
Building a Metrics Dashboard chapter. The KPI tiles and freshness panel are already
implemented — you only fill in `render_daily_trend_panel`.

## Task

Open `app.py` and implement `render_daily_trend_panel()`:

1. Call `run_query(sql)` (already defined above it) with:
   ```sql
   SELECT date_trunc('day', pickup_datetime) AS day, COUNT(*) AS trips
   FROM {DB_SCHEMA}.fct_trips
   GROUP BY 1
   ORDER BY 1
   ```
2. Set `"day"` as the index with `.set_index("day")`.
3. Render with `st.line_chart`.

## Run it

```bash
uv sync                   # creates .venv and installs from uv.lock
cp .env.example .env      # set POSTGRES_URL and DB_SCHEMA
uv run streamlit run app.py
```

## Success criteria

- The line chart shows trips per day for your real `fct_trips` data.
- The query goes through `run_query`, which is already wrapped in `@st.cache_data(ttl=300)`.
- No credentials hardcoded — everything comes from environment variables.

## Stretch

Resample to weekly buckets (`date_trunc('week', ...)`) and add a `st.radio` to switch the chart
between daily and weekly granularity.

## Compare

Check your work against the `practice-daily-trend-solution` branch.
