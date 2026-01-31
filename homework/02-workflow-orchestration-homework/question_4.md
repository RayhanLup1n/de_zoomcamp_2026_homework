# Question 4: Green Taxi 2020 Row Count

### Question
How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?
- 5,327,301
- 936,199
- **1,734,051**
- 1,342,034

### Methodology
1. Executed a **Backfill** for the `Green` taxi dataset for the entire year of 2020 using the `05_postgres_taxi_scheduled.yaml` flow.
2. Used the following kestra flow to query the database and retrieve the count:

```yaml
id: cek_data_hasil
namespace: zoomcamp

tasks:
  - id: total_baris_green_2020
    type: io.kestra.plugin.jdbc.postgresql.Queries
    sql: |
      SELECT COUNT(*) as total 
      FROM public.green_tripdata 
      WHERE filename LIKE 'green_tripdata_2020%';
    fetchType: FETCH_ONE

  - id: log_hasil
    type: io.kestra.plugin.core.log.Log
    message: "Total baris Green Taxi 2020 adalah: {{ outputs.total_baris_green_2020.row.total }}"

pluginDefaults:
  - type: io.kestra.plugin.jdbc.postgresql
    values:
      url: jdbc:postgresql://postgres:5432/kestra
      username: kestra
      password: k3str4
```

### Answer
The total number of rows for Green Taxi data in 2020 is **1,734,051**.
