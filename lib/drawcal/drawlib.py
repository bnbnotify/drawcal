#!/usr/bin/env python

__doc__ = """
contains calendar drawing classes and functions.
"""

import calendar
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw

d = datetime.today()
today_str = f"{d.month}/{d.day}/{d.year}"
today = datetime.strptime(today_str, "%m/%d/%Y")
delta = timedelta(days=1)


def draw_calendar(month=today.month, year=today.year, events=None,
                  do_highlights=True, outfile="output.png"):
    """draws a calendar as a png file."""

    width = 200
    height = 200
    pad = 20

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

    img = Image.new("RGBA", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # draw the month and year
    font = ImageFont.truetype("arial", size=15)
    header_w, header_h = draw.textsize(header, font=font)
    draw.text(((width-header_w)/2, pad/2), header,
        fill="#101010", font=font)

    # iterate over the calendar rows
    for i, row in enumerate(rows, 1):
        _h = int(height / num_rows)
        cols = row.split()

        # there are 7 days in a week...
        while len(cols) < 7:
            if i < len(rows)-1:
                cols.insert(0, "")
            else:
                cols.append("")

        # TODO: clean up / better var names
        foo = 0
        bar = 2
        if i > 1:
            foo = 12
        if i == 1:
            bar = 8
        x1 = pad/2
        x2 = width - pad/2
        y1 = _h*i+(pad/2)-(foo+2)
        y2 = y1

        # draw horizontal lines between rows
        if i < len(rows):
            draw.line((x1+2, y1, x2-3, y2), width=1, fill="#aeaeae")

        for j, col in enumerate(cols, 0):
            _w = int(width / 8.0)

            # reduce the pad between day of week and numbers
            foo = 0
            bar = 2
            if i > 1:
                foo = 12
            if i == 1:
                bar = 8

            x1 = _w * j + pad/2 + bar
            y1 = _h * i + (pad/2) - foo

            # begin draw events
            text_color = "#212121"
            event_color = "#ee2233"
            checkin = False
            checkout = False
            occupied = False
            past_date = False
            curr_day = None
            curr_date = None

            s = 0
            e = 25
            offset = 12
            dow = -1

            # dates outside this calendar's month
            if col == "":
                event_color = "#dededf"
                draw.line((x1+s, y1+offset, x1+e-1, y1+offset), width=27,
                    fill=event_color)

            if i>1 and col:
                dow = int(col.strip())
                curr_day = f"{month}/{dow}/{year}"
                curr_date = datetime.strptime(curr_day, "%m/%d/%Y")

            if (i>1 and col) and (curr_date < today):
                past_date = True

            # iterate over calendar events (date format: mm/dd/yyyy)
            for event in events:
                if not event:
                    continue

                if past_date:
                    event_color = "#858588"

                first_day = event[0]
                last_day = event[-1]

                try:
                    checkout_date = datetime.strptime(last_day, '%m/%d/%Y') + delta
                    checkout_day = f"{checkout_date.month}/{checkout_date.day}/{checkout_date.year}"
                except ValueError:
                    print("bad date!", event)
                    continue

                # handle each day in event
                if first_day == col:
                    s = 0
                if last_day == col:
                    e = 22

                # check-in
                if first_day == curr_day:
                    checkin = True
                    text_color = "#212121"
                    if today_str == curr_day:
                        event_color = "#ee2233"
                    draw.pieslice((x1+13,y1-1, x1+39,y1+25), 90, 270, fill=event_color)

                # check-out
                elif curr_day == checkout_day:
                    checkout = True
                    text_color = "#f9f9f9"
                    if today_str == checkout_day:
                        event_color = "#858588"
                    draw.pieslice((x1-13,y1-1, x1+13,y1+25), 270, 90, fill=event_color)

                # occupied
                elif curr_day in event:
                    occupied = True
                    text_color = "#f9f9f9"
                    draw.line((x1+s, y1+offset, x1+e-1, y1+offset), width=27,
                        fill=event_color)

            # draw vertical lines between days
            if i>1:
                fill_color = "#dededf"
                if occupied or checkout:
                    fill_color = "#ff5656"
                    if past_date:
                        fill_color = "#959598"
                draw.line((x1, y1, x1, y1+25), width=1,
                    fill=fill_color)

            # end draw events

            # highlight the checkout date
            if checkout and do_highlights:
                draw.ellipse((x1+3,y1+3, x1+22,y1+22), fill="#11ee33",
                    outline="#33ff55")

            # day=today indicator
            if i>1 and curr_date == today:
                xx, yy = 0, 24
                draw.rectangle((x1-xx, y1-2, x1+yy, y1+25), outline="#1122ff")

            # draw days of the week, and date numbers
            col_font = ImageFont.truetype("arial", size=12)
            col_w, col_h = draw.textsize(col, font=col_font)

            if past_date:
                text_color = "#aaaaad"
            else:
                text_color = "#787878"
            if checkout:
                text_color = "#252a25"
            elif occupied:
                text_color = "#e9e9e9"

            # text position
            x2 = _w * j + 25 - int(col_w/2.0)
            y2 = y1
            if i>1:
                y2 = y1+6

            # outline text for checkin/out days
            if checkin: # or checkout:
                draw.text((x2+1, y2), col, fill="#f9f9f9", font=col_font)

            draw.text((x2, y2), col, fill=text_color, font=col_font)

    # draw borders
    draw.line((0, 0, 0, height), width=22, fill="#f9f9f9")
    draw.line((width-2, 0, width-2, height), width=30, fill="#f9f9f9")
    draw.line((0, height+5, width, height+5), width=20, fill="#f9f9f9")

    # save the file
    img.save(outfile, "PNG")
