from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import psycopg2


app = FastAPI(
    title="Apex Manufacturing Intelligence API",
    description="Machine maintenance risk prediction API",
    version="1.0.0"
)


MODEL_PATH = "machine-learning/machine_failure_model.joblib"

model = joblib.load(MODEL_PATH)


def get_database_connection():
    return psycopg2.connect(
        dbname="apex_manufacturing",
        user="bidya",
        host="localhost",
        port="5432"
    )


class PredictionRequest(BaseModel):
    machine_id: int
    temperature: float
    vibration: float
    pressure: float
    rotation_speed: float
    power_consumption: float


@app.get("/")
def root():
    return {
        "application": "Apex Manufacturing Intelligence API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True
    }


@app.post("/predict")
def predict(request: PredictionRequest):

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT machine_type, operating_status
        FROM machine
        WHERE machine_id = %s
        """,
        (request.machine_id,)
    )

    machine = cursor.fetchone()

    if machine is None:
        cursor.close()
        connection.close()

        raise HTTPException(
            status_code=404,
            detail=f"Machine {request.machine_id} not found"
        )

    machine_type, operating_status = machine

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM maintenance_record
        WHERE machine_id = %s
        """,
        (request.machine_id,)
    )

    maintenance_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    input_data = pd.DataFrame([{
        "machine_key": 0,
        "machine_id": request.machine_id,
        "avg_temperature": request.temperature,
        "max_temperature": request.temperature,
        "avg_vibration": request.vibration,
        "max_vibration": request.vibration,
        "avg_pressure": request.pressure,
        "avg_rotation_speed": request.rotation_speed,
        "avg_power_consumption": request.power_consumption,
        "maintenance_count": maintenance_count,
        "machine_type": machine_type,
        "operating_status": operating_status
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if probability >= 0.70:
        risk_level = "High"
        recommendation = "Schedule maintenance inspection"
    elif probability >= 0.40:
        risk_level = "Medium"
        recommendation = "Monitor machine condition"
    else:
        risk_level = "Low"
        recommendation = "Continue normal operation"

    return {
        "machine_id": request.machine_id,
        "machine_type": machine_type,
        "operating_status": operating_status,
        "maintenance_count": maintenance_count,
        "failure_probability": round(float(probability), 4),
        "risk_level": risk_level,
        "recommendation": recommendation
    }