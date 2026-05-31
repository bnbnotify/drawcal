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

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional

DATE_FORMAT = "%m/%d/%Y"
DEFAULT_STYLE = "rounded"
VALID_STYLES = {"filled", "rounded", "diagonal"}
_DAY = timedelta(days=1)


def parse_date(value: str, field_name: str) -> datetime:
    """Parse an event date string."""

    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string in M/D/YYYY format")
    try:
        return datetime.strptime(value, DATE_FORMAT)
    except ValueError as exc:
        raise ValueError(f"invalid {field_name}: {value}") from exc


def format_date(value: datetime) -> str:
    """Return a drawcal date string without zero padding."""

    return f"{value.month}/{value.day}/{value.year}"


@dataclass(frozen=True)
class Event:
    start_date: datetime
    end_date: datetime
    color: Optional[str] = None
    style: str = DEFAULT_STYLE
    markers: Optional[List[datetime]] = None
    legacy: bool = False

    def validate(self) -> "Event":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        if self.style not in VALID_STYLES:
            raise ValueError(f"style must be one of: {', '.join(sorted(VALID_STYLES))}")
        if self.color is not None and not isinstance(self.color, str):
            raise ValueError("color must be a string when provided")
        if self.markers is not None:
            if not isinstance(self.markers, list):
                raise ValueError("markers must be a list of date strings")
            for marker in self.markers:
                if marker < self.start_date or marker > self.end_date:
                    raise ValueError("markers must fall within the event date range")
        return self

    @property
    def dates(self) -> List[str]:
        dates = []
        current = self.start_date
        while current <= self.end_date:
            dates.append(format_date(current))
            current += _DAY
        return dates

    @property
    def start_date_str(self) -> str:
        return format_date(self.start_date)

    @property
    def end_date_str(self) -> str:
        return format_date(self.end_date)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "start_date": self.start_date_str,
            "end_date": self.end_date_str,
        }
        if self.color is not None:
            data["color"] = self.color
        if self.style != DEFAULT_STYLE:
            data["style"] = self.style
        if self.markers:
            data["markers"] = [format_date(marker) for marker in self.markers]
        return data


def _event_from_legacy_dates(value: List[str]) -> Event:
    if not value:
        raise ValueError("events may not be empty")

    parsed_days = [parse_date(day, "event date") for day in value]

    for previous, current in zip(parsed_days, parsed_days[1:]):
        if current <= previous:
            raise ValueError("event dates must be in strictly increasing order")
        if current - previous != _DAY:
            raise ValueError("event dates must be consecutive with no gaps")

    return Event(
        start_date=parsed_days[0],
        end_date=parsed_days[-1],
        legacy=True,
    ).validate()


def _event_from_mapping(value: Dict[str, Any]) -> Event:
    unknown_keys = set(value) - {"start_date", "end_date", "color", "style", "markers"}
    if unknown_keys:
        keys = ", ".join(sorted(unknown_keys))
        raise ValueError(f"unsupported event field(s): {keys}")

    start_date = parse_date(value.get("start_date"), "start_date")
    end_date = parse_date(value.get("end_date"), "end_date")
    color = value.get("color")
    style = value.get("style", DEFAULT_STYLE)
    markers = value.get("markers")
    if markers is not None:
        if not isinstance(markers, list):
            raise ValueError("markers must be a list of date strings")
        markers = [parse_date(marker, "marker") for marker in markers]

    return Event(
        start_date=start_date,
        end_date=end_date,
        color=color,
        style=style,
        markers=markers,
    ).validate()


def normalize_event(value: Any) -> Event:
    """Convert supported user payloads into a normalized Event."""

    if isinstance(value, Event):
        return value.validate()
    if isinstance(value, list):
        return _event_from_legacy_dates(value)
    if isinstance(value, dict):
        return _event_from_mapping(value)
    raise ValueError("each event must be a legacy date list or an event dict")


def normalize_events(events: Iterable[Any]) -> List[Event]:
    """Normalize a list of event payloads."""

    if not isinstance(events, list):
        raise ValueError("events must be a list")
    return [normalize_event(event) for event in events]
