import joblib
import pandas as pd
import psycopg2


MODEL_PATH = "machine-learning/machine_failure_model.joblib"
FEATURES_PATH = "machine-learning/machine_failure_features.csv"


def load_model():
    return joblib.load(MODEL_PATH)


def load_data():
    return pd.read_csv(FEATURES_PATH)


def get_database_connection():
    return psycopg2.connect(
        dbname="apex_manufacturing",
        user="bidya",
        host="localhost",
        port="5432"
    )


def save_predictions_to_database(results):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        TRUNCATE TABLE ml_prediction
    """)

    prediction_rows = []

    for index, (_, row) in enumerate(results.iterrows(), start=1):
        prediction_rows.append((
            index,
            int(row["machine_id"]),
            "machine_failure_model_v1",
            row["failure_probability"],
            row["risk_level"]
        ))

    cursor.executemany(
        """
        INSERT INTO ml_prediction (
            prediction_id,
            machine_id,
            model_id,
            prediction_timestamp,
            failure_probability,
            risk_level,
            prediction_status
        )
        VALUES (
            %s,
            %s,
            %s,
            CURRENT_TIMESTAMP,
            %s,
            %s,
            'Completed'
        )
        """,
        prediction_rows
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("Predictions saved to PostgreSQL.")
    print(f"Records inserted: {len(prediction_rows)}")


def predict():
    print("Loading machine failure prediction model...")
    print("----------------------------------------")

    model = load_model()
    data = load_data()

    target_column = "maintenance_within_7_days"

    features = data.drop(columns=[target_column])

    predictions = model.predict(features)
    probabilities = model.predict_proba(features)[:, 1]

    results = data[
        ["machine_key", "machine_id"]
    ].copy()

    results["failure_risk_prediction"] = predictions
    results["failure_probability"] = probabilities

    results["risk_level"] = results["failure_probability"].apply(
        lambda probability:
        "High" if probability >= 0.70
        else "Medium" if probability >= 0.40
        else "Low"
    )

    output_path = "machine-learning/predictions.csv"
    results.to_csv(output_path, index=False)

    print("Predictions generated successfully.")
    print(f"Records: {len(results)}")
    print(f"Output: {output_path}")

    print("\nPrediction summary")
    print("----------------------------------------")
    print(results["risk_level"].value_counts())

    print("\nSaving predictions to PostgreSQL...")
    save_predictions_to_database(results)

    print("\nSample predictions")
    print("----------------------------------------")
    print(results.head(10))


if __name__ == "__main__":
    predict()