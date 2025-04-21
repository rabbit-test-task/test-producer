import random
from pydantic import Field
from typing import Dict, Any
from models.base_message import BaseMessageModel

class ValueMessage(BaseMessageModel):
    """Model with id and random value"""
    id: int
    value: int = Field(default_factory=lambda: random.randint(1, 1000))
    
    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "value": self.value}