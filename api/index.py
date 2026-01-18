from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

# Load telemetry data
TELEMETRY_DATA = [
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 171.74,
    "uptime_pct": 97.333,
    "timestamp": 20250301
  },
  {
    "region": "apac",
    "service": "recommendations",
    "latency_ms": 167.29,
    "uptime_pct": 98.243,
    "timestamp": 20250302
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 206.7,
    "uptime_pct": 99.241,
    "timestamp": 20250303
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 138,
    "uptime_pct": 97.256,
    "timestamp": 20250304
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 137.3,
    "uptime_pct": 97.989,
    "timestamp": 20250305
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 159.36,
    "uptime_pct": 97.745,
    "timestamp": 20250306
  },
  {
    "region": "apac",
    "service": "recommendations",
    "latency_ms": 202.2,
    "uptime_pct": 98.167,
    "timestamp": 20250307
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 193.05,
    "uptime_pct": 98.208,
    "timestamp": 20250308
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 127.12,
    "uptime_pct": 98.661,
    "timestamp": 20250309
  },
  {
    "region": "apac",
    "service": "catalog",
    "latency_ms": 195.79,
    "uptime_pct": 98.019,
    "timestamp": 20250310
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 191.53,
    "uptime_pct": 99.388,
    "timestamp": 20250311
  },
  {
    "region": "apac",
    "service": "recommendations",
    "latency_ms": 147.93,
    "uptime_pct": 98.718,
    "timestamp": 20250312
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 161.68,
    "uptime_pct": 99.192,
    "timestamp": 20250301
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 180.39,
    "uptime_pct": 99.185,
    "timestamp": 20250302
  },
  {
    "region": "emea",
    "service": "analytics",
    "latency_ms": 181.25,
    "uptime_pct": 97.536,
    "timestamp": 20250303
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 196.47,
    "uptime_pct": 97.169,
    "timestamp": 20250304
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 197.38,
    "uptime_pct": 97.379,
    "timestamp": 20250305
  },
  {
    "region": "emea",
    "service": "analytics",
    "latency_ms": 169.23,
    "uptime_pct": 97.994,
    "timestamp": 20250306
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 155.01,
    "uptime_pct": 97.999,
    "timestamp": 20250307
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 146.09,
    "uptime_pct": 97.804,
    "timestamp": 20250308
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 199.56,
    "uptime_pct": 97.694,
    "timestamp": 20250309
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 141.73,
    "uptime_pct": 99.065,
    "timestamp": 20250310
  },
  {
    "region": "emea",
    "service": "catalog",
    "latency_ms": 113.63,
    "uptime_pct": 97.614,
    "timestamp": 20250311
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 205.7,
    "uptime_pct": 99.444,
    "timestamp": 20250312
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 194.81,
    "uptime_pct": 98.546,
    "timestamp": 20250301
  },
  {
    "region": "amer",
    "service": "checkout",
    "latency_ms": 188.59,
    "uptime_pct": 97.471,
    "timestamp": 20250302
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 107.39,
    "uptime_pct": 99.131,
    "timestamp": 20250303
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 164.61,
    "uptime_pct": 97.373,
    "timestamp": 20250304
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 175.12,
    "uptime_pct": 97.521,
    "timestamp": 20250305
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 149.61,
    "uptime_pct": 99.094,
    "timestamp": 20250306
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 149.59,
    "uptime_pct": 97.389,
    "timestamp": 20250307
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 185.96,
    "uptime_pct": 99.408,
    "timestamp": 20250308
  },
  {
    "region": "amer",
    "service": "support",
    "latency_ms": 204.2,
    "uptime_pct": 98.589,
    "timestamp": 20250309
  },
  {
    "region": "amer",
    "service": "checkout",
    "latency_ms": 151.49,
    "uptime_pct": 97.227,
    "timestamp": 20250310
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 186.22,
    "uptime_pct": 99.392,
    "timestamp": 20250311
  },
  {
    "region": "amer",
    "service": "catalog",
    "latency_ms": 208.78,
    "uptime_pct": 98.855,
    "timestamp": 20250312
  }
]

class LatencyRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

@app.post("/api/latency")
async def check_latency(request: LatencyRequest):
    """Analyze latency metrics for specified regions"""
    results = []
    
    for region in request.regions:
        # Filter data for this region
        region_data = [d for d in TELEMETRY_DATA if d["region"] == region]
        
        if not region_data:
            continue
        
        # Extract latencies and uptimes
        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]
        
        # Calculate metrics
        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = float(np.mean(uptimes))
        breaches = sum(1 for lat in latencies if lat > request.threshold_ms)
        
        results.append({
            "region": region,
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        })
    
    return {"metrics": results}

@app.get("/")
async def root():
    return {"message": "Latency endpoint is running. POST to /api/latency"}
