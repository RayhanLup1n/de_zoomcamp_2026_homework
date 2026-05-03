{{
    config(
        materialized='table',
        tags=['analytics', 'mart']
    )
}}

-- Monthly weather trends across all cities
-- Used for Dashboard Tile 2: Temporal Distribution (Monthly Trends)
-- Shows how weather patterns change across months and years

SELECT
    city_name,
    observation_year,
    observation_month,
    COUNT(*) AS days_in_period,

    -- Temperature trends
    ROUND(AVG(temperature_mean_c), 1) AS avg_temperature_c,
    ROUND(AVG(temperature_max_c), 1) AS avg_max_temperature_c,
    ROUND(AVG(temperature_min_c), 1) AS avg_min_temperature_c,

    -- Precipitation trends
    ROUND(SUM(precipitation_mm), 1) AS total_precipitation_mm,
    ROUND(AVG(precipitation_mm), 1) AS avg_daily_precipitation_mm,
    SUM(CASE WHEN is_rainy_day THEN 1 ELSE 0 END) AS rainy_days,

    -- Other metrics
    ROUND(AVG(wind_speed_max_kmh), 1) AS avg_wind_speed_kmh,
    ROUND(AVG(sunshine_hours), 1) AS avg_sunshine_hours

FROM {{ ref('fct_weather') }}
GROUP BY city_name, observation_year, observation_month
ORDER BY city_name, observation_year, observation_month
