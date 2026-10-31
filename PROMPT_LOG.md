# PROMPT_LOG.md

## AI usage summary
- **Section 1 (cleaner.py):** written with guidance of AI.
- **Section 2 (summarize.py):** structure and error handling drafted with an AI assistant, then run and tested by me against a CSV containing bad rows and a missing-file case.
- **Section 3 (plot.py):** AI-generated, then reviewed and fixed (details below).

## Initial prompt
> Write a Python script that loads `output.json` (a dict mapping device_id to
> `{total_records, avg_temperature, error_count}`) and uses matplotlib to create a bar
> chart comparing average temperature per device. Save it as a PNG.

## First attempt: bug / formatting mistakes
The first version (`drafts/plot_v1.py`, output in `drafts/chart_v1.png`) ran but was not usable:
- No title and no axis labels, so the chart did not say what it showed.
- No value labels on the bars, and no indication of the 80 °C filter threshold.
- Hardcoded `"output.json"` path, `plt.show()` instead of saving a file, and no handling for a missing or empty JSON file.
- No `tight_layout()` and no rotation of x-axis labels, so labels would overlap with many devices.

## Follow-up prompt used to fix it
> Update the script: add a title, x/y axis labels with units (°C), value labels above each
> bar, and a dashed red line at the 80 °C threshold. Rotate x tick labels 45° and call
> `tight_layout()` so nothing overlaps. Take the JSON path and output path as argparse
> arguments instead of hardcoding them, save to `chart.png` (use the Agg backend), and print a
> friendly error if the JSON file is missing or empty.

## Result
`plot.py` is the fixed version; I ran it and checked `chart.png` visually.
