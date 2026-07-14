"""NYC Taxi metrics dashboard — practice-payment-filter exercise.

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres. The KPI, daily
trend, and freshness panels are already built and already interpolate a
``where_clause`` into their SQL. Your task: add the sidebar dropdown that sets
``where_clause`` so one control filters every panel by ``payment_type_label``.
See EXERCISE.md.
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


# ── Sidebar filter (TODO) ─────────────────────────────────────────
# Add a dropdown in the sidebar that filters every panel by payment type.
# The panels below already interpolate `where_clause` into their SQL, so
# once you set it correctly, all three react together.
#
#   1. Query the distinct payment_type_label values from fct_trips
#      (skip NULLs, order them).
#   2. Add a st.sidebar.selectbox with "All" plus those values.
#   3. Set where_clause to "" for "All", otherwise
#      "WHERE payment_type_label = '<selected>'".
#
# Until you implement it, where_clause stays empty and every panel shows
# all payment types. See EXERCISE.md for the exact snippets.
where_clause = ""


st.subheader("Headline KPIs")
kpis = run_query(f"""
    SELECT COUNT(*)          AS trip_count,
           AVG(fare_amount)  AS avg_fare,
           SUM(fare_amount)  AS total_fare
    FROM {DB_SCHEMA}.fct_trips
    {where_clause}
""").iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total trips", f"{int(kpis['trip_count']):,}")
col2.metric("Average fare", f"${kpis['avg_fare']:.2f}")
col3.metric("Total revenue", f"${kpis['total_fare']:,.0f}")


def render_daily_trend_panel():
    """Render the daily trip-volume line chart, filtered by payment type."""
    daily = run_query(f"""
        SELECT date_trunc('day', pickup_datetime) AS day,
               COUNT(*)                           AS trips
        FROM {DB_SCHEMA}.fct_trips
        {where_clause}
        GROUP BY 1
        ORDER BY 1
    """)

    if not daily.empty:
        st.line_chart(daily.set_index("day")["trips"])
    else:
        st.info("No trips found for this filter yet.")


st.subheader("Daily trip volume")
render_daily_trend_panel()

st.subheader("Data freshness")
fresh = run_query(f"""
    SELECT COUNT(*)              AS row_count,
           MAX(pickup_datetime)  AS last_pickup
    FROM {DB_SCHEMA}.fct_trips
    {where_clause}
""").iloc[0]

col1, col2 = st.columns(2)
col1.metric("Row count", f"{int(fresh['row_count']):,}")
col2.metric("Last pickup", str(fresh["last_pickup"])[:16] if fresh["last_pickup"] else "unknown")
