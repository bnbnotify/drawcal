import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from PIL import Image, ImageChops

from drawcal.drawlib import draw_calendar
import drawcal.drawlib as drawlib


FIXTURES_DIR = Path(__file__).parent / "fixtures"
EXPECTED_IMAGE = FIXTURES_DIR / "march-2025-expected.png"
EVENTS_FILE = FIXTURES_DIR / "march-2025-events.json"
FIXED_TODAY = datetime.strptime("1/1/2026", "%m/%d/%Y")


class RenderTests(unittest.TestCase):
    def test_draw_calendar_matches_expected_image(self):
        events = json.loads(EVENTS_FILE.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as tmpdir:
            outfile = Path(tmpdir) / "render.png"

            with mock.patch.object(drawlib, "today", FIXED_TODAY), mock.patch.object(
                drawlib, "today_str", "1/1/2026"
            ):
                draw_calendar(month=3, year=2025, events=events, outfile=str(outfile))

            with Image.open(EXPECTED_IMAGE) as expected, Image.open(outfile) as actual:
                diff = ImageChops.difference(expected, actual)
                self.assertIsNone(
                    diff.getbbox(), "rendered image does not match fixture"
                )

    def test_draw_calendar_rejects_gapped_events(self):
        with self.assertRaisesRegex(ValueError, "consecutive with no gaps"):
            draw_calendar(
                month=6,
                year=2022,
                events=[["6/3/2022", "6/6/2022", "6/7/2022"]],
            )
