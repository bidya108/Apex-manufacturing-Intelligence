SELECT
    COUNT(DISTINCT f.facility_id) AS total_facilities,
    COUNT(DISTINCT pl.production_line_id) AS total_production_lines,
    COUNT(DISTINCT m.machine_id) AS total_machines,
    SUM(pr.actual_production) AS total_production,
    ROUND(AVG(pr.production_efficiency), 2) AS average_production_efficiency,
    ROUND(SUM(pr.downtime_duration), 2) AS total_downtime_hours,
    SUM(qr.total_units_inspected) AS total_units_inspected,
    SUM(qr.defective_units) AS total_defective_units,
    ROUND(
        (SUM(qr.defective_units)::DECIMAL /
        NULLIF(SUM(qr.total_units_inspected), 0)) * 100,
        2
    ) AS overall_defect_rate
FROM facility f
JOIN production_line pl
    ON f.facility_id = pl.facility_id
JOIN machine m
    ON pl.production_line_id = m.production_line_id
JOIN production_record pr
    ON pl.production_line_id = pr.production_line_id
JOIN quality_record qr
    ON pr.production_record_id = qr.production_record_id;
