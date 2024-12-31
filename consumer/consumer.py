from kafka import KafkaConsumer
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Start consumer")

consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers='kafka:9093', 
    auto_offset_reset='latest',  
    enable_auto_commit=True,
    group_id='consumer'  
)

GREEN = "\033[92m"
RESET = "\033[0m"

try:
    logger.info("Waiting for messages...")
    while True:
        # Получаем сообщения с таймаутом в 1 секунду
        messages = consumer.poll(timeout_ms=100000)
        for topic_partition, message_list in messages.items():
            for message in message_list:
                logger.info(f'{GREEN}RX: {message.value.decode("utf-8")}{RESET}')
except KeyboardInterrupt:
    logger.info("Consumer stopped by user.")
except Exception as e:
    logger.error(f"An error occurred: {e}")
finally:
    consumer.close()
    logger.info("Consumer has been closed.")



