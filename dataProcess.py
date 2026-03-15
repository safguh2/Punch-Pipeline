import ast
from requests import RequestException


async def consume_data(queue, verifier, communicator):
    while True:
        try:
            data = await queue.get()
            obj = ast.literal_eval(data.decode('utf-8'))
            if 'count' in obj and obj["count"] <= 3:
                process(verifier, communicator, obj['data'])
            elif 'count' not in obj:
                process(verifier, communicator, obj)
            else:
                print("maximum retries reached")
                raise SyntaxError

        except RequestException as e:
            print(e.response)
            await reflow(queue, obj)
        except BaseException as e:
            print(e)

        finally:
            queue.task_done()


def process(verifier, communicator, obj):
    if verifier.verify(obj):
        communicator.send(obj)


async def reflow(queue, obj):
    if 'count' in obj:
        obj['count'] += 1
    else:
        obj = {'count': 1, 'data': obj}
    await queue.put(str(obj).encode())
