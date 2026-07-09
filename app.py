"""NYC Taxi metrics dashboard — Week 11 Streamlit starter (Chapter 4).

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres. This is the
starting point for the "Streamlit Fundamentals" chapter: add the primitives
(st.title, st.metric, st.columns, st.dataframe, st.line_chart) and the
Postgres/caching examples directly to this file as you follow along.

The "Building a Metrics Dashboard" chapter continues on the chapter-5-start
branch, which scaffolds the real dashboard this file leads into.
"""

import os

import pandas as pd
import sqlalchemy
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.environ["POSTGRES_URL"]
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname")

st.title("NYC Taxi Metrics")
