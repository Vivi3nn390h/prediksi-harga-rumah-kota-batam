"""
Pydantic data schemas for requests and responses.
"""

from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, List
from backend.config import ZONES, LIMITS, RESEARCH_METRICS

DISCLAIMER_TEXT = "Hasil prediksi merupakan estimasi berdasarkan pola data yang digunakan dalam penelitian dan bukan merupakan penilaian harga resmi properti."

class PredictRequest(BaseModel):
    land_area: float = Field(
        ..., 
        ge=LIMITS["land_area"]["min"], 
        le=LIMITS["land_area"]["max"],
        description="Luas Tanah (m²)"
    )
    building_area: float = Field(
        ..., 
        ge=LIMITS["building_area"]["min"], 
        le=LIMITS["building_area"]["max"],
        description="Luas Bangunan (m²)"
    )
    bedroom: int = Field(
        ..., 
        ge=LIMITS["bedroom"]["min"], 
        le=LIMITS["bedroom"]["max"],
        description="Jumlah Kamar Tidur"
    )
    bathroom: int = Field(
        ..., 
        ge=LIMITS["bathroom"]["min"], 
        le=LIMITS["bathroom"]["max"],
        description="Jumlah Kamar Mandi"
    )
    floor_count: int = Field(
        ..., 
        ge=LIMITS["floor_count"]["min"], 
        le=LIMITS["floor_count"]["max"],
        description="Jumlah Lantai"
    )
    location: str = Field(
        ..., 
        description="Lokasi / Zona Properti di Batam"
    )

    @model_validator(mode="after")
    def validate_cross_field_rules(self):
        if self.location not in ZONES:
            raise ValueError(f"Lokasi '{self.location}' tidak valid. Pilih salah satu dari: {', '.join(ZONES)}")
        
        max_allowed_building = self.land_area * self.floor_count
        if self.building_area > max_allowed_building:
            raise ValueError(
                f"Luas bangunan ({self.building_area:g} m²) tidak boleh melebihi "
                f"luas tanah x jumlah lantai ({self.land_area:g} x {self.floor_count} = {max_allowed_building:g} m²)."
            )
        
        max_allowed_bathroom = self.bedroom + 2
        if self.bathroom > max_allowed_bathroom:
            raise ValueError(
                f"Jumlah kamar mandi ({self.bathroom}) rasionalnya tidak melebihi "
                f"jumlah kamar tidur + 2 ({self.bedroom} + 2 = {max_allowed_bathroom})."
            )
        
        return self


class PredictResponse(BaseModel):
    predicted_price_idr: int
    formatted_price_idr: str
    price_per_sqm_land: int
    formatted_price_per_sqm: str
    mae_idr: int
    lower_bound_idr: int
    upper_bound_idr: int
    formatted_lower_bound: str
    formatted_upper_bound: str
    input_summary: Dict[str, Any]
    disclaimer: str = DISCLAIMER_TEXT


class MetadataResponse(BaseModel):
    app_title: str
    dataset_records: int
    zones: List[str]
    limits: Dict[str, Dict[str, float]]


class ModelInfoResponse(BaseModel):
    app_title: str
    metrics: Dict[str, Any]
    notes: List[str]
