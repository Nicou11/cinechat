from odmantic import Model, Field
from pydantic import BaseModel
from datetime import datetime
import pytz


def naive_ktc() -> datetime:
    """현재 시간을 KTC로 변환하고 naive datetime으로 반환"""
    kst = pytz.timezone("Asia/Seoul")
    return datetime.now(kst).replace(tzinfo=None)


class ChatLog(Model):
    chat_room: str = Field(...)
    sender: str = Field(...)
    message: str = Field(...)
    timestamp: datetime = Field(default_factory=naive_ktc)

    model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}


class Message(BaseModel):
    sender: str
    text: str

    model_config = {
        "json_schema_extra": {"example": {"sender": "유저", "text": "메세지"}}
    }
