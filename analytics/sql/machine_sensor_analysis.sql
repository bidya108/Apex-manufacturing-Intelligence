SELECT
    m.machine_id,
    m.machine_name,
    m.machine_type,
    ROUND(AVG(sr.temperature), 2) AS avg_temperature,
    ROUND(MAX(sr.temperature), 2) AS max_temperature,
    ROUND(AVG(sr.vibration), 2) AS avg_vibration,
    ROUND(MAX(sr.vibration), 2) AS max_vibration,
    ROUND(AVG(sr.pressure), 2) AS avg_pressure,
    ROUND(AVG(sr.power_consumption), 2) AS avg_power_consumption
FROM machine m
JOIN machine_sensor_reading sr
    ON m.machine_id = sr.machine_id
GROUP BY
    m.machine_id,
    m.machine_name,
    m.machine_type
ORDER BY avg_temperature DESC;
