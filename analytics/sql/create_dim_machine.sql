CREATE TABLE IF NOT EXISTS warehouse.dim_machine (
    machine_key SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL UNIQUE,
    machine_name VARCHAR(100) NOT NULL,
    machine_type VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100),
    operating_status VARCHAR(30) NOT NULL,
    production_line_key INTEGER NOT NULL,
    FOREIGN KEY (production_line_key)
        REFERENCES warehouse.dim_production_line(production_line_key)
);
