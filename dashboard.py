import json

def show_menu():
    print("\n--- Cloud Cost Governance Dashboard ---")
    print("1. View Inventory")
    print("2. View Metrics")
    print("3. View Cost")
    print("4. View Optimization")
    print("5. View Anomalies")
    print("6. Exit")


def load(file):
    with open(file) as f:
        return json.load(f)


while True:
    show_menu()
    choice = input("Select option: ")

    if choice == "1":
        print(load("inventory.json"))

    elif choice == "2":
        print(load("metrics_inventory.json"))

    elif choice == "3":
        print(load("cost_metrics_inventory.json"))

    elif choice == "4":
        print(load("optimization_report.json"))

    elif choice == "5":
        print(load("anomaly_report.json"))

    elif choice == "6":
        print("Exiting dashboard.")
        break

    else:
        print("Invalid choice")
