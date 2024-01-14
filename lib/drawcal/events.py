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


# TODO: move these test events to separate json files in a tests folder
def test_events():
    """Returns a list of test events."""

    # events = []
    # events = [['2/1/2022', '2/2/2022'], ['2/10/2022', '2/11/2022'], ['2/16/2022', '2/17/2022', '2/18/2022', '2/19/2022', '2/20/2022', '2/21/2022'], ['2/23/2022', '2/24/2022']]
    # events = [['1/28/2022', '1/29/2022', '1/30/2022', '1/31/2022'], ['2/1/2022', '2/2/2022', '2/3/2022', '2/4/2022', '2/5/2022'], ['2/7/2022', '2/8/2022', '2/9/2022', '2/10/2022'], ['2/13/2022', '2/14/2022', '2/15/2022', '2/16/2022'], ['2/24/2022', '2/25/2022'], ['2/28/2022', '3/1/2022']]
    # events = [['2/1/2022', '2/2/2022', '2/3/2022', '2/4/2022'], ['2/8/2022', '2/9/2022'], ['2/10/2022', '2/11/2022'], ['2/14/2022', '2/15/2022', '2/16/2022', '2/17/2022', '2/18/2022'], ['2/24/2022', '2/25/2022', '2/26/2022']]
    # events = [['2/22/2022','2/23/2022','2/24/2022'], ['2/25/2022','2/26/2022','2/27/2022']]
    # events = [['2/1/2022', '2/2/2022', '2/3/2022', '2/4/2022', '2/5/2022'], ['2/13/2022', '2/14/2022', '2/15/2022', '2/16/2022'], ['2/19/2022', '2/20/2022', '2/21/2022', '2/22/2022', '2/23/2022', '2/24/2022']]
    # events = [['3/22/2022', '3/23/2022', '3/24/2022'], ['3/25/2022', '3/26/2022', '3/27/2022']]
    # events = [['1/1/2022', '1/2/2022', '1/3/2022'], ['1/12/2022', '1/13/2022', '1/14/2022', '1/15/2022'], ['1/24/2022', '1/25/2022']]
    # events = [['2/1/2022', '2/2/2022', '2/3/2022', '2/4/2022', '2/5/2022'], ['2/12/2022', '2/13/2022', '2/14/2022', '2/15/2022', '2/16/2022', '2/17/2022'], ['2/24/2022', '2/25/2022', '2/26/2022']]

    # contains a fake date: 2/29/2022
    # events = [['2/1/2022', '2/2/2022'], ['2/27/2022', '2/28/2022', '2/29/2022']]

    # contains conflicting events
    # events = [['3/1/2022', '3/2/2022', '3/3/2022'], ['3/2/2022', '3/3/2022', '3/4/2022']]

    # issue no. 1
    # events = [['5/29/2022', '5/30/2022', '5/31/2022'], ['6/3/2022', '6/4/2022']]

    # gaps in events
    events = [["6/3/2022", "6/4/2022", "6/5/2022", "6/6/2022", "6/7/2022"]]

    return events
