import json
import time
import csv
from kafka import KafkaProducer
from pathlib import Path

# Setup
TOPIC = 'nfl_events'
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Read and stream CSV data
data_file = Path('data/sample_game.csv')

print(f"Starting producer on topic: {TOPIC}")

with open(data_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        message = {
            'timestamp': row['timestamp'],
            'team': row['team'],
            'play_type': row['play_type'],
            'points_scored': int(row['points_scored']),
            'home_score': int(row['home_score']),
            'away_score': int(row['away_score'])
        }
        producer.send(TOPIC, value=message)
        print(f"Sent: {message}")
        time.sleep(2)  # 2 second delay between plays

producer.close()
print("Producer finished")