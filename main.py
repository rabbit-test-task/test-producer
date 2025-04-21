import asyncio
import logging
from config.settings import settings
from utils.logging_setup import configure_logging
from producers.datetime_producer import DateTimeProducer
from producers.value_producer import ValueProducer

logger = logging.getLogger(__name__)

class MessageProducerApp:
    """Main application"""
    
    def __init__(self):
        configure_logging(settings.logging)
        
        self.producers = []
        self._init_producers()
    
    def _init_producers(self) -> None:
        """Initialize producers with provided settings"""

        datetime_producer = DateTimeProducer(
            rabbitmq_settings=settings.rabbitmq,
            interval=settings.producers.datetime_interval,
        )
        self.producers.append(datetime_producer)
        
        value_producer = ValueProducer(
            rabbitmq_settings=settings.rabbitmq,
            interval=settings.producers.value_interval,
        )
        self.producers.append(value_producer)
        logger.info("Producers initialized..")
    
    async def run(self) -> None:
        """Start all producers"""

        if not self.producers:
            logger.error("Producers not found, exiting..")
            return
        
        self.producer_tasks = [asyncio.create_task(producer.run()) for producer in self.producers]

    async def stop(self) -> None:
        """Stop all producers"""

        logger.info("Stopping all producers...")
        for task in self.producer_tasks:
            task.cancel()
        await asyncio.gather(*self.producer_tasks, return_exceptions=True)
        logger.info("All producers stopped..")

async def main() -> None:
    app = MessageProducerApp()
    
    logger.info("Starting app..")
    await app.run()
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.warning('Application shutdown..')
        await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass