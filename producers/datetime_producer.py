import logging
from producers.base_producer import BaseProducer
from config.settings import RabbitMQSettings
from models.datetime_message import DateTimeMessage

logger = logging.getLogger(__name__)

class DateTimeProducer(BaseProducer[DateTimeMessage]):
    """Producer for datetime messages."""

    def __init__(
        self,
        rabbitmq_settings: RabbitMQSettings,
        interval: float = 1.0,
    ):
        super().__init__(
            rabbitmq_settings=rabbitmq_settings,
            interval=interval,
        )

    async def generate_message(self) -> DateTimeMessage:
        """Generate message with the current datetime"""
        return DateTimeMessage()