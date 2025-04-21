from abc import ABC, abstractmethod
from typing import Any, Dict
from typing import TypeVar, Generic
from models.base_message import BaseMessageModel

T = TypeVar('T', bound=BaseMessageModel)

class IMessageProducer(Generic[T], ABC):
    """Interface for message producers."""
    
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the message broker."""
        pass
    
    @abstractmethod
    async def generate_message(self) -> T:
        """Generate a message to be published."""
        pass
    
    @abstractmethod
    async def publish(self, message: T) -> None:
        """Publish a message to the broker."""
        pass
    
    @abstractmethod
    async def run(self) -> None:
        """Run the producer continuously."""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """Stop the producer and clean up resources."""
        pass