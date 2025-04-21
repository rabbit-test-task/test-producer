import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from producers.value_producer import ValueProducer
from models.value_message import ValueMessage

class TestValueProducer:

    def test_init(self, rabbitmq_settings):
        producer = ValueProducer(rabbitmq_settings, interval=5.0)
        
        assert producer.settings == rabbitmq_settings
        assert producer.interval == 5.0
        assert producer.current_id == 0
    
    @pytest.mark.asyncio
    async def test_generate_message(self, rabbitmq_settings):
        producer = ValueProducer(rabbitmq_settings)
        
        first_message = await producer.generate_message()
        assert isinstance(first_message, ValueMessage)
        assert first_message.id == 1
        assert 1 <= first_message.value <= 1000
        
        second_message = await producer.generate_message()
        assert second_message.id == 2
    
    @pytest.mark.asyncio
    async def test_auto_increment(self, rabbitmq_settings):
        producer = ValueProducer(rabbitmq_settings)
        
        ids = []
        for _ in range(5):
            message = await producer.generate_message()
            ids.append(message.id)
        
        assert ids == [1, 2, 3, 4, 5]
    
    @pytest.mark.asyncio
    async def test_integration_with_base_producer(self, rabbitmq_settings):
        producer = ValueProducer(rabbitmq_settings)
        
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
            assert isinstance(publish_args[0][0], ValueMessage)