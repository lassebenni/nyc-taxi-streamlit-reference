"""NYC Taxi — Week 11 ADVANCED practice: session state + cached resource (starter).

This goes beyond the Week 11 chapters. Two patterns you will meet in real
Streamlit apps:

- `@st.cache_resource` caches a shared, non-serialisable object (here the
  SQLAlchemy engine / connection pool) once, instead of rebuilding it on every
  query. It is the sibling of `@st.cache_data`, which caches serialisable
  DATA (query results).
- `st.session_state` remembers values across reruns. A plain variable resets to
  its starting value on every rerun, so it can never count anything.

TODO 1: cache the engine as a resource (see get_engine below).
TODO 2: use st.session_state so the Refresh counter survives reruns.
See EXERCISE.md.
"""

import os

import pandas as pd
import sqlalchemy
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.environ["POSTGRES_URL"]
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname")

st.set_page_config(page_title="Advanced: state + resource", page_icon="🧠")


# TODO 1: add `@st.cache_resource` on the line above so the engine (a connection
#         pool) is created once and reused, not rebuilt on every query.
def get_engine():
    return sqlalchemy.create_engine(POSTGRES_URL)


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql(sql, conn)


st.title("🧠 Advanced: session state + cached resource")

# TODO 2: make this counter survive reruns.
#   A plain variable resets to 0 on every rerun, so it never grows. Initialise
#   st.session_state["refreshes"] to 0 if missing, then increment it on click.
refreshes = 0
if st.button("Refresh"):
    refreshes += 1  # resets to 0 next rerun — this is the bug to fix

st.metric("Times you clicked Refresh", refreshes)

kpis = run_query(
    f"SELECT COUNT(*) AS trips, AVG(fare_amount) AS avg_fare FROM {DB_SCHEMA}.fct_trips"
).iloc[0]
c1, c2 = st.columns(2)
c1.metric("Total trips", f"{int(kpis['trips']):,}")
c2.metric("Average fare", f"${kpis['avg_fare']:.2f}")
