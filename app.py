"""NYC Taxi metrics dashboard — Week 11 Streamlit practice exercise.

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres. Your job:
implement ``render_kpi_panel`` so the headline-KPI tiles show real data.
The daily-trend and freshness panels are already done. See EXERCISE.md.
"""

import os

import pandas as pd
import sqlalchemy
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # reads .env file if present

POSTGRES_URL = os.environ["POSTGRES_URL"]
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname")

st.set_page_config(page_title="NYC Taxi Metrics", layout="wide")
st.title("NYC Taxi Metrics")


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


def render_kpi_panel():
    """Render the headline-KPI tiles (total trips, average fare, total revenue).

    TODO: implement this function.
    Run: SELECT COUNT(*) AS trip_count, AVG(fare_amount) AS avg_fare,
                SUM(fare_amount) AS total_fare
         FROM {DB_SCHEMA}.fct_trips
    Render three st.metric tiles side by side with st.columns(3).
    See "Panel 1: Headline KPIs" in the Building a Metrics Dashboard chapter.
    """
    raise NotImplementedError("TODO: implement render_kpi_panel")


st.subheader("Headline KPIs")
try:
    render_kpi_panel()
except NotImplementedError:
    st.warning("Implement `render_kpi_panel` to see the KPI tiles.")

st.subheader("Daily trip volume")
daily = run_query(f"""
    SELECT date_trunc('day', pickup_datetime) AS day,
           COUNT(*)                           AS trips
    FROM {DB_SCHEMA}.fct_trips
    GROUP BY 1
    ORDER BY 1
""")

if not daily.empty:
    st.line_chart(daily.set_index("day")["trips"])
else:
    st.info("No trips found in fct_trips yet.")

st.subheader("Data freshness")
fresh = run_query(f"""
    SELECT COUNT(*)              AS row_count,
           MAX(pickup_datetime)  AS last_pickup
    FROM {DB_SCHEMA}.fct_trips
""").iloc[0]

col1, col2 = st.columns(2)
col1.metric("Row count", f"{int(fresh['row_count']):,}")
col2.metric("Last pickup", str(fresh["last_pickup"])[:16] if fresh["last_pickup"] else "unknown")
