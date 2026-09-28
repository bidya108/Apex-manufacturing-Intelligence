SELECT
    df.facility_name,
    dpl.production_line_name,
    dd.year,
    SUM(fp.actual_production) AS total_production,
    ROUND(AVG(fp.production_efficiency), 2) AS average_efficiency,
    ROUND(SUM(fp.downtime_duration), 2) AS total_downtime_hours
FROM warehouse.fact_production fp
JOIN warehouse.dim_date dd
    ON fp.date_key = dd.date_key
JOIN warehouse.dim_facility df
    ON fp.facility_key = df.facility_key
JOIN warehouse.dim_production_line dpl
    ON fp.production_line_key = dpl.production_line_key
GROUP BY
    df.facility_name,
    dpl.production_line_name,
    dd.year
ORDER BY
    df.facility_name,
    dpl.production_line_name;
