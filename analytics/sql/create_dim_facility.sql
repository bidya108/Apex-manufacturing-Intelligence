CREATE TABLE IF NOT EXISTS warehouse.dim_facility (
    facility_key SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL UNIQUE,
    facility_name VARCHAR(100) NOT NULL,
    location VARCHAR(150) NOT NULL,
    facility_status VARCHAR(30) NOT NULL
);
