{{
    config(
        materialized='table',
        tags=['analytics', 'mart']
    )
}}

-- Trip count and percentage by payment type
-- Used for Dashboard Tile 1: Categorical Distribution
WITH trip_counts AS (
    SELECT
        payment_type_name,
        trip_year,
        taxi_type,
        COUNT(*) AS trip_count
    FROM {{ ref('fct_trips') }}
    WHERE trip_year IS NOT NULL
    GROUP BY
        payment_type_name,
        trip_year,
        taxi_type
),
total_trips AS (
    SELECT
        trip_year,
        taxi_type,
        SUM(trip_count) AS total_count
    FROM trip_counts
    GROUP BY
        trip_year,
        taxi_type
)
SELECT
    tc.payment_type_name,
    tc.trip_year,
    tc.taxi_type,
    tc.trip_count,
    tt.total_count AS total_trip_count,
    ROUND(
        tc.trip_count * 100.0 / tt.total_count,
        2
    ) AS percentage
FROM trip_counts tc
JOIN total_trips tt
    ON tc.trip_year = tt.trip_year
    AND tc.taxi_type = tt.taxi_type
ORDER BY
    tc.trip_year DESC,
    tc.taxi_type,
    tc.trip_count DESC
