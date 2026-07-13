"""NYC Taxi metrics dashboard — practice-kpi-metrics solution.

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres. Finished
version of the render_kpi_panel exercise: compare against your own attempt
on the practice-kpi-metrics branch.
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
    """Render the headline-KPI tiles (total trips, average fare, total revenue)."""
    kpis = run_query(f"""
        SELECT COUNT(*)          AS trip_count,
               AVG(fare_amount)  AS avg_fare,
               SUM(fare_amount)  AS total_fare
        FROM {DB_SCHEMA}.fct_trips
    """).iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total trips", f"{int(kpis['trip_count']):,}")
    col2.metric("Average fare", f"${kpis['avg_fare']:.2f}")
    col3.metric("Total revenue", f"${kpis['total_fare']:,.0f}")


st.subheader("Headline KPIs")
render_kpi_panel()

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
