"""Section 2: Device Log Summarizer CLI.

Usage:
    python summarize.py device_telemetry.csv -o output.json --max-avg-temp 80
"""
import argparse
import csv
import json
import math
import sys
from collections import defaultdict

VALID_STATUSES = {"ACTIVE", "WARNING", "ERROR"}
REQUIRED_COLUMNS = {"device_id", "status", "temperature"}


def load_data(path):
    """Read the CSV and return (valid_rows, skipped_count).

    Rows with a missing device_id, invalid status, or non-numeric / non-finite
    temperature are skipped and counted rather than crashing the program.
    """
    rows, skipped = [], 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV is missing required column(s): {', '.join(sorted(missing))}")
        for row in reader:
            device = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            try:
                temp = float((row.get("temperature") or "").strip())
            except ValueError:
                temp = math.nan
            if not device or status not in VALID_STATUSES or not math.isfinite(temp):
                skipped += 1
                continue
            rows.append({"device_id": device, "status": status, "temperature": temp})
    return rows, skipped


def aggregate(rows):
    """Group rows by device_id -> {device: {total_records, avg_temperature, error_count}}."""
    groups = defaultdict(list)
    for r in rows:
        groups[r["device_id"]].append(r)
    result = {}
    for device, items in sorted(groups.items()):
        temps = [i["temperature"] for i in items]
        result[device] = {
            "total_records": len(items),
            "avg_temperature": round(sum(temps) / len(temps), 2),
            "error_count": sum(1 for i in items if i["status"] == "ERROR"),
        }
    return result


def filter_devices(stats, max_avg_temp=80.0):
    """Keep only devices whose average temperature is <= max_avg_temp."""
    return {d: s for d, s in stats.items() if s["avg_temperature"] <= max_avg_temp}


def export_json(stats, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def print_table(stats):
    if not stats:
        print("No devices to display.")
        return
    header = f"{'Device':<12}{'Records':>9}{'Avg Temp':>11}{'Errors':>8}"
    print(header)
    print("-" * len(header))
    for device, s in stats.items():
        print(f"{device:<12}{s['total_records']:>9}{s['avg_temperature']:>11.2f}{s['error_count']:>8}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarize device telemetry from a CSV file.")
    parser.add_argument("csv_path", help="Path to device_telemetry.csv")
    parser.add_argument("-o", "--output", default="output.json", help="JSON output path")
    parser.add_argument("--max-avg-temp", type=float, default=80.0,
                        help="Drop devices with average temperature above this (default 80.0)")
    args = parser.parse_args(argv)

    try:
        rows, skipped = load_data(args.csv_path)
    except FileNotFoundError:
        print(f"Error: file not found: {args.csv_path}", file=sys.stderr)
        return 1
    except (ValueError, OSError, csv.Error) as exc:
        print(f"Error: could not read {args.csv_path}: {exc}", file=sys.stderr)
        return 1

    if skipped:
        print(f"Warning: skipped {skipped} invalid row(s).", file=sys.stderr)
    if not rows:
        print("Error: no valid rows found in the CSV.", file=sys.stderr)
        return 1

    stats = aggregate(rows)
    kept = filter_devices(stats, args.max_avg_temp)
    dropped = sorted(set(stats) - set(kept))
    if dropped:
        print(f"Filtered out (avg temp > {args.max_avg_temp}): {', '.join(dropped)}\n")

    export_json(kept, args.output)
    print_table(kept)
    print(f"\nSaved results to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
