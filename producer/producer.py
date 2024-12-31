from datetime import datetime
from kafka import KafkaProducer
import time

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Start producer")

producer = KafkaProducer(bootstrap_servers='kafka:9093')  # Используйте внутренний адрес

RED = "\033[91m"
RESET = "\033[0m"

try:
    logger.info("Producer is starting...")
    
    while True:
        message = f'Message sent: {datetime.now()}'
        producer.send('test-topic', value=message.encode('utf-8'))
        logger.info(f'{RED}TX: {message}{RESET}')
        time.sleep(0.1)  

except Exception as e:
    logger.error(f"An error occurred: {e}")

finally:
    producer.close()
    logger.info("Producer has been closed.")