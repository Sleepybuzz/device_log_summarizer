"""Run with: python -m unittest test_cleaner  (or pytest)"""
import unittest
from cleaner import clean_readings


class TestCleanReadings(unittest.TestCase):
    def test_mixed_input(self):
        raw = ["12.5", None, -1, "abc", 700, " 42 ", 0, "nan", True, 500]
        self.assertEqual(clean_readings(raw), [12.5, 500.0, 42.0, 0.0, 500.0])

    def test_empty_and_none(self):
        self.assertEqual(clean_readings([]), [])
        self.assertEqual(clean_readings(None), [])

    def test_all_invalid(self):
        self.assertEqual(clean_readings([None, "x", -5, "-0.1", [], {}]), [])


if __name__ == "__main__":
    unittest.main()
