# Exercise: Daily trip-volume chart

Add the daily trend line chart to the metrics dashboard. The KPI tiles and freshness panel are
already implemented — you only fill in `get_daily_trips`.

## Task

Open `app.py` and implement `get_daily_trips(pg_url, schema)`:

1. Connect with `psycopg2.connect(pg_url)`.
2. Run:
   ```sql
   SELECT date_trunc('day', pickup_datetime) AS day, COUNT(*) AS trips
   FROM {schema}.fct_trips
   GROUP BY 1
   ORDER BY 1
   ```
3. Return a `pandas.DataFrame` indexed by `day` with a `trips` column
   (`pd.DataFrame(rows, columns=["day", "trips"]).set_index("day")`).

The app renders it with `st.line_chart`.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env      # set PG_URL and PG_SCHEMA
streamlit run app.py
```

## Success criteria

- The line chart shows trips per day for your `fct_trips` data.
- `get_daily_trips` uses `@st.cache_data(ttl=60)`.
- No credentials hardcoded — everything comes from environment variables.

## Stretch

Resample to weekly buckets (`date_trunc('week', ...)`) and add a `st.radio` to switch the chart
between daily and weekly granularity.

## Compare

Check your work against the `exercise-daily-trend-solution` branch.
