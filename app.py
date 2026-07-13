"""NYC Taxi metrics dashboard — Week 11 Streamlit starter (Chapter 5).

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres. This is the
starting point for the "Building a Metrics Dashboard" chapter: the
run_query caching helper and page setup are already here. Add each panel
(headline KPIs, daily trip volume, data freshness, dataset health, and the
sidebar borough filter) directly to this file as you follow the chapter.

See the chapter-5-solution branch for the finished dashboard.
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
