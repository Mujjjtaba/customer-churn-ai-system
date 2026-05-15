from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from models.train_models import train_all_models
from models.evaluate_models import get_metrics
from models.predict import predict_churn
from models.test_predict import run_validation
from utils.helper import generate_recommendation
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/charts", StaticFiles(directory="eda/charts"), name="charts")

@app.get("/")
def home():
    return {"message": "Customer Churn AI Backend Running"}

@app.get("/train-models")
def train_models():
    return train_all_models()

@app.get("/metrics")
def metrics():
    return get_metrics()

@app.post("/predict")
def predict(data: dict):
    result = predict_churn(data)
    result["recommendation"] = generate_recommendation(result["churn_probability"])
    return result

@app.get("/eda-images")
def eda_images():
    files = os.listdir("eda/charts")
    return {"charts": [f"/charts/{file}" for file in files]}

@app.get("/test")
def test_model():
    """Run model validation against known data from the dataset."""
    return run_validation(n_samples=50)