# NYC Taxi — Streamlit Reference
### Practice · Metric definitions as a contract (Ch6)

Reference Streamlit metrics app for **HYF Data Track Week 11 (Dashboarding)**, reading the Week 10 dbt mart `fct_trips` from Azure Postgres.

📐 **Practice.** You are on **`practice-metric-definitions`**: the app is finished and correct, but `metric_definitions.md` has **drifted** from the code. Reconcile the definitions so a teammate could reproduce every on-screen number. See `EXERCISE.md`.

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
git switch practice-metric-definitions
uv sync                                # creates .venv from uv.lock (Python pinned via .python-version)
cp .env.example .env                   # set your Week 9/10 POSTGRES_URL + DB_SCHEMA
uv run streamlit run app.py
```

Then open `metric_definitions.md` and fix the two definitions to match `app.py`.

## Prerequisites

- Your Week 10 `fct_trips` table populated in `dev_<name>` on the shared Azure Postgres.
- Your Postgres connection string (`POSTGRES_URL`) and schema name (`DB_SCHEMA`).
