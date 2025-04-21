import pytest
from config.settings import RabbitMQSettings

@pytest.fixture
def rabbitmq_settings():
    
    
    return RabbitMQSettings(
        host="test-host",
        port=5672,
        username="test-user",
        password="test-pass",
        exchange="test-exchange",
        queue="test-queue",
        routing_key="test-routing-key"
    )