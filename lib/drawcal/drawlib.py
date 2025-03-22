#!/usr/bin/env python
#
# Copyright (c) 2023-2025, Ryan Galloway (ryan@rsgalloway.com)
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
Contains calendar drawing classes and functions.
"""

import calendar
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw

from drawcal import config

# set some global date values
_d = datetime.today()
today_str = f"{_d.month}/{_d.day}/{_d.year}"
today = datetime.strptime(today_str, "%m/%d/%Y")
delta = timedelta(days=1)


# global color values
class colors:
    background = "#ffffff"  # calendar/cell background
    border = "#f9f9f9"  # calendar border
    border_fill = "#aeaeae"  # border between rows
    cell_border = "#ee4545"  # cell border color
    checkin_text = "#212121"  # checkin text color
    checkout_text = "#252a25"  # checkout text color
    conflict = "#ff9999"  # date conflicts / double events
    conflict_border = "#ffaaaa"  # date conflict border color
    highlight = "#11ee33"  # today and checkout date highlight color
    highlight_fill = "#33ff55"  # today and checkout date highlight color
    occupied = "#ee2233"  # busy/occupied date cell color
    occupied_text = "#e9e9e9"  # busy/occupied date text color
    other = "#dededf"  # dates outside current month
    past = "#858588"  # dates in the past
    past_text = "#aaaaad"  # past date text color
    past_border = "#959598"  # pdate date border color
    text = "#787878"  # default cell text color
    title_text = "#101010"  # month/year text color


def draw_calendar(
    month=today.month,
    year=today.year,
    events=None,
    do_highlights=True,
    show_today=False,
    outfile="output.png",
):
    """
    Draws a calendar as an output png filepath. Returns a data dict of checkin,
    checkout, occupied and conflict dates.

    Output:

        {
            "checkins": sorted(list(checkin_dates)),
            "checkouts": sorted(list(checkout_dates)),
            "conflicts": sorted(list(conflict_dates)),
            "occupied": sorted(list(occupied_dates)),
            "outfile": outfile
        }

    :param month: month to draw.
    :param year: year to draw.
    :param events:
    :param do_highlights: draw circles on check out events.
    :param show_today: draw square around current date.
    :param outfile: output file path to save image.

    :returns: dictionary containing grouped events and outfile
    """

    # set some initial values
    width = 200
    height = 200
    pad = 20

    # make sure events is a list
    if events == None:
        events = []

    # categorize and track dates
    conflict_dates = set()
    checkin_dates = set()
    checkout_dates = set()
    occupied_dates = set()

    # TODO: switch to a method that is already using list of lists
    textcal = calendar.TextCalendar(calendar.SUNDAY)
    cal = textcal.formatmonth(year, month)
    rows = cal.split("\n")

    # header is the month year string
    header = rows.pop(0).strip()

    # adjust the height based on how many rows in the calendar
    num_rows = len(rows)
    if num_rows == 8:
        height = 225

    img = Image.new("RGBA", (width, height), colors.background)
    draw = ImageDraw.Draw(img)

    # draw the month and year
    font = ImageFont.truetype(config.ARIAL_TTF_FILE, size=15)
    header_w, header_h = draw.textsize(header, font=font)
    draw.text(
        ((width - header_w) / 2, pad / 2), header, fill=colors.title_text, font=font
    )

    # iterate over the calendar rows
    for i, row in enumerate(rows, 1):
        _h = int(height / num_rows)
        cols = row.split()

        # there are 7 days in a week...
        while len(cols) < 7:
            if i < len(rows) - 1:
                cols.insert(0, "")
            else:
                cols.append("")

        # set initial cell x,y coordinates
        y_offset = 0
        x_offset = 2
        if i > 1:
            y_offset = 12
        if i == 1:
            x_offset = 8
        x1 = pad / 2
        x2 = width - pad / 2
        y1 = _h * i + (pad / 2) - (y_offset + 2)
        y2 = y1

        # draw horizontal lines between rows
        if i < len(rows):
            draw.line((x1 + 2, y1, x2 - 3, y2), width=1, fill=colors.border_fill)

        for j, col in enumerate(cols, 0):
            _w = int(width / 8.0)

            # reduce the pad between day of week and numbers
            y_offset = 0
            x_offset = 2
            if i > 1:
                y_offset = 12
            if i == 1:
                x_offset = 8

            x1 = _w * j + pad / 2 + x_offset
            y1 = _h * i + (pad / 2) - y_offset

            # begin draw events
            text_color = colors.checkin_text
            event_color = colors.occupied
            checkin = False
            checkout = False
            occupied = False
            past_date = False
            conflict = False
            curr_day = None
            curr_date = None

            s = 0
            e = 25
            offset = 12
            dow = -1

            # dates outside this calendar's month
            if col == "":
                event_color = colors.other
                draw.line(
                    (x1 + s, y1 + offset, x1 + e - 1, y1 + offset),
                    width=27,
                    fill=event_color,
                )

            if i > 1 and col:
                dow = int(col.strip())
                curr_day = f"{month}/{dow}/{year}"
                curr_date = datetime.strptime(curr_day, "%m/%d/%Y")

            if (i > 1 and col) and (curr_date < today):
                past_date = True

            # iterate over calendar events (date format: mm/dd/yyyy)
            for event in events:
                if not event:
                    continue

                # change event color of past dates
                if past_date:
                    event_color = colors.past

                first_day = event[0]
                last_day = event[-1]

                try:
                    checkout_date = datetime.strptime(last_day, "%m/%d/%Y") + delta
                    checkout_day = f"{checkout_date.month}/{checkout_date.day}/{checkout_date.year}"
                except ValueError:
                    print("invalid date!", event)
                    continue

                # handle each day in event
                if first_day == col:
                    s = 0
                if last_day == col:
                    e = 22

                # check-in
                if first_day == curr_day:
                    checkin = True
                    text_color = colors.checkin_text
                    if today_str == curr_day:
                        event_color = colors.occupied

                    if (
                        curr_day in occupied_dates or curr_day in checkin_dates
                    ) and not past_date:
                        conflict = True
                        conflict_dates.add(curr_day)
                        event_color = colors.conflict

                    draw.pieslice(
                        (x1 + 13, y1 - 1, x1 + 39, y1 + 25), 90, 270, fill=event_color
                    )

                    # track checkin nights
                    checkin_dates.add(curr_day)

                # check-out
                elif curr_day == checkout_day:
                    checkout = True
                    text_color = colors.border
                    if today_str == checkout_day:
                        event_color = colors.past

                    if (
                        (curr_day in occupied_dates or curr_day in checkout_dates)
                        and not past_date
                        and curr_date != today
                    ):
                        conflict = True
                        event_color = colors.conflict

                    draw.pieslice(
                        (x1 - 13, y1 - 1, x1 + 13, y1 + 25), 270, 90, fill=event_color
                    )

                    # track checkout nights
                    checkout_dates.add(curr_day)

                # occupied
                elif curr_day in event:
                    occupied = True
                    text_color = colors.border

                    if (
                        curr_day in occupied_dates
                        or curr_day in checkin_dates
                        or curr_day in checkout_dates
                    ) and not past_date:
                        conflict = True
                        conflict_dates.add(curr_day)
                        event_color = colors.conflict

                    draw.line(
                        (x1 + s, y1 + offset, x1 + e - 1, y1 + offset),
                        width=27,
                        fill=event_color,
                    )

                    # track occupied dates
                    occupied_dates.add(curr_day)

            # draw vertical lines between days
            if i > 1:
                fill_color = colors.other
                if occupied or checkout:
                    if conflict and not checkin:
                        fill_color = colors.conflict_border
                    else:
                        fill_color = colors.cell_border
                    if past_date:
                        fill_color = colors.past_border
                draw.line((x1, y1, x1, y1 + 25), width=1, fill=fill_color)

            # end draw events

            # add a green circle on checkout dates
            if checkout and do_highlights:
                draw.ellipse(
                    (x1 + 3, y1 + 3, x1 + 22, y1 + 22),
                    fill=colors.highlight,
                    outline=colors.highlight_fill,
                )

            # draw a square if current day is today
            if show_today and (i > 1 and curr_date == today):
                draw.rectangle((x1, y1 - 1, x1 + 24, y1 + 25), outline=colors.highlight)

            # draw days of the week and date numbers
            col_font = ImageFont.truetype(config.ARIAL_TTF_FILE, size=12)
            col_w, col_h = draw.textsize(col, font=col_font)

            # set date text color
            if past_date:
                text_color = colors.past_text
            else:
                text_color = colors.text
            if checkout:
                text_color = colors.checkout_text
            elif occupied:
                text_color = colors.occupied_text

            # text position
            x2 = _w * j + 25 - int(col_w / 2.0)
            y2 = y1
            if i > 1:
                y2 = y1 + 6

            # outline text for checkin/out days
            if checkin:  # or checkout:
                draw.text((x2 + 1, y2), col, fill=colors.border, font=col_font)

            draw.text((x2, y2), col, fill=text_color, font=col_font)

    # draw borders
    draw.line((0, 0, 0, height), width=22, fill=colors.border)
    draw.line((width - 2, 0, width - 2, height), width=30, fill=colors.border)
    draw.line((0, height + 5, width, height + 5), width=20, fill=colors.border)

    # save the file
    img.save(outfile, "PNG")

    # return data
    return {
        "checkins": sorted(list(checkin_dates)),
        "checkouts": sorted(list(checkout_dates)),
        "conflicts": sorted(list(conflict_dates)),
        "occupied": sorted(list(occupied_dates)),
        "outfile": outfile,
    }


if __name__ == "__main__":
    from drawcal.events import get_events

    events = get_events()
    outfile = "/var/tmp/drawcal-test.png"
    results = draw_calendar(events=events, outfile=outfile)
    print(results)
