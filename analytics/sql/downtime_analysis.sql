SELECT
    f.facility_name,
    pl.production_line_name,
    ROUND(SUM(pr.downtime_duration), 2) AS total_downtime_hours,
    ROUND(AVG(pr.downtime_duration), 2) AS average_downtime_hours,
    COUNT(pr.production_record_id) AS production_records
FROM production_record pr
JOIN production_line pl
    ON pr.production_line_id = pl.production_line_id
JOIN facility f
    ON pl.facility_id = f.facility_id
GROUP BY
    f.facility_name,
    pl.production_line_name
ORDER BY total_downtime_hours DESC;
