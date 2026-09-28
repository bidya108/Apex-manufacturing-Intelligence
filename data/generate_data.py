import pandas as pd
import random
from datetime import date, datetime, timedelta

random.seed(42)

DATA_PATH = "data"


def generate_facilities():
    data = [
        [1, "Apex Bengaluru Plant", "Bengaluru", "Active", "2024-01-15"],
        [2, "Apex Chennai Plant", "Chennai", "Active", "2024-02-10"],
        [3, "Apex Pune Plant", "Pune", "Active", "2024-03-05"],
        [4, "Apex Hyderabad Plant", "Hyderabad", "Active", "2024-04-12"],
        [5, "Apex Ahmedabad Plant", "Ahmedabad", "Active", "2024-05-20"]
    ]

    columns = [
        "facility_id",
        "facility_name",
        "location",
        "facility_status",
        "created_date"
    ]

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(f"{DATA_PATH}/facilities.csv", index=False)


def generate_production_lines():
    data = [
        [1, 1, "Assembly Line A", "Active", 1200, "2024-02-01"],
        [2, 1, "Assembly Line B", "Active", 1000, "2024-02-15"],
        [3, 2, "Assembly Line A", "Active", 1500, "2024-03-01"],
        [4, 2, "Packaging Line A", "Active", 1800, "2024-03-10"],
        [5, 3, "Assembly Line A", "Active", 1300, "2024-04-01"],
        [6, 3, "Quality Line A", "Active", 900, "2024-04-15"],
        [7, 4, "Assembly Line A", "Active", 1400, "2024-05-01"],
        [8, 4, "Packaging Line A", "Active", 1600, "2024-05-10"],
        [9, 5, "Assembly Line A", "Active", 1100, "2024-06-01"],
        [10, 5, "Packaging Line A", "Active", 1400, "2024-06-15"]
    ]

    columns = [
        "production_line_id",
        "facility_id",
        "production_line_name",
        "production_line_status",
        "production_capacity",
        "created_date"
    ]

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(f"{DATA_PATH}/production_lines.csv", index=False)


def generate_machines():
    data = [
        [1, 1, "CNC Machine 01", "CNC", "Siemens", "2024-02-05", "Running", "2026-08-15"],
        [2, 1, "Assembly Robot 01", "Robotic Arm", "ABB", "2024-02-10", "Running", "2026-08-20"],
        [3, 2, "CNC Machine 02", "CNC", "Fanuc", "2024-02-20", "Running", "2026-08-18"],
        [4, 2, "Welding Robot 01", "Robotic Welder", "KUKA", "2024-02-25", "Running", "2026-08-22"],
        [5, 3, "CNC Machine 03", "CNC", "Siemens", "2024-03-05", "Running", "2026-08-10"],
        [6, 3, "Press Machine 01", "Hydraulic Press", "Bosch", "2024-03-12", "Running", "2026-08-25"],
        [7, 4, "Packaging Machine 01", "Packaging", "ABB", "2024-03-15", "Running", "2026-08-12"],
        [8, 4, "Conveyor System 01", "Conveyor", "Siemens", "2024-03-20", "Running", "2026-08-19"],
        [9, 5, "CNC Machine 04", "CNC", "Fanuc", "2024-04-05", "Running", "2026-08-14"],
        [10, 5, "Assembly Robot 02", "Robotic Arm", "KUKA", "2024-04-10", "Running", "2026-08-21"],
        [11, 6, "Inspection Machine 01", "Inspection", "Bosch", "2024-04-20", "Running", "2026-08-16"],
        [12, 6, "Quality Scanner 01", "Scanner", "Siemens", "2024-04-25", "Running", "2026-08-23"],
        [13, 7, "CNC Machine 05", "CNC", "Siemens", "2024-05-05", "Running", "2026-08-11"],
        [14, 7, "Welding Robot 02", "Robotic Welder", "ABB", "2024-05-12", "Running", "2026-08-17"],
        [15, 8, "Packaging Machine 02", "Packaging", "KUKA", "2024-05-15", "Running", "2026-08-24"],
        [16, 8, "Conveyor System 02", "Conveyor", "Siemens", "2024-05-20", "Running", "2026-08-13"],
        [17, 9, "CNC Machine 06", "CNC", "Fanuc", "2024-06-05", "Running", "2026-08-18"],
        [18, 9, "Assembly Robot 03", "Robotic Arm", "ABB", "2024-06-10", "Running", "2026-08-20"],
        [19, 10, "Packaging Machine 03", "Packaging", "Bosch", "2024-06-20", "Running", "2026-08-15"],
        [20, 10, "Conveyor System 03", "Conveyor", "Siemens", "2024-06-25", "Running", "2026-08-22"]
    ]

    columns = [
        "machine_id",
        "production_line_id",
        "machine_name",
        "machine_type",
        "manufacturer",
        "installation_date",
        "operating_status",
        "last_maintenance_date"
    ]

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(f"{DATA_PATH}/machines.csv", index=False)


