from pydantic import BaseModel


class ClientMessage(BaseModel):
    text: str


class RagMessage(BaseModel):
    text: str
    response_time: int
