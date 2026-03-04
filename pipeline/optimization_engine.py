import json


def load_metrics():
    with open("data/metrics_inventory.json") as f:
        return json.load(f)


def load_cost():
    with open("data/cost_metrics_inventory.json") as f:
        return json.load(f)


def analyze_ec2(cpu, net_in, net_out):

    total_network = net_in + net_out

    if cpu < 5 and total_network < 10000:
        return "IDLE", "Stop instance"

    if cpu < 30:
        return "UNDERUTILIZED", "Downsize instance"

    return "HEALTHY", "No action required"


def main():

    metrics_data = load_metrics()
    cost_data = load_cost()

    recommendations = []

    ec2_cost = 0
    s3_cost = 0

    for r in cost_data["resources"]:
        if r["service"] == "ec2":
            ec2_cost = r["cost"]["last_7_days"]

        if r["service"] == "s3":
            s3_cost = r["cost"]["last_7_days"]

    for r in metrics_data["resources"]:

        if r["service"] == "ec2":

            cpu = r["metrics"]["CPUUtilization"]
            net_in = r["metrics"]["NetworkIn"]
            net_out = r["metrics"]["NetworkOut"]

            status, action = analyze_ec2(cpu, net_in, net_out)

            recommendations.append({
                "service": "ec2",
                "resource_id": r["resource_id"],
                "analysis": {
                    "status": status,
                    "recommendation": action,
                    "cpu_utilization": cpu,
                    "network_in": net_in,
                    "network_out": net_out,
                    "estimated_weekly_savings": ec2_cost
                }
            })

    if s3_cost > 0:

        recommendations.append({
            "service": "s3",
            "analysis": {
                "status": "OPTIMIZE",
                "recommendation": "Enable lifecycle policies",
                "reason": "Storage optimization possible",
                "estimated_weekly_savings": round(s3_cost * 0.3, 4)
            }
        })

    with open("data/optimization_report.json", "w") as f:
        json.dump({"recommendations": recommendations}, f, indent=4)

    print("Optimization analysis completed.")


if __name__ == "__main__":
    main()
