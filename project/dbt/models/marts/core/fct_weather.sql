{{
    config(
        materialized='table',
        tags=['core', 'mart'],
        partition_by={
            "field": "observation_date",
            "data_type": "date",
            "granularity": "month"
        },
        cluster_by=["city_name"]
    )
}}

-- Fact table: all daily weather observations across Indonesian cities
-- This is the single source of truth for all downstream analytics models.
--
-- BigQuery Optimization (ignored when running on DuckDB):
--   PARTITIONED BY observation_date (monthly granularity)
--     -> Reason: Most dashboard queries filter by date range (e.g., "show me 2024 data")
--     -> Benefit: BigQuery only scans relevant monthly partitions, reducing cost and latency
--
--   CLUSTERED BY city_name
--     -> Reason: Nearly all analytics queries filter or group by city
--     -> Benefit: Data is co-located by city within each partition for faster reads
--
-- These optimizations make the table efficient for the two main query patterns:
--   1. "Compare cities for year X" -> partition prunes to year, cluster on city
--   2. "Show monthly trend for city Y" -> cluster prunes to city, partition on month

SELECT
    weather_id,
    city_name,
    latitude,
    longitude,
    observation_date,
    observation_year,
    observation_month,
    observation_day,
    temperature_max_c,
    temperature_min_c,
    temperature_mean_c,
    temperature_range_c,
    precipitation_mm,
    rain_mm,
    wind_speed_max_kmh,
    sunshine_hours,
    weather_code,
    weather_description,
    weather_category,
    is_rainy_day

FROM {{ ref('stg_daily_weather') }}
