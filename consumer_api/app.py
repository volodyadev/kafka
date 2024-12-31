from fastapi import FastAPI, HTTPException
from kafka import KafkaConsumer
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers='kafka:9093',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='consumer_api'
)

last_message: str = ""

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Kafka consumer...")
    loop = asyncio.get_event_loop()
    loop.create_task(consume_messages())

async def consume_messages():
    global last_message
    while True:
        try:
            # Получаем сообщения с таймаутом в 1 секунду
            message_list = consumer.poll(timeout_ms=1000)
            for topic_partition, message_batch in message_list.items():
                for message in message_batch:
                    decoded_message = message.value.decode("utf-8")
                    last_message = decoded_message
            await asyncio.sleep(0.1) 
        except Exception as e:
            logger.error(f"An error occurred: {e}")


@app.get("/last_update", response_model=str)
async def get_last_message():
    if not last_message:
        raise HTTPException(status_code=404, detail="No messages found")
    return last_message

@app.on_event("shutdown")
def shutdown_event():
    consumer.close()
    logger.info("Consumer has been closed.")

