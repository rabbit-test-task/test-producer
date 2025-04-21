import pytest
import json
from models.datetime_message import DateTimeMessage
from datetime import datetime, timezone

class TestDateTimeMessage:
    def test_initialization(self):
        message = DateTimeMessage()
        assert hasattr(message, "datetime_now")
        assert isinstance(message.datetime_now, str)
        
        try:
            datetime.fromisoformat(message.datetime_now)
        except ValueError:
            pytest.fail("datetime_now is not in ISO format")
    
    def test_custom_datetime(self):
        custom_dt = "2025-04-21T12:00:00+00:00"
        message = DateTimeMessage(datetime_now=custom_dt)
        
        assert message.datetime_now == custom_dt
    
    def test_to_dict(self):
        message = DateTimeMessage(datetime_now="2025-04-21T12:00:00+00:00")
        result = message.to_dict()
        
        assert isinstance(result, dict)
        assert result["datetime_now"] == "2025-04-21T12:00:00+00:00"
    
    def test_serialization(self):
        message = DateTimeMessage(datetime_now="2025-04-21T12:00:00+00:00")
        json_str = message.to_json()
        
        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data == {"datetime_now": "2025-04-21T12:00:00+00:00"}
        
        bytes_data = message.to_bytes()
        assert isinstance(bytes_data, bytes)
        data = json.loads(bytes_data.decode("utf-8"))
        assert data == {"datetime_now": "2025-04-21T12:00:00+00:00"}