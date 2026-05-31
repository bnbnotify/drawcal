import json
import tempfile
import unittest
from datetime import datetime

from drawcal.models import Event, normalize_events
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

    def test_read_events_accepts_dict_events(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = f"{tmpdir}/events.json"

            with open(path, "w", encoding="utf-8") as fp:
                json.dump(
                    [
                        {
                            "start_date": "3/1/2025",
                            "end_date": "3/3/2025",
                            "color": "#ee2233",
                            "style": "rounded",
                            "markers": ["3/3/2025"],
                        }
                    ],
                    fp,
                )

            self.assertEqual(
                read_events(path)[0]["start_date"],
                "3/1/2025",
            )


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

    def test_validate_events_accepts_dict_events(self):
        validate_events(
            [
                {
                    "start_date": "3/14/2022",
                    "end_date": "3/17/2022",
                    "style": "filled",
                    "markers": ["3/14/2022", "3/17/2022"],
                }
            ]
        )

    def test_validate_events_accepts_marker_only_events(self):
        validate_events([{"markers": ["3/14/2022", "3/17/2022"]}])

    def test_validate_events_rejects_non_datetime_markers_on_event_instance(self):
        with self.assertRaisesRegex(ValueError, "markers must be datetime values"):
            Event(markers=["3/14/2022"]).validate()


class NormalizeEventsTests(unittest.TestCase):
    def test_normalize_events_supports_legacy_lists(self):
        normalized = normalize_events([["3/14/2022", "3/15/2022", "3/16/2022"]])

        self.assertEqual(
            normalized,
            [
                Event(
                    start_date=datetime(2022, 3, 14),
                    end_date=datetime(2022, 3, 16),
                    legacy=True,
                )
            ],
        )

    def test_normalize_events_supports_dict_schema(self):
        normalized = normalize_events(
            [
                {
                    "start_date": "3/14/2022",
                    "end_date": "3/17/2022",
                    "color": "#ee2233",
                    "style": "rounded",
                    "markers": ["3/16/2022"],
                }
            ]
        )

        self.assertEqual(
            normalized[0].dates, ["3/14/2022", "3/15/2022", "3/16/2022", "3/17/2022"]
        )
        self.assertEqual(normalized[0].color, "#ee2233")
        self.assertEqual(normalized[0].style, "rounded")
        self.assertEqual(normalized[0].to_dict()["markers"], ["3/16/2022"])
        self.assertFalse(normalized[0].legacy)

    def test_normalize_events_rejects_markers_outside_range(self):
        with self.assertRaisesRegex(ValueError, "within the event date range"):
            normalize_events(
                [
                    {
                        "start_date": "3/14/2022",
                        "end_date": "3/17/2022",
                        "markers": ["3/18/2022"],
                    }
                ]
            )

    def test_normalize_events_supports_marker_only_schema(self):
        normalized = normalize_events([{"markers": ["3/16/2022"]}])

        self.assertFalse(normalized[0].has_range)
        self.assertEqual(normalized[0].dates, [])
        self.assertEqual(normalized[0].to_dict()["markers"], ["3/16/2022"])
