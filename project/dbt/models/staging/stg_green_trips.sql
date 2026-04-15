{{
    config(
        materialized='table',
        tags=['staging']
    )
}}

-- Staging model for Green taxi trips
-- Source: single raw.trips_resource table, filtered by taxi type
-- Responsibilities: rename columns, filter invalid data, add computed fields

WITH cleaned_trips AS (
    SELECT
        -- Standardize column names
        vendor_id,
        CAST(lpep_pickup_datetime AS TIMESTAMP) AS pickup_datetime,
        CAST(lpep_dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,
        passenger_count,
        trip_distance,
        ratecode_id,
        store_and_fwd_flag,
        pu_location_id,
        do_location_id,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        congestion_surcharge,
        airport_fee,

        -- Metadata from dlt ingestion
        _ingest_year AS ingest_year,
        _ingest_month AS ingest_month,
        _ingest_taxi_type AS ingest_taxi_type,
        _ingest_file AS ingest_file,

        -- Create unique trip ID using row_number
        ROW_NUMBER() OVER (ORDER BY lpep_pickup_datetime, pu_location_id, do_location_id) AS row_idx

    FROM {{ source('raw', 'trips_resource') }}

    WHERE
        -- Only green taxi data
        _ingest_taxi_type = 'green'
        -- Filter invalid trips
        AND trip_distance > 0
        AND trip_distance < 100
        AND lpep_pickup_datetime IS NOT NULL
        AND lpep_dropoff_datetime IS NOT NULL
        AND CAST(lpep_pickup_datetime AS TIMESTAMP) <= CAST(lpep_dropoff_datetime AS TIMESTAMP)
        AND {{ dbt.datediff("CAST(lpep_pickup_datetime AS TIMESTAMP)", "CAST(lpep_dropoff_datetime AS TIMESTAMP)", "minute") }} > 1
        AND {{ dbt.datediff("CAST(lpep_pickup_datetime AS TIMESTAMP)", "CAST(lpep_dropoff_datetime AS TIMESTAMP)", "minute") }} < 240
)

SELECT
    -- Generate unique trip ID
    CONCAT('green-', CAST(row_idx AS STRING)) AS trip_id,

    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    ratecode_id,
    store_and_fwd_flag,
    pu_location_id,
    do_location_id,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    airport_fee,

    -- Metadata
    ingest_year,
    ingest_month,
    ingest_file,

    -- Calculate duration in minutes
    {{ dbt.datediff("pickup_datetime", "dropoff_datetime", "minute") }} AS trip_duration_minutes,

    -- Extract temporal fields for analytics
    EXTRACT(YEAR FROM pickup_datetime) AS trip_year,
    EXTRACT(MONTH FROM pickup_datetime) AS trip_month,
    EXTRACT(DAY FROM pickup_datetime) AS trip_day,
    EXTRACT(HOUR FROM pickup_datetime) AS trip_hour,
    EXTRACT(DAYOFWEEK FROM pickup_datetime) AS trip_day_of_week,

    -- Standardize taxi type label
    'Green' AS taxi_type,

    -- Payment type mapping
    CASE payment_type
        WHEN 1 THEN 'Credit Card'
        WHEN 2 THEN 'Cash'
        WHEN 3 THEN 'No Charge'
        WHEN 4 THEN 'Dispute'
        WHEN 5 THEN 'Unknown'
        WHEN 6 THEN 'Voided'
        ELSE 'Other'
    END AS payment_type_name

FROM cleaned_trips
