import pytest
import asyncio
import aio_pika
from unittest.mock import patch, AsyncMock
from producers.base_producer import BaseProducer
from models.base_message import BaseMessageModel

class TestMessage(BaseMessageModel):
    value: str = "test"
    
    def to_dict(self):
        return {"value": self.value}

class ConcreteProducer(BaseProducer[TestMessage]):
    async def generate_message(self) -> TestMessage:
        return TestMessage(value="generated")

class TestBaseProducer:
    def test_init(self, rabbitmq_settings):
        producer = ConcreteProducer(rabbitmq_settings, interval=2.0)
        
        assert producer.settings == rabbitmq_settings
        assert producer.interval == 2.0
        assert producer.connection is None
        assert producer.channel is None
        assert producer.exchange is None
        assert producer.stopping is False
    
    @pytest.mark.asyncio
    async def test_connect(self, rabbitmq_settings):
        producer = ConcreteProducer(rabbitmq_settings)
        
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_exchange = AsyncMock()
        mock_queue = AsyncMock()
        
        mock_channel.declare_exchange.return_value = mock_exchange
        mock_channel.declare_queue.return_value = mock_queue
        mock_connection.channel.return_value = mock_channel
        
        with patch('aio_pika.connect_robust', return_value=mock_connection) as mock_connect:
            await producer.connect()
            
            mock_connect.assert_called_once_with(
                host=rabbitmq_settings.host,
                port=rabbitmq_settings.port,
                login=rabbitmq_settings.username,
                password=rabbitmq_settings.password
            )
            
            mock_connection.channel.assert_called_once()
            mock_channel.declare_exchange.assert_called_once_with(
                rabbitmq_settings.exchange,
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )
            mock_channel.declare_queue.assert_called_once_with(
                rabbitmq_settings.queue,
                durable=True
            )
            mock_queue.bind.assert_called_once_with(
                exchange=mock_exchange,
                routing_key=rabbitmq_settings.routing_key
            )
    
    @pytest.mark.asyncio
    async def test_publish(self, rabbitmq_settings):
        producer = ConcreteProducer(rabbitmq_settings)
        message = TestMessage(value="test_publish")
        
        mock_exchange = AsyncMock()
        producer.exchange = mock_exchange
        
        await producer.publish(message)
        
        mock_exchange.publish.assert_called_once()
        
        call_args = mock_exchange.publish.call_args
        actual_message = call_args[1]['message']
        assert actual_message.body == message.to_bytes()
        assert actual_message.delivery_mode == aio_pika.DeliveryMode.PERSISTENT
        assert actual_message.content_type == "application/json"
        
        assert call_args[1]['routing_key'] == rabbitmq_settings.routing_key
    
    @pytest.mark.asyncio
    async def test_publish_when_not_connected(self, rabbitmq_settings):
        producer = ConcreteProducer(rabbitmq_settings)
        message = TestMessage(value="test_publish")
        
        producer.exchange = None
        
        producer.connect = AsyncMock()
        mock_exchange = AsyncMock()
        
        async def set_exchange(*args, **kwargs):
            producer.exchange = mock_exchange
        
        producer.connect.side_effect = set_exchange
        
        await producer.publish(message)
        
        producer.connect.assert_called_once()
        
        mock_exchange.publish.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_run(self, rabbitmq_settings):
        producer = ConcreteProducer(rabbitmq_settings)
        
        producer.connect = AsyncMock()
        producer.generate_message = AsyncMock(return_value=TestMessage(value="test"))
        producer.publish = AsyncMock()
        
        original_sleep = asyncio.sleep
        
        sleep_counter = 0
        
        async def mock_sleep(interval):
            nonlocal sleep_counter
            sleep_counter += 1
            if sleep_counter >= 2:
                producer.stopping = True
            await original_sleep(0)
        
        with patch('asyncio.sleep', side_effect=mock_sleep):
            await producer.run()
            
            producer.connect.assert_called_once()
            assert producer.generate_message.call_count >= 1
            assert producer.publish.call_count >= 1
    
    @pytest.mark.asyncio
    async def test_stop(self, rabbitmq_settings):
        producer = ConcreteProducer(rabbitmq_settings)
        
        mock_connection = AsyncMock()
        producer.connection = mock_connection
        
        await producer.stop()
        
        assert producer.stopping is True
        
        mock_connection.close.assert_called_once()