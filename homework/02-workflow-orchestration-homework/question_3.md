# Question 3: Yellow Taxi 2020 Row Count

### Question
How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?
- 13,537,299
- **24,648,499**
- 18,324,219
- 29,430,127

### Methodology
1. Executed a **Backfill** for the `Yellow` taxi dataset for the entire year of 2020 using the `05_postgres_taxi_scheduled.yaml` flow.
2. After all 12 months were loaded into the Postgres database, the following query flow was used to count the total rows:

```yaml
id: cek_data_hasil_nomor_3
namespace: zoomcamp

tasks:
  - id: total_baris_yellow_2020
    type: io.kestra.plugin.jdbc.postgresql.Queries
    sql: |
      SELECT COUNT(*) as total 
      FROM public.yellow_tripdata 
      WHERE filename LIKE 'yellow_tripdata_2020%';
    fetchType: FETCH_ONE

  - id: log_hasil
    type: io.kestra.plugin.core.log.Log
    message: "Total baris Yellow Taxi 2020 adalah: {{ outputs.total_baris_yellow_2020.row.total }}"

pluginDefaults:
  - type: io.kestra.plugin.jdbc.postgresql
    values:
      url: jdbc:postgresql://postgres:5432/kestra
      username: kestra
      password: k3str4
```

### Answer
The total number of rows for Yellow Taxi data in 2020 is **24,648,499**.
