# Metric definitions

A metric definition is a **contract**: anyone should be able to read it and
reproduce the exact number the app shows. Each metric needs all five fields
(Name, Description, Calculation, Data source, Refresh frequency).

---

## avg_fare_per_trip

| Field | Value |
|---|---|
| **Name** | `avg_fare_per_trip` |
| **Description** | Average fare charged per completed taxi trip, **excluding zero-fare and negative-fare trips** (refunds, voided rides). |
| **Calculation** | `AVG(fare_amount)` on `fct_trips` **where `fare_amount > 0`** |
| **Data source** | `dev_<name>.fct_trips` (built by your Week 10 dbt project) |
| **Refresh frequency** | Once per day, after the dbt build |

---

## trips_per_day

| Field | Value |
|---|---|
| **Name** | `trips_per_day` |
| **Description** | Average number of taxi trips per calendar pickup day, across the full date range in the mart. |
| **Calculation** | `AVG(daily_count)`, where `daily_count = COUNT(*)` grouped by `date_trunc('day', pickup_datetime)` on `fct_trips` |
| **Data source** | `dev_<name>.fct_trips` (built by your Week 10 dbt project) |
| **Refresh frequency** | Once per day, after the dbt build |
