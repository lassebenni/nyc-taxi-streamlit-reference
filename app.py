"""NYC Taxi — Week 11 error-handling practice (solution).

The database-side "dataset health" panel is wrapped in try/except (the Chapter 5
pattern). When its query fails, the app shows a warning and the KPI panel above
still renders, instead of the whole app crashing with a traceback.
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

# Panel 2 — database-side "dataset health", wrapped so a failure degrades
# gracefully instead of taking down the whole dashboard.
st.subheader("Dataset health")
try:
    size = run_query(
        f"SELECT pg_size_pretty(pg_total_relation_size('{DB_SCHEMA}.fct_trips_unavailable')) AS mart_size"
    ).iloc[0]
    st.metric("Mart size on disk", size["mart_size"])
except Exception:
    st.warning(
        "Dataset-health metrics unavailable: the table or catalog access is missing. "
        "The rest of the dashboard is unaffected."
    )
