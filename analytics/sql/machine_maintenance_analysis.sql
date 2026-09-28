SELECT
    m.machine_id,
    m.machine_name,
    m.machine_type,
    m.manufacturer,
    COUNT(mr.maintenance_record_id) AS maintenance_events,
    ROUND(SUM(mr.maintenance_duration), 2) AS total_maintenance_hours,
    MAX(mr.maintenance_date) AS last_recorded_maintenance
FROM machine m
LEFT JOIN maintenance_record mr
    ON m.machine_id = mr.machine_id
GROUP BY
    m.machine_id,
    m.machine_name,
    m.machine_type,
    m.manufacturer
ORDER BY total_maintenance_hours DESC;

