import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

if not os.environ.get("PYTEST_RUNNING"):
    load_dotenv()

class RabbitMQSettings(BaseModel):
    host: str = Field(default_factory=lambda: os.getenv("RABBITMQ_HOST", "localhost"))
    port: int = Field(default_factory=lambda: int(os.getenv("RABBITMQ_PORT", "5672")))
    username: str = Field(default_factory=lambda: os.getenv("RABBITMQ_USERNAME", "guest"))
    password: str = Field(default_factory=lambda: os.getenv("RABBITMQ_PASSWORD", "guest"))
    exchange: str = Field(default_factory=lambda: os.getenv("RABBITMQ_EXCHANGE", "message-exchange"))
    queue: str = Field(default_factory=lambda: os.getenv("RABBITMQ_QUEUE", "message-queue"))
    routing_key: str = Field(default_factory=lambda: os.getenv("RABBITMQ_ROUTING_KEY", "message-routing-key"))

class ProducerSettings(BaseModel):
    datetime_interval: float = Field(
        default_factory=lambda: float(os.getenv("DATETIME_INTERVAL", "5.0"))
    )
    value_interval: float = Field(
        default_factory=lambda: float(os.getenv("VALUE_INTERVAL", "3.0"))
    )

class LoggingSettings(BaseModel):
    level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

class Settings(BaseModel):
    rabbitmq: RabbitMQSettings = Field(default_factory=RabbitMQSettings)
    producers: ProducerSettings = Field(default_factory=ProducerSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

settings = Settings()