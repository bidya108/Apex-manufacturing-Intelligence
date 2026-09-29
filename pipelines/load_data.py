import psycopg2
import pandas as pd

connection = psycopg2.connect(
    dbname="apex_manufacturing",
    user="bidya",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

tables = [
    "ml_prediction",
    "data_quality_issue",
    "quality_record",
    "maintenance_record",
    "machine_sensor_reading",
    "production_record",
    "machine",
    "production_line",
    "facility"
]

cursor.execute(
    "TRUNCATE TABLE " + ", ".join(tables)
)

connection.commit()


def load_table(csv_file, table_name, columns):
    df = pd.read_csv(csv_file)

    for _, row in df.iterrows():
        values = tuple(
            None if pd.isna(value) else value
            for value in row
        )

        placeholders = ", ".join(["%s"] * len(columns))
        column_names = ", ".join(columns)

        cursor.execute(
            f"""
            INSERT INTO {table_name} ({column_names})
            VALUES ({placeholders})
            """,
            values
        )

    print(f"{table_name}: {len(df)} records loaded")


load_table(
    "data/facilities.csv",
    "facility",
    [
        "facility_id",
        "facility_name",
        "location",
        "facility_status",
        "created_date"
    ]
)

load_table(
    "data/production_lines.csv",
    "production_line",
    [
        "production_line_id",
        "facility_id",
        "production_line_name",
        "production_line_status",
        "production_capacity",
        "created_date"
    ]
)

load_table(
    "data/machines.csv",
    "machine",
    [
        "machine_id",
        "production_line_id",
        "machine_name",
        "machine_type",
        "manufacturer",
        "installation_date",
        "operating_status",
        "last_maintenance_date"
    ]
)

load_table(
    "data/production_records.csv",
    "production_record",
    [
        "production_record_id",
        "production_line_id",
        "production_date",
        "production_target",
        "actual_production",
        "production_efficiency",
        "downtime_duration",
        "shift"
    ]
)

load_table(
    "data/machine_sensor_readings.csv",
    "machine_sensor_reading",
    [
        "sensor_reading_id",
        "machine_id",
        "reading_timestamp",
        "temperature",
        "vibration",
        "pressure",
        "rotation_speed",
        "power_consumption"
    ]
)

load_table(
    "data/maintenance_records.csv",
    "maintenance_record",
    [
        "maintenance_record_id",
        "machine_id",
        "maintenance_date",
        "maintenance_type",
        "maintenance_description",
        "technician",
        "maintenance_duration",
        "maintenance_status"
    ]
)

load_table(
    "data/quality_records.csv",
    "quality_record",
    [
        "quality_record_id",
        "production_record_id",
        "inspection_date",
        "total_units_inspected",
        "defective_units",
        "defect_rate",
        "quality_status"
    ]
)

load_table(
    "data/data_quality_issues.csv",
    "data_quality_issue",
    [
        "issue_id",
        "dataset",
        "record_identifier",
        "issue_type",
        "issue_description",
        "severity",
        "detected_date",
        "resolution_status",
        "resolved_date"
    ]
)

connection.commit()

cursor.close()
connection.close()

print("All manufacturing datasets loaded successfully.")