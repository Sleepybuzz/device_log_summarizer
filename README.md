# Device Log Summarizer

Requires Python 3.8+ and `matplotlib` (only for `plot.py`).

```bash
python -m unittest test_cleaner                              # Section 1 tests
python summarize.py device_telemetry.csv -o output.json     # Section 2
python plot.py output.json -o chart.png                     # Section 3
```

- `cleaner.py` / `test_cleaner.py`: sensor value cleaning function and tests.
- `summarize.py`: CSV -> per-device stats (records, mean temp, ERROR count), drops devices with avg temp > 80, writes JSON, prints a table. Invalid rows are skipped with a warning; a missing file gives a clean error.
- `plot.py`: bar chart of average temperature per device.
- `make_sample_csv.py`: generates the sample `device_telemetry.csv` (swap in the provided CSV).
- `drafts/`: the AI's first-attempt plot and its output, referenced in `PROMPT_LOG.md`.
