CREATE OR REPLACE VIEW PersonVictimsView AS
WITH PersonVictimsCTE AS (
    SELECT
		p.person_id,
        p.person_sex,
        p.person_age,
        p.collision_id,
        v.total_persons_killed,
        v.total_persons_injured
    FROM
        traffic_accidents1.dim_person AS p
    INNER JOIN
        traffic_accidents1.dim_victims AS v ON p.collision_id = v.collision_id
)
SELECT *
FROM PersonVictimsCTE;