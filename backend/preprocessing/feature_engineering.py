def create_features(df):
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

    return df