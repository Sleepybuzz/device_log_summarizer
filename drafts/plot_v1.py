import json
import matplotlib.pyplot as plt

with open("output.json") as f:
    data = json.load(f)

devices = list(data.keys())
temps = [data[d]["avg_temperature"] for d in devices]

plt.bar(devices, temps)
plt.show()
