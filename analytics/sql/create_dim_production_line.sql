CREATE TABLE IF NOT EXISTS warehouse.dim_production_line (
    production_line_key SERIAL PRIMARY KEY,
    production_line_id INTEGER NOT NULL UNIQUE,
    production_line_name VARCHAR(100) NOT NULL,
    production_line_status VARCHAR(30) NOT NULL,
    production_capacity INTEGER NOT NULL,
    facility_key INTEGER NOT NULL,
    FOREIGN KEY (facility_key)
        REFERENCES warehouse.dim_facility(facility_key)
);
