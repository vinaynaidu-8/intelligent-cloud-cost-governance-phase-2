#!/bin/bash
echo "Starting Cost Governance Pipeline..."

python3 pipeline/resource_discovery.py
python3 pipeline/cost_collection.py
python3 pipeline/optimization_engine.py
python3 pipeline/anomaly_engine.py

echo "Pipeline completed successfully."
