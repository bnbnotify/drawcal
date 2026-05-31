# Python API

## Basic Usage

```python
from drawcal import draw_calendar

events = [
    {
        "start_date": "3/1/2025",
        "end_date": "3/5/2025",
        "style": "rounded",
        "markers": ["3/5/2025"],
    }
]

result = draw_calendar(month=3, year=2025, events=events, outfile="drawcal.png")
```

## Return Value

`draw_calendar()` returns a dictionary like:

```python
{
    "checkins": [...],
    "checkouts": [...],
    "conflicts": [...],
    "occupied": [...],
    "outfile": "drawcal.png",
}
```

Notes:

- `checkouts` is mainly relevant for legacy list-based events
- structured events only produce markers you explicitly request
- invalid event payloads raise `ValueError`

## Reading Events From JSON

```python
from drawcal.events import read_events

events = read_events("events.json")
```

`read_events()` validates the schema before returning data.
