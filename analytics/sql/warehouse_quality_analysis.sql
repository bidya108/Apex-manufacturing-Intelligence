SELECT
    dpl.production_line_name,
    COUNT(fq.quality_fact_key) AS inspection_records,
    SUM(fq.total_units_inspected) AS total_units_inspected,
    SUM(fq.defective_units) AS total_defective_units,
    ROUND(
        (SUM(fq.defective_units)::DECIMAL /
        NULLIF(SUM(fq.total_units_inspected), 0)) * 100,
        2
    ) AS overall_defect_rate
FROM warehouse.fact_quality fq
JOIN warehouse.dim_production_line dpl
    ON fq.production_line_key = dpl.production_line_key
GROUP BY
    dpl.production_line_name
ORDER BY
    overall_defect_rate DESC;
