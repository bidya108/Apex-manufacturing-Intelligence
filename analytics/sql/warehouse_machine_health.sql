SELECT
    dm.machine_id,
    dm.machine_name,
    dm.machine_type,
    dpl.production_line_name,
    ROUND(AVG(fms.temperature), 2) AS avg_temperature,
    ROUND(MAX(fms.temperature), 2) AS max_temperature,
    ROUND(AVG(fms.vibration), 2) AS avg_vibration,
    ROUND(MAX(fms.vibration), 2) AS max_vibration,
    ROUND(AVG(fms.pressure), 2) AS avg_pressure,
    ROUND(AVG(fms.power_consumption), 2) AS avg_power_consumption
FROM warehouse.fact_machine_sensor fms
JOIN warehouse.dim_machine dm
    ON fms.machine_key = dm.machine_key
JOIN warehouse.dim_production_line dpl
    ON dm.production_line_key = dpl.production_line_key
GROUP BY
    dm.machine_id,
    dm.machine_name,
    dm.machine_type,
    dpl.production_line_name
ORDER BY avg_temperature DESC;
