# Exercise: metric definitions as a contract (Ch6)

Companion to **Chapter 6: Metric Definitions** and the in-class demo "break a
metric definition." A metric without a written definition is an opinion: two
people computing the "same" number can get different results because their
assumptions differ. The definition documents those assumptions so the number is
reproducible.

The trap this exercise drills is **drift**: someone changes the SQL that produces
a metric but not the text that describes it. The code and the contract now
disagree, and the definition silently lies.

## The situation

`app.py` is finished and correct. It shows two metrics:

- **Avg fare per trip** — `AVG(fare_amount)` **where `fare_amount > 0`** (zero and
  negative fares, such as refunds, are excluded).
- **Avg trips per day** — the average of daily trip counts.

But `metric_definitions.md` is out of sync with that code:

1. The `avg_fare_per_trip` definition still describes the **old** query, before the
   `fare_amount > 0` filter was added. Its Description and Calculation are wrong.
2. The `trips_per_day` definition is a **stub**: every field says `TODO`.

## Task

Do **not** change `app.py`. Fix `metric_definitions.md` so both definitions match
what the app actually runs:

1. Read the `avg_fare` query in `app.py`. Update the definition's **Description**
   (say that zero/negative fares are excluded) and **Calculation** (add the
   `where fare_amount > 0` clause).
2. Read the `trips_per_day` query. Fill in all five fields.

## Run it

```bash
uv sync
cp .env.example .env      # set POSTGRES_URL and DB_SCHEMA
uv run streamlit run app.py
```

Read each on-screen number, then open `metric_definitions.md` beside it and check
the Calculation field would reproduce that exact number.

## Why the number barely moves (and why it still matters)

On the class dataset, excluding zero-fare trips changes the average by only a cent
or two: there are just a handful of them. The point is **not** the size of the
change. It is that a teammate who reads `AVG(fare_amount)` and reruns it will get a
*different* number the moment refunds or voided trips spike, because the filter
that protects the metric was never written down. A definition is a contract; drift
breaks it quietly.

## Success criteria

- `app.py` is unchanged.
- The `avg_fare_per_trip` Calculation includes `where fare_amount > 0`, and its
  Description says zero/negative fares are excluded.
- Every field of `trips_per_day` is filled in (no `TODO` left).
- A teammate could reproduce both on-screen numbers from the definition file alone.

## Compare

Check your work against the `practice-metric-definitions-solution` branch.
