from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RealtimeContext:
    request_timestamp: Optional[datetime] = None
