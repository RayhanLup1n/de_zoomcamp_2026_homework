{{
    config(
        materialized='table',
        tags=['analytics', 'mart']
    )
}}

-- Weather metrics aggregated by city and year
-- Used for Dashboard Tile 1: City Comparison (Categorical Distribution)
-- Shows how weather patterns differ across Indonesian cities

SELECT
    city_name,
    observation_year,
    COUNT(*) AS total_observations,

    -- Temperature metrics
    ROUND(AVG(temperature_mean_c), 1) AS avg_temperature_c,
    ROUND(MIN(temperature_min_c), 1) AS min_temperature_c,
    ROUND(MAX(temperature_max_c), 1) AS max_temperature_c,
    ROUND(AVG(temperature_range_c), 1) AS avg_daily_range_c,

    -- Precipitation metrics
    ROUND(SUM(precipitation_mm), 1) AS total_precipitation_mm,
    ROUND(AVG(precipitation_mm), 1) AS avg_daily_precipitation_mm,
    SUM(CASE WHEN is_rainy_day THEN 1 ELSE 0 END) AS rainy_days,

    -- Wind metrics
    ROUND(AVG(wind_speed_max_kmh), 1) AS avg_wind_speed_kmh,
    ROUND(MAX(wind_speed_max_kmh), 1) AS max_wind_speed_kmh,

    -- Sunshine metrics
    ROUND(AVG(sunshine_hours), 1) AS avg_sunshine_hours,

    -- Weather category distribution
    SUM(CASE WHEN weather_category = 'Clear' THEN 1 ELSE 0 END) AS clear_days,
    SUM(CASE WHEN weather_category = 'Cloudy' THEN 1 ELSE 0 END) AS cloudy_days,
    SUM(CASE WHEN weather_category IN ('Rain', 'Rain Showers', 'Drizzle') THEN 1 ELSE 0 END) AS rain_category_days,
    SUM(CASE WHEN weather_category = 'Thunderstorm' THEN 1 ELSE 0 END) AS thunderstorm_days

FROM {{ ref('fct_weather') }}
GROUP BY city_name, observation_year
ORDER BY city_name, observation_year
