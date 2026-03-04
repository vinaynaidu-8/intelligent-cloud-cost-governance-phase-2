import boto3
import json
from datetime import datetime, timedelta


def load_inventory():
    with open("data/inventory.json") as f:
        return json.load(f)


def collect_ec2_metrics(instance_id, region):

    cloudwatch = boto3.client("cloudwatch", region_name=region)

    end = datetime.utcnow()
    start = end - timedelta(hours=1)

    metrics = {}

    metric_names = [
        "CPUUtilization",
        "NetworkIn",
        "NetworkOut"
    ]

    for metric in metric_names:

        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName=metric,
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            StartTime=start,
            EndTime=end,
            Period=300,
            Statistics=["Average"]
        )

        datapoints = response.get("Datapoints", [])

        if datapoints:
            latest = sorted(datapoints, key=lambda x: x["Timestamp"])[-1]
            metrics[metric] = round(latest["Average"], 3)
        else:
            metrics[metric] = 0

    return metrics


def main():

    inventory = load_inventory()
    region = inventory["region"]

    enriched_resources = []

    for r in inventory["resources"]:

        if r["service"] == "ec2":

            metrics = collect_ec2_metrics(
                r["resource_id"],
                region
            )

            r["metrics"] = metrics

        enriched_resources.append(r)

    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "resources": enriched_resources
    }

    with open("data/metrics_inventory.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Metrics collection completed.")
    print("Resources processed:", len(enriched_resources))


if __name__ == "__main__":
    main()
