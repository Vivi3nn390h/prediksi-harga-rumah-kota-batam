"""
Feature engineering and input transformation for model prediction.
"""

import pandas as pd
from typing import Dict, Any

FEATURE_COLUMNS = [
    'land_area', 
    'building_area', 
    'bedroom', 
    'bathroom', 
    'floor_count', 
    'room_ratio', 
    'area_ratio', 
    'loc_Batu Aji', 
    'loc_Batu Ampar', 
    'loc_Bengkong', 
    'loc_Lubuk Baja', 
    'loc_Nongsa', 
    'loc_Sagulung', 
    'loc_Sekupang'
]

ONE_HOT_LOCATIONS = [
    'Batu Aji',
    'Batu Ampar',
    'Bengkong',
    'Lubuk Baja',
    'Nongsa',
    'Sagulung',
    'Sekupang'
]

def prepare_input_dataframe(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Transforms user input dictionary into a pandas DataFrame matching exact
    14 features expected by the scikit-learn pipeline.
    """
    land_area = float(data['land_area'])
    building_area = float(data['building_area'])
    bedroom = int(data['bedroom'])
    bathroom = int(data['bathroom'])
    floor_count = int(data['floor_count'])
    location = str(data['location'])

    # Computed ratio features
    room_ratio = bedroom / bathroom if bathroom > 0 else bedroom / 1.0
    area_ratio = building_area / land_area if land_area > 0 else 1.0

    # One-hot encoding for location (Batam Center is the reference category = all 0)
    loc_encoded = {f"loc_{loc}": 1 if location == loc else 0 for loc in ONE_HOT_LOCATIONS}

    feature_dict = {
        'land_area': land_area,
        'building_area': building_area,
        'bedroom': bedroom,
        'bathroom': bathroom,
        'floor_count': floor_count,
        'room_ratio': room_ratio,
        'area_ratio': area_ratio,
        **loc_encoded
    }

    # Construct DataFrame with exact column ordering
    df = pd.DataFrame([feature_dict])[FEATURE_COLUMNS]
    return df
