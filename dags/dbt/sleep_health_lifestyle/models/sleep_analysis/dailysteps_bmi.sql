SELECT
    "BMI Category" AS bmi_category,
    ROUND(AVG("Daily Steps"), 2) AS avg_daily_steps,
    COUNT(*) AS record_count
FROM {{ source('main', 'sleep_health') }}
GROUP BY
    bmi_category
ORDER BY avg_daily_steps DESC
