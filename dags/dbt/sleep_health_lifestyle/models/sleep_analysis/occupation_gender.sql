SELECT
    Occupation,
    Gender,
    COUNT(Gender) as "Gender Count"
FROM {{ source('main', 'sleep_health') }}
GROUP BY
    Occupation, Gender
ORDER BY
    Occupation, Gender
