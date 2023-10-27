CREATE TABLE IF NOT EXISTS traffic_accidents.agg_yearly_accidents AS
WITH AccidentAggregates AS (
    SELECT
        EXTRACT(YEAR FROM crash_date) AS year,
        COUNT(collision_id) AS total_crashes
    FROM
        traffic_accidents.fact_accidents
    GROUP BY
        year
)
SELECT
    a.year,
    a.total_crashes,
    LAG(a.total_crashes) OVER (ORDER BY a.year) AS last_year_crashes,
    CASE
        WHEN LAG(a.total_crashes) OVER (ORDER BY a.year) IS NOT NULL THEN
            ROUND(((a.total_crashes - LAG(a.total_crashes) OVER (ORDER BY a.year)) * 100.0 / LAG(a.total_crashes) OVER (ORDER BY a.year)), 1)
        ELSE
            NULL
    END AS percent_difference
FROM
    AccidentAggregates AS a;

--AGG YEARLY INJURED - KILLED
CREATE TABLE traffic_accidents.agg_yearly_killed_injured AS
SELECT
    EXTRACT(YEAR FROM crash_date) AS year,
    SUM(total_killed) AS total_killed,
    SUM(total_injured) AS total_injured
FROM
    traffic_accidents.fact_accidents
GROUP BY
    year
ORDER BY
    year

