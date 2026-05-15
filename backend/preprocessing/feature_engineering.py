def create_features(df):
    yes_no_columns = [
        "PhoneService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    # Convert Yes/No style fields into temporary numeric count
    service_count = 0
    for col in yes_no_columns:
        service_count += df[col].apply(lambda x: 1 if str(x).strip().lower() == "yes" else 0)

    df["ServiceCount"] = service_count

    # safer average monthly spend
    df["AvgMonthlySpend"] = df["TotalCharges"] / df["tenure"].replace(0, 1)

    return df