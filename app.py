"""NYC Taxi — Week 11 caching practice (solution).

`run_query` is wrapped in `@st.cache_data(ttl=300)`. Streamlit still reruns the
whole script on every widget interaction, but the query result is reused from
cache until the TTL expires, so Postgres is only hit on a cache miss (first load,
a changed SQL string, or after 300 s). Drag the slider: the query time drops to
near zero after the first load.
"""

import os
import time

import pandas as pd
import sqlalchemy
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.environ["POSTGRES_URL"]
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname")

st.set_page_config(page_title="Caching practice", page_icon="⚡")


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


st.title("⚡ Caching practice")
st.write(
    "Streamlit reruns this whole script on every widget change. "
    "Drag the slider and watch the query time."
)

# A widget that forces a rerun but does NOT change the SQL.
st.sidebar.slider("Drag me to force a rerun", 0, 100, 50)

t0 = time.perf_counter()
kpis = run_query(
    f"SELECT COUNT(*) AS trips, AVG(fare_amount) AS avg_fare "
    f"FROM {DB_SCHEMA}.fct_trips"
).iloc[0]
elapsed_ms = (time.perf_counter() - t0) * 1000

c1, c2, c3 = st.columns(3)
c1.metric("Total trips", f"{int(kpis['trips']):,}")
c2.metric("Average fare", f"${kpis['avg_fare']:.2f}")
c3.metric("Query time", f"{elapsed_ms:.1f} ms")

st.caption(
    "Cached: the first load is a cache miss (slow), then every slider drag is a "
    "cache hit (near-instant). The query only re-runs when the SQL string "
    "changes or the 300 s TTL expires."
)
