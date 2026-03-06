import asyncio
import schema
import ast
import configluz
from sources import start_stream


async def consume_data(queue, verifier, api):
    while True:
        data = await queue.get()
        obj = ast.literal_eval(data.decode('utf-8'))
        if(verifier.verify(obj)):
            api.send(obj)
        queue.task_done()


async def main():
    api, kafka_address, rabbitmq_address = configluz.loadConfig()
    verifier = schema.SchemaValidator(api)
    queue: asyncio.Queue = start_stream(kafka_address, rabbitmq_address)
    await consume_data(queue, verifier, api)


if __name__ == "__main__":
    asyncio.run(main())
