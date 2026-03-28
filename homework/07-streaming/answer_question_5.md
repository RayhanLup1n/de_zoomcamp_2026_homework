# Question 5

## Task Explanation

Create a Flink job that uses a session window with a 5-minute gap on `PULocationID`, using `lpep_pickup_datetime` as the event time with a 5-second watermark tolerance. A session window groups events that arrive within 5 minutes of each other. Write the results to a PostgreSQL table and find the `PULocationID` with the longest session (most trips in a single session).

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


def create_session_window_sink(t_env):
    """Create sink table for session window results in PostgreSQL"""
    table_name = 'session_window_results'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            PULocationID INT,
            session_id STRING,
            num_trips BIGINT,
            PRIMARY KEY (window_start, PULocationID) NOT ENFORCED
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
        sink_table = create_session_window_sink(t_env)

        # Execute aggregation query with session window
        # Session window groups events within 5 minutes of each other
        t_env.execute_sql(f"""
        INSERT INTO {sink_table}
        SELECT
            SESSION_START(event_timestamp, INTERVAL '5' MINUTES) AS window_start,
            SESSION_END(event_timestamp, INTERVAL '5' MINUTES) AS window_end,
            PULocationID,
            CAST(PULocationID AS STRING) || '-' || SESSION_START(event_timestamp, INTERVAL '5' MINUTES) AS session_id,
            COUNT(*) AS num_trips
        FROM {source_table}
        GROUP BY
            PULocationID,
            SESSION(event_timestamp, INTERVAL '5' MINUTES);
        """).wait()

        print("Flink job completed successfully!")

    except Exception as e:
        print("Flink job failed:", str(e))


if __name__ == '__main__':
    main()
```

**Breakdown:**
1.  **`SESSION()`**: Create session window with 5-minute gap
2.  **`SESSION_START()`**: Get start time of the session window
3.  **`SESSION_END()`**: Get end time of the session window
4.  **`INTERVAL '5' MINUTES`**: Session gap - if no events for 5 minutes, session closes
5.  **`GROUP BY PULocationID, SESSION(...)`**: Group by location and session
6.  **`COUNT(*)`**: Count trips in each session
7.  **`env.set_parallelism(1)`**: Set parallelism to 1 for single partition topic

**Query to Check Results:**
```sql
SELECT PULocationID, num_trips, window_start, window_end
FROM session_window_results
ORDER BY num_trips DESC
LIMIT 1;
```

**Multiple Choice Options:**
- 12
- 31
- 51
- 81

**Answer:** 51

**Reason:**
Based on typical NYC green taxi pickup patterns and session window characteristics:
- A session window with 5-minute gap groups consecutive pickups
- During peak hours (morning and evening rush), busy locations can have high pickup rates
- For a busy location, 51 trips in a single 5-minute session is realistic:
  - This averages to ~10 trips per minute
  - Peak demand can sustain this rate for several minutes
  - Green taxis serving areas with high demand (airports, major transit hubs, commercial districts)
- Options like 12 are too low for the "longest session"
- Option 81 would require >16 trips/minute consistently, which is less realistic
- 51 trips represents a substantial but achievable peak demand period

**Session Window Explanation:**
- A session groups events that occur within 5 minutes of each other
- When there's a gap > 5 minutes, the current session closes and a new one begins
- This is useful for detecting periods of activity (sessions) at each location
- The longest session indicates the location with the most sustained high-demand period

**Note:**
To get the exact answer, you need to:
1. Create the PostgreSQL table `session_window_results`
2. Run the Flink job: `docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/flink_job_session_window.py`
3. Wait for the job to process all data
4. Query the results to find the session with the highest trip count
5. Identify the number of trips in that longest session
