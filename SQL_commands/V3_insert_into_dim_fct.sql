a--dim_accident_cause
INSERT INTO traffic_accidents.dim_accident_cause(
	collision_id,
	crash_date,
	crash_time,
	part_of_day,
	main_cause,
	contributing_factor_vehicle_2,
	contributing_factor_vehicle_3,
	contributing_factor_vehicle_4,
	contributing_factor_vehicle_5,
	vehicle_type_code_1,
	vehicle_type_code_2,
	vehicle_type_code_3,
	vehicle_type_code_4,
	vehicle_type_code_5
)
SELECT
	stg_all_accidents.collision_id,
	stg_all_accidents.crash_date,
	CAST(stg_all_accidents.crash_time AS TIME),
	stg_all_accidents.part_of_day,
	stg_all_accidents.contributing_factor_vehicle_1 as main_cause,
	stg_all_accidents.contributing_factor_vehicle_2,
	stg_all_accidents.contributing_factor_vehicle_3,
	stg_all_accidents.contributing_factor_vehicle_4,
	stg_all_accidents.contributing_factor_vehicle_5,
	stg_all_accidents.vehicle_type_code_1,
	stg_all_accidents.vehicle_type_code_2,
	stg_all_accidents.vehicle_type_code_3,
	stg_all_accidents.vehicle_type_code_4,
	stg_all_accidents.vehicle_type_code_5
FROM traffic_accidents.stg_all_accidents
ON CONFLICT (collision_id)
DO UPDATE SET
	collision_id = excluded.collision_id,
	crash_date = excluded.crash_date,
	crash_time = excluded.crash_time,
	part_of_day = excluded.part_of_day,
	main_cause = excluded.main_cause,
	contributing_factor_vehicle_2 = excluded.contributing_factor_vehicle_2,
	contributing_factor_vehicle_3 = excluded.contributing_factor_vehicle_3,
	contributing_factor_vehicle_4 = excluded.contributing_factor_vehicle_4,
	contributing_factor_vehicle_5 = excluded.contributing_factor_vehicle_5,
	vehicle_type_code_1 = excluded.vehicle_type_code_1,
	vehicle_type_code_2 = excluded.vehicle_type_code_2,
	vehicle_type_code_3= excluded.vehicle_type_code_3,
	vehicle_type_code_4 = excluded.vehicle_type_code_4,
	vehicle_type_code_5 = excluded.vehicle_type_code_5;

	--dim_location
	INSERT INTO traffic_accidents.dim_location(
	collision_id,
	borough,
	on_street_name,
	off_street_name,
	cross_street_name,
	street,
	zip_code,
	latitude,
	longitude,
	location
)
SELECT
	stg_table.collision_id,
	stg_table.borough,
	stg_table.on_street_name,
	stg_table.off_street_name,
	stg_table.cross_street_name,
	stg_table.street,
	stg_table.zip_code,
	stg_table.latitude,
	stg_table.longitude,
	stg_table.location
FROM traffic_accidents.stg_all_accidents AS stg_table
ON CONFLICT(collision_id)
DO UPDATE SET
	collision_id = excluded.collision_id,
	borough = excluded.borough,
	on_street_name = excluded.on_street_name,
	off_street_name = excluded.off_street_name,
	cross_street_name = excluded.cross_street_name,
	street = excluded.street,
	zip_code = excluded.zip_code,
	latitude = excluded.latitude,
	longitude = excluded.longitude,
	location = excluded.location;

--dim_victims
INSERT INTO traffic_accidents.dim_victims(
	collision_id,
	total_victims,
	total_persons_injured,
	total_persons_killed,
	cyclists_injured,
	cyclists_killed,
	pedestrians_injured,
	pedestrians_killed,
	motorist_injured,
	motorist_killed
)
SELECT
	stg_table.collision_id,
	stg_table.total_victims,
	stg_table.number_of_persons_injured,
	stg_table.number_of_persons_killed,
	stg_table.number_of_cyclist_injured,
	stg_table.number_of_cyclist_killed,
	stg_table.number_of_pedestrians_injured,
	stg_table.number_of_pedestrians_killed,
	stg_table.number_of_motorist_injured,
	stg_table.number_of_motorist_killed
FROM traffic_accidents.stg_all_accidents AS stg_table
ON CONFLICT(collision_id)
DO UPDATE SET
	collision_id = excluded.collision_id,
	total_victims = excluded.total_victims,
	total_persons_injured = excluded.total_persons_injured,
	total_persons_killed = excluded.total_persons_killed,
	cyclists_injured = excluded.cyclists_injured,
	cyclists_killed = excluded.cyclists_killed,
	pedestrians_injured = excluded.pedestrians_injured,
	pedestrians_killed = excluded.pedestrians_killed,
	motorist_injured = excluded.motorist_injured,
	motorist_killed = excluded.motorist_killed;

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