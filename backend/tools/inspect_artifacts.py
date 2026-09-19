"""
Diagnostic script to inspect ensemble_model.pkl artifact and test prediction.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import MODEL_PATH
from backend.model_service import get_model_service

def inspect():
    print("=" * 60)
    print("ARTIFACT INSPECTION TOOL")
    print("=" * 60)
    print(f"Target model path: {MODEL_PATH}")
    print(f"Exists: {MODEL_PATH.exists()}")
    
    if not MODEL_PATH.exists():
        print("ERROR: Model artifact file not found!")
        return

    try:
        service = get_model_service()
        print("\nPipeline architecture:")
        print(service.model)

        print("\nTesting sample prediction...")
        sample_input = {
            "land_area": 120,
            "building_area": 90,
            "bedroom": 3,
            "bathroom": 2,
            "floor_count": 1,
            "location": "Batam Center"
        }
        res = service.predict(sample_input)
        print("\nPrediction Result:")
        print(f"  Input: {sample_input}")
        print(f"  Estimated Price: {res['formatted_price_idr']}")
        print(f"  Price/m² land:  {res['formatted_price_per_sqm']}")
        print(f"  MAE Bound:      {res['formatted_lower_bound']} - {res['formatted_upper_bound']}")
        print("\nInspection Status: SUCCESS")
    except Exception as e:
        print(f"\nInspection Failed with Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    inspect()
