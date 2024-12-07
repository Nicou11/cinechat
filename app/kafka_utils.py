from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer, KafkaConsumer
import json, os

KAFKA_IP = os.getenv("KAFKA_IP")
KAFKA_BOOTSTRAP_SERVERS = f"{KAFKA_IP}:9092"


def create_topic_name(id: str, id2: str) -> str:
    """
    채팅방 이름을 Kafka topic 이름으로 변환
    """
    return f"{id}_{id2}"


def create_topic(room_name: str):
    """Kafka Topic 생성"""
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    topic = NewTopic(name=room_name, num_partitions=1, replication_factor=1)
    print(f"Attempting to create topic: {room_name}")
    print(f"Using bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")
    try:
        admin_client.create_topics([topic])
        print(f"Topic '{room_name}' created.")
        return {"status": "success", "topic": room_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_producer():
    """Kafka Producer 생성"""
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def get_consumer(room_name: str):
    """Kafka Consumer 생성"""
    return KafkaConsumer(
        room_name,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        consumer_timeout_ms=10000,
    )


def delete_topic(room_name: str):
    """Kafka Topic 삭제"""
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    try:
        # 토픽이 존재하는지 먼저 확인
        topics = admin_client.list_topics()
        if room_name not in topics:
            return {"message": "Topic does not exist", "topic": room_name}

        admin_client.delete_topics([room_name])
        print(f"Topic '{room_name}' 삭제.")
        return {"status": "success", "topic": room_name}
    except Exception as e:
        print(f"Error deleting topic '{room_name}': {e}")
        return {"status": "error", "message": str(e)}
    finally:
        admin_client.close()
