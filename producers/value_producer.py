import logging
from typing import Dict, Any
from config.settings import RabbitMQSettings
from producers.base_producer import BaseProducer
from models.value_message import ValueMessage

logger = logging.getLogger(__name__)

class ValueProducer(BaseProducer[ValueMessage]):
    """Producer for value messages with auto-incrementing ID."""
    
    def __init__(
        self,
        rabbitmq_settings: RabbitMQSettings,
        interval: float = 3.0,
    ):
        super().__init__(
            rabbitmq_settings=rabbitmq_settings,
            interval=interval,
        )
        self.current_id = 0
    
    async def generate_message(self) -> Dict[str, Any]:
        """Generate a value message with incrementing ID and random value."""
        self.current_id += 1
        return ValueMessage(id=self.current_id)