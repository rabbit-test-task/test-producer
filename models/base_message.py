import json
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Dict, Any

class BaseMessageModel(BaseModel, ABC):
    """Base class for all message models"""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dict"""
        pass
    
    def to_json(self) -> str:
        """Convert model to json string"""
        return json.dumps(self.to_dict())
    
    def to_bytes(self) -> bytes:
        """Convert model to bytes"""
        return self.to_json().encode('utf-8')