# Question 1: Extract Task File Size

### Question
Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?
- **128.3 MiB**
- 134.5 MiB
- 364.7 MiB
- 692.6 MiB

### Methodology
To answer this question, the flow `04_postgres_taxi.yaml` was executed with the following parameters:
- `taxi`: yellow
- `year`: 2020
- `month`: 12

After the execution completed successfully, the file size was verified in the **Outputs** tab of the `extract` task in the Kestra UI.

### Answer
The uncompressed file size is **128.3 MiB**.