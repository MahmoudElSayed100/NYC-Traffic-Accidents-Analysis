--not done needs edits/fixing
INSERT INTO traffic_accidents.dim_accident_cause(
	collision_id,
	crash_date,
	crash_time,
	part_of_day,
	main_cause,
	contributing_factor_vehicle2,
	contributing_factor_vehicle3,
	contributing_factor_vehicle4,
	contributing_factor_vehicle5,
	vehicle_code_type_1,
	vehicle_code_type_2,
	vehicle_code_type_3,
	vehicle_code_type_4,
	vehicle_code_type_5
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
	contributing_factor_vehicle2 = excluded.contributing_factor_vehicle2,
	contributing_factor_vehicle3 = excluded.contributing_factor_vehicle3,
	contributing_factor_vehicle4 = excluded.contributing_factor_vehicle4,
	contributing_factor_vehicle5 = excluded.contributing_factor_vehicle5,
	vehicle_code_type_1 = excluded.vehicle_code_type_1,
	vehicle_code_type_2 = excluded.vehicle_code_type_2,
	vehicle_code_type_3= excluded.vehicle_code_type_3,
	vehicle_code_type_4 = excluded.vehicle_code_type_4,
	vehicle_code_type_5 = excluded.vehicle_code_type_5;
	
select * from traffic_accidents.dim_accident_cause