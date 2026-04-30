import json
from config import METRICS_PATH

def get_metrics():
    with open(METRICS_PATH, "r") as f:
        return json.load(f)