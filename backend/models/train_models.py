import os
import json
import time
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from preprocessing.clean_data import load_and_clean_data
from preprocessing.encoder import encode_features
from preprocessing.scaler import scale_features
from preprocessing.feature_engineering import create_features
from eda.perform_eda import perform_eda
from config import MODEL_SAVE_PATH, METRICS_PATH

def train_all_models():
    os.makedirs(MODEL_SAVE_PATH, exist_ok=True)

    df = load_and_clean_data()
    df = create_features(df)

    raw_df = df.copy()
    perform_eda(raw_df)

    df, encoders = encode_features(df)

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    feature_columns = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(),
        "AdaBoost": AdaBoostClassifier(),
        "SVM": SVC(probability=True),
        "KNN": KNeighborsClassifier(),
        "XGBoost": XGBClassifier(eval_metric='logloss'),
        "LightGBM": LGBMClassifier(),
        "CatBoost": CatBoostClassifier(verbose=0)
    }

    scaled_models = ["Logistic Regression", "SVM", "KNN"]

    metrics = {}
    best_model = None
    best_score = 0
    best_model_name = ""
    best_requires_scaling = False

    for name, model in models.items():
        start = time.time()

        if name in scaled_models:
            model.fit(X_train_scaled, y_train)
            preds = model.predict(X_test_scaled)
            probs = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            probs = model.predict_proba(X_test)[:, 1]

        end = time.time()
        train_time = round(end - start, 4)

        acc = round(accuracy_score(y_test, preds), 4)
        prec = round(precision_score(y_test, preds), 4)
        rec = round(recall_score(y_test, preds), 4)
        f1 = round(f1_score(y_test, preds), 4)
        roc = round(roc_auc_score(y_test, probs), 4)

        metrics[name] = {
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1 Score": f1,
            "ROC AUC": roc,
            "Training Time": train_time
        }

        if f1 > best_score:
            best_score = f1
            best_model = model
            best_model_name = name
            best_requires_scaling = name in scaled_models

    joblib.dump(best_model, MODEL_SAVE_PATH + "best_churn_model.pkl")
    joblib.dump(encoders, MODEL_SAVE_PATH + "label_encoders.pkl")
    joblib.dump(scaler, MODEL_SAVE_PATH + "scaler.pkl")
    joblib.dump(feature_columns, MODEL_SAVE_PATH + "feature_columns.pkl")

    metadata = {
        "best_model_name": best_model_name,
        "requires_scaling": best_requires_scaling
    }

    with open(MODEL_SAVE_PATH + "model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)

    return metrics