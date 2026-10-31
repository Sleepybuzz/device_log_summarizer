"""Section 1: clean and normalize raw sensor readings."""
import math

MAX_VALUE = 500.0


def clean_readings(values):
    """Return a cleaned list of floats from a list of mixed sensor inputs.

    Rules:
      1. Convert each element to float; drop None, unconvertible values,
         NaN/inf, booleans, and negative values (error flags).
      2. Cap any value above 500.0 to 500.0.
      3. Empty / None / non-iterable input returns [] instead of raising.
    """
    if values is None:
        return []
    try:
        iterator = iter(values)
    except TypeError:
        return []

    cleaned = []
    for item in iterator:
        if item is None or isinstance(item, bool):
            continue
        try:
            number = float(item)
        except (ValueError, TypeError):
            continue
        if not math.isfinite(number) or number < 0:
            continue
        cleaned.append(min(number, MAX_VALUE))
    return cleaned


if __name__ == "__main__":
    print(clean_readings(["12.5", None, -1, "abc", 700, "  42 ", 0]))
