# Module 4 Homework - Question 1

## Question: dbt Lineage and Execution

Given a dbt project with the following structure:

```
models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
```

If you run `dbt run --select int_trips_unioned`, what models will be built?

### Options:
- A) `stg_green_tripdata`, `stg_yellow_tripdata`, and `int_trips_unioned` (upstream dependencies)
- B) Any model with upstream and downstream dependencies to `int_trips_unioned`
- C) `int_trips_unioned` only
- D) `int_trips_unioned`, `int_trips`, and `fct_trips` (downstream dependencies)

---

### Answer: C

**Reasoning:**
- `dbt run --select <model>` without any additional operator only runs the model(s) that exactly match the selection criteria
- To include upstream dependencies, you need to use the `+` operator:
  - `--select int_trips_unioned` → runs only `int_trips_unioned`
  - `--select +int_trips_unioned` → runs `stg_green_tripdata`, `stg_yellow_tripdata`, and `int_trips_unioned`
- Proof from practical testing:
  - Without `+`: `int_trips_unioned` fails because upstream dependencies are not built
  - With `+`: All 3 models are successfully built (staging + intermediate)

