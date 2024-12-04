from odmantic import AIOEngine
from app.schemas import ChatLog
from motor.motor_asyncio import AsyncIOMotorClient
from app.chat_utils import encode_topic_name
from bson import ObjectId

# MongoDB 연결 설정
MONGO_URI = f"mongodb://root:cine@172.17.0.1:27017"
DB_NAME = "chat"
engine = AIOEngine(client=AsyncIOMotorClient(MONGO_URI), database=DB_NAME)


async def save_message_to_db(chat_room: str, sender: str, message: str):
    """
    MongoDB에 메시지 저장
    - chat_room: 원래 한글 채팅방 이름
    """
    encoded_room = encode_topic_name(chat_room)  # 채팅방 이름 인코딩
    chat_log = ChatLog(chat_room=encoded_room, sender=sender, message=message)
    await engine.save(chat_log)


async def get_messages_from_db(chat_room: str, limit: int = 10):
    """
    MongoDB에서 메시지 조회
    - chat_room: 원래 한글 채팅방 이름
    """
    encoded_room = encode_topic_name(chat_room)
    messages = await engine.find(
        ChatLog,
        ChatLog.chat_room == encoded_room,
        sort=ChatLog.timestamp.desc(),
        limit=limit,
    )

    # ObjectId를 str로 변환하여 반환
    return [
        {
            "id": str(msg.id),  # ObjectId를 문자열로 변환
            "chat_room": msg.chat_room,
            "message": msg.message,
            "timestamp": msg.timestamp,
        }
        for msg in messages
    ]
