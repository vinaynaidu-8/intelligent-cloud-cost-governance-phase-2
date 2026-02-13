import boto3
import json
from datetime import datetime, timedelta

BUCKET = "cost-governance-phase2-320003239859"
PREFIX = "cost-governance/"

s3 = boto3.client("s3")


def load_last_n_days(days=7):
    end_date = datetime.utcnow().date()
    data_points = []

    for i in range(days):
        day = end_date - timedelta(days=i)
        prefix = (
            f"{PREFIX}year={day.year}/"
            f"month={day.month:02d}/"
            f"day={day.day:02d}/"
        )

        response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
        if "Contents" not in response:
            continue

        for obj in response["Contents"]:
            if obj["Key"].endswith("cost_metrics_inventory.json"):
                file_obj = s3.get_object(Bucket=BUCKET, Key=obj["Key"])
                content = json.loads(file_obj["Body"].read())

                for res in content["resources"]:
                    if res["service"] == "ec2":
                        data_points.append({
                            "date": str(day),
                            "cpu": res["metrics"]["CPUUtilization"],
                            "net_in": res["metrics"]["NetworkIn"],
                            "net_out": res["metrics"]["NetworkOut"],
                            "cost": res["cost"]["last_7_days"]
                        })

    return data_points


if __name__ == "__main__":
    data = load_last_n_days()
    with open("ml_dataset.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"ML dataset created with {len(data)} records")
