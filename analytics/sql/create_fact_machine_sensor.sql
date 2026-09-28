CREATE TABLE IF NOT EXISTS warehouse.fact_machine_sensor (
    sensor_fact_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL,
    machine_key INTEGER NOT NULL,
    reading_timestamp TIMESTAMP NOT NULL,
    temperature DECIMAL(8,2) NOT NULL,
    vibration DECIMAL(8,2) NOT NULL,
    pressure DECIMAL(8,2) NOT NULL,
    rotation_speed DECIMAL(10,2) NOT NULL,
    power_consumption DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (date_key)
        REFERENCES warehouse.dim_date(date_key),
    FOREIGN KEY (machine_key)
        REFERENCES warehouse.dim_machine(machine_key)
);
