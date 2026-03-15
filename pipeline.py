import asyncio
import schema
import configluz
import SOTPipeline
from dataProcess import consume_data
from Sources.sources import start_stream


async def main():
    communicator, kafka_address, rabbitmq_address, workers_amount, external_db = configluz.load_config()
    verifier = schema.SchemaValidator(communicator.neo)
    queue: asyncio.Queue = start_stream(kafka_address, rabbitmq_address, external_db)
    workers = [asyncio.create_task(consume_data(queue, verifier, communicator)) for _ in range(workers_amount)]
    await asyncio.create_task(SOTPipeline.backup_pipeline(communicator))
    await asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(main())
