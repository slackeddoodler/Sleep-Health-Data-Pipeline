SELECT
    Occupation,
    ROUND(AVG("Sleep Duration"), 2) AS avg_sleep_duration,
    ROUND(AVG("Quality of Sleep"), 2) AS avg_sleep_quality,
    ROUND(AVG("Stress Level"), 2) AS avg_stress,
    ROUND(AVG("Daily Steps"), 2) AS avg_steps,
    COUNT(*) AS record_count
FROM {{ source('main', 'sleep_health') }}
GROUP BY Occupation
