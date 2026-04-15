{{
    config(
        materialized='table',
        tags=['core', 'mart']
    )
}}

-- Fact table: Union ALL taxi trips (green + yellow) into one table
-- This is the single source of truth for all downstream analytics models

SELECT
    trip_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    ratecode_id,
    store_and_fwd_flag,
    pu_location_id,
    do_location_id,
    payment_type,
    payment_type_name,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    airport_fee,
    trip_duration_minutes,
    trip_year,
    trip_month,
    trip_day,
    trip_hour,
    trip_day_of_week,
    taxi_type,
    ingest_year,
    ingest_month,
    ingest_file

FROM {{ ref('stg_green_trips') }}

UNION ALL

SELECT
    trip_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    ratecode_id,
    store_and_fwd_flag,
    pu_location_id,
    do_location_id,
    payment_type,
    payment_type_name,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    airport_fee,
    trip_duration_minutes,
    trip_year,
    trip_month,
    trip_day,
    trip_hour,
    trip_day_of_week,
    taxi_type,
    ingest_year,
    ingest_month,
    ingest_file

FROM {{ ref('stg_yellow_trips') }}
