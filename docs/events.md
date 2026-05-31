# Events

`drawcal` supports a structured event format and also keeps the original legacy
format for backward compatibility.

## Structured Format

Structured events are objects:

```json
[
  {
    "start_date": "3/1/2025",
    "end_date": "3/5/2025",
    "style": "rounded",
    "color": "#123456",
    "markers": ["3/5/2025"]
  }
]
```

Rules:

- `start_date` and `end_date` are inclusive
- both dates must be present together when using a range event
- `end_date` must not be earlier than `start_date`
- `markers` must be inside the event range when a range is present

Structured events are explicit. They do not create an automatic checkout day.

Example structured render:

![Rounded Event](images/rounded.png)

## Marker-Only Events

You can also draw markers without a date span:

```json
[
  {
    "markers": ["3/5/2025", "3/18/2025"]
  }
]
```

This is useful for simple calendar annotations where you do not want a filled
range.

Example marker-only render:

![Markers Only](images/markers-only.png)

## Legacy Compatibility Format

Legacy events are lists of consecutive date strings:

```json
[
  ["3/1/2025", "3/2/2025", "3/3/2025"]
]
```

Rules:

- dates must use `M/D/YYYY`
- dates must be strictly increasing
- dates must be consecutive with no gaps

Legacy events preserve the original drawcal behavior, including the implicit
checkout marker on the day after the final date.
