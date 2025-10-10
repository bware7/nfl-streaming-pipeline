from kafka import KafkaProducer, KafkaConsumer
import json

def create_kafka_producer(bootstrap_servers='localhost:9092'):
    """Create a Kafka producer with JSON serialization."""
    return KafkaProducer(
        bootstrap_servers=[bootstrap_servers],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        api_version=(0, 10, 1)
    )

def create_kafka_consumer(topic, bootstrap_servers='localhost:9092'):
    """Create a Kafka consumer with JSON deserialization."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=[bootstrap_servers],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='latest',
        api_version=(0, 10, 1)
    )