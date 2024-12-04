import base64

def encode_topic_name(name: str) -> str:
    """Kafka Topic 이름을 Base64로 인코딩"""
    return base64.urlsafe_b64encode(name.encode("utf-8")).decode("utf-8")

def decode_topic_name(encoded_name: str) -> str:
    """Base64로 인코딩된 Kafka Topic 이름을 디코딩"""
    return base64.urlsafe_b64decode(encoded_name.encode("utf-8")).decode("utf-8")