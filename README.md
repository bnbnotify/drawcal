drawcal
=======

Python library for drawing simple monthly calendar images with events.

<img src="drawcal.png" alt="drwacal clendar image" />

## Installation

Install from PyPI:

```bash
$ pip install -U drawcal
```

## Quickstart

Generate a calendar image for a given events file:

```bash
$ drawcal --events events.json --month 3 --year 2025
```

Python:

```python
>>> from drawcal import draw_calendar
>>> draw_calendar(month, year, events=events, outfile=outfile)
```

## Events format

`drawcal` uses a structured event object format:

```json
[
  {
    "start_date": "3/1/2025",
    "end_date": "3/3/2025",
    "color": "#ee2233",
    "style": "rounded",
    "markers": ["3/3/2025"]
  },
  {
    "start_date": "3/14/2025",
    "end_date": "3/15/2025",
    "style": "filled",
    "markers": ["3/14/2025", "3/15/2025"]
  }
]
```

Supported `style` values are `filled`, `rounded`, and `diagonal`. Use
`markers` to draw green marker indicators on specific dates within the event
range, or use marker-only events when you only want calendar annotations.

Legacy list-based events are still supported for backward compatibility and are
documented in [docs/events.md](docs/events.md).

## Documentation

Additional docs:

- [docs/README.md](docs/README.md)
- [docs/events.md](docs/events.md)
- [docs/rendering.md](docs/rendering.md)
- [docs/customization.md](docs/customization.md)
- [docs/python-api.md](docs/python-api.md)
