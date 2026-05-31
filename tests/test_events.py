import json
import tempfile
import unittest
from datetime import datetime

from drawcal.events import get_events, read_events


class ReadEventsTests(unittest.TestCase):
    def test_read_events_rejects_invalid_json(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".json") as handle:
            handle.write("{not json}")
            handle.flush()

            with self.assertRaises(ValueError):
                read_events(handle.name)

    def test_read_events_rejects_invalid_dates(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".json") as handle:
            json.dump([["2/30/2025"]], handle)
            handle.flush()

            with self.assertRaises(ValueError):
                read_events(handle.name)


class GetEventsTests(unittest.TestCase):
    def test_get_events_stays_within_month(self):
        events = get_events(month=2, year=2025)

        for event in events:
            for day in event:
                parsed = datetime.strptime(day, "%m/%d/%Y")
                self.assertEqual(parsed.month, 2)
                self.assertEqual(parsed.year, 2025)
                self.assertLessEqual(parsed.day, 28)
