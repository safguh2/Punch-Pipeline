import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.queue_declare(queue="test")

channel.basic_publish(
    exchange="",
    routing_key="test",
    body="hello"
)

print("sent")

connection.close()