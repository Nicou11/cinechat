from odmantic import AIOEngine
from app.schemas import ChatLog
from motor.motor_asyncio import AsyncIOMotorClient


# MongoDB 연결 설정
MONGO_URI = f"mongodb://root:cine@172.17.0.1:27017"
DB_NAME = "chat"
engine = AIOEngine(client=AsyncIOMotorClient(MONGO_URI), database=DB_NAME)


async def save_message_to_db(chat_room: str, sender: str, message: str):
    """
    MongoDB에 메시지 저장
    - chat_room: 인코딩된 채팅방 이름 (예: chat_1234abcd)
    - sender: 보낸 사람 이름 (한글 가능)
    - message: 메시지 내용 (한글 가능)
    """
    try:
        chat_log = ChatLog(chat_room=chat_room, sender=sender, message=message)
        await engine.save(chat_log)
    except Exception as e:
        print(f"메시지 저장 중 오류 발생: {e}")
        raise


async def get_messages_from_db(chat_room: str, limit: int = 10):
    """
    MongoDB에서 메시지 조회
    - chat_room: 인코딩된 채팅방 이름 (예: chat_1234abcd)
    """
    try:
        messages = await engine.find(
            ChatLog,
            ChatLog.chat_room == chat_room,
            sort=ChatLog.timestamp.desc(),
            limit=limit,
        )

        # 한글이 포함된 메시지를 JSON으로 직렬화할 수 있게 처리
        return [
            {
                "id": str(msg.id),
                "chat_room": msg.chat_room,
                "sender": msg.sender,
                "message": msg.message,
                "timestamp": msg.timestamp.isoformat(),  # datetime을 문자열로 변환
            }
            for msg in messages
        ]
    except Exception as e:
        print(f"메시지 조회 중 오류 발생: {e}")
        raise
