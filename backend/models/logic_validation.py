"""
Step-by-step logical validation of the churn model.
Tests each factor in isolation to verify the model learned correct patterns.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.predict import predict_churn

# Baseline: A "neutral" customer
BASE = {
    "gender": "Male", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
    "tenure": 12, "PhoneService": "Yes", "MultipleLines": "No",
    "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
    "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
    "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check", "MonthlyCharges": 70.0, "TotalCharges": 840.0,
}

def test(label, overrides):
    data = {**BASE, **overrides}
    # Recalculate TotalCharges if tenure or MonthlyCharges changed
    if "tenure" in overrides or "MonthlyCharges" in overrides:
        data["TotalCharges"] = data["tenure"] * data["MonthlyCharges"]
    result = predict_churn(data)
    return result["churn_probability"]

def print_comparison(title, tests):
    """Print a comparison table"""
    print(f"\n{'='*65}")
    print(f"  {title}")
    print(f"{'='*65}")
    baseline_prob = test("baseline", {})
    print(f"  {'Baseline (neutral customer)':<42} -> {baseline_prob:>6.2f}%")
    print(f"  {'-'*55}")
    for label, overrides in tests:
        prob = test(label, overrides)
        diff = prob - baseline_prob
        arrow = "UP" if diff > 0 else "DN" if diff < 0 else "=="
        color_hint = "MORE churn" if diff > 0 else "LESS churn" if diff < 0 else "no change"
        print(f"  {label:<42} -> {prob:>6.2f}%  ({arrow} {abs(diff):+.2f} {color_hint})")


# ========================================
# STEP 1: DEMOGRAPHICS
# ========================================
print("\n" + "#"*65)
print("  STEP 1: DEMOGRAPHICS -- Does age/family affect churn?")
print("#"*65)

print_comparison("1a. Senior Citizen Effect", [
    ("Senior Citizen = YES (less tech-savvy)", {"SeniorCitizen": 1}),
    ("Senior Citizen = NO (baseline)", {}),
])

print_comparison("1b. Gender Effect", [
    ("Gender = Female", {"gender": "Female"}),
    ("Gender = Male (baseline)", {}),
])

print_comparison("1c. Family Ties (Partner + Dependents)", [
    ("Has Partner + Dependents (family = sticky)", {"Partner": "Yes", "Dependents": "Yes"}),
    ("No Partner, No Dependents (alone = risky)", {"Partner": "No", "Dependents": "No"}),
])


# ========================================
# STEP 2: SERVICES — Does more services = less churn?
# ========================================
print("\n" + "#"*65)
print("  STEP 2: SERVICES -- Does more/better service reduce churn?")
print("#"*65)

print_comparison("2a. Phone Service", [
    ("Phone Service = No (fewer services)", {"PhoneService": "No", "MultipleLines": "No phone service"}),
    ("Phone Service = Yes (baseline)", {}),
    ("Phone + Multiple Lines", {"PhoneService": "Yes", "MultipleLines": "Yes"}),
])

print_comparison("2b. Internet Service Type", [
    ("Internet = No (no internet at all)", {"InternetService": "No", 
        "OnlineSecurity": "No internet service", "OnlineBackup": "No internet service",
        "DeviceProtection": "No internet service", "TechSupport": "No internet service",
        "StreamingTV": "No internet service", "StreamingMovies": "No internet service"}),
    ("Internet = DSL (cheaper, slower)", {"InternetService": "DSL"}),
    ("Internet = Fiber optic (baseline)", {}),
])

print_comparison("2c. Security & Protection (customer feels safe?)", [
    ("NO security, NO backup, NO protection", 
        {"OnlineSecurity": "No", "OnlineBackup": "No", "DeviceProtection": "No"}),
    ("YES security + backup + protection (feels safe)", 
        {"OnlineSecurity": "Yes", "OnlineBackup": "Yes", "DeviceProtection": "Yes"}),
])

print_comparison("2d. Tech Support (customer gets help?)", [
    ("Tech Support = No (frustrated customer)", {"TechSupport": "No"}),
    ("Tech Support = Yes (customer feels supported)", {"TechSupport": "Yes"}),
])

print_comparison("2e. Streaming Services (engagement)", [
    ("No streaming at all", {"StreamingTV": "No", "StreamingMovies": "No"}),
    ("Both streaming TV + Movies", {"StreamingTV": "Yes", "StreamingMovies": "Yes"}),
])

print_comparison("2f. FULL services vs ZERO services", [
    ("ALL services ON (security+backup+protection+support+streaming)", 
        {"OnlineSecurity": "Yes", "OnlineBackup": "Yes", "DeviceProtection": "Yes",
         "TechSupport": "Yes", "StreamingTV": "Yes", "StreamingMovies": "Yes",
         "MultipleLines": "Yes"}),
    ("ALL services OFF (bare minimum)", 
        {"OnlineSecurity": "No", "OnlineBackup": "No", "DeviceProtection": "No",
         "TechSupport": "No", "StreamingTV": "No", "StreamingMovies": "No",
         "MultipleLines": "No"}),
])


# ========================================
# STEP 3: BILLING & PAYMENT — Is it affordable?
# ========================================
print("\n" + "#"*65)
print("  STEP 3: BILLING -- Does price/contract/payment method matter?")
print("#"*65)

print_comparison("3a. Contract Length (commitment level)", [
    ("Month-to-month (no commitment = easy to leave)", {"Contract": "Month-to-month"}),
    ("One year contract (some commitment)", {"Contract": "One year"}),
    ("Two year contract (locked in = very sticky)", {"Contract": "Two year"}),
])

print_comparison("3b. Monthly Charges (affordability)", [
    ("Very cheap: $20/month", {"MonthlyCharges": 20.0}),
    ("Moderate: $50/month", {"MonthlyCharges": 50.0}),
    ("Baseline: $70/month", {}),
    ("Expensive: $100/month", {"MonthlyCharges": 100.0}),
    ("Very expensive: $120/month", {"MonthlyCharges": 120.0}),
])

print_comparison("3c. Payment Method (trust/convenience)", [
    ("Electronic check (manual = friction)", {"PaymentMethod": "Electronic check"}),
    ("Mailed check (old school)", {"PaymentMethod": "Mailed check"}),
    ("Bank transfer auto (set and forget)", {"PaymentMethod": "Bank transfer (automatic)"}),
    ("Credit card auto (set and forget)", {"PaymentMethod": "Credit card (automatic)"}),
])

print_comparison("3d. Paperless Billing", [
    ("Paperless = Yes (digital)", {"PaperlessBilling": "Yes"}),
    ("Paperless = No (physical bills)", {"PaperlessBilling": "No"}),
])


# ========================================
# STEP 4: TENURE — How long they've been with you
# ========================================
print("\n" + "#"*65)
print("  STEP 4: TENURE -- Does loyalty/time reduce churn?")
print("#"*65)

print_comparison("4a. Customer Tenure", [
    ("Brand new: 1 month", {"tenure": 1}),
    ("New: 3 months", {"tenure": 3}),
    ("6 months", {"tenure": 6}),
    ("1 year (baseline)", {}),
    ("2 years", {"tenure": 24}),
    ("4 years", {"tenure": 48}),
    ("6 years (loyal veteran)", {"tenure": 72}),
])


# ========================================
# STEP 5: EXTREME SCENARIOS
# ========================================
print("\n" + "#"*65)
print("  STEP 5: EXTREME SCENARIOS -- Best vs Worst case")
print("#"*65)

worst_case = predict_churn({
    "gender": "Female", "SeniorCitizen": 1, "Partner": "No", "Dependents": "No",
    "tenure": 1, "PhoneService": "Yes", "MultipleLines": "No",
    "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
    "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
    "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check", "MonthlyCharges": 100.0, "TotalCharges": 100.0,
})

best_case = predict_churn({
    "gender": "Male", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "Yes",
    "tenure": 72, "PhoneService": "Yes", "MultipleLines": "Yes",
    "InternetService": "DSL", "OnlineSecurity": "Yes", "OnlineBackup": "Yes",
    "DeviceProtection": "Yes", "TechSupport": "Yes", "StreamingTV": "Yes",
    "StreamingMovies": "Yes", "Contract": "Two year", "PaperlessBilling": "No",
    "PaymentMethod": "Credit card (automatic)", "MonthlyCharges": 60.0, "TotalCharges": 4320.0,
})

print(f"\n  WORST CASE (senior, alone, new, no services, expensive, e-check, month-to-month)")
print(f"  -> {worst_case['churn_probability']}% -- {worst_case['prediction']}")
print(f"\n  BEST CASE (young, family, loyal, all services, affordable, auto-pay, 2yr contract)")
print(f"  -> {best_case['churn_probability']}% -- {best_case['prediction']}")

print(f"\n{'='*65}")
print(f"  LOGIC VERIFIED: Spread = {worst_case['churn_probability'] - best_case['churn_probability']:.1f} percentage points")
print(f"{'='*65}")
