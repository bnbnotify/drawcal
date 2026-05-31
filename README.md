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

`drawcal` accepts either the legacy list-of-dates format or a richer event
object format.

Legacy format:

```json
[
  ["3/1/2025", "3/2/2025", "3/3/2025"],
  ["3/14/2025", "3/15/2025"]
]
```

Object format:

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
range. The new object schema is forward-looking; legacy date lists remain
supported for backward compatibility.
