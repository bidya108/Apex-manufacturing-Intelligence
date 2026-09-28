CREATE TABLE IF NOT EXISTS warehouse.fact_production (
    production_fact_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL,
    facility_key INTEGER NOT NULL,
    production_line_key INTEGER NOT NULL,
    production_target INTEGER NOT NULL,
    actual_production INTEGER NOT NULL,
    production_efficiency DECIMAL(5,2) NOT NULL,
    downtime_duration DECIMAL(10,2) NOT NULL,
    shift VARCHAR(30) NOT NULL,
    FOREIGN KEY (date_key)
        REFERENCES warehouse.dim_date(date_key),
    FOREIGN KEY (facility_key)
        REFERENCES warehouse.dim_facility(facility_key),
    FOREIGN KEY (production_line_key)
        REFERENCES warehouse.dim_production_line(production_line_key)
);
