"""NYC Taxi Streamlit Reference — main landing branch.

This branch is a signpost, not a dashboard. It holds the shared project setup
(pyproject.toml, uv.lock, .env.example) and points you at the branch to start on.
Run it to see where to go, then `git switch` to a chapter or practice branch.
"""

import streamlit as st

st.set_page_config(page_title="NYC Taxi Streamlit Reference", page_icon="🗺️")
st.title("NYC Taxi — Streamlit Reference")
st.caption("HYF Data Track · Week 11 (Dashboarding)")

st.info("You are on the **main** branch. Pick a branch below, then `git switch` to it.")

st.subheader("Chapter track (self-study)")
st.markdown(
    "- `chapter-4-start` — Streamlit Fundamentals (Ch4): build up from a bare app.\n"
    "- `chapter-5-start` — Building a Metrics Dashboard (Ch5): assemble the panels.\n"
    "- `chapter-5-solution` — the finished dashboard (full reference)."
)

st.subheader("Practice / live-build track")
st.markdown(
    "- `practice-kpi-metrics` (+`-solution`) — the live class build; fill `render_kpi_panel`.\n"
    "- `practice-daily-trend` (+`-solution`) — fill `render_daily_trend_panel`."
)

st.divider()
st.code(
    "git switch practice-kpi-metrics   # or any branch above\n"
    "uv sync                           # pinned Python via .python-version\n"
    "cp .env.example .env              # set POSTGRES_URL + DB_SCHEMA\n"
    "uv run streamlit run app.py",
    language="bash",
)
