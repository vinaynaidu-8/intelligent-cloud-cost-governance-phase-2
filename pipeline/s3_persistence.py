import boto3
import os
from datetime import datetime


BUCKET_NAME = "cost-governance-phase2-320003239859"


# -------------------------------------------------
# Upload a file to S3 with date-based partitioning
# -------------------------------------------------
def upload_file(file_name):
    s3 = boto3.client("s3")

    today = datetime.utcnow()
    s3_key = (
        f"cost-governance/"
        f"year={today.year}/"
        f"month={today.month:02d}/"
        f"day={today.day:02d}/"
        f"{file_name}"
    )

    s3.upload_file(file_name, BUCKET_NAME, s3_key)
    print(f"Uploaded {file_name} → s3://{BUCKET_NAME}/{s3_key}")


# -------------------------------------------------
# Main Execution
# -------------------------------------------------
def main():
    files_to_upload = [
        "inventory.json",
        "metrics_inventory.json",
        "cost_metrics_inventory.json",
        "optimization_report.json"
    ]

    for file in files_to_upload:
        if os.path.exists(file):
            upload_file(file)
        else:
            print(f"File not found: {file}")


if __name__ == "__main__":
    main()
