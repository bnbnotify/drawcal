#!/usr/bin/env python
#
# Copyright (c) 2022-2025, Ryan Galloway (ryan@rsgalloway.com)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  - Neither the name of the software nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

__doc__ = """
Contains event functions and classes.
"""

import json
from datetime import datetime, timedelta

d = datetime.today()
today_str = f"{d.month}/{d.day}/{d.year}"
today = datetime.strptime(today_str, "%m/%d/%Y")
delta = timedelta(days=1)


def get_events(month=today.month, year=today.year):
    """Returns a list of randomly generated events."""
    from random import randint

    events = []
    num_events = randint(2, 8)
    i = 1

    for _ in range(2, num_events):
        event = []
        for dd in range(i, randint(i + 2, i + randint(3, 8))):
            event.append(f"{month}/{dd}/{year}")
            i += 1
            if i >= 31:
                break
        if i >= 31:
            break
        i += randint(1, 10)
        if event:
            events.append(event)

        # every 1 in 25 times add a duplicate event
        if (randint(1, 100) % 25) == 0:
            events.append(event)

    return events


# TODO: update read_events to support export from bnbnotify
def read_events(filepath):
    """Returns JSON serialized events from a given filepath."""

    events = []

    try:
        fp = open(filepath)
        events = json.load(fp)
        fp.close()
    except Exception as e:
        print(e)

    return events
