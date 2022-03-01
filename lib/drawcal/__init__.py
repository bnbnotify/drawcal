#!/usr/bin/env python

__doc__ = """
drawcal python library for drawing calendars with events.
"""

__prog__ = "drawcal"
__version__ = "0.4.0"
__author__ = "ryan@rsg.io"

from .drawlib import draw_calendar
from .events import get_events, test_events
