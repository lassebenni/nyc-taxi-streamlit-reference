# Exercise: Keep one broken panel from crashing the whole app

A Streamlit app runs top to bottom. If **any** line raises an exception, the
whole script stops and the user sees a traceback instead of your dashboard, even
the panels that worked. Chapter 5 shows the fix: wrap a query that *might* fail in
`try/except` so the rest of the page still renders.

## Why this matters

Your `fct_trips` queries always work, but a **database-side "health" query** can
fail for reasons outside your control:

- a locked-down Postgres role denied access to catalog functions,
- a mart that has not been built yet,
- a table that was renamed.

You don't want one optional panel to take down the KPIs everyone actually needs.

## Task

Open `app.py`. Run it: the **Dataset health** query reads a table that does not
exist, so the app crashes and the KPI panel above vanishes.

> ⚠️ Do **not** fix the query. The missing table stands in for a real
> catalog-access failure you cannot control. Your job is to make the app survive it.

Wrap the Dataset-health block in `try/except`, and show a message on failure:

```python
st.subheader("Dataset health")
try:
    size = run_query(...).iloc[0]
    st.metric("Mart size on disk", size["mart_size"])
except Exception:
    st.warning("Dataset-health metrics unavailable. The rest of the dashboard is unaffected.")
```

## Run it

```bash
uv sync
cp .env.example .env      # set POSTGRES_URL and DB_SCHEMA
uv run streamlit run app.py
```

## Success criteria

- Before: the app shows a traceback and no KPIs.
- After: the **Headline KPIs** panel renders normally, and the **Dataset health**
  panel shows a warning instead of crashing.

## Stretch

Add a second `except` that catches the *empty result* case separately (a query
that returns zero rows) and shows "no data yet" rather than an error.

## Compare

Check your work against the `practice-error-handling-solution` branch.
