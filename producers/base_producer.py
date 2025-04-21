import asyncio
import json
import logging
import aio_pika
from interfaces.IProducer import IMessageProducer
from typing import TypeVar, Generic
from models.base_message import BaseMessageModel
from config.settings import RabbitMQSettings

T = TypeVar('T', bound=BaseMessageModel)

logger = logging.getLogger(__name__)

class BaseProducer(Generic[T], IMessageProducer[T]):
    """Base implementation of IMessageProducer."""

    def __init__(
        self, 
        rabbitmq_settings: RabbitMQSettings,
        interval: float = 1.0,
    ):
        self.settings = rabbitmq_settings
        self.interval = interval

        self.connection = None
        self.channel = None
        self.exchange = None
        self.stopping = False
    
    async def connect(self) -> None:
        try:
            self.connection = await aio_pika.connect_robust(
                host=self.settings.host,
                port=self.settings.port,
                login=self.settings.username,
                password=self.settings.password,
            )
            
            self.channel = await self.connection.channel()
            
            self.exchange = await self.channel.declare_exchange(
                self.settings.exchange, 
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
            
            # Объявляем очередь
            queue = await self.channel.declare_queue(
                self.settings.queue,
                durable=True,
            )
            
            await queue.bind(
                exchange=self.exchange,
                routing_key=self.settings.routing_key,
            )
            
            logger.info(f"Connected to RabbitMQ at {self.settings.host}:{self.settings.port}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    async def generate_message(self) -> T:
        raise NotImplementedError()
    
    async def publish(self, message: T) -> None:
        if not self.exchange:
            logger.warning("Not connected to RabbitMQ. Attempting to connect...")
            await self.connect()
        
        try:

            message_obj = aio_pika.Message(
                body=message.to_bytes(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
            )
            
            await self.exchange.publish(
                message=message_obj,
                routing_key=self.settings.routing_key,
            )
            
            logger.debug(f"Published message: {message}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            self.exchange = None
            raise
    
    async def run(self) -> None:
        await self.connect()
        
        while not self.stopping:
            try:
                message = await self.generate_message()
                await self.publish(message)
                logger.info(f"Published message: {message}")
                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                logger.info("Producer task cancelled")
                break
            except Exception as e:
                logger.error(f"Error in producer loop: {e}")
                await asyncio.sleep(1)
    
    async def stop(self) -> None:
        self.stopping = True
        
        if self.connection:
            await self.connection.close()
            logger.info("RabbitMQ connection closed")