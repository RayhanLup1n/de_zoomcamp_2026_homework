{{
    config(
        materialized='table',
        tags=['analytics', 'mart']
    )
}}

-- Trip volume by hour of day
-- Used for Dashboard Tile 2: Temporal Distribution

WITH hourly_trips AS (
    SELECT
        trip_year,
        trip_month,
        trip_day_of_week,
        trip_hour,
        taxi_type,
        COUNT(*) AS trip_count,
        AVG(fare_amount) AS avg_fare_amount,
        AVG(tip_amount) AS avg_tip_amount,
        AVG(trip_distance) AS avg_trip_distance,
        SUM(fare_amount + tip_amount + tolls_amount) AS total_revenue
    FROM {{ ref('fct_trips') }}
    GROUP BY
        trip_year,
        trip_month,
        trip_day_of_week,
        trip_hour,
        taxi_type
)

SELECT
    trip_year,
    trip_month,
    CASE
        WHEN trip_day_of_week = 0 THEN 'Sunday'
        WHEN trip_day_of_week = 1 THEN 'Monday'
        WHEN trip_day_of_week = 2 THEN 'Tuesday'
        WHEN trip_day_of_week = 3 THEN 'Wednesday'
        WHEN trip_day_of_week = 4 THEN 'Thursday'
        WHEN trip_day_of_week = 5 THEN 'Friday'
        WHEN trip_day_of_week = 6 THEN 'Saturday'
        ELSE 'Unknown'
    END AS day_of_week,
    trip_hour,
    taxi_type,
    trip_count,
    ROUND(avg_fare_amount, 2) AS avg_fare_amount,
    ROUND(avg_tip_amount, 2) AS avg_tip_amount,
    ROUND(avg_trip_distance, 2) AS avg_trip_distance,
    ROUND(total_revenue, 2) AS total_revenue

FROM hourly_trips

ORDER BY
    trip_year,
    trip_month,
    trip_day_of_week,
    trip_hour,
    taxi_type
