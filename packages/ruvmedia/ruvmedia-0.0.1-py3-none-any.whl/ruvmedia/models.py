from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Media:
    """Object information for a station from the Radio Browser."""

    name: str
    identifier: str
    url: str
