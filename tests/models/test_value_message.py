import pytest
import json
from models.value_message import ValueMessage

class TestValueMessage:
    def test_initialization(self):
        message = ValueMessage(id=1)
        assert hasattr(message, "id")
        assert hasattr(message, "value")
        assert message.id == 1
        assert isinstance(message.value, int)
        assert 1 <= message.value <= 1000
        
        message = ValueMessage(id=5, value=500)
        assert message.id == 5
        assert message.value == 500
    
    def test_id_required(self):
        with pytest.raises(Exception):
            ValueMessage()
    
    def test_to_dict(self):
        message = ValueMessage(id=10, value=100)
        result = message.to_dict()
        
        assert isinstance(result, dict)
        assert result["id"] == 10
        assert result["value"] == 100
    
    def test_serialization(self):
        message = ValueMessage(id=10, value=100)
        json_str = message.to_json()
        
        assert isinstance(json_str, str)

        data = json.loads(json_str)
        assert data == {"id": 10, "value": 100}
        
        bytes_data = message.to_bytes()
        assert isinstance(bytes_data, bytes)

        data = json.loads(bytes_data.decode("utf-8"))
        assert data == {"id": 10, "value": 100}
    
    def test_random_value_generation(self):
        values = set()
        for _ in range(100):
            message = ValueMessage(id=1)
            values.add(message.value)
        
        assert len(values) > 1
        assert all(1 <= v <= 1000 for v in values)