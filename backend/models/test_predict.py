"""
Test script to validate the churn prediction model against known data.
Picks real customers from the dataset and checks if predictions match actual labels.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from config import DATA_PATH
from models.predict import predict_churn


def run_validation(n_samples=50):
    """Validate the model by predicting on known customers from the dataset."""
    df = pd.read_csv(DATA_PATH)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

    # Get balanced sample: half churned, half not churned
    churned = df[df["Churn"] == "Yes"].sample(n=min(n_samples // 2, len(df[df["Churn"] == "Yes"])), random_state=42)
    not_churned = df[df["Churn"] == "No"].sample(n=min(n_samples // 2, len(df[df["Churn"] == "No"])), random_state=42)
    sample = pd.concat([churned, not_churned])

    results = []
    correct = 0
    total = len(sample)

    feature_cols = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
        "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
        "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
        "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
        "MonthlyCharges", "TotalCharges"
    ]

    for _, row in sample.iterrows():
        actual_label = row["Churn"]  # "Yes" or "No"

        # Build input dict from the row
        input_data = {}
        for col in feature_cols:
            val = row[col]
            if col == "SeniorCitizen":
                val = int(val)
            elif col in ("tenure",):
                val = int(val)
            elif col in ("MonthlyCharges", "TotalCharges"):
                val = float(val)
            else:
                val = str(val)
            input_data[col] = val

        result = predict_churn(input_data)

        predicted_churn = result["prediction"] == "Likely to Churn"
        actual_churn = actual_label == "Yes"

        is_correct = predicted_churn == actual_churn
        if is_correct:
            correct += 1

        results.append({
            "actual": actual_label,
            "predicted": result["prediction"],
            "probability": result["churn_probability"],
            "correct": is_correct
        })

    accuracy = round(correct / total * 100, 2)

    # Calculate breakdown
    tp = sum(1 for r in results if r["actual"] == "Yes" and "Likely to Churn" == r["predicted"])
    tn = sum(1 for r in results if r["actual"] == "No" and "Not Likely" in r["predicted"])
    fp = sum(1 for r in results if r["actual"] == "No" and "Likely to Churn" == r["predicted"])
    fn = sum(1 for r in results if r["actual"] == "Yes" and "Not Likely" in r["predicted"])

    return {
        "total_tested": total,
        "correct": correct,
        "accuracy_pct": accuracy,
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "sample_results": results[:10]  # First 10 as sample
    }


if __name__ == "__main__":
    result = run_validation()
    print(f"\n{'='*50}")
    print(f"  MODEL VALIDATION RESULTS")
    print(f"{'='*50}")
    print(f"  Total Tested:     {result['total_tested']}")
    print(f"  Correct:          {result['correct']}")
    print(f"  Accuracy:         {result['accuracy_pct']}%")
    print(f"  True Positives:   {result['true_positives']}")
    print(f"  True Negatives:   {result['true_negatives']}")
    print(f"  False Positives:  {result['false_positives']}")
    print(f"  False Negatives:  {result['false_negatives']}")
    print(f"{'='*50}\n")

    print("Sample predictions:")
    for i, r in enumerate(result["sample_results"]):
        status = "✓" if r["correct"] else "✗"
        print(f"  {status} Actual: {r['actual']:3s} | Predicted: {r['predicted']:22s} | Prob: {r['probability']}%")
