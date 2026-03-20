from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette_exporter import PrometheusMiddleware, handle_metrics
import joblib
import numpy as np
import json
import logging
from datetime import datetime
from pythonjsonlogger import jsonlogger
import psycopg2
import os
import time

app = FastAPI(title="ML Service API")

app.add_middleware(PrometheusMiddleware, app_name="ml_service")
app.add_route("/metrics", handle_metrics)

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

model = None
try:
    model = joblib.load("model.pkl")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")

def get_db_connection():
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host="postgres_ml_service",
                database=os.getenv("ML_SERVICE_DB_NAME", "ml_service_db"),
                user=os.getenv("ML_SERVICE_DB_USER", "ml_service_user"),
                password=os.getenv("ML_SERVICE_DB_PASSWORD", "ml_service_pass_2026")
            )
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection attempt {attempt + 1} failed, retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to database after {max_retries} attempts")
                raise

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                input_data JSONB,
                prediction FLOAT,
                model_version VARCHAR(50),
                execution_time FLOAT
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

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

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "ML Service API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/api/v1/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    start_time = datetime.now()
    
    if model is None:
        logger.error("Model not loaded")
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    features = np.array([[
        request.age, request.sex, request.bmi, request.bp,
        request.s1, request.s2, request.s3, request.s4,
        request.s5, request.s6
    ]])
    
    prediction = model.predict(features)[0]
    execution_time = (datetime.now() - start_time).total_seconds()
    
    input_data = request.dict()
    
    logger.info({
        "event": "prediction",
        "input": input_data,
        "output": float(prediction),
        "execution_time": execution_time
    })
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO predictions 
               (timestamp, input_data, prediction, model_version, execution_time) 
               VALUES (%s, %s, %s, %s, %s)""",
            (start_time, json.dumps(input_data), float(prediction), "v1.0", execution_time)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to log prediction to database: {e}")
    
    return PredictResponse(predict=float(prediction))
