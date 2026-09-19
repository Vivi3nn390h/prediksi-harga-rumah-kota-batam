"""
FastAPI Main Application.
Serves prediction API endpoints under /api/* and mounts static frontend files.
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pathlib import Path

from backend.config import APP_TITLE, APP_VERSION, DATASET_RECORDS, ZONES, LIMITS, RESEARCH_METRICS
from backend.schemas import PredictRequest, PredictResponse, MetadataResponse, ModelInfoResponse
from backend.model_service import get_model_service

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="Sistem Prediksi Harga Rumah Kota Batam menggunakan Model Ensemble (Linear Regression + Random Forest)"
)

# Initialize model service on startup
model_service = get_model_service()

# --- API ENDPOINTS ---

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": APP_TITLE, "version": APP_VERSION}


@app.get("/api/metadata", response_model=MetadataResponse)
def get_metadata():
    return MetadataResponse(
        app_title=APP_TITLE,
        dataset_records=DATASET_RECORDS,
        zones=ZONES,
        limits=LIMITS
    )


@app.get("/api/model-info", response_model=ModelInfoResponse)
def get_model_info():
    notes = [
        "Pengujian menggunakan 5-Fold Cross-Validation pada 3.150 data rumah Kota Batam.",
        "Model Ridge Regression mengalami keterbatasan pada pola non-linear pasar properti Batam (R² 0.4107).",
        "Random Forest Regressor mampu menangkap interaksi kompleks fitur non-linear (R² 0.4544).",
        "Hasil Optimasi OOF Weighting menetapkan bobot Ridge = 0.00 dan Random Forest = 1.00, menjadikan Ensemble setara dengan kinerja optimal Random Forest."
    ]
    return ModelInfoResponse(
        app_title=APP_TITLE,
        metrics=RESEARCH_METRICS,
        notes=notes
    )


@app.post("/api/predict", response_model=PredictResponse)
def predict_house_price(payload: PredictRequest):
    try:
        result = model_service.predict(payload.model_dump())
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan saat memproses prediksi: {str(e)}"
        )


# --- EXCEPTION HANDLERS ---

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_messages = []
    for err in errors:
        msg = err.get("msg", "")
        # Strip "Value error, " prefix if added by Pydantic
        if msg.startswith("Value error, "):
            msg = msg.replace("Value error, ", "")
        custom_messages.append(msg)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": custom_messages,
            "message": "Input tidak valid. Periksa kembali form isian Anda."
        }
    )


# --- STATIC FILES & 404 ROUTING ---

# Serve 404 page if static resource not found
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    html_404 = FRONTEND_DIR / "404.html"
    if html_404.exists():
        return FileResponse(html_404, status_code=404)
    return JSONResponse(status_code=404, content={"detail": "Halaman tidak ditemukan"})


# Mount static files at root
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
