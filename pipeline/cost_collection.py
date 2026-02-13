import boto3
import json
from datetime import datetime, timedelta

ce = boto3.client("ce")

SERVICE_MAP = {
    "ec2": "Amazon Elastic Compute Cloud - Compute",
    "s3": "Amazon Simple Storage Service"
}

def main():
    end = datetime.utcnow().date()
    start = end - timedelta(days=7)

    resources = []

    for svc, name in SERVICE_MAP.items():
        response = ce.get_cost_and_usage(
            TimePeriod={"Start": str(start), "End": str(end)},
            Granularity="DAILY",
            Metrics=["UnblendedCost"],
            Filter={
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": [name]
                }
            }
        )

        total = sum(
            float(d["Total"]["UnblendedCost"]["Amount"])
            for d in response["ResultsByTime"]
        )

        resources.append({
            "service": svc,
            "cost": {
                "currency": "USD",
                "last_7_days": round(total, 4)
            }
        })

    with open("data/cost_metrics_inventory.json", "w") as f:
        json.dump({"resources": resources}, f, indent=2)

    print("Cost collection completed.")

if __name__ == "__main__":
    main()
