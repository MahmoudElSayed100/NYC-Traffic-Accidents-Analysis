CREATE TABLE IF NOT EXISTS traffic_accidents.agg_yearly_accidents AS
WITH AccidentAggregates AS (
    SELECT
        EXTRACT(YEAR FROM crash_date) AS year,
        COUNT(collision_id) AS total_crashes,
        LAG(COUNT(collision_id)) OVER (ORDER BY EXTRACT(YEAR FROM crash_date)) AS last_year_crashes,
        SUM(COUNT(collision_id)) OVER (ORDER BY EXTRACT(YEAR FROM crash_date)) AS running_total
    FROM
        traffic_accidents.fact_accidents
    GROUP BY
        year
)
SELECT
    a.year,
    a.total_crashes,
    a.last_year_crashes,
    a.running_total,
    CASE
        WHEN LAG(a.total_crashes) OVER (ORDER BY a.year) IS NOT NULL THEN
            ((a.total_crashes - LAG(a.total_crashes) OVER (ORDER BY a.year)) / LAG(a.total_crashes) OVER (ORDER BY a.year)) * 100
        ELSE
            NULL
    END AS percent_difference
FROM
    AccidentAggregates AS a;
