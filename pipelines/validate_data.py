import psycopg2


connection = psycopg2.connect(
    dbname="apex_manufacturing",
    user="bidya",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

errors = []


def check_negative_values():
    checks = [
        ("Production target", "SELECT COUNT(*) FROM production_record WHERE production_target < 0"),
        ("Actual production", "SELECT COUNT(*) FROM production_record WHERE actual_production < 0"),
        ("Downtime", "SELECT COUNT(*) FROM production_record WHERE downtime_duration < 0"),
        ("Defective units", "SELECT COUNT(*) FROM quality_record WHERE defective_units < 0"),
        ("Maintenance duration", "SELECT COUNT(*) FROM maintenance_record WHERE maintenance_duration < 0")
    ]

    for name, query in checks:
        cursor.execute(query)
        count = cursor.fetchone()[0]

        if count > 0:
            errors.append(f"{name}: {count} invalid records")


def check_quality_values():
    cursor.execute("""
        SELECT COUNT(*)
        FROM quality_record
        WHERE defective_units > total_units_inspected
    """)

    count = cursor.fetchone()[0]

    if count > 0:
        errors.append(
            f"Quality records: {count} records have defective units greater than inspected units"
        )


def check_failure_probability():
    cursor.execute("""
        SELECT COUNT(*)
        FROM ml_prediction
        WHERE failure_probability < 0
           OR failure_probability > 1
    """)

    count = cursor.fetchone()[0]

    if count > 0:
        errors.append(
            f"ML predictions: {count} invalid failure probabilities"
        )


def check_duplicate_ids():
    checks = [
        (
            "Facility",
            """
            SELECT COUNT(*)
            FROM (
                SELECT facility_id
                FROM facility
                GROUP BY facility_id
                HAVING COUNT(*) > 1
            ) duplicates
            """
        ),
        (
            "Machine",
            """
            SELECT COUNT(*)
            FROM (
                SELECT machine_id
                FROM machine
                GROUP BY machine_id
                HAVING COUNT(*) > 1
            ) duplicates
            """
        ),
        (
            "Production Record",
            """
            SELECT COUNT(*)
            FROM (
                SELECT production_record_id
                FROM production_record
                GROUP BY production_record_id
                HAVING COUNT(*) > 1
            ) duplicates
            """
        )
    ]

    for name, query in checks:
        cursor.execute(query)
        count = cursor.fetchone()[0]

        if count > 0:
            errors.append(
                f"{name}: {count} duplicate IDs"
            )


def check_missing_required_values():
    checks = [
        (
            "Facility",
            """
            SELECT COUNT(*)
            FROM facility
            WHERE facility_name IS NULL
               OR location IS NULL
               OR facility_status IS NULL
            """
        ),
        (
            "Machine",
            """
            SELECT COUNT(*)
            FROM machine
            WHERE machine_name IS NULL
               OR machine_type IS NULL
               OR operating_status IS NULL
            """
        ),
        (
            "Production Record",
            """
            SELECT COUNT(*)
            FROM production_record
            WHERE production_date IS NULL
               OR production_target IS NULL
               OR actual_production IS NULL
            """
        )
    ]

    for name, query in checks:
        cursor.execute(query)
        count = cursor.fetchone()[0]

        if count > 0:
            errors.append(
                f"{name}: {count} records with missing required values"
            )

def check_foreign_keys():
    checks = [
        (
            "Production Lines",
            """
            SELECT COUNT(*)
            FROM production_line pl
            LEFT JOIN facility f
                ON pl.facility_id = f.facility_id
            WHERE f.facility_id IS NULL
            """
        ),
        (
            "Machines",
            """
            SELECT COUNT(*)
            FROM machine m
            LEFT JOIN production_line pl
                ON m.production_line_id = pl.production_line_id
            WHERE pl.production_line_id IS NULL
            """
        ),
        (
            "Production Records",
            """
            SELECT COUNT(*)
            FROM production_record pr
            LEFT JOIN production_line pl
                ON pr.production_line_id = pl.production_line_id
            WHERE pl.production_line_id IS NULL
            """
        ),
        (
            "Sensor Readings",
            """
            SELECT COUNT(*)
            FROM machine_sensor_reading sr
            LEFT JOIN machine m
                ON sr.machine_id = m.machine_id
            WHERE m.machine_id IS NULL
            """
        ),
        (
            "Maintenance Records",
            """
            SELECT COUNT(*)
            FROM maintenance_record mr
            LEFT JOIN machine m
                ON mr.machine_id = m.machine_id
            WHERE m.machine_id IS NULL
            """
        ),
        (
            "Quality Records",
            """
            SELECT COUNT(*)
            FROM quality_record qr
            LEFT JOIN production_record pr
                ON qr.production_record_id = pr.production_record_id
            WHERE pr.production_record_id IS NULL
            """
        ),
        (
            "ML Predictions",
            """
            SELECT COUNT(*)
            FROM ml_prediction mp
            LEFT JOIN machine m
                ON mp.machine_id = m.machine_id
            WHERE m.machine_id IS NULL
            """
        )
    ]

    for name, query in checks:
        cursor.execute(query)
        count = cursor.fetchone()[0]

        if count > 0:
            errors.append(
                f"{name}: {count} records with invalid foreign keys"
            )

def check_data_counts():
    checks = [
        ("Facility", "SELECT COUNT(*) FROM facility"),
        ("Production Line", "SELECT COUNT(*) FROM production_line"),
        ("Machine", "SELECT COUNT(*) FROM machine"),
        ("Production Record", "SELECT COUNT(*) FROM production_record"),
        ("Sensor Reading", "SELECT COUNT(*) FROM machine_sensor_reading"),
        ("Maintenance Record", "SELECT COUNT(*) FROM maintenance_record"),
        ("Quality Record", "SELECT COUNT(*) FROM quality_record")
    ]

    print("\nDATASET COUNTS")
    print("-" * 40)

    for name, query in checks:
        cursor.execute(query)
        count = cursor.fetchone()[0]
        print(f"{name}: {count}")


check_negative_values()
check_quality_values()
check_failure_probability()
check_duplicate_ids()
check_missing_required_values()
check_foreign_keys()
check_data_counts()


print("\nDATA QUALITY VALIDATION")
print("-" * 40)

if errors:
    validation_status = "FAILED"

    print("Validation completed with issues:")

    for error in errors:
        print(f"- {error}")

else:
    validation_status = "PASSED"

    print("All validation checks passed successfully.")


cursor.execute(
    """
    INSERT INTO data_validation_run (
        validation_status,
        issue_count
    )
    VALUES (%s, %s)
    """,
    (validation_status, len(errors))
)

connection.commit()


cursor.close()
connection.close()