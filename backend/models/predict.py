import json
import joblib
import pandas as pd
from config import MODEL_SAVE_PATH

model = joblib.load(MODEL_SAVE_PATH + "best_churn_model.pkl")
encoders = joblib.load(MODEL_SAVE_PATH + "label_encoders.pkl")
scaler = joblib.load(MODEL_SAVE_PATH + "scaler.pkl")
feature_columns = joblib.load(MODEL_SAVE_PATH + "feature_columns.pkl")

# Load model metadata to determine if scaling is needed
with open(MODEL_SAVE_PATH + "model_metadata.json", "r") as f:
    model_metadata = json.load(f)

REQUIRES_SCALING = model_metadata.get("requires_scaling", False)


def safe_encode(value, encoder):
    value = str(value).strip()
    classes = [str(x).strip() for x in encoder.classes_]

    if value not in classes:
        value = classes[0]

    return encoder.transform([value])[0]


def preprocess_input(data_dict):
    df = pd.DataFrame([data_dict])

    # -------- FIX: SeniorCitizen accepts both 0/1 int AND "Yes"/"No" string ----------
    raw_val = str(df.loc[0, "SeniorCitizen"]).strip().lower()
    if raw_val in ("yes", "1", "1.0"):
        df["SeniorCitizen"] = 1
    else:
        df["SeniorCitizen"] = 0

    # -------- ENGINEERED FEATURES ----------
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
    df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce").fillna(0)
    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce").fillna(0)

    df["AvgMonthlySpend"] = df["TotalCharges"] / (df["tenure"] + 1)

    service_yes_count = 0
    for col in [
        "PhoneService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]:
        if str(df.loc[0, col]).strip().lower() == "yes":
            service_yes_count += 1

    df["ServiceCount"] = service_yes_count

    # -------- LABEL ENCODE OTHER CATEGORICALS ----------
    for col, encoder in encoders.items():
        if col in df.columns:
            df[col] = safe_encode(df.loc[0, col], encoder)

    # -------- EXACT TRAINING ORDER ----------
    df = df.reindex(columns=feature_columns, fill_value=0)

    # -------- FORCE FLOAT ----------
    df = df.astype(float)

    return df


def predict_churn(data_dict):
    df = preprocess_input(data_dict)

    # Use metadata flag to determine scaling, not try/except
    if REQUIRES_SCALING:
        df_input = scaler.transform(df)
    else:
        df_input = df.values

    pred = model.predict(df_input)[0]
    prob = model.predict_proba(df_input)[0][1]

    return {
        "prediction": "Likely to Churn" if int(pred) == 1 else "Not Likely to Churn",
        "churn_probability": round(float(prob) * 100, 2)
    }