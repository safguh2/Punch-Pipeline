import asyncio
from aiokafka import AIOKafkaConsumer
import aio_pika
import DBSource

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


async def rabbitmq_handler(rabbitmq_address):
    connection = await aio_pika.connect_robust(rabbitmq_address)

    async with connection:
        channel = await connection.channel()

        mq_queue = await channel.declare_queue("test")

        async with mq_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await queue.put(message.body)


def create_db_handlers(db_list):
    for db in db_list:
        try:
            if db['type'] != 'postgres':
                print("db not supported")
            else:
                db_handler = DBSource.DatabaseSource(queue, db['dsn'])
                asyncio.create_task(db_handler.run())
        except:
            print("error in db handlers")


def start_stream(kafka_address, rabbitmq_address, external_db):
    asyncio.create_task(kafka_handler(kafka_address))
    asyncio.create_task(rabbitmq_handler(rabbitmq_address))
    create_db_handlers(external_db)
    return queue
