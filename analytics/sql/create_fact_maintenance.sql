CREATE TABLE IF NOT EXISTS warehouse.fact_maintenance (
    maintenance_fact_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL,
    machine_key INTEGER NOT NULL,
    maintenance_type VARCHAR(50) NOT NULL,
    maintenance_description TEXT,
    technician VARCHAR(100) NOT NULL,
    maintenance_duration DECIMAL(10,2) NOT NULL,
    maintenance_status VARCHAR(30) NOT NULL,
    FOREIGN KEY (date_key)
        REFERENCES warehouse.dim_date(date_key),
    FOREIGN KEY (machine_key)
        REFERENCES warehouse.dim_machine(machine_key)
);
