from odmantic import Model, Field
from pydantic import BaseModel
from datetime import datetime
import pytz

def naive_ktc() -> datetime:
    """현재 시간을 KTC로 변환하고 naive datetime으로 반환"""
    kst = pytz.timezone("Asia/Seoul")
    return datetime.now(kst).replace(tzinfo=None)

class ChatLog(Model):
    chat_room: str
    sender: str
    message: str
    timestamp: datetime = Field(default_factory=naive_ktc)


class Message(BaseModel):
    sender: str
    text: str