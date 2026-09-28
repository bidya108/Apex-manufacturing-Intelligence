SELECT
    dm.machine_id,
    dm.machine_name,
    dm.machine_type,
    COUNT(fm.maintenance_fact_key) AS maintenance_count,
    ROUND(SUM(fm.maintenance_duration), 2) AS total_maintenance_hours,
    ROUND(AVG(fm.maintenance_duration), 2) AS avg_maintenance_hours
FROM warehouse.fact_maintenance fm
JOIN warehouse.dim_machine dm
    ON fm.machine_key = dm.machine_key
GROUP BY
    dm.machine_id,
    dm.machine_name,
    dm.machine_type
ORDER BY
    maintenance_count DESC;
