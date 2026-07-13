"""NYC Taxi — Week 11 ADVANCED practice: batch inputs with st.form (solution).

The two filter widgets are wrapped in `st.form`, so changing the borough or the
minimum-fare slider does NOT rerun the query. The script only re-filters when the
user clicks "Apply" (the form_submit_button). One round-trip per intended filter,
not one per keystroke.
"""

import os

import pandas as pd
import sqlalchemy
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.environ["POSTGRES_URL"]
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname")

st.set_page_config(page_title="Form practice", page_icon="📝")


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


st.title("📝 Batch inputs with a form")

boroughs = ["All"] + run_query(
    f"SELECT DISTINCT pickup_borough FROM {DB_SCHEMA}.fct_trips "
    f"WHERE pickup_borough IS NOT NULL ORDER BY 1"
)["pickup_borough"].tolist()

# The widgets only take effect when "Apply" is clicked: no rerun-per-keystroke.
with st.sidebar.form("filters"):
    borough = st.selectbox("Pickup borough", boroughs)
    min_fare = st.slider("Minimum fare ($)", 0, 100, 0)
    st.form_submit_button("Apply")

conditions = []
if borough != "All":
    conditions.append(f"pickup_borough = '{borough}'")
if min_fare:
    conditions.append(f"fare_amount >= {min_fare}")
where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

kpis = run_query(
    f"SELECT COUNT(*) AS trips, AVG(fare_amount) AS avg_fare FROM {DB_SCHEMA}.fct_trips {where}"
).iloc[0]
c1, c2 = st.columns(2)
c1.metric("Trips (filtered)", f"{int(kpis['trips']):,}")
c2.metric("Average fare", f"${kpis['avg_fare']:.2f}" if kpis["avg_fare"] is not None else "n/a")
