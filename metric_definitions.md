# Metric definitions

A metric definition is a **contract**: anyone should be able to read it and
reproduce the exact number the app shows. Each metric needs all five fields
(Name, Description, Calculation, Data source, Refresh frequency).

Two things are wrong with this file. Fix both so it matches `app.py`.

---

## avg_fare_per_trip

> ⚠️ **This definition has drifted from the code.** Open `app.py` and read the
> query that computes `avg_fare`. The Description and Calculation below describe
> an older version that did **not** exclude zero-fare and negative-fare trips.
> Update both fields so the contract matches what the app actually runs.

| Field | Value |
|---|---|
| **Name** | `avg_fare_per_trip` |
| **Description** | Average fare charged per taxi trip. |
| **Calculation** | `AVG(fare_amount)` on `fct_trips` |
| **Data source** | `dev_<name>.fct_trips` (built by your Week 10 dbt project) |
| **Refresh frequency** | Once per day, after the dbt build |

---

## trips_per_day

> ⚠️ **This definition is a stub.** The app shows an "Avg trips per day" metric,
> but nobody documented it. Read the second query in `app.py` and fill in all
> five fields.

| Field | Value |
|---|---|
| **Name** | `trips_per_day` |
| **Description** | TODO |
| **Calculation** | TODO |
| **Data source** | TODO |
| **Refresh frequency** | TODO |
