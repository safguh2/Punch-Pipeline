from aiokafka import AIOKafkaConsumer
import asyncio


async def create_kafka_handler(kafka_address, queue: asyncio.Queue, interval: int = 60):
    created: bool = False

    while not created:
        try:
            await kafka_handler(kafka_address, queue)
            created = True

        except Exception as e:
            print(f"couldn't connect to kafka service, error: {str(e)}")
            await asyncio.sleep(interval)


async def kafka_handler(kafka_address,queue: asyncio.Queue):
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
