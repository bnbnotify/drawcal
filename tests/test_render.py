import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from PIL import Image, ImageChops, ImageColor

from drawcal.drawlib import draw_calendar
import drawcal.drawlib as drawlib


FIXTURES_DIR = Path(__file__).parent / "fixtures"
LEGACY_EXPECTED_IMAGE = FIXTURES_DIR / "march-2025-expected.png"
LEGACY_EVENTS_FILE = FIXTURES_DIR / "march-2025-events.json"
STRUCTURED_EXPECTED_IMAGE = FIXTURES_DIR / "march-2025-expected-v2.png"
STRUCTURED_EVENTS_FILE = FIXTURES_DIR / "march-2025-events-v2.json"
FIXED_TODAY = datetime.strptime("1/1/2026", "%m/%d/%Y")


class RenderTests(unittest.TestCase):
    def _assert_render_matches_fixture(self, events_file, expected_image):
        events = json.loads(events_file.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as tmpdir:
            outfile = Path(tmpdir) / "render.png"

            with mock.patch.object(drawlib, "today", FIXED_TODAY), mock.patch.object(
                drawlib, "today_str", "1/1/2026"
            ):
                draw_calendar(month=3, year=2025, events=events, outfile=str(outfile))

            with Image.open(expected_image) as expected, Image.open(outfile) as actual:
                diff = ImageChops.difference(expected, actual)
                self.assertIsNone(
                    diff.getbbox(), "rendered image does not match fixture"
                )

    def test_draw_calendar_matches_legacy_fixture(self):
        self._assert_render_matches_fixture(
            LEGACY_EVENTS_FILE,
            LEGACY_EXPECTED_IMAGE,
        )

    def test_draw_calendar_matches_structured_fixture(self):
        self._assert_render_matches_fixture(
            STRUCTURED_EVENTS_FILE,
            STRUCTURED_EXPECTED_IMAGE,
        )

    def test_draw_calendar_accepts_dict_events(self):
        draw_calendar(
            month=3,
            year=2025,
            events=[
                {
                    "start_date": "3/1/2025",
                    "end_date": "3/5/2025",
                    "style": "filled",
                    "markers": ["3/1/2025", "3/5/2025"],
                }
            ],
        )

    def test_dict_events_do_not_draw_implicit_checkout_day(self):
        result = draw_calendar(
            month=3,
            year=2025,
            events=[
                {
                    "start_date": "3/1/2025",
                    "end_date": "3/5/2025",
                    "style": "filled",
                }
            ],
        )

        self.assertNotIn("3/6/2025", result["checkouts"])

    def test_legacy_events_keep_implicit_checkout_day(self):
        result = draw_calendar(
            month=3,
            year=2025,
            events=[["3/1/2025", "3/2/2025", "3/3/2025", "3/4/2025", "3/5/2025"]],
        )

        self.assertIn("3/6/2025", result["checkouts"])

    def test_draw_calendar_rejects_gapped_events(self):
        with self.assertRaisesRegex(ValueError, "consecutive with no gaps"):
            draw_calendar(
                month=6,
                year=2022,
                events=[["6/3/2022", "6/6/2022", "6/7/2022"]],
            )

    def test_explicit_event_color_wins(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            outfile = Path(tmpdir) / "render.png"

            with mock.patch.object(drawlib, "today", FIXED_TODAY), mock.patch.object(
                drawlib, "today_str", "1/1/2026"
            ):
                draw_calendar(
                    month=3,
                    year=2025,
                    events=[
                        {
                            "start_date": "3/1/2025",
                            "end_date": "3/5/2025",
                            "style": "filled",
                            "color": "#123456",
                        }
                    ],
                    outfile=str(outfile),
                )

            with Image.open(outfile) as image:
                expected = ImageColor.getrgb("#123456")
                self.assertEqual(image.getpixel((163, 53))[:3], expected)
