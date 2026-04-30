import joblib
import pandas as pd
from config import MODEL_SAVE_PATH

model = joblib.load(MODEL_SAVE_PATH + "best_churn_model.pkl")
encoders = joblib.load(MODEL_SAVE_PATH + "label_encoders.pkl")
scaler = joblib.load(MODEL_SAVE_PATH + "scaler.pkl")

def preprocess_input(data_dict):
    df = pd.DataFrame([data_dict])

    df["AvgMonthlySpend"] = df["TotalCharges"] / (df["tenure"] + 1)

    df["ServiceCount"] = (
        df["PhoneService"] +
        df["OnlineSecurity"] +
        df["OnlineBackup"] +
        df["DeviceProtection"] +
        df["TechSupport"] +
        df["StreamingTV"] +
        df["StreamingMovies"]
    )

    for col, encoder in encoders.items():
        if col in df.columns:
            df[col] = encoder.transform(df[col])

    return df

def predict_churn(data_dict):
    df = preprocess_input(data_dict)

    try:
        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]
    except:
        df_scaled = scaler.transform(df)
        pred = model.predict(df_scaled)[0]
        prob = model.predict_proba(df_scaled)[0][1]

    return {
        "prediction": "Likely to Churn" if pred == 1 else "Not Likely to Churn",
        "churn_probability": round(float(prob) * 100, 2)
    }