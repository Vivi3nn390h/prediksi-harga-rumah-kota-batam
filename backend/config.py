"""
Configuration file containing system constants, research metrics, and validation limits.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "ensemble_model.pkl"

APP_TITLE = "Sistem Prediksi Harga Rumah Kota Batam"
APP_VERSION = "1.0.0"

# Dataset and Zone metadata
DATASET_RECORDS = 3150
ZONES = [
    "Batam Center",
    "Batu Aji",
    "Batu Ampar",
    "Bengkong",
    "Lubuk Baja",
    "Nongsa",
    "Sagulung",
    "Sekupang"
]

# Exact Academic Research Metrics
RESEARCH_METRICS = {
    "ridge": {
        "name": "Ridge Regression",
        "r2": 0.4107,
        "mae": 1130387741,
        "rmse": 2547456340,
        "weight": 0.00
    },
    "random_forest": {
        "name": "Random Forest Regressor",
        "r2": 0.4544,
        "mae": 1015916527,
        "rmse": 2451145415,
        "weight": 1.00
    },
    "ensemble": {
        "name": "Voting Regressor (Ensemble)",
        "r2": 0.4544,
        "mae": 1015916527,
        "rmse": 2451145415
    }
}

# Validation Limits
LIMITS = {
    "land_area": {"min": 20, "max": 2000},
    "building_area": {"min": 20, "max": 2000},
    "bedroom": {"min": 1, "max": 20},
    "bathroom": {"min": 1, "max": 20},
    "floor_count": {"min": 1, "max": 10}
}
