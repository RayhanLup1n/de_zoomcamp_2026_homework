{{
    config(
        materialized='table',
        tags=['staging']
    )
}}

-- Staging model for daily weather observations
-- Source: raw.daily_weather loaded by dlt from Open-Meteo API
-- Responsibilities: clean data, standardize types, add computed fields

WITH source AS (
    SELECT * FROM {{ source('raw', 'daily_weather') }}
),

cleaned AS (
    SELECT
        city_name,
        latitude,
        longitude,
        CAST(observation_date AS DATE) AS observation_date,

        -- Temperature metrics (Celsius)
        ROUND(CAST(temperature_2m_max AS DOUBLE), 1) AS temperature_max_c,
        ROUND(CAST(temperature_2m_min AS DOUBLE), 1) AS temperature_min_c,
        ROUND(CAST(temperature_2m_mean AS DOUBLE), 1) AS temperature_mean_c,
        ROUND(
            CAST(temperature_2m_max AS DOUBLE) - CAST(temperature_2m_min AS DOUBLE), 1
        ) AS temperature_range_c,

        -- Precipitation metrics (millimeters)
        ROUND(COALESCE(CAST(precipitation_sum AS DOUBLE), 0), 1) AS precipitation_mm,
        ROUND(COALESCE(CAST(rain_sum AS DOUBLE), 0), 1) AS rain_mm,

        -- Wind speed (km/h)
        ROUND(COALESCE(CAST(windspeed_10m_max AS DOUBLE), 0), 1) AS wind_speed_max_kmh,

        -- Sunshine duration (convert from seconds to hours)
        ROUND(COALESCE(CAST(sunshine_duration AS DOUBLE), 0) / 3600.0, 1) AS sunshine_hours,

        -- WMO Weather code
        CAST(weather_code AS INTEGER) AS weather_code,

        -- Temporal fields
        EXTRACT(YEAR FROM CAST(observation_date AS DATE)) AS observation_year,
        EXTRACT(MONTH FROM CAST(observation_date AS DATE)) AS observation_month,
        EXTRACT(DAY FROM CAST(observation_date AS DATE)) AS observation_day,

        -- Simplified weather category based on WMO weather interpretation codes
        -- Ref: https://open-meteo.com/en/docs
        CASE
            WHEN CAST(weather_code AS INTEGER) IN (0, 1) THEN 'Clear'
            WHEN CAST(weather_code AS INTEGER) IN (2, 3) THEN 'Cloudy'
            WHEN CAST(weather_code AS INTEGER) IN (45, 48) THEN 'Fog'
            WHEN CAST(weather_code AS INTEGER) IN (51, 53, 55, 56, 57) THEN 'Drizzle'
            WHEN CAST(weather_code AS INTEGER) IN (61, 63, 65, 66, 67) THEN 'Rain'
            WHEN CAST(weather_code AS INTEGER) IN (80, 81, 82) THEN 'Rain Showers'
            WHEN CAST(weather_code AS INTEGER) IN (95, 96, 99) THEN 'Thunderstorm'
            ELSE 'Unknown'
        END AS weather_category,

        -- Detailed weather description
        CASE CAST(weather_code AS INTEGER)
            WHEN 0 THEN 'Clear Sky'
            WHEN 1 THEN 'Mainly Clear'
            WHEN 2 THEN 'Partly Cloudy'
            WHEN 3 THEN 'Overcast'
            WHEN 45 THEN 'Fog'
            WHEN 48 THEN 'Rime Fog'
            WHEN 51 THEN 'Light Drizzle'
            WHEN 53 THEN 'Moderate Drizzle'
            WHEN 55 THEN 'Dense Drizzle'
            WHEN 61 THEN 'Slight Rain'
            WHEN 63 THEN 'Moderate Rain'
            WHEN 65 THEN 'Heavy Rain'
            WHEN 80 THEN 'Slight Rain Showers'
            WHEN 81 THEN 'Moderate Rain Showers'
            WHEN 82 THEN 'Violent Rain Showers'
            WHEN 95 THEN 'Thunderstorm'
            WHEN 96 THEN 'Thunderstorm with Hail'
            WHEN 99 THEN 'Thunderstorm with Heavy Hail'
            ELSE 'Unknown'
        END AS weather_description,

        -- Rainy day flag (precipitation > 0.1mm threshold)
        CASE
            WHEN COALESCE(CAST(precipitation_sum AS DOUBLE), 0) > 0.1 THEN TRUE
            ELSE FALSE
        END AS is_rainy_day

    FROM source
    WHERE
        observation_date IS NOT NULL
        AND temperature_2m_mean IS NOT NULL
)

SELECT
    -- Generate unique weather observation ID
    CONCAT(city_name, '-', CAST(observation_date AS VARCHAR)) AS weather_id,
    *
FROM cleaned
