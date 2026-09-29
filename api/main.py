from api.auth import router as auth_router

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

import psycopg2
import pandas as pd
import joblib

from api.security import security, verify_token


app = FastAPI(
    title="Apex Manufacturing Intelligence API",
    description="REST API for Apex Manufacturing analytics and predictive operations",
    version="1.0.0"
)

app.include_router(auth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_PATH = "machine-learning/machine_failure_model.joblib"


def get_database_connection():
    return psycopg2.connect(
        dbname="apex_manufacturing",
        user="bidya",
        host="localhost",
        port="5432"
    )


def load_model():
    return joblib.load(MODEL_PATH)


def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return verify_token(credentials)


def require_role(allowed_roles):

    def role_checker(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        payload = verify_token(credentials)

        user_role = payload.get("role")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )

        return payload

    return role_checker


class PredictionRequest(BaseModel):
    machine_id: int


def calculate_machine_risk(
    model,
    machine_type,
    operating_status,
    temperature,
    vibration,
    pressure,
    rotation_speed,
    power_consumption,
    maintenance_count
):
    data = pd.DataFrame([{
        "machine_id": 0,
        "machine_key": 0,
        "machine_type": machine_type,
        "operating_status": operating_status,
        "avg_temperature": temperature,
        "max_temperature": temperature,
        "avg_vibration": vibration,
        "max_vibration": vibration,
        "avg_pressure": pressure,
        "avg_rotation_speed": rotation_speed,
        "avg_power_consumption": power_consumption,
        "maintenance_count": maintenance_count
    }])

    probability = model.predict_proba(data)[:, 1][0]

    if probability >= 0.70:
        risk_level = "High"
        recommendation = "Schedule maintenance inspection"
    elif probability >= 0.40:
        risk_level = "Medium"
        recommendation = "Monitor machine condition"
    else:
        risk_level = "Low"
        recommendation = "Continue normal monitoring"

    return probability, risk_level, recommendation


def get_machine_health_data():
    connection = get_database_connection()

    query = """
        SELECT
            m.machine_id,
            m.machine_name,
            m.machine_type,
            m.operating_status,
            s.reading_timestamp,
            s.temperature,
            s.vibration,
            s.pressure,
            s.rotation_speed,
            s.power_consumption,
            COALESCE(mc.maintenance_count, 0) AS maintenance_count
        FROM machine m

        LEFT JOIN LATERAL (
            SELECT
                reading_timestamp,
                temperature,
                vibration,
                pressure,
                rotation_speed,
                power_consumption
            FROM machine_sensor_reading
            WHERE machine_id = m.machine_id
            ORDER BY reading_timestamp DESC
            LIMIT 1
        ) s ON TRUE

        LEFT JOIN (
            SELECT
                machine_id,
                COUNT(*) AS maintenance_count
            FROM maintenance_record
            GROUP BY machine_id
        ) mc
        ON mc.machine_id = m.machine_id

        ORDER BY m.machine_id;
    """

    data = pd.read_sql(query, connection)
    connection.close()

    return data


@app.get("/")
def root():
    return {
        "message": "Apex Manufacturing Intelligence API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# EXECUTIVE / GENERAL ANALYTICS
# ============================================================

@app.get(
    "/kpis",
    dependencies=[
        Depends(
            require_role([
                "Executive",
                "Production Manager",
                "Data Analyst",
                "Data Scientist",
                "System Administrator"
            ])
        )
    ]
)
def get_kpis():

    connection = get_database_connection()

    query = """
        SELECT
            SUM(production_target) AS total_target,
            SUM(actual_production) AS total_production,
            AVG(production_efficiency) AS average_efficiency,
            SUM(downtime_duration) AS total_downtime
        FROM production_record;
    """

    production = pd.read_sql(query, connection)

    quality_query = """
        SELECT
            SUM(total_units_inspected) AS total_inspected,
            SUM(defective_units) AS total_defective
        FROM quality_record;
    """

    quality = pd.read_sql(quality_query, connection)

    connection.close()

    total_inspected = float(quality.iloc[0]["total_inspected"])
    total_defective = float(quality.iloc[0]["total_defective"])

    defect_rate = (
        total_defective / total_inspected * 100
        if total_inspected > 0
        else 0
    )

    return {
        "production_efficiency": round(
            float(production.iloc[0]["average_efficiency"]), 2
        ),
        "total_production": round(
            float(production.iloc[0]["total_production"]), 2
        ),
        "downtime_hours": round(
            float(production.iloc[0]["total_downtime"]), 2
        ),
        "defect_rate": round(defect_rate, 2)
    }


@app.get(
    "/production-performance",
    dependencies=[
        Depends(
            require_role([
                "Executive",
                "Production Manager",
                "Data Analyst",
                "Data Scientist",
                "System Administrator"
            ])
        )
    ]
)
def get_production_performance():

    connection = get_database_connection()

    query = """
        SELECT
            TO_CHAR(production_date, 'Mon') AS month,
            EXTRACT(MONTH FROM production_date) AS month_number,
            SUM(production_target) AS target,
            SUM(actual_production) AS actual
        FROM production_record
        GROUP BY
            TO_CHAR(production_date, 'Mon'),
            EXTRACT(MONTH FROM production_date)
        ORDER BY month_number;
    """

    data = pd.read_sql(query, connection)
    connection.close()

    return data[
        ["month", "target", "actual"]
    ].to_dict(orient="records")


@app.get(
    "/facility-performance",
    dependencies=[
        Depends(
            require_role([
                "Executive",
                "Production Manager",
                "Data Analyst",
                "Data Scientist",
                "System Administrator"
            ])
        )
    ]
)
def get_facility_performance():

    connection = get_database_connection()

    query = """
        SELECT
            f.facility_name AS facility,
            SUM(pr.actual_production) AS actual_production,
            SUM(pr.production_target) AS production_target,
            AVG(pr.production_efficiency) AS average_efficiency,
            SUM(pr.downtime_duration) AS downtime_hours
        FROM production_record pr

        JOIN production_line pl
            ON pr.production_line_id = pl.production_line_id

        JOIN facility f
            ON pl.facility_id = f.facility_id

        GROUP BY f.facility_id, f.facility_name
        ORDER BY f.facility_id;
    """

    data = pd.read_sql(query, connection)
    connection.close()

    return data.to_dict(orient="records")


@app.get(
    "/machine-risk-distribution",
    dependencies=[
        Depends(
            require_role([
                "Executive",
                "Maintenance Manager",
                "Data Scientist",
                "Data Analyst",
                "System Administrator"
            ])
        )
    ]
)
def get_machine_risk_distribution():

    connection = get_database_connection()

    query = """
        SELECT
            risk_level,
            COUNT(*) AS count
        FROM ml_prediction
        GROUP BY risk_level
        ORDER BY
            CASE risk_level
                WHEN 'Low' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'High' THEN 3
            END;
    """

    data = pd.read_sql(query, connection)
    connection.close()

    return data.to_dict(orient="records")


# ============================================================
# MACHINE HEALTH / MAINTENANCE
# ============================================================

@app.get(
    "/machine-health",
    dependencies=[
        Depends(
            require_role([
                "Maintenance Manager",
                "Data Scientist",
                "Data Analyst",
                "System Administrator"
            ])
        )
    ]
)
def get_machine_health():

    data = get_machine_health_data()
    model = load_model()

    results = []

    for _, row in data.iterrows():

        probability, risk_level, recommendation = calculate_machine_risk(
            model=model,
            machine_type=row["machine_type"],
            operating_status=row["operating_status"],
            temperature=row["temperature"],
            vibration=row["vibration"],
            pressure=row["pressure"],
            rotation_speed=row["rotation_speed"],
            power_consumption=row["power_consumption"],
            maintenance_count=row["maintenance_count"]
        )

        results.append({
            "machine_id": int(row["machine_id"]),
            "machine_name": row["machine_name"],
            "machine_type": row["machine_type"],
            "operating_status": row["operating_status"],
            "last_reading": row["reading_timestamp"],
            "temperature": round(float(row["temperature"]), 2),
            "vibration": round(float(row["vibration"]), 2),
            "pressure": round(float(row["pressure"]), 2),
            "rotation_speed": round(float(row["rotation_speed"]), 2),
            "power_consumption": round(float(row["power_consumption"]), 2),
            "maintenance_count": int(row["maintenance_count"]),
            "failure_probability": round(float(probability), 3),
            "risk_level": risk_level,
            "recommendation": recommendation
        })

    return results


@app.get(
    "/maintenance-alerts",
    dependencies=[
        Depends(
            require_role([
                "Maintenance Manager",
                "Data Scientist",
                "System Administrator"
            ])
        )
    ]
)
def get_maintenance_alerts():

    data = get_machine_health_data()
    model = load_model()

    connection = get_database_connection()

    line_query = """
        SELECT
            m.machine_id,
            pl.production_line_name
        FROM machine m
        JOIN production_line pl
            ON m.production_line_id = pl.production_line_id;
    """

    line_data = pd.read_sql(line_query, connection)
    connection.close()

    data = data.merge(
        line_data,
        on="machine_id",
        how="left"
    )

    alerts = []

    for _, row in data.iterrows():

        probability, risk_level, recommendation = calculate_machine_risk(
            model=model,
            machine_type=row["machine_type"],
            operating_status=row["operating_status"],
            temperature=row["temperature"],
            vibration=row["vibration"],
            pressure=row["pressure"],
            rotation_speed=row["rotation_speed"],
            power_consumption=row["power_consumption"],
            maintenance_count=row["maintenance_count"]
        )

        if risk_level in ["High", "Medium"]:
            alerts.append({
                "machine_id": int(row["machine_id"]),
                "machine_name": row["machine_name"],
                "machine_type": row["machine_type"],
                "production_line": row["production_line_name"],
                "operating_status": row["operating_status"],
                "temperature": round(float(row["temperature"]), 2),
                "vibration": round(float(row["vibration"]), 2),
                "failure_probability": round(float(probability), 3),
                "risk_level": risk_level,
                "recommendation": recommendation,
                "last_reading": row["reading_timestamp"]
            })

    alerts.sort(
        key=lambda x: x["failure_probability"],
        reverse=True
    )

    return alerts


@app.post(
    "/predict",
    dependencies=[
        Depends(
            require_role([
                "Maintenance Manager",
                "Data Scientist",
                "System Administrator"
            ])
        )
    ]
)
def predict_machine(request: PredictionRequest):

    connection = get_database_connection()

    query = """
        SELECT
            m.machine_id,
            m.machine_type,
            m.operating_status,
            s.temperature,
            s.vibration,
            s.pressure,
            s.rotation_speed,
            s.power_consumption,
            COALESCE(mc.maintenance_count, 0) AS maintenance_count
        FROM machine m

        LEFT JOIN LATERAL (
            SELECT
                temperature,
                vibration,
                pressure,
                rotation_speed,
                power_consumption
            FROM machine_sensor_reading
            WHERE machine_id = m.machine_id
            ORDER BY reading_timestamp DESC
            LIMIT 1
        ) s ON TRUE

        LEFT JOIN (
            SELECT
                machine_id,
                COUNT(*) AS maintenance_count
            FROM maintenance_record
            GROUP BY machine_id
        ) mc
        ON mc.machine_id = m.machine_id

        WHERE m.machine_id = %s;
    """

    data = pd.read_sql(
        query,
        connection,
        params=(request.machine_id,)
    )

    connection.close()

    if data.empty:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    row = data.iloc[0]
    model = load_model()

    probability, risk_level, recommendation = calculate_machine_risk(
        model=model,
        machine_type=row["machine_type"],
        operating_status=row["operating_status"],
        temperature=row["temperature"],
        vibration=row["vibration"],
        pressure=row["pressure"],
        rotation_speed=row["rotation_speed"],
        power_consumption=row["power_consumption"],
        maintenance_count=row["maintenance_count"]
    )

    return {
        "machine_id": request.machine_id,
        "failure_probability": round(float(probability), 3),
        "risk_level": risk_level,
        "recommendation": recommendation
    }


# ============================================================
# ANALYTICS ENDPOINTS
# ============================================================

@app.get(
    "/analytics/production",
    dependencies=[
        Depends(
            require_role([
                "Executive",
                "Data Analyst",
                "Data Scientist",
                "Production Manager",
                "System Administrator"
            ])
        )
    ]
)
def analytics_production():

    connection = get_database_connection()

    summary_query = """
        SELECT
            SUM(production_target) AS total_target,
            SUM(actual_production) AS total_actual
        FROM production_record;
    """

    summary = pd.read_sql(
        summary_query,
        connection
    ).iloc[0]

    facility_query = """
        SELECT
            f.facility_name AS facility,
            SUM(pr.production_target) AS target,
            SUM(pr.actual_production) AS actual
        FROM production_record pr
        JOIN production_line pl
            ON pr.production_line_id = pl.production_line_id
        JOIN facility f
            ON pl.facility_id = f.facility_id
        GROUP BY f.facility_id, f.facility_name
        ORDER BY f.facility_id;
    """

    facility_data = pd.read_sql(
        facility_query,
        connection
    )

    monthly_query = """
        SELECT
            TO_CHAR(production_date, 'Mon') AS month,
            EXTRACT(MONTH FROM production_date) AS month_number,
            SUM(production_target) AS target,
            SUM(actual_production) AS actual
        FROM production_record
        GROUP BY
            TO_CHAR(production_date, 'Mon'),
            EXTRACT(MONTH FROM production_date)
        ORDER BY month_number;
    """

    monthly_data = pd.read_sql(
        monthly_query,
        connection
    )

    connection.close()

    total_target = float(summary["total_target"])
    total_actual = float(summary["total_actual"])
    total_gap = total_target - total_actual

    gap_percentage = (
        total_gap / total_target * 100
        if total_target > 0
        else 0
    )

    facility_results = []

    for _, row in facility_data.iterrows():

        target = float(row["target"])
        actual = float(row["actual"])
        gap = target - actual

        facility_results.append({
            "facility": row["facility"],
            "target": round(target, 2),
            "actual": round(actual, 2),
            "gap": round(gap, 2),
            "gap_percentage": round(
                gap / target * 100 if target else 0,
                2
            )
        })

    monthly_results = []

    for _, row in monthly_data.iterrows():

        target = float(row["target"])
        actual = float(row["actual"])
        gap = target - actual

        monthly_results.append({
            "month": row["month"],
            "target": round(target, 2),
            "actual": round(actual, 2),
            "gap": round(gap, 2),
            "gap_percentage": round(
                gap / target * 100 if target else 0,
                2
            )
        })

    largest_facility_gap = max(
        facility_results,
        key=lambda x: x["gap"]
    )

    largest_month_gap = max(
        monthly_results,
        key=lambda x: x["gap"]
    )

    return {
        "summary": {
            "total_target": round(total_target, 2),
            "total_actual": round(total_actual, 2),
            "production_gap": round(total_gap, 2),
            "gap_percentage": round(gap_percentage, 2)
        },
        "facility": facility_results,
        "monthly": monthly_results,
        "insights": {
            "largest_facility_gap": largest_facility_gap["facility"],
            "largest_facility_gap_value": largest_facility_gap["gap"],
            "largest_month_gap": largest_month_gap["month"],
            "largest_month_gap_value": largest_month_gap["gap"]
        }
    }


@app.get(
    "/analytics/downtime",
    dependencies=[
        Depends(
            require_role([
                "Executive",
                "Data Analyst",
                "Data Scientist",
                "Production Manager",
                "System Administrator"
            ])
        )
    ]
)
def analytics_downtime():

    connection = get_database_connection()

    facility_query = """
        SELECT
            f.facility_name AS facility,
            SUM(pr.downtime_duration) AS downtime_hours
        FROM production_record pr
        JOIN production_line pl
            ON pr.production_line_id = pl.production_line_id
        JOIN facility f
            ON pl.facility_id = f.facility_id
        GROUP BY f.facility_id, f.facility_name
        ORDER BY downtime_hours DESC;
    """

    facility_data = pd.read_sql(
        facility_query,
        connection
    )

    line_query = """
        SELECT
            pl.production_line_name AS production_line,
            f.facility_name AS facility,
            SUM(pr.downtime_duration) AS downtime_hours
        FROM production_record pr
        JOIN production_line pl
            ON pr.production_line_id = pl.production_line_id
        JOIN facility f
            ON pl.facility_id = f.facility_id
        GROUP BY
            pl.production_line_id,
            pl.production_line_name,
            f.facility_name
        ORDER BY downtime_hours DESC;
    """

    line_data = pd.read_sql(
        line_query,
        connection
    )

    connection.close()

    total_downtime = float(
        facility_data["downtime_hours"].sum()
    )

    facility_results = []

    for _, row in facility_data.iterrows():

        downtime = float(row["downtime_hours"])

        facility_results.append({
            "facility": row["facility"],
            "downtime_hours": round(downtime, 2),
            "contribution_percentage": round(
                downtime / total_downtime * 100
                if total_downtime
                else 0,
                2
            )
        })

    line_results = []

    for _, row in line_data.iterrows():

        line_results.append({
            "production_line": row["production_line"],
            "facility": row["facility"],
            "downtime_hours": round(
                float(row["downtime_hours"]),
                2
            )
        })

    highest_facility = facility_results[0]
    highest_line = line_results[0]

    return {
        "summary": {
            "total_downtime_hours": round(
                total_downtime,
                2
            )
        },
        "facility": facility_results,
        "production_line": line_results,
        "insights": {
            "highest_downtime_facility":
                highest_facility["facility"],
            "highest_downtime_facility_hours":
                highest_facility["downtime_hours"],
            "highest_downtime_line":
                highest_line["production_line"],
            "highest_downtime_line_hours":
                highest_line["downtime_hours"]
        }
    }


@app.get(
    "/analytics/quality",
    dependencies=[
        Depends(
            require_role([
                "Executive",
                "Data Analyst",
                "Data Scientist",
                "Production Manager",
                "System Administrator"
            ])
        )
    ]
)
def analytics_quality():

    connection = get_database_connection()

    facility_query = """
        SELECT
            f.facility_name AS facility,
            SUM(q.total_units_inspected) AS inspected,
            SUM(q.defective_units) AS defective
        FROM quality_record q
        JOIN production_record pr
            ON q.production_record_id = pr.production_record_id
        JOIN production_line pl
            ON pr.production_line_id = pl.production_line_id
        JOIN facility f
            ON pl.facility_id = f.facility_id
        GROUP BY f.facility_id, f.facility_name
        ORDER BY f.facility_id;
    """

    facility_data = pd.read_sql(
        facility_query,
        connection
    )

    line_query = """
        SELECT
            pl.production_line_name AS production_line,
            f.facility_name AS facility,
            SUM(q.total_units_inspected) AS inspected,
            SUM(q.defective_units) AS defective
        FROM quality_record q
        JOIN production_record pr
            ON q.production_record_id = pr.production_record_id
        JOIN production_line pl
            ON pr.production_line_id = pl.production_line_id
        JOIN facility f
            ON pl.facility_id = f.facility_id
        GROUP BY
            pl.production_line_id,
            pl.production_line_name,
            f.facility_name
        ORDER BY defective DESC;
    """

    line_data = pd.read_sql(
        line_query,
        connection
    )

    monthly_query = """
        SELECT
            TO_CHAR(q.inspection_date, 'Mon') AS month,
            EXTRACT(MONTH FROM q.inspection_date) AS month_number,
            SUM(q.total_units_inspected) AS inspected,
            SUM(q.defective_units) AS defective
        FROM quality_record q
        GROUP BY
            TO_CHAR(q.inspection_date, 'Mon'),
            EXTRACT(MONTH FROM q.inspection_date)
        ORDER BY month_number;
    """

    monthly_data = pd.read_sql(
        monthly_query,
        connection
    )

    connection.close()

    facility_results = []

    for _, row in facility_data.iterrows():

        inspected = float(row["inspected"])
        defective = float(row["defective"])

        facility_results.append({
            "facility": row["facility"],
            "inspected": round(inspected, 2),
            "defective": round(defective, 2),
            "defect_rate": round(
                defective / inspected * 100
                if inspected
                else 0,
                2
            )
        })

    line_results = []

    for _, row in line_data.iterrows():

        inspected = float(row["inspected"])
        defective = float(row["defective"])

        line_results.append({
            "production_line": row["production_line"],
            "facility": row["facility"],
            "inspected": round(inspected, 2),
            "defective": round(defective, 2),
            "defect_rate": round(
                defective / inspected * 100
                if inspected
                else 0,
                2
            )
        })

    monthly_results = []

    for _, row in monthly_data.iterrows():

        inspected = float(row["inspected"])
        defective = float(row["defective"])

        monthly_results.append({
            "month": row["month"],
            "defect_rate": round(
                defective / inspected * 100
                if inspected
                else 0,
                2
            ),
            "defective": round(defective, 2)
        })

    highest_facility = max(
        facility_results,
        key=lambda x: x["defect_rate"]
    )

    highest_line = max(
        line_results,
        key=lambda x: x["defect_rate"]
    )

    return {
        "facility": facility_results,
        "production_line": line_results,
        "monthly": monthly_results,
        "insights": {
            "highest_defect_facility":
                highest_facility["facility"],
            "highest_defect_rate":
                highest_facility["defect_rate"],
            "highest_defect_line":
                highest_line["production_line"],
            "highest_defect_line_rate":
                highest_line["defect_rate"]
        }
    }


@app.get(
    "/analytics/machines",
    dependencies=[
        Depends(
            require_role([
                "Executive",
                "Data Analyst",
                "Data Scientist",
                "Maintenance Manager",
                "System Administrator"
            ])
        )
    ]
)
def analytics_machines():

    connection = get_database_connection()

    sensor_query = """
        SELECT
            m.machine_type,
            AVG(s.temperature) AS avg_temperature,
            AVG(s.vibration) AS avg_vibration,
            AVG(s.power_consumption) AS avg_power_consumption
        FROM machine_sensor_reading s
        JOIN machine m
            ON s.machine_id = m.machine_id
        GROUP BY m.machine_type
        ORDER BY m.machine_type;
    """

    sensor_data = pd.read_sql(
        sensor_query,
        connection
    )

    maintenance_query = """
        SELECT
            m.machine_name,
            m.machine_type,
            COUNT(mr.maintenance_record_id) AS maintenance_count,
            COALESCE(
                AVG(mr.maintenance_duration),
                0
            ) AS average_maintenance_duration
        FROM machine m
        LEFT JOIN maintenance_record mr
            ON m.machine_id = mr.machine_id
        GROUP BY
            m.machine_id,
            m.machine_name,
            m.machine_type
        ORDER BY maintenance_count DESC;
    """

    maintenance_data = pd.read_sql(
        maintenance_query,
        connection
    )

    maintenance_type_query = """
        SELECT
            maintenance_type,
            COUNT(*) AS count
        FROM maintenance_record
        GROUP BY maintenance_type
        ORDER BY count DESC;
    """

    maintenance_type_data = pd.read_sql(
        maintenance_type_query,
        connection
    )

    risk_query = """
        SELECT
            m.machine_type,
            AVG(mp.failure_probability) AS average_failure_probability,
            COUNT(*) FILTER (
                WHERE mp.risk_level = 'High'
            ) AS high_risk_count,
            COUNT(*) AS prediction_count
        FROM ml_prediction mp
        JOIN machine m
            ON mp.machine_id = m.machine_id
        GROUP BY m.machine_type
        ORDER BY average_failure_probability DESC;
    """

    risk_data = pd.read_sql(
        risk_query,
        connection
    )

    connection.close()

    sensor_results = []

    for _, row in sensor_data.iterrows():

        sensor_results.append({
            "machine_type": row["machine_type"],
            "avg_temperature": round(
                float(row["avg_temperature"]),
                2
            ),
            "avg_vibration": round(
                float(row["avg_vibration"]),
                2
            ),
            "avg_power_consumption": round(
                float(row["avg_power_consumption"]),
                2
            )
        })

    maintenance_results = []

    for _, row in maintenance_data.iterrows():

        maintenance_results.append({
            "machine_name": row["machine_name"],
            "machine_type": row["machine_type"],
            "maintenance_count": int(
                row["maintenance_count"]
            ),
            "average_maintenance_duration": round(
                float(row["average_maintenance_duration"]),
                2
            )
        })

    maintenance_type_results = []

    for _, row in maintenance_type_data.iterrows():

        maintenance_type_results.append({
            "maintenance_type": row["maintenance_type"],
            "count": int(row["count"])
        })

    risk_results = []

    for _, row in risk_data.iterrows():

        risk_results.append({
            "machine_type": row["machine_type"],
            "average_failure_probability": round(
                float(row["average_failure_probability"]),
                3
            ),
            "high_risk_count": int(
                row["high_risk_count"]
            ),
            "prediction_count": int(
                row["prediction_count"]
            )
        })

    highest_maintenance_machine = maintenance_results[0]
    highest_risk_type = risk_results[0]

    return {
        "sensor_summary": sensor_results,
        "maintenance_by_machine": maintenance_results,
        "maintenance_types": maintenance_type_results,
        "risk_by_machine_type": risk_results,
        "insights": {
            "highest_maintenance_machine":
                highest_maintenance_machine["machine_name"],
            "highest_maintenance_count":
                highest_maintenance_machine["maintenance_count"],
            "highest_risk_machine_type":
                highest_risk_type["machine_type"],
            "highest_risk_average_probability":
                highest_risk_type["average_failure_probability"]
        }
    }


# ============================================================
# DATA QUALITY
# ============================================================

@app.get(
    "/data-quality/summary",
    dependencies=[
        Depends(
            require_role([
                "Data Analyst",
                "Data Administrator",
                "Data Scientist",
                "System Administrator"
            ])
        )
    ]
)
def data_quality_summary():

    connection = get_database_connection()

    issue_query = """
        SELECT
            COUNT(*) AS total_issues,
            COUNT(*) FILTER (
                WHERE resolution_status != 'Resolved'
            ) AS open_issues,
            COUNT(*) FILTER (
                WHERE resolution_status = 'Resolved'
            ) AS resolved_issues,
            COUNT(*) FILTER (
                WHERE severity = 'Critical'
            ) AS critical_issues,
            COUNT(*) FILTER (
                WHERE severity = 'High'
            ) AS high_issues,
            COUNT(*) FILTER (
                WHERE severity = 'Medium'
            ) AS medium_issues,
            COUNT(*) FILTER (
                WHERE severity = 'Low'
            ) AS low_issues
        FROM data_quality_issue;
    """

    issue_data = pd.read_sql(
        issue_query,
        connection
    ).iloc[0]

    validation_query = """
        SELECT
            run_id,
            run_timestamp,
            validation_status,
            issue_count
        FROM data_validation_run
        ORDER BY run_timestamp DESC
        LIMIT 1;
    """

    validation_data = pd.read_sql(
        validation_query,
        connection
    )

    connection.close()

    latest_validation = None

    if not validation_data.empty:
        row = validation_data.iloc[0]

        latest_validation = {
            "run_id": int(row["run_id"]),
            "run_timestamp": row["run_timestamp"],
            "validation_status": row["validation_status"],
            "issue_count": int(row["issue_count"])
        }

    return {
        "total_issues": int(issue_data["total_issues"]),
        "open_issues": int(issue_data["open_issues"]),
        "resolved_issues": int(issue_data["resolved_issues"]),
        "severity": {
            "critical": int(issue_data["critical_issues"]),
            "high": int(issue_data["high_issues"]),
            "medium": int(issue_data["medium_issues"]),
            "low": int(issue_data["low_issues"])
        },
        "latest_validation": latest_validation
    }


@app.get(
    "/data-quality/issues",
    dependencies=[
        Depends(
            require_role([
                "Data Analyst",
                "Data Administrator",
                "Data Scientist",
                "System Administrator"
            ])
        )
    ]
)
def data_quality_issues():

    connection = get_database_connection()

    query = """
        SELECT
            issue_id,
            dataset,
            record_identifier,
            issue_type,
            issue_description,
            severity,
            detected_date,
            resolution_status,
            resolved_date
        FROM data_quality_issue
        ORDER BY detected_date DESC, issue_id DESC;
    """

    data = pd.read_sql(
        query,
        connection
    )

    connection.close()

    results = []

    for _, row in data.iterrows():

        results.append({
            "issue_id": int(row["issue_id"]),
            "dataset": row["dataset"],
            "record_identifier": row["record_identifier"],
            "issue_type": row["issue_type"],
            "issue_description": row["issue_description"],
            "severity": row["severity"],
            "detected_date": row["detected_date"],
            "resolution_status": row["resolution_status"],
            "resolved_date": row["resolved_date"]
        })

    return results


@app.get(
    "/data-quality/validation-runs",
    dependencies=[
        Depends(
            require_role([
                "Data Analyst",
                "Data Administrator",
                "Data Scientist",
                "System Administrator"
            ])
        )
    ]
)
def data_quality_validation_runs():

    connection = get_database_connection()

    query = """
        SELECT
            run_id,
            run_timestamp,
            validation_status,
            issue_count
        FROM data_validation_run
        ORDER BY run_timestamp DESC;
    """

    data = pd.read_sql(
        query,
        connection
    )

    connection.close()

    results = []

    for _, row in data.iterrows():

        results.append({
            "run_id": int(row["run_id"]),
            "run_timestamp": row["run_timestamp"],
            "validation_status": row["validation_status"],
            "issue_count": int(row["issue_count"])
        })

    return results