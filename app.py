"""NYC Taxi — Week 11 practice: metric definitions as a contract.

This app is finished and correct. The exercise is NOT in this file: it is to make
`metric_definitions.md` describe exactly what this code does. Read each query,
then reconcile the definition file so a teammate could reproduce these numbers.
"""

import os

import pandas as pd
import sqlalchemy
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.environ["POSTGRES_URL"]
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname")

st.set_page_config(page_title="Metric definitions", page_icon="📐")


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


st.title("📐 Two metrics, one contract")
st.caption("Every number here must match its entry in metric_definitions.md")

# avg_fare_per_trip EXCLUDES zero and negative fares (note the WHERE clause).
avg_fare = run_query(
    f"SELECT AVG(fare_amount) AS v "
    f"FROM {DB_SCHEMA}.fct_trips "
    f"WHERE fare_amount > 0"
).iloc[0]["v"]

# trips_per_day: average number of trips per calendar pickup day.
trips_per_day = run_query(
    f"SELECT AVG(daily_count) AS v FROM ("
    f"  SELECT date_trunc('day', pickup_datetime) AS day, COUNT(*) AS daily_count "
    f"  FROM {DB_SCHEMA}.fct_trips "
    f"  GROUP BY 1"
    f") d"
).iloc[0]["v"]

c1, c2 = st.columns(2)
c1.metric("Avg fare per trip", f"${avg_fare:,.2f}")
c2.metric("Avg trips per day", f"{trips_per_day:,.0f}")
