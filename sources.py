import asyncio
from aiokafka import AIOKafkaConsumer

queue: asyncio.Queue = asyncio.Queue()
async def kafka_handler(kafka_address):
    consumer = AIOKafkaConsumer(
        "test-topic",
        bootstrap_servers=kafka_address,
        group_id="my_group"
    )
    await consumer.start()
    try:
        async for message in consumer:
            await queue.put(message.value)

    finally:
        await consumer.stop()


def start_stream(kafka_address):
    asyncio.create_task(kafka_handler(kafka_address))
    return queue
