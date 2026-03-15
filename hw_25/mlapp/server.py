from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette_exporter import PrometheusMiddleware, handle_metrics
import joblib
import numpy as np
from pathlib import Path

app = FastAPI(title="Diabetes Prediction API with Monitoring")

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

model_path = Path(__file__).parent / "model.pkl"
model = None

try:
    model = joblib.load(model_path)
except Exception as e:
    print(f"Warning: Could not load model: {e}")

class PredictRequest(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float

class PredictResponse(BaseModel):
    predict: float

@app.get("/")
def root():
    return {"message": "Diabetes Prediction API with Monitoring"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/v1/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    features = np.array([[
        request.age, request.sex, request.bmi, request.bp,
        request.s1, request.s2, request.s3, request.s4,
        request.s5, request.s6
    ]])
    
    prediction = model.predict(features)
    
    return PredictResponse(predict=float(prediction[0]))
