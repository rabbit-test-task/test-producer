import pytest
from unittest.mock import patch, MagicMock
from models.base_message import BaseMessageModel
from pydantic import Field
import json

# Test implementation
class ConcreteMessage(BaseMessageModel):
    field1: str = "test"
    field2: int = 123
    
    def to_dict(self):
        return {"field1": self.field1, "field2": self.field2}

class TestBaseMessageModel:
    def test_abstract_methods(self):
        with pytest.raises(TypeError):
            BaseMessageModel()
    
    def test_to_json(self):
        message = ConcreteMessage()
        json_str = message.to_json()
        
        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data == {"field1": "test", "field2": 123}
    
    def test_to_bytes(self):
        message = ConcreteMessage()
        bytes_data = message.to_bytes()
        
        assert isinstance(bytes_data, bytes)
        data = json.loads(bytes_data.decode('utf-8'))
        assert data == {"field1": "test", "field2": 123}
    
    def test_custom_values(self):
        message = ConcreteMessage(field1="custom", field2=456)
        
        assert message.field1 == "custom"
        assert message.field2 == 456
        assert message.to_dict() == {"field1": "custom", "field2": 456}