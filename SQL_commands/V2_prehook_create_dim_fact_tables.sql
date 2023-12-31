CREATE TABLE IF NOT EXISTS traffic_accidents.dim_accident_cause (
    collision_id SERIAL PRIMARY KEY,
    crash_date DATE,
    crash_time TIME,
    part_of_day TEXT,
    main_cause TEXT,
    contributing_factor_vehicle_2 TEXT,
    contributing_factor_vehicle_3 TEXT,
    contributing_factor_vehicle_4 TEXT,
    contributing_factor_vehicle_5 TEXT,
    vehicle_type_code_1 TEXT,
    vehicle_type_code_2 TEXT,
    vehicle_type_code_3 TEXT,
    vehicle_type_code_4 TEXT,
    vehicle_type_code_5 TEXT
);

CREATE TABLE IF NOT EXISTS traffic_accidents.dim_location (
    collision_id SERIAL PRIMARY KEY,
    borough TEXT,
    on_street_name TEXT,
    off_street_name TEXT,
    cross_street_name TEXT,
    street TEXT,
    zip_code TEXT,
    latitude FLOAT,
    longitude FLOAT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS traffic_accidents.dim_victims (
    collision_id SERIAL PRIMARY KEY,
    total_victims INT,
    total_persons_injured INT,
    total_persons_killed INT,
    cyclists_injured INT,
    cyclists_killed INT,
    pedestrians_injured INT,
    pedestrians_killed INT,
    motorist_injured INT,
    motorist_killed INT
);

CREATE TABLE IF NOT EXISTS traffic_accidents.fact_accidents (
    collision_id SERIAL PRIMARY KEY,
    crash_date DATE,
    part_of_day TEXT,
    borough TEXT,
    street TEXT,
    total_injured INT,
    total_killed INT,
    vehicle_type_code_1 TEXT,
    main_cause TEXT
);

CREATE TABLE IF NOT EXISTS traffic_accidents.dim_person (
    person_id TEXT  PRIMARY KEY,
    collision_id INT,
    person_sex TEXT,
    person_age TEXT,
    person_type TEXT
);

CREATE TABLE IF NOT EXISTS traffic_accidents.fact_injuries (
    injury_id TEXT PRIMARY KEY,
    person_id TEXT REFERENCES traffic_accidents.dim_person(person_id),
    collision_id INT ,
    vehicle_id VARCHAR(70),
    bodily_injury TEXT,
    safety_equipment TEXT,
    ejection TEXT,
    emotional_status TEXT,
    pedestrian_role TEXT
);



CREATE INDEX IF NOT EXISTS idx_collision_id ON traffic_accidents.dim_accident_cause(collision_id);
CREATE INDEX IF NOT EXISTS idx_collision_id_location ON traffic_accidents.dim_location(collision_id);
CREATE INDEX IF NOT EXISTS idx_collision_id_victims ON traffic_accidents.dim_victims(collision_id);
CREATE INDEX IF NOT EXISTS idx_collision_id_fct_accidents ON traffic_accidents.fact_accidents(collision_id);
CREATE INDEX IF NOT EXISTS idx_person_id_injuries ON traffic_accidents.fact_injuries(injury_id);
CREATE INDEX IF NOT EXISTS idx_person_id ON traffic_accidents.dim_person(person_id);