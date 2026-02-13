import boto3
import json
from datetime import datetime, timedelta


# -------------------------------------------------
# Load Inventory from Phase 2.1
# -------------------------------------------------
def load_inventory():
    with open("inventory.json", "r") as f:
        return json.load(f)


# -------------------------------------------------
# Collect CloudWatch Metrics for EC2
# -------------------------------------------------
def collect_ec2_metrics(instance_id, region):
    cloudwatch = boto3.client("cloudwatch", region_name=region)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)

    metrics_to_collect = [
        "CPUUtilization",
        "NetworkIn",
        "NetworkOut"
    ]

    metrics_data = {}

    for metric in metrics_to_collect:
        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName=metric,
            Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average"]
        )

        datapoints = response.get("Datapoints", [])

        if datapoints:
            latest_point = sorted(
                datapoints, key=lambda x: x["Timestamp"]
            )[-1]
            metrics_data[metric] = latest_point["Average"]
        else:
            metrics_data[metric] = None

    return metrics_data


# -------------------------------------------------
# Main Execution
# -------------------------------------------------
def main():
    inventory = load_inventory()
    region = inventory["region"]

    enriched_resources = []

    for resource in inventory["resources"]:
        if resource["service"] == "ec2":
            resource["metrics"] = collect_ec2_metrics(
                resource["resource_id"],
                region
            )

        enriched_resources.append(resource)

    metrics_inventory = {
        "account_id": inventory["account_id"],
        "region": region,
        "timestamp": datetime.utcnow().isoformat(),
        "resources": enriched_resources
    }

    with open("metrics_inventory.json", "w") as f:
        json.dump(metrics_inventory, f, indent=4)

    print("Metrics collection completed successfully.")
    print(f"Resources processed: {len(enriched_resources)}")


if __name__ == "__main__":
    main()
