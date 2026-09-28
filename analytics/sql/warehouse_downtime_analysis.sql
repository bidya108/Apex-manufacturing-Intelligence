SELECT
    df.facility_name,
    dpl.production_line_name,
    COUNT(fp.production_fact_key) AS production_records,
    ROUND(SUM(fp.downtime_duration), 2) AS total_downtime_hours,
    ROUND(AVG(fp.downtime_duration), 2) AS avg_downtime_hours,
    ROUND(AVG(fp.production_efficiency), 2) AS average_efficiency
FROM warehouse.fact_production fp
JOIN warehouse.dim_facility df
    ON fp.facility_key = df.facility_key
JOIN warehouse.dim_production_line dpl
    ON fp.production_line_key = dpl.production_line_key
GROUP BY
    df.facility_name,
    dpl.production_line_name
ORDER BY
    total_downtime_hours DESC;
