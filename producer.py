from kafka import KafkaProducer

print("connecting...")

producer = KafkaProducer(
    bootstrap_servers="localhost:9092"
)

print("sending message")

future = producer.send("test-topic", b"hello-from-python")

result = future.get(timeout=10)

print("message sent", result)

producer.flush()

