import os
import psycopg2
import pandas as pd


OUTPUT_PATH = "machine-learning/machine_failure_features.csv"


connection = psycopg2.connect(
    dbname="apex_manufacturing",
    user="bidya",
    host="localhost",
    port="5432"
)


query = """
WITH daily_sensor AS (
    SELECT
        fms.machine_key,
        dm.machine_id,
        dm.machine_name,
        dm.machine_type,
        dm.operating_status,
        fms.date_key,
        dd.full_date,

        AVG(fms.temperature) AS avg_temperature,
        MAX(fms.temperature) AS max_temperature,

        AVG(fms.vibration) AS avg_vibration,
        MAX(fms.vibration) AS max_vibration,

        AVG(fms.pressure) AS avg_pressure,
        AVG(fms.rotation_speed) AS avg_rotation_speed,
        AVG(fms.power_consumption) AS avg_power_consumption

    FROM warehouse.fact_machine_sensor fms

    JOIN warehouse.dim_machine dm
        ON fms.machine_key = dm.machine_key

    JOIN warehouse.dim_date dd
        ON fms.date_key = dd.date_key

    GROUP BY
        fms.machine_key,
        dm.machine_id,
        dm.machine_name,
        dm.machine_type,
        dm.operating_status,
        fms.date_key,
        dd.full_date
),

maintenance_history AS (
    SELECT
        fm.machine_key,
        fm.date_key,
        COUNT(*) AS maintenance_count
    FROM warehouse.fact_maintenance fm
    GROUP BY
        fm.machine_key,
        fm.date_key
),

features AS (
    SELECT
        ds.machine_key,
        ds.machine_id,
        ds.machine_name,
        ds.machine_type,
        ds.operating_status,
        ds.full_date,

        ds.avg_temperature,
        ds.max_temperature,
        ds.avg_vibration,
        ds.max_vibration,
        ds.avg_pressure,
        ds.avg_rotation_speed,
        ds.avg_power_consumption,

        COALESCE(mh.maintenance_count, 0)
            AS maintenance_count,

        CASE
            WHEN EXISTS (
                SELECT 1
                FROM warehouse.fact_maintenance fm_future
                JOIN warehouse.dim_date dd_future
                    ON fm_future.date_key = dd_future.date_key
                WHERE fm_future.machine_key = ds.machine_key
                  AND dd_future.full_date > ds.full_date
                  AND dd_future.full_date <= ds.full_date + INTERVAL '7 days'
            )
            THEN 1
            ELSE 0
        END AS maintenance_within_7_days

    FROM daily_sensor ds

    LEFT JOIN maintenance_history mh
        ON ds.machine_key = mh.machine_key
       AND ds.date_key = mh.date_key
)

SELECT *
FROM features
ORDER BY machine_id, full_date
"""


print("Creating machine failure feature dataset...")
print("----------------------------------------")


data = pd.read_sql(query, connection)

connection.close()


os.makedirs("machine-learning", exist_ok=True)

data.to_csv(
    OUTPUT_PATH,
    index=False
)


print(f"Feature dataset created successfully.")
print(f"Rows: {len(data)}")
print(f"Columns: {len(data.columns)}")
print(f"Output: {OUTPUT_PATH}")

print("\nTarget distribution")
print("----------------------------------------")

print(
    data["maintenance_within_7_days"]
    .value_counts()
    .sort_index()
)


print("\nFeature preview")
print("----------------------------------------")

print(data.head())