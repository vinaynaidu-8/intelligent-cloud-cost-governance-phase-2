import boto3
import json
from datetime import datetime

ec2 = boto3.client("ec2")
s3 = boto3.client("s3")
rds = boto3.client("rds")

def main():
    resources = []

    # EC2
    for r in ec2.describe_instances()["Reservations"]:
        for i in r["Instances"]:
            resources.append({
                "service": "ec2",
                "resource_id": i["InstanceId"],
                "region": ec2.meta.region_name
            })

    # S3
    for b in s3.list_buckets()["Buckets"]:
        resources.append({
            "service": "s3",
            "resource_id": b["Name"],
            "region": "global"
        })

    # RDS
    for db in rds.describe_db_instances()["DBInstances"]:
        resources.append({
            "service": "rds",
            "resource_id": db["DBInstanceIdentifier"],
            "region": rds.meta.region_name
        })

    data = {
        "account_id": boto3.client("sts").get_caller_identity()["Account"],
        "region": ec2.meta.region_name,
        "timestamp": datetime.utcnow().isoformat(),
        "resources": resources
    }

    with open("data/inventory.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Resource discovery completed.")

if __name__ == "__main__":
    main()

