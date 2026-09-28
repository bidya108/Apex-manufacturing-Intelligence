SELECT
    f.facility_id,
    f.facility_name,
    f.location,
    COUNT(DISTINCT pl.production_line_id) AS production_lines,
    SUM(pr.actual_production) AS total_production,
    ROUND(AVG(pr.production_efficiency), 2) AS average_efficiency,
    ROUND(SUM(pr.downtime_duration), 2) AS total_downtime
FROM facility f
JOIN production_line pl
    ON f.facility_id = pl.facility_id
JOIN production_record pr
    ON pl.production_line_id = pr.production_line_id
GROUP BY
    f.facility_id,
    f.facility_name,
    f.location
ORDER BY average_efficiency DESC;
