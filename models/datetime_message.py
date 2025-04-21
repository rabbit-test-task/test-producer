from datetime import datetime, timezone
from pydantic import Field
from typing import Dict, Any
from models.base_message import BaseMessageModel

class DateTimeMessage(BaseMessageModel):
    """Message with current datotime"""

    datetime_now: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def to_dict(self) -> Dict[str, Any]:
        return {"datetime_now": self.datetime_now}