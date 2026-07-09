"""NYC Taxi metrics dashboard — Week 11 Streamlit starter.

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres. This is the
starting point for the "Streamlit Fundamentals" chapter: all three query
functions are stubbed with TODOs. Pick a specific exercise branch
(03-exercise-kpi-metrics, 04-exercise-daily-trend) to practice one function
at a time. See each branch's EXERCISE.md, or the -solution branches for the
fully working app. Your Week 11 assignment dashboard is a separate project;
see the "Building a Metrics Dashboard" chapter.
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
    """Return headline KPIs for fct_trips.

    TODO: implement this function.
    Use psycopg2.connect(pg_url) to connect.
    Run: SELECT COUNT(*), AVG(fare_amount), SUM(fare_amount) FROM {schema}.fct_trips
    Return a dict: {"trip_count": int, "avg_fare": float, "total_fare": float}
    """
    raise NotImplementedError("TODO: implement get_trip_metrics")


@st.cache_data(ttl=60)
def get_daily_trips(pg_url: str, schema: str) -> pd.DataFrame:
    """Return daily trip counts for fct_trips, indexed by day.

    TODO: implement this function.
    Use psycopg2.connect(pg_url) to connect.
    Run: SELECT date_trunc('day', pickup_datetime) AS day, COUNT(*) AS trips
         FROM {schema}.fct_trips GROUP BY 1 ORDER BY 1
    Return a pandas.DataFrame with columns ["day", "trips"], indexed by "day".
    """
    raise NotImplementedError("TODO: implement get_daily_trips")


@st.cache_data(ttl=60)
def get_fct_trips_freshness(pg_url: str, schema: str) -> dict:
    """Return row count and most recent pickup timestamp for fct_trips.

    TODO: implement this function.
    Use psycopg2.connect(pg_url) to connect.
    Run: SELECT COUNT(*), MAX(pickup_datetime) FROM {schema}.fct_trips
    Return a dict: {"row_count": int, "last_pickup": datetime | None}
    """
    raise NotImplementedError("TODO: implement get_fct_trips_freshness")


st.title("NYC Taxi Metrics")

st.subheader("Headline KPIs")
try:
    metrics = get_trip_metrics(POSTGRES_URL, DB_SCHEMA)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total trips", f"{metrics['trip_count']:,}")
    c2.metric("Avg fare", f"${metrics['avg_fare']:.2f}")
    c3.metric("Total fare revenue", f"${metrics['total_fare']:,.0f}")
except NotImplementedError:
    st.warning("Implement `get_trip_metrics` to see the KPI tiles.")

st.subheader("Daily trip volume")
try:
    st.line_chart(get_daily_trips(POSTGRES_URL, DB_SCHEMA))
except NotImplementedError:
    st.warning("Implement `get_daily_trips` to see the trend chart.")

st.subheader("Data freshness")
try:
    freshness = get_fct_trips_freshness(POSTGRES_URL, DB_SCHEMA)
    f1, f2 = st.columns(2)
    f1.metric("Row count", f"{freshness['row_count']:,}")
    last = freshness["last_pickup"]
    f2.metric("Last pickup", str(last) if last else "None")
except NotImplementedError:
    st.warning("Implement `get_fct_trips_freshness` to see the freshness panel.")
