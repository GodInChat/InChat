from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

class NewMessageChatSchemaRequest(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    chat_id: uuid.UUID
    human_question: str
    pdf_id: str

class NewMessageChatSchemaRespond(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    chat_id: uuid.UUID
    human_question: str
    ai_answer: str

class ChatMessageSchemaResponse(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    text: str
    owner_type: str
    created_at: datetime

class ChatSchemaResponse(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    id: uuid.UUID
    messages: list[ChatMessageSchemaResponse]
    created_at: datetime
