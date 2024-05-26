from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class OriginatorEnum(Enum):
    rag = "rag"
    client = "client"


class Message(BaseModel):
    originator: OriginatorEnum
    timestamp: datetime
    text: str
