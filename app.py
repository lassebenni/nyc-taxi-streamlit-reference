"""NYC Taxi metrics dashboard — practice-payment-filter solution.

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres. Finished
version of the payment-type sidebar-filter exercise: a ``st.sidebar.selectbox``
filters every panel (KPIs, daily trend, freshness) by ``payment_type_label``.
Compare against your own attempt on the practice-payment-filter branch.
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


# ── Sidebar filter ────────────────────────────────────────────────
# One dropdown drives every panel below. "All" applies no filter.
payment_types = run_query(f"""
    SELECT DISTINCT payment_type_label
    FROM {DB_SCHEMA}.fct_trips
    WHERE payment_type_label IS NOT NULL
    ORDER BY 1
""")["payment_type_label"].tolist()

selected = st.sidebar.selectbox("Payment type", ["All"] + payment_types)

# The value can only be one of the fixed dropdown options, so interpolating
# it into the SQL string is safe here. If it ever came from a free-text
# input, switch to a parameterized query instead.
where_clause = "" if selected == "All" else f"WHERE payment_type_label = '{selected}'"


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
