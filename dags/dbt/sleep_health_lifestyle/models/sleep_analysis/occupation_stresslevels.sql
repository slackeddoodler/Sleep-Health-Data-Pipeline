SELECT
    Occupation,
    ROUND(AVG("Stress Level"), 2) AS avg_stress_level
FROM {{ source('main', 'sleep_health') }}
GROUP BY Occupation
ORDER BY avg_stress_level DESC