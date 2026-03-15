import asyncio
import aio_pika


async def create_rabbitmq_handler(rabbitmq_address, queue: asyncio.Queue, interval: int = 60):
    created: bool = False

    while not created:
        try:
            await rabbitmq_handler(rabbitmq_address, queue)
            created = True

        except Exception as e:
            print(f"couldn't connect to rabbitmq service, error: {str(e)}")
            await asyncio.sleep(interval)


async def rabbitmq_handler(rabbitmq_address, queue: asyncio.Queue):
    connection = await aio_pika.connect_robust(rabbitmq_address)

    async with connection:
        channel = await connection.channel()

        mq_queue = await channel.declare_queue("test")

        async with mq_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await queue.put(message.body)