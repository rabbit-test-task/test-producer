import pytest
from unittest.mock import patch, AsyncMock
from producers.datetime_producer import DateTimeProducer
from models.datetime_message import DateTimeMessage

class TestDateTimeProducer:
    def test_init(self, rabbitmq_settings):
        producer = DateTimeProducer(rabbitmq_settings, interval=10.0)
        
        assert producer.settings == rabbitmq_settings
        assert producer.interval == 10.0
    
    @pytest.mark.asyncio
    async def test_generate_message(self, rabbitmq_settings):
        producer = DateTimeProducer(rabbitmq_settings)
        message = await producer.generate_message()
        
        assert isinstance(message, DateTimeMessage)
        assert hasattr(message, "datetime_now")
        assert isinstance(message.datetime_now, str)
    
    @pytest.mark.asyncio
    async def test_integration_with_base_producer(self, rabbitmq_settings):
        producer = DateTimeProducer(rabbitmq_settings)
        
        producer.connect = AsyncMock()
        producer.publish = AsyncMock()
        
        with patch('asyncio.sleep', AsyncMock()) as mock_sleep:
            async def side_effect(*args, **kwargs):
                producer.stopping = True
            
            mock_sleep.side_effect = side_effect
            
            await producer.run()
            
            producer.connect.assert_called_once()
            producer.publish.assert_called_once()
            
            publish_args = producer.publish.call_args
            assert isinstance(publish_args[0][0], DateTimeMessage)