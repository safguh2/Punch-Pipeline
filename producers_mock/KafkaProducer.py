import json
import random
import time
from kafka import KafkaProducer

# Create producer with JSON serializer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # <-- serialize to JSON bytes
)
data = [{
    "label": "relationShip",
    "properties": {
        "sourceType": "person",
        "sourceId": "person-sarah-chen",
        "targetType": "organization",
         "targetId": "org-mit",
        "relationshipType": "ENROLLED_IN",
         "tenantId": "tenant_mit",
         "properties": {
              "program": "BSc Computer Science",
              "start_date": "2024-09-01"
        }
    }
}]
print(data)
# Send to topic
for item in data:
    producer.send('test-topic', value=item)
    #print(f"test number {item['fields']['code']} has been sent")
    print(item)
    time.sleep(random.randint(0, 3))


# Make sure it actually gets sent
producer.flush()

print("JSON message sent!")