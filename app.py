"""NYC Taxi — Week 11 caching practice (starter).

Streamlit reruns the ENTIRE script top to bottom on every widget interaction.
Right now `run_query` has no cache, so it hits Postgres on every rerun. Drag the
slider in the sidebar and watch the "Query time" metric stay high: every drag is
a fresh database round-trip.

Your job: cache `run_query` so the result is reused across reruns. See EXERCISE.md.
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


# TODO: add `@st.cache_data(ttl=300)` on the line directly above this function
#       so Streamlit reuses the result instead of re-querying on every rerun.
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
    "Uncached: the query time stays high on every slider drag (a new Postgres "
    "round-trip each rerun). Once you cache run_query, the first load is slow "
    "(cache miss) and every rerun after is near-instant (cache hit), until the "
    "TTL expires."
)
