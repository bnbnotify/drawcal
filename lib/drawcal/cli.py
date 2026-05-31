#!/usr/bin/env python
#
# Copyright (c) 2022-2026, Bnbnotify
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
Contains command line wrapper functions and classes.
"""

import sys
from datetime import datetime, timedelta

from drawcal import __prog__, __version__
from drawcal.events import get_events, read_events

d = datetime.today()
today_str = f"{d.month}/{d.day}/{d.year}"
today = datetime.strptime(today_str, "%m/%d/%Y")
delta = timedelta(days=1)


def parse_args():
    """Parses and returns command line arguments."""
    import argparse

    parser = argparse.ArgumentParser(prog=__prog__, description=__doc__)
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"drawcal {__version__}",
    )
    parser.add_argument(
        "--events",
        metavar="EVENTSFILE",
        type=str,
        default=None,
        help="file path to json file with event data",
    )
    parser.add_argument(
        "--month",
        metavar="MONTH",
        type=int,
        default=today.month,
        help="which month to draw (defaults to current month)",
    )
    parser.add_argument(
        "--year",
        metavar="YEAR",
        type=int,
        default=today.year,
        help="which year to draw (defaults to current year)",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        metavar="OUTFILE",
        type=str,
        default="drawcal.png",
        help="output file path",
    )

    args = parser.parse_args()
    return args


def main():
    """Main event loop."""
    import envstack

    envstack.init(__prog__)

    args = parse_args()

    try:
        if args.events:
            events = read_events(args.events)
        else:
            events = get_events(args.month, args.year)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    from drawcal.drawlib import draw_calendar

    try:
        draw_calendar(
            month=args.month,
            year=args.year,
            events=events,
            outfile=args.outfile,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