def generate_production_records():
    records = []
    record_id = 1

    current_date = date(2025, 1, 1)
    end_date = date(2025, 12, 31)

    while current_date <= end_date:
        for line_id in range(1, 11):
            target = random.randint(800, 1800)

            actual = random.randint(
                int(target * 0.75),
                target
            )

            efficiency = round(
                (actual / target) * 100,
                2
            )

            downtime = round(
                random.uniform(0, 8),
                2
            )

            shift = random.choice([
                "Morning",
                "Evening",
                "Night"
            ])

            records.append([
                record_id,
                line_id,
                current_date,
                target,
                actual,
                efficiency,
                downtime,
                shift
            ])

            record_id += 1

        current_date += timedelta(days=1)

    columns = [
        "production_record_id",
        "production_line_id",
        "production_date",
        "production_target",
        "actual_production",
        "production_efficiency",
        "downtime_duration",
        "shift"
    ]

    df = pd.DataFrame(
        records,
        columns=columns
    )

    df.to_csv(
        f"{DATA_PATH}/production_records.csv",
        index=False
    )


def generate_maintenance_records():
    records = []
    record_id = 1

    technicians = [
        "Rahul Sharma",
        "Arjun Patel",
        "Priya Nair",
        "Vikram Singh",
        "Ananya Rao"
    ]

    maintenance_types = [
        "Preventive",
        "Corrective",
        "Inspection"
    ]

    current_date = date(2025, 1, 1)
    end_date = date(2025, 12, 31)

    while current_date <= end_date:
        for machine_id in range(1, 21):

            if random.random() < 0.08:
                records.append([
                    record_id,
                    machine_id,
                    current_date,
                    random.choice(maintenance_types),
                    "Routine machine maintenance and inspection",
                    random.choice(technicians),
                    round(random.uniform(1, 8), 2),
                    "Completed"
                ])

                record_id += 1

        current_date += timedelta(days=1)

    columns = [
        "maintenance_record_id",
        "machine_id",
        "maintenance_date",
        "maintenance_type",
        "maintenance_description",
        "technician",
        "maintenance_duration",
        "maintenance_status"
    ]

    df = pd.DataFrame(
        records,
        columns=columns
    )

    df.to_csv(
        f"{DATA_PATH}/maintenance_records.csv",
        index=False
    )


def generate_sensor_readings():
    maintenance_records = pd.read_csv(
        f"{DATA_PATH}/maintenance_records.csv"
    )

    maintenance_records["maintenance_date"] = pd.to_datetime(
        maintenance_records["maintenance_date"]
    )

    maintenance_dates = {}

    for machine_id in range(1, 21):
        dates = maintenance_records[
            maintenance_records["machine_id"] == machine_id
        ]["maintenance_date"].tolist()

        maintenance_dates[machine_id] = dates

    readings = []
    reading_id = 1

    current_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)

    while current_date <= end_date:

        for machine_id in range(1, 21):

            future_maintenance = []

            for maintenance_date in maintenance_dates[machine_id]:

                days_until = (
                    maintenance_date.date()
                    - current_date.date()
                ).days

                if 1 <= days_until <= 7:
                    future_maintenance.append(days_until)

            if future_maintenance:

                days_until = min(future_maintenance)

                deterioration = (
                    (8 - days_until) / 7
                )

                temperature = (
                    random.uniform(65, 82)
                    + deterioration * random.uniform(8, 14)
                )

                vibration = (
                    random.uniform(2, 5)
                    + deterioration * random.uniform(2, 3)
                )

                pressure = (
                    random.uniform(55, 85)
                    + deterioration * random.uniform(8, 15)
                )

                rotation_speed = (
                    random.uniform(1400, 2800)
                    + deterioration * random.uniform(-350, 350)
                )

                power_consumption = (
                    random.uniform(35, 65)
                    + deterioration * random.uniform(10, 20)
                )

            else:

                temperature = random.uniform(55, 85)
                vibration = random.uniform(1, 6)
                pressure = random.uniform(40, 90)
                rotation_speed = random.uniform(1200, 3000)
                power_consumption = random.uniform(20, 75)

            temperature = round(
                max(temperature, 0),
                2
            )

            vibration = round(
                max(vibration, 0),
                2
            )

            pressure = round(
                max(pressure, 0),
                2
            )

            rotation_speed = round(
                max(rotation_speed, 0),
                2
            )

            power_consumption = round(
                max(power_consumption, 0),
                2
            )

            readings.append([
                reading_id,
                machine_id,
                current_date,
                temperature,
                vibration,
                pressure,
                rotation_speed,
                power_consumption
            ])

            reading_id += 1

        current_date += timedelta(days=1)

    columns = [
        "sensor_reading_id",
        "machine_id",
        "reading_timestamp",
        "temperature",
        "vibration",
        "pressure",
        "rotation_speed",
        "power_consumption"
    ]

    df = pd.DataFrame(
        readings,
        columns=columns
    )

    df.to_csv(
        f"{DATA_PATH}/machine_sensor_readings.csv",
        index=False
    )


