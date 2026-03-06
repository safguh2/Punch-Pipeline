import random
import time

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.queue_declare(queue="test")

data = []
for x in range(0,20):
    data.append({"label": "Department", "fields": {"code": str(x), "department_id": f'00{str(x)}',
                                             "head_name": "gluz", "name": "gluz_research",
                                             "org_id": "6767"
                                             }})

print(data)
# Send to topic
for item in data:
    channel.basic_publish(
        exchange="",
        routing_key="test",
        body=str(item).encode()
    )
    print(f"test number {item['fields']['code']} has been sent")
    print(item)
    time.sleep(random.randint(0,3))

print("sent")

connection.close()