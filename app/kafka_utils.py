from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer, KafkaConsumer
import json

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"


def create_topic(topic_name: str):
    """Kafka Topic 생성"""
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
    try:
        admin_client.create_topics([topic])
        print(f"Topic '{topic_name}' created.")
        return {"status": "success", "topic": topic_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_producer():
    """Kafka Producer 생성"""
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def get_consumer(topic_name: str):
    """Kafka Consumer 생성"""
    return KafkaConsumer(
        topic_name,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        consumer_timeout_ms=10000,
    )


def delete_topic(topic_name: str):
    """Kafka Topic 삭제"""
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    try:
        admin_client.delete_topics([topic_name])
        print(f"Topic '{topic_name}' has been deleted.")
        return {"status": "success", "topic": topic_name}
    except Exception as e:
        print(f"Error deleting topic '{topic_name}': {e}")
        return {"status": "error", "message": str(e)}
