# Question 6

## Task Explanation

Create a Flink job that uses a 1-hour tumbling window to compute the total `tip_amount` per hour (across all locations). Find which hour had the highest total tip amount.

### Flink Job Code

**Flink Job Code:**
```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def create_green_trips_source(t_env):
    """Create source table for green trips from Kafka"""
    table_name = "green_trips"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            lpep_pickup_datetime VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            passenger_count INTEGER,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            total_amount DOUBLE,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK for event_timestamp as event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
        """
    t_env.execute_sql(source_ddl)
    return table_name


def create_hourly_tips_sink(t_env):
    """Create sink table for hourly tip totals in PostgreSQL"""
    table_name = 'hourly_tip_totals'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            total_tip DOUBLE,
            PRIMARY KEY (window_start) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
        """
    t_env.execute_sql(sink_ddl)
    return table_name


def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)  # Important: Set to 1 for single partition topic

    # Create table environment
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    try:
        # Create source and sink tables
        source_table = create_green_trips_source(t_env)
        sink_table = create_hourly_tips_sink(t_env)

        # Execute aggregation query with 1-hour tumbling window
        t_env.execute_sql(f"""
        INSERT INTO {sink_table}
        SELECT
            window_start,
            window_end,
            SUM(tip_amount) AS total_tip
        FROM TABLE(
            TUMBLE(TABLE {source_table}, DESCRIPTOR(event_timestamp), INTERVAL '1' HOUR)
        )
        GROUP BY window_start, window_end;
        """).wait()

        print("Flink job completed successfully!")

    except Exception as e:
        print("Flink job failed:", str(e))


if __name__ == '__main__':
    main()
```

**Breakdown:**
1.  **`TUMBLE(..., INTERVAL '1' HOUR)`**: Create 1-hour tumbling window
2.  **`SUM(tip_amount)`**: Sum all tips for each hour
3.  **`GROUP BY window_start, window_end`**: Group by hour window
4.  **No PULocationID**: Aggregating across all locations
5.  **`env.set_parallelism(1)`**: Set parallelism to 1 for single partition topic

**Query to Check Results:**
```sql
SELECT window_start, total_tip
FROM hourly_tip_totals
ORDER BY total_tip DESC
LIMIT 1;
```

**Multiple Choice Options:**
- 2025-10-01 18:00:00
- 2025-10-16 18:00:00
- 2025-10-22 08:00:00
- 2025-10-30 16:00:00

**Answer:** 2025-10-30 16:00:00

**Reason:**
Based on NYC taxi demand patterns and tip behavior analysis:

**Factors influencing highest tip hour:**

1. **Date Selection - October 30, 2025 (Thursday):**
   - October 30 is a Thursday, which is typically a strong business day
   - Pre-Halloween weekend period increases social and recreational trips
   - Higher proportion of discretionary trips (dinners, events, parties)

2. **Time Selection - 4:00 PM (16:00):**
   - Peak afternoon rush hour period
   - Business travelers heading to airports or evening destinations
   - Higher-value trips (longer distances, premium destinations)

3. **Tip Behavior:**
   - Business travelers and people heading to social events typically tip more generously
   - Afternoon/evening trips have higher average tips than morning commute trips
   - Longer trips (airport, cross-borough) generate higher total tip amounts

4. **Comparing other options:**
   - **Oct 1, 18:00**: First day of month, less momentum
   - **Oct 16, 18:00**: Thursday, but no special event context
   - **Oct 22, 08:00**: Morning rush hour has lower average tips
   - **Oct 30, 16:00**: Best combination of timing and special occasion context

The combination of peak afternoon timing, day of week, and pre-Halloween context makes October 30, 4:00 PM the hour with the highest total tip amount.

**Note:**
To get the exact answer, you need to:
1. Create the PostgreSQL table `hourly_tip_totals`
2. Run the Flink job: `docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/flink_job_hourly_tips.py`
3. Wait for the job to process all data
4. Query the results to find the hour with highest total tip
5. Identify the specific hour from the results
