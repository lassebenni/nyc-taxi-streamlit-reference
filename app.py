"""NYC Taxi — Week 11 ADVANCED practice: session state + cached resource (solution).

- `get_engine` is wrapped in `@st.cache_resource`, so the SQLAlchemy engine
  (connection pool) is created once and reused across reruns and sessions.
- The Refresh counter lives in `st.session_state`, so it survives reruns and
  actually counts up each click (a plain variable would reset to 0 every rerun).
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


@st.cache_resource
def get_engine():
    return sqlalchemy.create_engine(POSTGRES_URL)


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql(sql, conn)


st.title("🧠 Advanced: session state + cached resource")

# The counter survives reruns because it lives in session_state.
if "refreshes" not in st.session_state:
    st.session_state["refreshes"] = 0
if st.button("Refresh"):
    st.session_state["refreshes"] += 1

st.metric("Times you clicked Refresh", st.session_state["refreshes"])

kpis = run_query(
    f"SELECT COUNT(*) AS trips, AVG(fare_amount) AS avg_fare FROM {DB_SCHEMA}.fct_trips"
).iloc[0]
c1, c2 = st.columns(2)
c1.metric("Total trips", f"{int(kpis['trips']):,}")
c2.metric("Average fare", f"${kpis['avg_fare']:.2f}")
