import asyncio
import aio_pika
import DBSource

from kafka import create_kafka_handler

queue: asyncio.Queue = asyncio.Queue()


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
    asyncio.create_task(create_kafka_handler(kafka_address, queue))
    #asyncio.create_task(rabbitmq_handler(rabbitmq_address))
    #create_db_handlers(external_db)
    return queue
