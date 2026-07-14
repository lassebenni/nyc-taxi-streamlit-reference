# Exercise: Payment-type sidebar filter

Add a sidebar dropdown that filters **every** panel (KPIs, daily trend, freshness)
by payment type. This is the one Required assignment skill that no other exercise
drills, so it is worth doing even if the rest of the app felt easy.

The KPI, daily-trend, and freshness panels are already built and already
interpolate a `where_clause` into their SQL. You only add the sidebar control
that sets it.

## Task

Open `app.py` and replace the `where_clause = ""` stub near the top:

1. Query the distinct payment types:
   ```sql
   SELECT DISTINCT payment_type_label
   FROM {DB_SCHEMA}.fct_trips
   WHERE payment_type_label IS NOT NULL
   ORDER BY 1
   ```
2. Add the dropdown:
   ```python
   selected = st.sidebar.selectbox("Payment type", ["All"] + payment_types)
   ```
3. Build the filter clause:
   ```python
   where_clause = "" if selected == "All" else f"WHERE payment_type_label = '{selected}'"
   ```

## Run it

```bash
uv sync                   # creates .venv and installs from uv.lock
cp .env.example .env      # set POSTGRES_URL and DB_SCHEMA
uv run streamlit run app.py
```

## Success criteria

- The sidebar shows a "Payment type" dropdown with "All" plus each payment type.
- Picking a value updates the KPIs, the trend chart, and the freshness panel together.
- Choosing "All" shows every trip again.
- No credentials hardcoded; every query still goes through the cached `run_query`.

## Why string interpolation is safe here

The value can only be one of the fixed dropdown options, so splicing it into the
SQL string cannot inject anything. The moment the value comes from a free-text
`st.text_input`, switch to a parameterized query (`%s` / bound parameters) instead.

## Compare

Check your work against the `practice-payment-filter-solution` branch.
