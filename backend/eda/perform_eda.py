import matplotlib.pyplot as plt
import seaborn as sns
import os
from config import CHART_PATH

def perform_eda(df):
    os.makedirs(CHART_PATH, exist_ok=True)

    plt.figure(figsize=(6,4))
    sns.countplot(x="Churn", data=df)
    plt.savefig(CHART_PATH + "churn_distribution.png")
    plt.close()

    plt.figure(figsize=(8,4))
    sns.histplot(df["tenure"], kde=True)
    plt.savefig(CHART_PATH + "tenure_distribution.png")
    plt.close()

    plt.figure(figsize=(8,4))
    sns.boxplot(x="Churn", y="MonthlyCharges", data=df)
    plt.savefig(CHART_PATH + "monthlycharges_vs_churn.png")
    plt.close()

    numeric_df = df.select_dtypes(include=["number"])

    plt.figure(figsize=(12,8))
    sns.heatmap(numeric_df.corr(), cmap="coolwarm")
    plt.savefig(CHART_PATH + "correlation_heatmap.png")
    plt.close()