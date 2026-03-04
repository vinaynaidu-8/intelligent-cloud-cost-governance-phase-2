import boto3
import json
from datetime import datetime, timedelta

ce = boto3.client("ce")


def get_service_cost(service_name):

    end = datetime.utcnow().date()
    start = end - timedelta(days=7)

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": str(start),
            "End": str(end)
        },
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        Filter={
            "Dimensions": {
                "Key": "SERVICE",
                "Values": [service_name]
            }
        }
    )

    total = 0

    for day in response["ResultsByTime"]:
        total += float(day["Total"]["UnblendedCost"]["Amount"])

    return round(total, 4)


def main():

    ec2_cost = get_service_cost(
        "Amazon Elastic Compute Cloud - Compute"
    )

    s3_cost = get_service_cost(
        "Amazon Simple Storage Service"
    )

    resources = [

        {
            "service": "ec2",
            "cost": {
                "last_7_days": ec2_cost
            }
        },

        {
            "service": "s3",
            "cost": {
                "last_7_days": s3_cost
            }
        }

    ]

    with open("data/cost_metrics_inventory.json", "w") as f:
        json.dump({"resources": resources}, f, indent=4)

    print("Cost collection completed.")
    print("EC2 Cost:", ec2_cost)
    print("S3 Cost:", s3_cost)


if __name__ == "__main__":
    main()
