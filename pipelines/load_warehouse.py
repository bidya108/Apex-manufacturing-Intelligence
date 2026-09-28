import psycopg2


connection = psycopg2.connect(
    dbname="apex_manufacturing",
    user="bidya",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()


def load_warehouse():
    print("Loading data warehouse...")

    cursor.execute("""
        TRUNCATE TABLE
            warehouse.fact_quality,
            warehouse.fact_maintenance,
            warehouse.fact_machine_sensor,
            warehouse.fact_production
        RESTART IDENTITY
        CASCADE
    """)

    cursor.execute("""
        INSERT INTO warehouse.dim_facility (
            facility_id,
            facility_name,
            location,
            facility_status
        )
        SELECT
            facility_id,
            facility_name,
            location,
            facility_status
        FROM facility
        ON CONFLICT (facility_id)
        DO UPDATE SET
            facility_name = EXCLUDED.facility_name,
            location = EXCLUDED.location,
            facility_status = EXCLUDED.facility_status
    """)

    cursor.execute("""
        INSERT INTO warehouse.dim_production_line (
            production_line_id,
            production_line_name,
            production_line_status,
            production_capacity,
            facility_key
        )
        SELECT
            pl.production_line_id,
            pl.production_line_name,
            pl.production_line_status,
            pl.production_capacity,
            df.facility_key
        FROM production_line pl
        JOIN warehouse.dim_facility df
            ON pl.facility_id = df.facility_id
        ON CONFLICT (production_line_id)
        DO UPDATE SET
            production_line_name = EXCLUDED.production_line_name,
            production_line_status = EXCLUDED.production_line_status,
            production_capacity = EXCLUDED.production_capacity,
            facility_key = EXCLUDED.facility_key
    """)

    cursor.execute("""
        INSERT INTO warehouse.dim_machine (
            machine_id,
            machine_name,
            machine_type,
            manufacturer,
            operating_status,
            production_line_key
        )
        SELECT
            m.machine_id,
            m.machine_name,
            m.machine_type,
            m.manufacturer,
            m.operating_status,
            dpl.production_line_key
        FROM machine m
        JOIN warehouse.dim_production_line dpl
            ON m.production_line_id = dpl.production_line_id
        ON CONFLICT (machine_id)
        DO UPDATE SET
            machine_name = EXCLUDED.machine_name,
            machine_type = EXCLUDED.machine_type,
            manufacturer = EXCLUDED.manufacturer,
            operating_status = EXCLUDED.operating_status,
            production_line_key = EXCLUDED.production_line_key
    """)

    cursor.execute("""
        INSERT INTO warehouse.fact_production (
            date_key,
            facility_key,
            production_line_key,
            production_target,
            actual_production,
            production_efficiency,
            downtime_duration,
            shift
        )
        SELECT
            TO_CHAR(pr.production_date, 'YYYYMMDD')::INTEGER,
            df.facility_key,
            dpl.production_line_key,
            pr.production_target,
            pr.actual_production,
            pr.production_efficiency,
            pr.downtime_duration,
            pr.shift
        FROM production_record pr
        JOIN production_line pl
            ON pr.production_line_id = pl.production_line_id
        JOIN warehouse.dim_facility df
            ON pl.facility_id = df.facility_id
        JOIN warehouse.dim_production_line dpl
            ON pl.production_line_id = dpl.production_line_id
    """)

    cursor.execute("""
        INSERT INTO warehouse.fact_machine_sensor (
            date_key,
            machine_key,
            reading_timestamp,
            temperature,
            vibration,
            pressure,
            rotation_speed,
            power_consumption
        )
        SELECT
            TO_CHAR(msr.reading_timestamp, 'YYYYMMDD')::INTEGER,
            dm.machine_key,
            msr.reading_timestamp,
            msr.temperature,
            msr.vibration,
            msr.pressure,
            msr.rotation_speed,
            msr.power_consumption
        FROM machine_sensor_reading msr
        JOIN warehouse.dim_machine dm
            ON msr.machine_id = dm.machine_id
    """)

    cursor.execute("""
        INSERT INTO warehouse.fact_maintenance (
            date_key,
            machine_key,
            maintenance_type,
            maintenance_description,
            technician,
            maintenance_duration,
            maintenance_status
        )
        SELECT
            TO_CHAR(mr.maintenance_date, 'YYYYMMDD')::INTEGER,
            dm.machine_key,
            mr.maintenance_type,
            mr.maintenance_description,
            mr.technician,
            mr.maintenance_duration,
            mr.maintenance_status
        FROM maintenance_record mr
        JOIN warehouse.dim_machine dm
            ON mr.machine_id = dm.machine_id
    """)

    cursor.execute("""
        INSERT INTO warehouse.fact_quality (
            date_key,
            production_line_key,
            production_record_id,
            total_units_inspected,
            defective_units,
            defect_rate,
            quality_status
        )
        SELECT
            TO_CHAR(qr.inspection_date, 'YYYYMMDD')::INTEGER,
            dpl.production_line_key,
            qr.production_record_id,
            qr.total_units_inspected,
            qr.defective_units,
            qr.defect_rate,
            qr.quality_status
        FROM quality_record qr
        JOIN production_record pr
            ON qr.production_record_id = pr.production_record_id
        JOIN warehouse.dim_production_line dpl
            ON pr.production_line_id = dpl.production_line_id
    """)

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM warehouse.dim_facility")
    facility_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM warehouse.dim_production_line")
    line_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM warehouse.dim_machine")
    machine_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM warehouse.fact_production")
    production_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM warehouse.fact_machine_sensor")
    sensor_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM warehouse.fact_maintenance")
    maintenance_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM warehouse.fact_quality")
    quality_count = cursor.fetchone()[0]

    print(f"dim_facility: {facility_count} records")
    print(f"dim_production_line: {line_count} records")
    print(f"dim_machine: {machine_count} records")
    print(f"fact_production: {production_count} records")
    print(f"fact_machine_sensor: {sensor_count} records")
    print(f"fact_maintenance: {maintenance_count} records")
    print(f"fact_quality: {quality_count} records")

    cursor.close()
    connection.close()

    print("Warehouse loading completed successfully.")


if __name__ == "__main__":
    load_warehouse()