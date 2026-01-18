from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from typing import List

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class LatencyRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

class RegionMetrics(BaseModel):
    region: str
    avg_latency: float
    p95_latency: float
    avg_uptime: float
    breaches:  int

class LatencyResponse(BaseModel):
    metrics: List[RegionMetrics]

# Load the telemetry data (you'll need to place your CSV file here)
# For Vercel, place the CSV in the api directory or use a public URL
try:
    df = pd.read_csv('api/telemetry. csv')  # Adjust path based on where you store the CSV
except FileNotFoundError:
    df = None

@app.post("/", response_model=LatencyResponse)
async def check_latency(request: LatencyRequest):
    if df is None:
        return {"metrics": []}
    
    metrics = []
    
    for region in request.regions:
        # Filter data for the specific region
        region_data = df[df['region']. str.lower() == region.lower()]
        
        if len(region_data) == 0:
            continue
        
        # Calculate metrics
        avg_latency = round(region_data['latency_ms'].mean(), 2)
        p95_latency = round(region_data['latency_ms'].quantile(0.95), 2)
        avg_uptime = round(region_data['uptime']. mean(), 2)
        breaches = int((region_data['latency_ms'] > request.threshold_ms).sum())
        
        metrics.append(RegionMetrics(
            region=region,
            avg_latency=avg_latency,
            p95_latency=p95_latency,
            avg_uptime=avg_uptime,
            breaches=breaches
        ))
    
    return LatencyResponse(metrics=metrics)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
