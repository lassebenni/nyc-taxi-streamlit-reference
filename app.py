"""NYC Taxi — Week 11 ADVANCED practice: batch inputs with st.form (starter).

This goes beyond the Week 11 chapters. Without a form, Streamlit reruns the whole
script (and re-queries Postgres) on EVERY widget change: every dropdown pick and
every slider drag. When several inputs belong together (a filter), you usually
want the query to run once, after the user has set all of them and clicked a
button. `st.form` batches inputs and only reruns on submit.

TODO: wrap the two filter widgets in a form with a submit button. See EXERCISE.md.
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

# TODO: wrap these two widgets in `with st.sidebar.form("filters"):` and add
#       `submitted = st.form_submit_button("Apply")`. Without a form, moving
#       EITHER widget reruns the script and re-filters immediately.
borough = st.sidebar.selectbox("Pickup borough", boroughs)
min_fare = st.sidebar.slider("Minimum fare ($)", 0, 100, 0)

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
