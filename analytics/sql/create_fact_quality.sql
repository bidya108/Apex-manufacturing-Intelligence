CREATE TABLE IF NOT EXISTS warehouse.fact_quality (
    quality_fact_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL,
    production_line_key INTEGER NOT NULL,
    production_record_id INTEGER NOT NULL,
    total_units_inspected INTEGER NOT NULL,
    defective_units INTEGER NOT NULL,
    defect_rate DECIMAL(5,2) NOT NULL,
    quality_status VARCHAR(30) NOT NULL,
    FOREIGN KEY (date_key)
        REFERENCES warehouse.dim_date(date_key),
    FOREIGN KEY (production_line_key)
        REFERENCES warehouse.dim_production_line(production_line_key)
);
