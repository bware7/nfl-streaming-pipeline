from kafka import KafkaConsumer
import json

TOPIC = 'nfl_events'

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest'
)

print(f"Consumer listening on topic: {TOPIC}")

for message in consumer:
    data = message.value
    print(f"Received: {data['team']} - {data['play_type']} - Score: {data['home_score']}-{data['away_score']}")