def generate_quality_records():
    production_records = pd.read_csv(
        f"{DATA_PATH}/production_records.csv"
    )

    records = []

    for _, row in production_records.iterrows():

        total_inspected = random.randint(
            50,
            200
        )

        defective_units = random.randint(
            0,
            int(total_inspected * 0.08)
        )

        defect_rate = round(
            (defective_units / total_inspected) * 100,
            2
        )

        if defect_rate <= 3:
            quality_status = "Good"
        elif defect_rate <= 5:
            quality_status = "Warning"
        else:
            quality_status = "Poor"

        records.append([
            int(row["production_record_id"]),
            int(row["production_record_id"]),
            row["production_date"],
            total_inspected,
            defective_units,
            defect_rate,
            quality_status
        ])

    columns = [
        "quality_record_id",
        "production_record_id",
        "inspection_date",
        "total_units_inspected",
        "defective_units",
        "defect_rate",
        "quality_status"
    ]

    df = pd.DataFrame(
        records,
        columns=columns
    )

    df.to_csv(
        f"{DATA_PATH}/quality_records.csv",
        index=False
    )


def generate_employee_users():
    data = [
        [1, "Aarav Mehta", "aarav.mehta@apexmanufacturing.com", "Executive", "Active", "2024-01-10"],
        [2, "Priya Nair", "priya.nair@apexmanufacturing.com", "Production Manager", "Active", "2024-01-15"],
        [3, "Rahul Sharma", "rahul.sharma@apexmanufacturing.com", "Maintenance Manager", "Active", "2024-01-20"],
        [4, "Ananya Rao", "ananya.rao@apexmanufacturing.com", "Data Analyst", "Active", "2024-02-01"],
        [5, "Vikram Singh", "vikram.singh@apexmanufacturing.com", "Data Scientist", "Active", "2024-02-05"],
        [6, "Neha Patel", "neha.patel@apexmanufacturing.com", "Data Administrator", "Active", "2024-02-10"],
        [7, "Karan Shah", "karan.shah@apexmanufacturing.com", "System Administrator", "Active", "2024-02-15"]
    ]

    columns = [
        "user_id",
        "name",
        "email",
        "role",
        "account_status",
        "created_date"
    ]

    df = pd.DataFrame(
        data,
        columns=columns
    )

    df.to_csv(
        f"{DATA_PATH}/employee_users.csv",
        index=False
    )


def generate_data_quality_issues():
    data = [
        [
            1,
            "production_records",
            "PR-1023",
            "Missing Value",
            "Production target missing",
            "Medium",
            "2025-03-10 09:15:00",
            "Resolved",
            "2025-03-10 11:30:00"
        ],
        [
            2,
            "machine_sensor_readings",
            "SR-2055",
            "Invalid Value",
            "Temperature outside expected range",
            "High",
            "2025-04-12 14:20:00",
            "Resolved",
            "2025-04-12 16:00:00"
        ],
        [
            3,
            "maintenance_records",
            "MR-0342",
            "Duplicate",
            "Duplicate maintenance record detected",
            "Low",
            "2025-05-18 10:45:00",
            "Resolved",
            "2025-05-18 12:10:00"
        ],
        [
            4,
            "quality_records",
            "QR-1876",
            "Missing Value",
            "Quality status missing",
            "Medium",
            "2025-06-22 08:30:00",
            "Open",
            None
        ]
    ]

    columns = [
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

    df = pd.DataFrame(
        data,
        columns=columns
    )

    df.to_csv(
        f"{DATA_PATH}/data_quality_issues.csv",
        index=False
    )


def generate_ml_predictions():
    records = []

    for prediction_id in range(1, 101):

        machine_id = random.randint(
            1,
            20
        )

        probability = round(
            random.uniform(0.01, 0.95),
            5
        )

        if probability < 0.30:
            risk_level = "Low"
        elif probability < 0.70:
            risk_level = "Medium"
        else:
            risk_level = "High"

        records.append([
            prediction_id,
            machine_id,
            "failure_prediction_v1",
            "2025-12-31 18:00:00",
            probability,
            risk_level,
            "Completed"
        ])

    columns = [
        "prediction_id",
        "machine_id",
        "model_id",
        "prediction_timestamp",
        "failure_probability",
        "risk_level",
        "prediction_status"
    ]

    df = pd.DataFrame(
        records,
        columns=columns
    )

    df.to_csv(
        f"{DATA_PATH}/ml_predictions.csv",
        index=False
    )


def main():
    generate_facilities()
    generate_production_lines()
    generate_machines()
    generate_production_records()
    generate_maintenance_records()
    generate_sensor_readings()
    generate_quality_records()
    generate_employee_users()
    generate_data_quality_issues()
    generate_ml_predictions()

    print("All manufacturing datasets generated successfully.")
    print("Facilities: 5")
    print("Production Lines: 10")
    print("Machines: 20")
    print("Production Records: 3650")
    print("Sensor Readings: 7300")
    print("Maintenance Records: generated")
    print("Quality Records: 3650")
    print("Employee Users: 7")
    print("Data Quality Issues: 4")
    print("ML Predictions: 100")


if __name__ == "__main__":
    main()