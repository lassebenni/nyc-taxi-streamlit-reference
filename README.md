# NYC Taxi — Streamlit Reference
### Practice solution · Metric definitions as a contract (Ch6)

Reference Streamlit metrics app for **HYF Data Track Week 11 (Dashboarding)**, reading the Week 10 dbt mart `fct_trips` from Azure Postgres.

📐 **Practice solution.** You are on **`practice-metric-definitions-solution`**: both definitions in `metric_definitions.md` now match the code (the `avg_fare_per_trip` filter is documented, the `trips_per_day` stub is filled in). Compare against your attempt on `practice-metric-definitions`.

> 🧭 **All branches:** see the [`main`](../../tree/main) branch for the full map of the chapter track vs the practice track.

## Architecture: source to dashboard

```mermaid
flowchart LR
    raw[("Raw NYC taxi data")] --> dbt["dbt models<br/>(Week 10)"]
    dbt --> mart[("fct_trips mart<br/>dev_&lt;name&gt; · Azure Postgres")]
    mart -->|"sqlalchemy + pd.read_sql<br/>cached with @st.cache_data"| app["Streamlit app<br/>run_query() helper"]
    app --> panels["Two metric tiles<br/>+ metric_definitions.md contract"]
    panels --> user["You / your team<br/>browser :8501"]

    classDef store fill:#eaf3fc,stroke:#509ee3,stroke-width:2px,color:#333;
    classDef code fill:#fdecea,stroke:#ff4b4b,stroke-width:2px,color:#333;
    class raw,mart store;
    class app,panels code;
```

## Setup

```bash
git switch practice-metric-definitions-solution
uv sync                                # creates .venv from uv.lock (Python pinned via .python-version)
cp .env.example .env                   # set your Week 9/10 POSTGRES_URL + DB_SCHEMA
uv run streamlit run app.py
```

## Prerequisites

- Your Week 10 `fct_trips` table populated in `dev_<name>` on the shared Azure Postgres.
- Your Postgres connection string (`POSTGRES_URL`) and schema name (`DB_SCHEMA`).
