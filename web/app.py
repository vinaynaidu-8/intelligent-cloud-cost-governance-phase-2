from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

DATA_DIR = "/home/ec2-user/cost-governance/data"

def load_json(file):
    path = os.path.join(DATA_DIR, file)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

@app.route("/", methods=["GET", "POST"])
def dashboard():
    result = None

    if request.method == "POST":
        resource = request.form.get("resource")
        days = request.form.get("days", "7")

        inventory = load_json("inventory.json")
        cost_data = load_json("cost_metrics_inventory.json")
        optimization = load_json("optimization_report.json")

        total_cost = 0.0
        recs = []

        for r in cost_data.get("resources", []):
            if r["service"] == resource:
                total_cost += r["cost"]["last_7_days"]

        for r in optimization.get("recommendations", []):
            if r["service"] == resource:
                recs.append(r)

        result = {
            "resource": resource.upper(),
            "days": days,
            "total_cost": round(total_cost, 4),
            "recommendations": recs
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
