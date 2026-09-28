import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


DATA_PATH = "machine-learning/machine_failure_features.csv"
MODEL_PATH = "machine-learning/machine_failure_model.joblib"


print("Loading ML dataset...")
print("----------------------------------------")

data = pd.read_csv(DATA_PATH)

target = "maintenance_within_7_days"

features = [
    "machine_type",
    "operating_status",
    "avg_temperature",
    "max_temperature",
    "avg_vibration",
    "max_vibration",
    "avg_pressure",
    "avg_rotation_speed",
    "avg_power_consumption",
    "maintenance_count"
]

X = data[features]
y = data[target]


categorical_features = [
    "machine_type",
    "operating_status"
]

numeric_features = [
    "avg_temperature",
    "max_temperature",
    "avg_vibration",
    "max_vibration",
    "avg_pressure",
    "avg_rotation_speed",
    "avg_power_consumption",
    "maintenance_count"
]


preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")


print("\nTraining Random Forest model...")
print("----------------------------------------")

pipeline.fit(X_train, y_train)

predictions = pipeline.predict(X_test)


accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, zero_division=0)
recall = recall_score(y_test, predictions, zero_division=0)
f1 = f1_score(y_test, predictions, zero_division=0)


print("\nMODEL PERFORMANCE")
print("----------------------------------------")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")


print("\nCLASSIFICATION REPORT")
print("----------------------------------------")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


print("\nCONFUSION MATRIX")
print("----------------------------------------")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)


print("\nFEATURE IMPORTANCE")
print("----------------------------------------")

feature_names = (
    pipeline
    .named_steps["preprocessor"]
    .get_feature_names_out()
)

feature_importance = (
    pipeline
    .named_steps["model"]
    .feature_importances_
)

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": feature_importance
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print(importance_df.to_string(index=False))


os.makedirs("machine-learning", exist_ok=True)

joblib.dump(
    pipeline,
    MODEL_PATH
)


print("\nModel saved successfully.")
print(f"Output: {MODEL_PATH}")