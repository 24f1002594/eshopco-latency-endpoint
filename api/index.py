import json
import math
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Load data into memory on startup
try:
    with open('q-vercel-latency.json', 'r') as f:
        DATASET = json.load(f)
except FileNotFoundError:
    print("Error: q-vercel-latency.json not found.")
    DATASET = []

def calculate_p95(values):
    """Calculates the 95th percentile using linear interpolation."""
    if not values:
        return 0
    values.sort()
    n = len(values)
    # Calculate rank (using n-1 for 0-based indexing interpolation)
    rank = 0.95 * (n - 1)
    lower_idx = int(math.floor(rank))
    upper_idx = int(math.ceil(rank))
    
    if lower_idx == upper_idx:
        return values[lower_idx]
    
    # Interpolate
    weight = rank - lower_idx
    return values[lower_idx] * (1 - weight) + values[upper_idx] * weight

@app.route('/', methods=['POST'])
def check_latency():
    # 1. Parse Input
    req_data = request.get_json()
    if not req_data:
        return jsonify({"error": "Invalid JSON"}), 400
        
    target_regions = req_data.get('regions', [])
    threshold = req_data.get('threshold_ms', 0)
    
    results = {}

    # 2. Process per region
    for region in target_regions:
        # Filter data for this specific region
        region_records = [d for d in DATASET if d['region'] == region]
        
        if not region_records:
            results[region] = "No data found"
            continue

        latencies = [d['latency_ms'] for d in region_records]
        uptimes = [d['uptime_pct'] for d in region_records]

        # Calculate Metrics
        avg_latency = sum(latencies) / len(latencies)
        avg_uptime = sum(uptimes) / len(uptimes)
        breaches = sum(1 for l in latencies if l > threshold)
        p95 = calculate_p95(latencies)

        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95, 2),
            "avg_uptime": round(avg_uptime, 3),
            "breaches": breaches
        }

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
