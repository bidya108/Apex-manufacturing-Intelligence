SELECT
    pl.production_line_id,
    pl.production_line_name,
    f.facility_name,
    ROUND(AVG(pr.production_efficiency), 2) AS average_efficiency,
    SUM(pr.actual_production) AS total_production,
    SUM(pr.downtime_duration) AS total_downtime
FROM production_record pr
JOIN production_line pl
    ON pr.production_line_id = pl.production_line_id
JOIN facility f
    ON pl.facility_id = f.facility_id
GROUP BY
    pl.production_line_id,
    pl.production_line_name,
    f.facility_name
ORDER BY average_efficiency DESC;
