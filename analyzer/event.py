from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    """
    Normalized event representation used across the system.
    """

    timestamp: datetime
    host: str
    service: str
    pid: Optional[int]
    event_type: str
    message: str
    source_ip: Optional[str] = None
    severity: Optional[str] = None
