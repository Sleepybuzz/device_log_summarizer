"""Section 3: bar chart of average temperature per device (reads summarize.py's JSON)."""
import argparse
import json
import sys

import matplotlib
matplotlib.use("Agg")  # render to file; works without a display
import matplotlib.pyplot as plt


def load_stats(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def make_chart(stats, out_path, threshold=80.0):
    devices = list(stats)
    temps = [stats[d]["avg_temperature"] for d in devices]

    fig, ax = plt.subplots(figsize=(max(6, len(devices) * 1.2), 5))
    bars = ax.bar(devices, temps, color="#3b7dd8", edgecolor="black")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.axhline(threshold, color="red", linestyle="--", linewidth=1,
               label=f"Filter threshold ({threshold:g}°C)")

    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature (°C)")
    ax.set_ylim(0, max(max(temps), threshold) * 1.15)
    ax.legend(loc="upper left")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Plot average temperature per device.")
    parser.add_argument("json_path", nargs="?", default="output.json")
    parser.add_argument("-o", "--output", default="chart.png")
    parser.add_argument("--threshold", type=float, default=80.0)
    args = parser.parse_args(argv)

    try:
        stats = load_stats(args.json_path)
    except FileNotFoundError:
        print(f"Error: file not found: {args.json_path} (run summarize.py first)", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {args.json_path}: {exc}", file=sys.stderr)
        return 1
    if not stats:
        print("Error: no devices in the JSON file; nothing to plot.", file=sys.stderr)
        return 1

    make_chart(stats, args.output, args.threshold)
    print(f"Saved chart to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
