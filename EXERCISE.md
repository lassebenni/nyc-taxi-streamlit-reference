# Exercise: Cache your database queries

Streamlit reruns your **entire script, top to bottom, on every widget interaction**
(every slider drag, dropdown change, button click). Without caching, that means a
fresh Postgres query on every rerun: slow for you, and needless load on the shared
class database that everyone is querying at once.

`@st.cache_data` fixes this. It stores a function's return value keyed by its
arguments and reuses it on the next call, until the **TTL** (time-to-live) expires.

## Why this matters

- **Speed:** a cached result returns in microseconds instead of a full DB round-trip.
- **Shared-DB load:** the shared Azure Postgres is not hammered by every widget move from every student.
- **Freshness you control:** the TTL decides how stale a number may get, instead of either always re-querying or never refreshing.

## Task

Open `app.py`. The `run_query` helper has **no cache**. Run the app and drag the
sidebar slider: the **Query time** metric stays high because every rerun re-queries
Postgres.

Add the caching decorator on the line directly above `run_query`:

```python
@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    ...
```

## Run it

```bash
uv sync                   # creates .venv from uv.lock
cp .env.example .env      # set POSTGRES_URL and DB_SCHEMA
uv run streamlit run app.py
```

## Success criteria

- On first load the **Query time** is high (a cache miss: the DB was queried).
- After that, dragging the sidebar slider keeps the query time near **0 ms**: the
  script still reruns, but the query result is reused (a cache hit).
- The query only re-runs when the SQL string changes or after 300 s (the TTL).

## Stretch

Change the SQL string (for example add `WHERE fare_amount > 0`) and confirm the
query runs once more (a new cache key produces a fresh result), then caches again.

## Compare

Check your work against the `practice-caching-solution` branch.
