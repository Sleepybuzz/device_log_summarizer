"""Generates a sample device_telemetry.csv (includes a few deliberately bad rows)."""
import csv
import random

random.seed(42)
profiles = {"DEV_A": 65, "DEV_B": 72, "DEV_C": 55, "DEV_D": 91, "DEV_E": 78}
rows = []
for dev, base in profiles.items():
    for _ in range(12):
        temp = round(random.gauss(base, 4), 1)
        r = random.random()
        status = "ERROR" if r < 0.15 else "WARNING" if r < 0.4 else "ACTIVE"
        rows.append([dev, status, temp])
rows += [["DEV_A", "ACTIVE", "N/A"], ["DEV_B", "WARNING", ""], ["", "ACTIVE", 50.0],
         ["DEV_C", "BROKEN", 60.0], ["DEV_C", "ERROR", "abc"]]
random.shuffle(rows)
with open("device_telemetry.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["device_id", "status", "temperature"])
    w.writerows(rows)
