import asyncio

from requests import RequestException
from pydantic import ValidationError

import schema
import ast
import configluz
from sources import start_stream


async def consume_data(queue, verifier, api):
    while True:
        try:
            data = await queue.get()
            obj = ast.literal_eval(data.decode('utf-8'))
            if 'count' in obj and obj["count"] <= 3:
                process(verifier, api, obj['data'])
            elif 'count' not in obj:
                process(verifier, api, obj)
            else:
                print("maximum retries reached")
                raise SyntaxError

        except ValidationError as e:
            print("invalid schema")
        except SyntaxError as e:
            print("invalid data")
        except RequestException as e:
            await reflow(queue, obj)
        except BaseException as e:
            print("some error accord")

        finally:
            queue.task_done()


def process(verifier, api, obj):
    if (verifier.verify(obj)):
        api.send(obj)


async def reflow(queue, obj):
    if 'count' in obj:
        obj['count'] = obj['count']+1
    else:
        obj = {'count': 1, 'data': obj}
    await queue.put(str(obj).encode())


async def main():
    api, kafka_address, rabbitmq_address = configluz.load_config()
    verifier = schema.SchemaValidator(api)
    queue: asyncio.Queue = start_stream(kafka_address, rabbitmq_address)
    await consume_data(queue, verifier, api)


if __name__ == "__main__":
    asyncio.run(main())
