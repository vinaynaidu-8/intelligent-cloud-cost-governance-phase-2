#!/bin/bash
echo "Running pipeline..."
python3 pipeline/resource_discovery.py
python3 pipeline/cost_collection.py
python3 pipeline/optimization_engine.py
echo "Pipeline finished."
