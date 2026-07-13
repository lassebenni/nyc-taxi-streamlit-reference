"""NYC Taxi metrics dashboard — finished app for Building a Metrics Dashboard.

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres and renders
headline KPIs, a daily trip-volume chart, a data-freshness panel, database-
side dataset-health metrics, and a sidebar borough filter. Matches the
Building a Metrics Dashboard chapter panel by panel.
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


# Place near the top, before the panels.
with st.sidebar:
    st.header("Filters")
    boroughs = run_query(f"""
        SELECT DISTINCT pickup_borough
        FROM {DB_SCHEMA}.fct_trips
        WHERE pickup_borough IS NOT NULL
        ORDER BY 1
    """)["pickup_borough"].tolist()
    selected = st.selectbox("Pickup borough", options=["All"] + boroughs)

# Build a reusable WHERE clause from the selection.
where = "" if selected == "All" else f"WHERE pickup_borough = '{selected}'"

st.subheader("Headline KPIs")
kpis = run_query(f"""
    SELECT COUNT(*)          AS trip_count,
           AVG(fare_amount)  AS avg_fare,
           SUM(fare_amount)  AS total_fare
    FROM {DB_SCHEMA}.fct_trips {where}
""").iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total trips", f"{int(kpis['trip_count']):,}")
col2.metric("Average fare", f"${kpis['avg_fare']:.2f}")
col3.metric("Total revenue", f"${kpis['total_fare']:,.0f}")

st.subheader("Daily trip volume")
daily = run_query(f"""
    SELECT date_trunc('day', pickup_datetime) AS day,
           COUNT(*)                           AS trips
    FROM {DB_SCHEMA}.fct_trips {where}
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
    FROM {DB_SCHEMA}.fct_trips {where}
""").iloc[0]

col1, col2 = st.columns(2)
col1.metric("Row count", f"{int(fresh['row_count']):,}")
col2.metric("Last pickup", str(fresh["last_pickup"])[:16] if fresh["last_pickup"] else "unknown")

# Table-level metrics ignore the borough filter: they describe the mart
# itself, not a slice of its rows.
try:
    size = run_query(
        f"SELECT pg_size_pretty(pg_total_relation_size('{DB_SCHEMA}.fct_trips')) AS mart_size"
    ).iloc[0]
    span = run_query(f"""
        SELECT MIN(pickup_datetime)::date        AS first_day,
               MAX(pickup_datetime)::date        AS last_day,
               COUNT(DISTINCT pickup_datetime::date) AS n_days
        FROM {DB_SCHEMA}.fct_trips
    """).iloc[0]
    tables = run_query(f"""
        SELECT COUNT(*) AS n
        FROM information_schema.tables
        WHERE table_schema = '{DB_SCHEMA}'
    """).iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Mart size on disk", size["mart_size"])
    col2.metric("Date range", f"{span['first_day']} to {span['last_day']}")
    col3.metric("Tables in schema", int(tables["n"]))
    st.caption(f"Covers {int(span['n_days'])} days of trips.")
except Exception:
    st.caption("Database-side metrics unavailable: your role may lack catalog access.")
