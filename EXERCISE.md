# Exercise (advanced): batch inputs with st.form

> ⚙️ **Advanced / beyond the chapters.** This exercise is optional. It is not
> required for the Week 11 assignment; it teaches a Streamlit pattern you will
> want once your dashboards have several filters.

Streamlit reruns the whole script on **every** widget change. With two separate
filter widgets, picking a borough reruns and re-queries, and then dragging the
minimum-fare slider reruns and re-queries again: two DB round-trips for one
intended filter. When inputs belong together, `st.form` collects them and only
reruns when a submit button is clicked.

## Task

Open `app.py`. Right now the borough `selectbox` and the fare `slider` are loose
in the sidebar, so each change re-filters immediately.

Wrap them in a form with a submit button:

```python
with st.sidebar.form("filters"):
    borough = st.selectbox("Pickup borough", boroughs)
    min_fare = st.slider("Minimum fare ($)", 0, 100, 0)
    st.form_submit_button("Apply")
```

Now changing either widget does nothing until **Apply** is clicked.

## Run it

```bash
uv sync
cp .env.example .env      # set POSTGRES_URL and DB_SCHEMA
uv run streamlit run app.py
```

## Success criteria

- Before: changing the borough or slider re-filters the KPIs immediately.
- After: the KPIs only change when you click **Apply**, no matter how many times
  you move the widgets first.

## Stretch

Add `clear_on_submit=False` and a second `st.form_submit_button("Reset")` that,
when clicked, filters back to "All".

## Compare

Check your work against the `practice-form-solution` branch.
