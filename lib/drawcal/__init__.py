#!/usr/bin/env python

__doc__ = """
Draws calendars and events.
"""

__prog__ = "drawcal"
__version__ = "0.5.1"
__author__ = "ryan@rsg.io"

__todo__ = """
- support json file with list of event dicts with start/end dates
"""

import os

LIBDIR = os.path.dirname(os.path.abspath(__file__))
ARIAL_TTF_FILE = os.path.join(LIBDIR, "arial.ttf")
