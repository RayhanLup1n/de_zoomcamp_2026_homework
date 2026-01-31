# Question 5: Yellow Taxi March 2021 Row Count

### Question
How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?
- 1,428,092
- 706,911
- **1,925,152**
- 2,561,031

### Methodology
1. Executed the flow manually for Yellow Taxi, Year 2021, and Month 03.
2. Used the following query flow to check the row count in the database:

```yaml
id: cek_data_hasil_nomor_5
namespace: zoomcamp

tasks:
  - id: total_baris_yellow_maret_2021
    type: io.kestra.plugin.jdbc.postgresql.Queries
    sql: |
      SELECT COUNT(*) as total 
      FROM public.yellow_tripdata 
      WHERE filename LIKE 'yellow_tripdata_2021_03%';
    fetchType: FETCH_ONE

  - id: log_hasil
    type: io.kestra.plugin.core.log.Log
    message: "Total baris Yellow Taxi Maret 2021 adalah: {{ outputs.total_baris_yellow_maret_2021.row.total }}"

pluginDefaults:
  - type: io.kestra.plugin.jdbc.postgresql
    values:
      url: jdbc:postgresql://postgres:5432/kestra
      username: kestra
      password: k3str4
```

### Answer
The total number of rows for Yellow Taxi in March 2021 is **1,925,152**.
