import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class RabbitMQSettings(BaseModel):
    host: str = os.getenv("RABBITMQ_HOST", "localhost")
    port: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    username: str = os.getenv("RABBITMQ_USERNAME", "guest")
    password: str = os.getenv("RABBITMQ_PASSWORD", "guest")
    exchange: str = os.getenv("RABBITMQ_EXCHANGE", "message-exchange")
    queue: str = os.getenv("RABBITMQ_QUEUE", "message-queue")
    routing_key: str = os.getenv("RABBITMQ_ROUTING_KEY", "message-routing-key")

class ProducerSettings(BaseModel):
    datetime_interval: float = float(os.getenv("DATETIME_INTERVAL", "5.0"))
    value_interval: float = float(os.getenv("VALUE_INTERVAL", "3.0"))

class LoggingSettings(BaseModel):
    level: str = os.getenv("LOG_LEVEL", "INFO")

class Settings(BaseModel):
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    producers: ProducerSettings = ProducerSettings()
    logging: LoggingSettings = LoggingSettings()

settings = Settings()