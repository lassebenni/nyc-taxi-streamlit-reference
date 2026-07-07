"""NYC Taxi metrics dashboard — reference Streamlit app.

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres and renders KPI
tiles, a daily trip-volume chart, and a data-freshness panel. No orchestration
involved: the app queries the table directly.
"""

import os

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.environ["POSTGRES_URL"]
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname")


@st.cache_data(ttl=60)
def get_trip_metrics(pg_url: str, schema: str) -> dict:
    with psycopg2.connect(pg_url) as conn, conn.cursor() as cur:
        cur.execute(
            f"SELECT COUNT(*), AVG(fare_amount), SUM(fare_amount) FROM {schema}.fct_trips"
        )
        trip_count, avg_fare, total_fare = cur.fetchone()
    return {
        "trip_count": trip_count or 0,
        "avg_fare": float(avg_fare or 0),
        "total_fare": float(total_fare or 0),
    }


@st.cache_data(ttl=60)
def get_daily_trips(pg_url: str, schema: str) -> pd.DataFrame:
    with psycopg2.connect(pg_url) as conn, conn.cursor() as cur:
        cur.execute(
            f"SELECT date_trunc('day', pickup_datetime) AS day, COUNT(*) AS trips "
            f"FROM {schema}.fct_trips GROUP BY 1 ORDER BY 1"
        )
        rows = cur.fetchall()
    return pd.DataFrame(rows, columns=["day", "trips"]).set_index("day")


@st.cache_data(ttl=60)
def get_fct_trips_freshness(pg_url: str, schema: str) -> dict:
    with psycopg2.connect(pg_url) as conn, conn.cursor() as cur:
        cur.execute(
            f"SELECT COUNT(*), MAX(pickup_datetime) FROM {schema}.fct_trips"
        )
        row_count, last_pickup = cur.fetchone()
    return {"row_count": row_count or 0, "last_pickup": last_pickup}


st.title("NYC Taxi Metrics")

st.subheader("Headline KPIs")
metrics = get_trip_metrics(POSTGRES_URL, DB_SCHEMA)
c1, c2, c3 = st.columns(3)
c1.metric("Total trips", f"{metrics['trip_count']:,}")
c2.metric("Avg fare", f"${metrics['avg_fare']:.2f}")
c3.metric("Total fare revenue", f"${metrics['total_fare']:,.0f}")

st.subheader("Daily trip volume")
st.line_chart(get_daily_trips(POSTGRES_URL, DB_SCHEMA))

st.subheader("Data freshness")
freshness = get_fct_trips_freshness(POSTGRES_URL, DB_SCHEMA)
f1, f2 = st.columns(2)
f1.metric("Row count", f"{freshness['row_count']:,}")
last = freshness["last_pickup"]
f2.metric("Last pickup", str(last) if last else "None")
