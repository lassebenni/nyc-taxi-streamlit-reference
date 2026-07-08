# Exercise: KPI tiles from `fct_trips`

Build the headline KPI row of the metrics dashboard. The chart and freshness panels are already
implemented — you only fill in `get_trip_metrics`.

## Task

Open `app.py` and implement `get_trip_metrics(pg_url, schema)`:

1. Connect with `psycopg2.connect(pg_url)`.
2. Run `SELECT COUNT(*), AVG(fare_amount), SUM(fare_amount) FROM {schema}.fct_trips`.
3. Return `{"trip_count": int, "avg_fare": float, "total_fare": float}`.

The app renders it as three `st.metric` tiles (Total trips, Avg fare, Total fare revenue).

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env      # set POSTGRES_URL and DB_SCHEMA
streamlit run app.py
```

Expected once done:

```text
┌───────────────┬───────────────┬─────────────────────┐
│ Total trips   │ Avg fare      │ Total fare revenue  │
│ 57,000        │ $13.42        │ $765,000            │
└───────────────┴───────────────┴─────────────────────┘
```

## Success criteria

- The three tiles show non-zero values from your real `fct_trips`.
- `get_trip_metrics` uses `@st.cache_data(ttl=60)`.
- No credentials hardcoded — everything comes from environment variables.

## Stretch

Add a `st.selectbox` in the sidebar to filter the KPIs by `pickup_borough`, using a parameterised
`WHERE pickup_borough = %s`.

## Compare

Check your work against the `exercise-kpi-metrics-solution` branch.
