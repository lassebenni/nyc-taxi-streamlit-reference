"""NYC Taxi — Week 11 error-handling practice (starter).

This dashboard has two panels: headline KPIs (always available) and a
database-side "dataset health" panel that reads Postgres catalog info. As
Chapter 5 explains, the health query can fail in the real world: a locked-down
database role can be denied catalog access, or a mart may not have been built.

Right now the health query has NO error handling, so when it fails it takes down
the WHOLE app: the KPI panel above disappears behind a traceback. Your job is to
wrap the health panel so the rest of the dashboard still renders. See EXERCISE.md.
"""

import os

import pandas as pd
import sqlalchemy
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.environ["POSTGRES_URL"]
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname")

st.set_page_config(page_title="Error-handling practice", page_icon="🛡️")


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


st.title("🛡️ Error-handling practice")

# Panel 1 — headline KPIs. These queries always work.
st.subheader("Headline KPIs")
kpis = run_query(
    f"SELECT COUNT(*) AS trips, AVG(fare_amount) AS avg_fare FROM {DB_SCHEMA}.fct_trips"
).iloc[0]
c1, c2 = st.columns(2)
c1.metric("Total trips", f"{int(kpis['trips']):,}")
c2.metric("Average fare", f"${kpis['avg_fare']:.2f}")

# Panel 2 — database-side "dataset health".
# The query below fails on purpose: it reads a table that does not exist, which
# stands in for a real catalog-access failure (a denied role, or a mart that was
# never built). Do NOT fix the query. Wrap it so the app survives the failure.
st.subheader("Dataset health")
size = run_query(
    f"SELECT pg_size_pretty(pg_total_relation_size('{DB_SCHEMA}.fct_trips_unavailable')) AS mart_size"
).iloc[0]
st.metric("Mart size on disk", size["mart_size"])
