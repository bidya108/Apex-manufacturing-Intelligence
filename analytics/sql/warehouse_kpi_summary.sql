SELECT
    (SELECT COUNT(*) FROM warehouse.dim_facility) AS total_facilities,
    (SELECT COUNT(*) FROM warehouse.dim_production_line) AS total_production_lines,
    (SELECT COUNT(*) FROM warehouse.dim_machine) AS total_machines,
    (SELECT COUNT(*) FROM warehouse.fact_production) AS production_records,
    (SELECT ROUND(SUM(actual_production), 2)
     FROM warehouse.fact_production) AS total_production,
    (SELECT ROUND(AVG(production_efficiency), 2)
     FROM warehouse.fact_production) AS average_production_efficiency,
    (SELECT ROUND(SUM(downtime_duration), 2)
     FROM warehouse.fact_production) AS total_downtime_hours,
    (SELECT SUM(total_units_inspected)
     FROM warehouse.fact_quality) AS total_units_inspected,
    (SELECT SUM(defective_units)
     FROM warehouse.fact_quality) AS total_defective_units,
    (SELECT ROUND(
        SUM(defective_units)::DECIMAL /
        NULLIF(SUM(total_units_inspected), 0) * 100,
        2
    )
     FROM warehouse.fact_quality) AS overall_defect_rate;
