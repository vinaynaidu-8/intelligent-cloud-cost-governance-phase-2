import json
import numpy as np
from datetime import datetime


def load_dataset():
    with open("ml_dataset.json") as f:
        return json.load(f)


def detect_anomalies(data):
    cpu_values = np.array([d["cpu"] for d in data])
    mean = cpu_values.mean()
    std = cpu_values.std()

    anomalies = []

    for d in data:
        z = 0 if std == 0 else (d["cpu"] - mean) / std
        if abs(z) > 2:
            anomalies.append({
                "date": d["date"],
                "cpu": d["cpu"],
                "z_score": round(z, 2),
                "reason": "CPU anomaly detected"
            })

    return anomalies


if __name__ == "__main__":
    dataset = load_dataset()
    anomalies = detect_anomalies(dataset)

    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_records": len(dataset),
        "anomalies_detected": anomalies
    }

    with open("anomaly_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print(f"Anomalies detected: {len(anomalies)}")
