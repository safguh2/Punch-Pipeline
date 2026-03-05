import json
import random
import time
from kafka import KafkaProducer

# Create producer with JSON serializer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # <-- serialize to JSON bytes
)
data = []
for x in range(0,20):
    data.append({"label": "test", "fields": {"test": x}})

print(data)
# Send to topic
for item in data:
    producer.send('test-topic', value=item)
    print(f"test number {item['fields']['test']} has been sent")
    time.sleep(random.randint(0,3))


# Make sure it actually gets sent
producer.flush()

print("JSON message sent!")