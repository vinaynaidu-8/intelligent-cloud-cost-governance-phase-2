import json

def main():
    with open("data/cost_metrics_inventory.json") as f:
        cost_data = json.load(f)

    recommendations = []

    for r in cost_data["resources"]:
        if r["service"] == "ec2" and r["cost"]["last_7_days"] > 0:
            recommendations.append({
                "service": "ec2",
                "analysis": {
                    "status": "IDLE",
                    "recommendation": "Stop or downsize instance",
                    "reason": "Low utilization detected",
                    "estimated_weekly_savings": r["cost"]["last_7_days"]
                }
            })

        if r["service"] == "s3" and r["cost"]["last_7_days"] > 0:
            recommendations.append({
                "service": "s3",
                "analysis": {
                    "status": "OPTIMIZE",
                    "recommendation": "Enable lifecycle rules",
                    "reason": "Storage optimization possible",
                    "estimated_weekly_savings": round(r["cost"]["last_7_days"] * 0.3, 4)
                }
            })

    with open("data/optimization_report.json", "w") as f:
        json.dump({"recommendations": recommendations}, f, indent=2)

    print("Optimization completed.")

if __name__ == "__main__":
    main()

