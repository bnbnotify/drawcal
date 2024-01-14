#!/usr/bin/env python

__doc__ = """
Draws calendars and events.
"""

__prog__ = "drawcal"
__version__ = "0.5.4"
__author__ = "ryan@rsg.io"

__todo__ = """
- support json file with list of event dicts with start/end dates
"""

import os

# file paths
LIB_DIR = os.path.dirname(os.path.abspath(__file__))
ARIAL_TTF_FILE = os.path.join(LIB_DIR, "arial.ttf")
