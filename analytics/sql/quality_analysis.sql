SELECT
    f.facility_name,
    pl.production_line_name,
    COUNT(qr.quality_record_id) AS inspections,
    SUM(qr.total_units_inspected) AS units_inspected,
    SUM(qr.defective_units) AS defective_units,
    ROUND(
        (SUM(qr.defective_units)::DECIMAL /
        NULLIF(SUM(qr.total_units_inspected), 0)) * 100,
        2
    ) AS overall_defect_rate
FROM quality_record qr
JOIN production_record pr
    ON qr.production_record_id = pr.production_record_id
JOIN production_line pl
    ON pr.production_line_id = pl.production_line_id
JOIN facility f
    ON pl.facility_id = f.facility_id
GROUP BY
    f.facility_name,
    pl.production_line_name
ORDER BY overall_defect_rate DESC;
