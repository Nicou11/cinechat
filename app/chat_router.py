from fastapi import APIRouter, HTTPException
from app.kafka_utils import create_topic, delete_topic, get_producer, get_consumer
from app.chat_utils import encode_topic_name
from app.db_utils import save_message_to_db, get_messages_from_db
from app.schemas import Message
from concurrent.futures import ThreadPoolExecutor

chat_router = APIRouter(prefix="/chat", tags=["Chat"])
executor = ThreadPoolExecutor()


@chat_router.post("/create_room/")
def create_chat_room(room_name: str):
    """
    Kafka Topic 생성
    - room_name: 한글로 전달된 채팅방 이름
    """
    # 한글 Topic 이름을 Base64로 변환
    encoded_name = encode_topic_name(room_name)
    result = create_topic(encoded_name)  # 인코딩된 이름으로 Topic 생성
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return {
        "status": "success",
        "original_name": room_name,
        "encoded_name": encoded_name,
    }


@chat_router.post("/send_message/")
async def send_message(room_name: str, message: Message):
    producer = get_producer()
    producer.send(room_name, value=message.model_dump())
    producer.flush()
    await save_message_to_db(room_name, message.sender, message.text)
    return {"status": "success", "message": "Message sent."}


def consume_messages(topic_name: str, limit: int):
    """Kafka 메시지를 가져오는 함수 (블로킹 방식)"""
    consumer = get_consumer(topic_name)  # Kafka Consumer 생성
    messages = []
    for message in consumer:
        messages.append(message.value)
        if len(messages) >= limit:
            break
    consumer.close()
    return messages


@chat_router.get("/receive_messages/")
async def receive_messages(room_name: str, limit: int = 10):
    """
    채팅방의 메시지를 가져오는 엔드포인트
    """
    encoded_name = encode_topic_name(room_name)
    try:
        # MongoDB에서 메시지 가져오기 (이미 딕셔너리 형태로 변환됨)
        messages = await get_messages_from_db(room_name, limit)
        return {"room_name": room_name, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.delete("/delete_room/")
def delete_chat_room(room_name: str):
    """
    Kafka Topic 삭제
    - room_name: 한글로 전달된 채팅방 이름
    """
    encoded_name = encode_topic_name(room_name)  # Topic 이름 인코딩
    result = delete_topic(encoded_name)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return {"status": "success", "room_name": room_name, "encoded_name": encoded_name}
