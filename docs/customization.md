# Customization

`drawcal` currently uses module-level color defaults in
`drawcal.drawlib.colors`.

Example:

```python
from drawcal.drawlib import colors, draw_calendar

colors.background = "#f7f4ee"
colors.text = "#555555"
colors.border = "#e7dfcf"

draw_calendar(month=3, year=2025, events=events, outfile="drawcal.png")
```

Available color attributes include:

- `background`
- `border`
- `border_fill`
- `cell_border`
- `checkin_text`
- `checkout_text`
- `conflict`
- `conflict_border`
- `highlight`
- `highlight_fill`
- `occupied`
- `occupied_text`
- `other`
- `past`
- `past_text`
- `past_border`
- `text`
- `title_text`

Notes:

- this is global mutable state
- changes affect later renders in the same Python process
- this works today, but it is better thought of as an advanced usage pattern
  than a polished public theming API
