INSERT INTO traffic_accidents.dim_person(
	person_id,
	collision_id,
	person_sex,
	person_age,
	person_type
)
SELECT
	stg_all_injuries.person_id,
	stg_all_injuries.collision_id::INT,
	stg_all_injuries.person_sex,
	stg_all_injuries.person_age,
	stg_all_injuries.person_type
FROM traffic_accidents.stg_all_injuries as stg_all_injuries
ON CONFLICT (person_id)
DO UPDATE SET
	person_id = excluded.person_id,
	collision_id = excluded.collision_id,
	person_sex = excluded.person_sex,
	person_age = excluded.person_age,
	person_type = excluded.person_type;

	--fact injury needs testing
	INSERT INTO traffic_accidents.fact_injuries(
	injury_id,
	person_id,
	collision_id,
	vehicle_id,
	bodily_injury,
	safety_equipment,
	ejection,
	emotional_status,
	pedestrian_role
)
SELECT 
	stg_all_injuries.unique_id,
	stg_all_injuries.person_id,
	stg_all_injuries.collision_id::INT,
	stg_all_injuries.vehicle_id,
	stg_all_injuries.bodily_injury,
	stg_all_injuries.safety_equipment,
	stg_all_injuries.ejection,
	stg_all_injuries.emotional_status,
	stg_all_injuries.ped_role
FROM traffic_accidents.stg_all_injuries as stg_all_injuries
ON CONFLICT(injury_id)
DO UPDATE SET
	injury_id = excluded.injury_id,
	person_id = excluded.person_id,
	collision_id = excluded.collision_id,
	vehicle_id = excluded.vehicle_id,
	bodily_injury = excluded.bodily_injury,
	safety_equipment = excluded.safety_equipment,
	ejection = excluded.ejection,
	emotional_status = excluded.emotional_status,
	pedestrian_role = excluded.pedestrian_role;