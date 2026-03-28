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
        # Note: In PyFlink, session window syntax may vary
        # This is the standard SQL syntax for session windows
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
