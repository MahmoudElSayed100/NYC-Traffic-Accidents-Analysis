	--fact_accidents
	INSERT INTO traffic_accidents.fact_accidents(
	collision_id,
	crash_date,
	part_of_day,
	borough,
	street,
	total_injured,
	total_killed,
	vehicle_type_code_1,
	main_cause
)
SELECT
	stg_table.collision_id,
	stg_table.crash_date,
	stg_table.part_of_day,
	stg_table.borough,
	stg_table.street,
	stg_table.number_of_persons_injured,
	stg_table.number_of_persons_killed,
	stg_table.vehicle_type_code_1,
	stg_table.contributing_factor_vehicle_1
FROM traffic_accidents.stg_all_accidents AS stg_table
ON CONFLICT(collision_id)
DO UPDATE SET
	collision_id = excluded.collision_id,
	crash_date = excluded.crash_date,
	part_of_day = excluded.part_of_day,
	borough = excluded.borough,
	street = excluded.street,
	total_injured = excluded.total_injured,
	total_killed = excluded.total_killed,
	vehicle_type_code_1 = excluded.vehicle_type_code_1,
	main_cause = excluded.main_cause;

--dim person 
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

	--fact injury 
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