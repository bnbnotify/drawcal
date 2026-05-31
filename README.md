drawcal
=======

Python library for drawing simple monthly calendar images with events.

<img src="drawcal.png" alt="drwacal clendar image" />

## Installation

Install from PyPI:

```bash
$ pip install -U drawcal
```

Build locally:

```bash
$ python -m pip install --upgrade build
$ python -m build
```

Upload to PyPI:

```bash
$ python -m pip install --upgrade twine
$ python -m twine upload dist/*
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

`drawcal` expects a JSON file containing a list of events, where each event is a
list of dates in `M/D/YYYY` format:

```json
[
  ["3/1/2025", "3/2/2025", "3/3/2025"],
  ["3/14/2025", "3/15/2025"]
]
```
