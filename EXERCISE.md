# Exercise (advanced): session state + a cached resource

> ⚙️ **Advanced / beyond the chapters.** This exercise is optional. It is not
> required for the Week 11 assignment; it teaches two patterns you will meet in
> real Streamlit apps.

Streamlit reruns the whole script on every interaction. Two consequences:

1. A **plain variable resets** to its starting value on every rerun, so it can
   never accumulate anything (a click counter, a running list, a wizard step).
   `st.session_state` is a dictionary that persists across reruns.
2. Rebuilding an expensive **shared object** (a DB engine / connection pool) on
   every rerun is wasteful. `@st.cache_resource` builds it once and reuses it.
   It is the sibling of `@st.cache_data`: `cache_data` caches serialisable
   **data** (query results); `cache_resource` caches a live **object** (an
   engine, a client, a model) that should not be copied.

## Task

Open `app.py`.

**TODO 1 — cache the resource.** Add `@st.cache_resource` above `get_engine()` so
the engine is created once, not on every query.

**TODO 2 — persist the counter.** The Refresh counter uses a plain variable, so
it always shows 0. Move it into `st.session_state`:

```python
if "refreshes" not in st.session_state:
    st.session_state["refreshes"] = 0
if st.button("Refresh"):
    st.session_state["refreshes"] += 1
st.metric("Times you clicked Refresh", st.session_state["refreshes"])
```

## Run it

```bash
uv sync
cp .env.example .env      # set POSTGRES_URL and DB_SCHEMA
uv run streamlit run app.py
```

## Success criteria

- Clicking **Refresh** makes the counter climb (1, 2, 3, ...) instead of staying at 0.
- The app still shows the KPI tiles.
- `get_engine` is decorated with `@st.cache_resource` (not `@st.cache_data`).

## Stretch

Use `st.session_state` to remember the last borough a `st.selectbox` was set to,
and show "You last looked at: <borough>" across reruns.

## Compare

Check your work against the `practice-advanced-state-solution` branch.
