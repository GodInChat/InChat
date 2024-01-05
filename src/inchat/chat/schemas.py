from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

class NewMessageChatSchemaRequest(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    chat_id: uuid.UUID
    human_question: str
    pdf_name: str

class NewMessageChatSchemaRespond(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    chat_id: uuid.UUID
    human_question: str
    ai_answer: str


class InitChatSchemaResponse(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    id: uuid.UUID
    created_at: datetime