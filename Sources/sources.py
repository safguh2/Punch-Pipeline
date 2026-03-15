import asyncio

from Sources.DBSource import DatabaseSource
from Sources.kafka import create_kafka_handler
from Sources.rabbitmq import create_rabbitmq_handler


def create_db_handlers(db_list, queue: asyncio.Queue):
    for db in db_list:
        try:
            if db['type'] != 'postgres':
                print("db not supported")
            else:
                db_handler = DatabaseSource(queue, db['dsn'])
                asyncio.create_task(db_handler.run())
        except Exception as e:
            print(f"couldn't create external database handler {db['dsn']}, error: {str(e)}")


def start_stream(kafka_address, rabbitmq_address, external_db):
    queue: asyncio.Queue = asyncio.Queue()

    asyncio.create_task(create_kafka_handler(kafka_address, queue))
    asyncio.create_task(create_rabbitmq_handler(rabbitmq_address, queue))
    create_db_handlers(external_db, queue)
    return queue
