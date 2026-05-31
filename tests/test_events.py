import json
import tempfile
import unittest
from datetime import datetime

from drawcal.events import get_events, read_events, validate_events


class ReadEventsTests(unittest.TestCase):
    def test_read_events_rejects_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = f"{tmpdir}/events.json"

            with open(path, "w", encoding="utf-8") as fp:
                fp.write("{not json}")

            with self.assertRaises(ValueError):
                read_events(path)

    def test_read_events_rejects_invalid_dates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = f"{tmpdir}/events.json"

            with open(path, "w", encoding="utf-8") as fp:
                json.dump([["2/30/2025"]], fp)

            with self.assertRaises(ValueError):
                read_events(path)

    def test_read_events_rejects_gapped_events(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = f"{tmpdir}/events.json"

            with open(path, "w", encoding="utf-8") as fp:
                json.dump([["6/3/2022", "6/6/2022", "6/7/2022"]], fp)

            with self.assertRaisesRegex(ValueError, "consecutive with no gaps"):
                read_events(path)


class GetEventsTests(unittest.TestCase):
    def test_get_events_stays_within_month(self):
        events = get_events(month=2, year=2025)

        for event in events:
            for day in event:
                parsed = datetime.strptime(day, "%m/%d/%Y")
                self.assertEqual(parsed.month, 2)
                self.assertEqual(parsed.year, 2025)
                self.assertLessEqual(parsed.day, 28)


class ValidateEventsTests(unittest.TestCase):
    def test_validate_events_rejects_gapped_direct_input(self):
        with self.assertRaisesRegex(ValueError, "consecutive with no gaps"):
            validate_events([["6/3/2022", "6/6/2022", "6/7/2022"]])
