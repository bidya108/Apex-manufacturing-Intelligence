import psycopg2


connection = psycopg2.connect(
    dbname="apex_manufacturing",
    user="bidya",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

issues = []


def check_count(table_name, expected_count):
    cursor.execute(f"SELECT COUNT(*) FROM warehouse.{table_name}")
    actual_count = cursor.fetchone()[0]

    print(
        f"{table_name}: {actual_count} records "
        f"(expected {expected_count})"
    )

    if actual_count != expected_count:
        issues.append(
            f"{table_name}: expected {expected_count}, found {actual_count}"
        )


def check_nulls(table_name, column_name):
    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM warehouse.{table_name}
        WHERE {column_name} IS NULL
        """
    )

    null_count = cursor.fetchone()[0]

    if null_count > 0:
        issues.append(
            f"{table_name}.{column_name}: {null_count} NULL values"
        )


def check_orphans(query, description):
    cursor.execute(query)
    orphan_count = cursor.fetchone()[0]

    if orphan_count > 0:
        issues.append(
            f"{description}: {orphan_count} orphan records"
        )


print("APEX MANUFACTURING WAREHOUSE VALIDATION")
print("----------------------------------------")

print("\nROW COUNT VALIDATION")
print("----------------------------------------")

check_count("dim_date", 365)
check_count("dim_facility", 5)
check_count("dim_production_line", 10)
check_count("dim_machine", 20)
check_count("fact_production", 3650)
check_count("fact_machine_sensor", 7300)
check_count("fact_maintenance", 602)
check_count("fact_quality", 3650)


print("\nNULL VALUE VALIDATION")
print("----------------------------------------")

check_nulls("dim_facility", "facility_id")
check_nulls("dim_production_line", "production_line_id")
check_nulls("dim_machine", "machine_id")

check_nulls("fact_production", "date_key")
check_nulls("fact_production", "facility_key")
check_nulls("fact_production", "production_line_key")

check_nulls("fact_machine_sensor", "date_key")
check_nulls("fact_machine_sensor", "machine_key")

check_nulls("fact_maintenance", "date_key")
check_nulls("fact_maintenance", "machine_key")

check_nulls("fact_quality", "date_key")
check_nulls("fact_quality", "production_line_key")


print("\nREFERENTIAL INTEGRITY VALIDATION")
print("----------------------------------------")

check_orphans(
    """
    SELECT COUNT(*)
    FROM warehouse.fact_production fp
    LEFT JOIN warehouse.dim_date dd
        ON fp.date_key = dd.date_key
    WHERE dd.date_key IS NULL
    """,
    "fact_production → dim_date"
)

check_orphans(
    """
    SELECT COUNT(*)
    FROM warehouse.fact_production fp
    LEFT JOIN warehouse.dim_facility df
        ON fp.facility_key = df.facility_key
    WHERE df.facility_key IS NULL
    """,
    "fact_production → dim_facility"
)

check_orphans(
    """
    SELECT COUNT(*)
    FROM warehouse.fact_production fp
    LEFT JOIN warehouse.dim_production_line dpl
        ON fp.production_line_key = dpl.production_line_key
    WHERE dpl.production_line_key IS NULL
    """,
    "fact_production → dim_production_line"
)

check_orphans(
    """
    SELECT COUNT(*)
    FROM warehouse.fact_machine_sensor fms
    LEFT JOIN warehouse.dim_machine dm
        ON fms.machine_key = dm.machine_key
    WHERE dm.machine_key IS NULL
    """,
    "fact_machine_sensor → dim_machine"
)

check_orphans(
    """
    SELECT COUNT(*)
    FROM warehouse.fact_maintenance fm
    LEFT JOIN warehouse.dim_machine dm
        ON fm.machine_key = dm.machine_key
    WHERE dm.machine_key IS NULL
    """,
    "fact_maintenance → dim_machine"
)

check_orphans(
    """
    SELECT COUNT(*)
    FROM warehouse.fact_quality fq
    LEFT JOIN warehouse.dim_production_line dpl
        ON fq.production_line_key = dpl.production_line_key
    WHERE dpl.production_line_key IS NULL
    """,
    "fact_quality → dim_production_line"
)

check_orphans(
    """
    SELECT COUNT(*)
    FROM warehouse.fact_production fp
    LEFT JOIN warehouse.dim_date dd
        ON fp.date_key = dd.date_key
    WHERE dd.date_key IS NULL
    """,
    "fact_production → dim_date"
)


print("\nDUPLICATE KEY VALIDATION")
print("----------------------------------------")

duplicate_checks = [
    (
        "dim_facility",
        "facility_id"
    ),
    (
        "dim_production_line",
        "production_line_id"
    ),
    (
        "dim_machine",
        "machine_id"
    )
]

for table_name, column_name in duplicate_checks:
    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM (
            SELECT {column_name}
            FROM warehouse.{table_name}
            GROUP BY {column_name}
            HAVING COUNT(*) > 1
        ) duplicates
        """
    )

    duplicate_count = cursor.fetchone()[0]

    if duplicate_count > 0:
        issues.append(
            f"{table_name}.{column_name}: "
            f"{duplicate_count} duplicate keys"
        )


print("\nBUSINESS DATA VALIDATION")
print("----------------------------------------")

cursor.execute("""
    SELECT COUNT(*)
    FROM warehouse.fact_production
    WHERE production_target < 0
       OR actual_production < 0
       OR downtime_duration < 0
       OR production_efficiency < 0
       OR production_efficiency > 100
""")

production_issues = cursor.fetchone()[0]

if production_issues > 0:
    issues.append(
        f"fact_production: {production_issues} invalid production records"
    )


cursor.execute("""
    SELECT COUNT(*)
    FROM warehouse.fact_machine_sensor
    WHERE temperature < 0
       OR vibration < 0
       OR pressure < 0
       OR rotation_speed < 0
       OR power_consumption < 0
""")

sensor_issues = cursor.fetchone()[0]

if sensor_issues > 0:
    issues.append(
        f"fact_machine_sensor: {sensor_issues} invalid sensor records"
    )


cursor.execute("""
    SELECT COUNT(*)
    FROM warehouse.fact_quality
    WHERE total_units_inspected < 0
       OR defective_units < 0
       OR defective_units > total_units_inspected
       OR defect_rate < 0
       OR defect_rate > 100
""")

quality_issues = cursor.fetchone()[0]

if quality_issues > 0:
    issues.append(
        f"fact_quality: {quality_issues} invalid quality records"
    )


print("\nVALIDATION RESULT")
print("----------------------------------------")

if issues:
    print("Warehouse validation FAILED.")
    print("\nIssues found:")

    for issue in issues:
        print(f"- {issue}")

else:
    print("All warehouse validation checks passed successfully.")


cursor.close()
connection.close()