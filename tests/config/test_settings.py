import os
from unittest.mock import patch
from config.settings import RabbitMQSettings, ProducerSettings, LoggingSettings, Settings

class TestRabbitMQSettings:

    def test_default_values(self):
        settings = RabbitMQSettings()
        assert settings.host == "localhost"
        assert settings.port == 5672
        assert settings.username == "guest"
        assert settings.password == "guest"
        assert settings.exchange == "message-exchange"
        assert settings.queue == "message-queue"
        assert settings.routing_key == "message-routing-key"
    
    def test_custom_values(self):
        settings = RabbitMQSettings(
            host="test-host",
            port=1234,
            username="test-user",
            password="test-pass",
            exchange="test-exchange",
            queue="test-queue",
            routing_key="test-key"
        )
        assert settings.host == "test-host"
        assert settings.port == 1234
        assert settings.username == "test-user"
        assert settings.password == "test-pass"
        assert settings.exchange == "test-exchange"
        assert settings.queue == "test-queue"
        assert settings.routing_key == "test-key"
    
    @patch.dict(os.environ, {
        "RABBITMQ_HOST": "env-host", 
        "RABBITMQ_PORT": "9999",
        "RABBITMQ_USERNAME": "env-user",
        "RABBITMQ_PASSWORD": "env-pass",
        "RABBITMQ_EXCHANGE": "env-exchange",
        "RABBITMQ_QUEUE": "env-queue",
        "RABBITMQ_ROUTING_KEY": "env-key"
    })
    def test_env_values(self):
        settings = RabbitMQSettings()
        
        assert settings.host == "env-host"
        assert settings.port == 9999
        assert settings.username == "env-user"
        assert settings.password == "env-pass"
        assert settings.exchange == "env-exchange"
        assert settings.queue == "env-queue"
        assert settings.routing_key == "env-key"


class TestProducerSettings:

    def test_default_values(self):
        settings = ProducerSettings()
        assert settings.datetime_interval == 5.0
        assert settings.value_interval == 3.0
    
    def test_custom_values(self):
        settings = ProducerSettings(
            datetime_interval=10.0,
            value_interval=20.0
        )
        assert settings.datetime_interval == 10.0
        assert settings.value_interval == 20.0
    
    @patch.dict(os.environ, {
        "DATETIME_INTERVAL": "15.5",
        "VALUE_INTERVAL": "7.5",
    })
    def test_env_values(self):
        settings = ProducerSettings()
        
        assert settings.datetime_interval == 15.5
        assert settings.value_interval == 7.5


class TestLogSettings:

    def test_default_values(self):
        settings = LoggingSettings()
        assert settings.level == "INFO"
    
    def test_custom_values(self):
        settings = LoggingSettings(level="DEBUG")
        assert settings.level == "DEBUG"
    
    @patch.dict(os.environ, {"LOG_LEVEL": "ERROR"})
    def test_env_values(self):
        settings = LoggingSettings()
        
        assert settings.level == "ERROR"


class TestSettings:
    def test_default_values(self):
        settings = Settings()
        
        assert isinstance(settings.rabbitmq, RabbitMQSettings)
        assert isinstance(settings.producers, ProducerSettings)
        assert isinstance(settings.logging, LoggingSettings)