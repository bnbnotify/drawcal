import io
import tempfile
import unittest
from contextlib import redirect_stderr
from unittest import mock

from drawcal import cli


class CliTests(unittest.TestCase):
    def test_main_reports_invalid_json_cleanly(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            events_path = f"{tmpdir}/events.json"
            with open(events_path, "w", encoding="utf-8") as fp:
                fp.write("{not json}")

            stderr = io.StringIO()
            with mock.patch(
                "sys.argv", ["drawcal", "--events", events_path]
            ), mock.patch("envstack.init"), redirect_stderr(stderr):
                exit_code = cli.main()

        self.assertEqual(exit_code, 1)
        self.assertIn("Error: invalid JSON in events file", stderr.getvalue())
