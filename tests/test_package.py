import unittest

import drawcal


class PackageImportTests(unittest.TestCase):
    def test_package_metadata_is_importable_without_renderer(self):
        self.assertEqual(drawcal.__prog__, "drawcal")
        self.assertRegex(drawcal.__version__, r"^\d+\.\d+\.\d+$")

    def test_draw_calendar_symbol_is_exposed(self):
        self.assertTrue(callable(drawcal.draw_calendar))
