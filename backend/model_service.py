"""
Model loading and prediction service.
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Any

from backend.config import MODEL_PATH, RESEARCH_METRICS
from backend.preprocessing import prepare_input_dataframe
from backend.utils import format_rupiah

class ModelService:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"File model tidak ditemukan pada path: {self.model_path}")
        self.model = joblib.load(self.model_path)

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes feature preprocessing, model inference, log-inversion,
        and bounds computation.
        """
        if self.model is None:
            self._load_model()

        # 1. Preprocess inputs into 14-feature DataFrame
        df_input = prepare_input_dataframe(input_data)

        # 2. Pipeline prediction (returns log1p(price))
        log_pred = self.model.predict(df_input)[0]

        # 3. Target Inversion using expm1
        price_pred = float(np.expm1(log_pred))
        price_pred_int = int(round(max(0, price_pred)))

        # 4. Secondary metrics calculation
        land_area = float(input_data['land_area'])
        price_per_sqm = int(round(price_pred_int / land_area)) if land_area > 0 else 0

        # MAE from academic research: Rp1,015,916,527
        mae = int(RESEARCH_METRICS['ensemble']['mae'])
        lower_bound = max(0, price_pred_int - mae)
        upper_bound = price_pred_int + mae

        return {
            "predicted_price_idr": price_pred_int,
            "formatted_price_idr": format_rupiah(price_pred_int),
            "price_per_sqm_land": price_per_sqm,
            "formatted_price_per_sqm": format_rupiah(price_per_sqm) + " / m²",
            "mae_idr": mae,
            "lower_bound_idr": lower_bound,
            "upper_bound_idr": upper_bound,
            "formatted_lower_bound": format_rupiah(lower_bound),
            "formatted_upper_bound": format_rupiah(upper_bound),
            "input_summary": input_data
        }


# Singleton instance
_model_service_instance = None

def get_model_service() -> ModelService:
    global _model_service_instance
    if _model_service_instance is None:
        _model_service_instance = ModelService()
    return _model_service_instance
